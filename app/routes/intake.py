import secrets
from fastapi import APIRouter, Request, Form, HTTPException, status, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.models.schemas import QuizSubmission, QuizAnswer, ArchetypeEnum
from app.services.scoring import evaluate_intake_exam
from app.services.email import send_diocesan_assessment_email

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# In-memory store for verification tokens (token -> email)
VERIFICATION_TOKENS: dict[str, str] = {}


@router.get("/", response_class=HTMLResponse)
async def render_intake_page(request: Request):
    """Renders the main Academy Intake Diagnostic Exam page."""
    is_authenticated = request.cookies.get("rsfw_member_token") is not None
    return templates.TemplateResponse(
        request=request,
        name="pages/intake.html",
        context={
            "page_title": "Academy Intake & Diagnostic Protocol | Our Lady of Tears",
            "meta_description": "Submit to the Diocesan Diagnostic Protocol at Our Lady of Tears Academy. Determine your spiritual frequency and receive your Official Disciplinary File.",
            "is_authenticated": is_authenticated
        }
    )


@router.post("/evaluate", response_class=HTMLResponse)
async def evaluate_intake_submission(
    request: Request,
    background_tasks: BackgroundTasks,
    user_email: str = Form(...),
    user_alias: str = Form(...),
    q1: str = Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4: str = Form(...),
    q5: str = Form(...)
):
    """Processes intake choices, sends verification email, and keeps member clearance locked until verified."""
    clean_email = user_email.strip().lower()
    clean_alias = user_alias.strip()

    try:
        answers = [
            QuizAnswer(question_id=1, selected_option=q1),
            QuizAnswer(question_id=2, selected_option=q2),
            QuizAnswer(question_id=3, selected_option=q3),
            QuizAnswer(question_id=4, selected_option=q4),
            QuizAnswer(question_id=5, selected_option=q5),
        ]
        
        submission = QuizSubmission(
            user_email=clean_email,
            user_alias=clean_alias,
            answers=answers
        )
    except ValidationError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid diagnostic submission: {err.errors()}"
        )

    # 1. Calculate diagnostic result
    result = evaluate_intake_exam(submission.user_alias, submission.answers)

    # 2. Convert Pydantic object to dict for background task compatibility
    if hasattr(result.diocesan_letter, "model_dump"):
        letter_dict = result.diocesan_letter.model_dump()
    elif hasattr(result.diocesan_letter, "dict"):
        letter_dict = result.diocesan_letter.dict()
    else:
        letter_dict = result.diocesan_letter

    archetype_title = str(result.archetype.value if hasattr(result.archetype, 'value') else result.archetype)

    # 3. Generate verification token and link string
    verify_token = secrets.token_urlsafe(24)
    VERIFICATION_TOKENS[verify_token] = clean_email

    base_domain = str(request.base_url).rstrip("/")
    verify_url = f"{base_domain}/intake/verify?token={verify_token}"

    # 4. Queue background task
    background_tasks.add_task(
        send_diocesan_assessment_email,
        recipient_email=submission.user_email,
        recipient_alias=submission.user_alias,
        archetype_title=archetype_title,
        letter_obj=letter_dict,
        verify_url=verify_url
    )

    # 5. Render result view prompting user to check email
    resp = templates.TemplateResponse(
        request=request,
        name="components/diocesan_letter.html",
        context={
            "letter": result.diocesan_letter,
            "user_email": submission.user_email,
            "is_verified": False
        }
    )

    # NO MEMBER COOKIE IS SET HERE (Guarantees double opt-in verification)

    if result.archetype in (ArchetypeEnum.CO_LINK_PARTNER, "The Co-Link Partner"):
        resp.headers["HX-Trigger"] = "launchCoLinkCutscene"

    return resp


@router.get("/verify", response_class=HTMLResponse)
async def verify_email_token(request: Request, token: str):
    """Validates verification link from Brevo email and grants permanent member access cookie."""
    email = VERIFICATION_TOKENS.get(token)
    
    if not email:
        return templates.TemplateResponse(
            request=request,
            name="pages/intake_required.html",
            context={
                "page_title": "Verification Link Expired | Our Lady of Tears",
                "meta_description": "The diocesan verification link is invalid or expired."
            }
        )

    # Set permanent member clearance cookie upon clicking email link
    response = RedirectResponse(url="/interactive/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="rsfw_member_token",
        value=f"initiate_{email}",
        path="/",
        samesite="lax",
        max_age=2592000
    )
    # Token consumed
    VERIFICATION_TOKENS.pop(token, None)
    return response