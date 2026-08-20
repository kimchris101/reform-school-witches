from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.models.schemas import QuizSubmission, QuizAnswer, ArchetypeEnum
from app.services.scoring import evaluate_intake_exam

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def render_intake_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/intake.html",
        context={
            "page_title": "Academy Intake & Diagnostic Protocol | Our Lady of Tears",
            "meta_description": "Submit to the Diocesan Diagnostic Protocol at Our Lady of Tears Academy. Determine your spiritual frequency and receive your Official Disciplinary File."
        }
    )

@router.post("/evaluate", response_class=HTMLResponse)
async def evaluate_intake_submission(
    request: Request,
    user_email: str = Form(...),
    user_alias: str = Form(...),
    q1: str = Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4: str = Form(...),
    q5: str = Form(...)
):
    try:
        answers = [
            QuizAnswer(question_id=1, selected_option=q1),
            QuizAnswer(question_id=2, selected_option=q2),
            QuizAnswer(question_id=3, selected_option=q3),
            QuizAnswer(question_id=4, selected_option=q4),
            QuizAnswer(question_id=5, selected_option=q5),
        ]
        
        submission = QuizSubmission(
            user_email=user_email,
            user_alias=user_alias,
            answers=answers
        )
    except ValidationError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid diagnostic submission: {err.errors()}"
        )

    result = evaluate_intake_exam(submission.user_alias, submission.answers)

    resp = templates.TemplateResponse(
        request=request,
        name="components/diocesan_letter.html",
        context={
            "letter": result.diocesan_letter,
            "user_email": submission.user_email
        }
    )

    # Trigger Sacramental Bond cutscene automatically for Co-Link results
    if result.archetype in (ArchetypeEnum.CO_LINK_PARTNER, "The Co-Link Partner"):
        resp.headers["HX-Trigger"] = "launchCoLinkCutscene"

    return resp