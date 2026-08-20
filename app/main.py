import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import intake, dossier, media, interactive
from app.routes import intake, dossier, media, interactive, vault



app = FastAPI(
    title="Our Lady of Tears Academy - Reader Portal API",
    description="Backend engine for interactive visual novel choices, archetype intake diagnostics, and cinematic unlocks.",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files & Jinja2 Templates Setup
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Register Feature Routers
app.include_router(intake.router, prefix="/intake", tags=["Academy Intake"])
app.include_router(dossier.router, prefix="/dossiers", tags=["Character Dossiers"])
app.include_router(media.router, prefix="/media", tags=["Cinematic Unlocks"])
app.include_router(interactive.router, prefix="/interactive", tags=["Interactive Script Engine"])
app.include_router(vault.router, prefix="/vault", tags=["Book Vault"])

@app.get("/", include_in_schema=False)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={
            "page_title": "The Reform School for Witches Series | Official Reader Portal (rsfwseries.com)",
            "meta_description": "Step into the Southern Gothic Sacramental Noir universe. Complete your Academy Intake Exam at Our Lady of Tears Academy, inspect classified character dossiers, and navigate interactive visual novel choices."
        }
    )
@app.get("/healthz", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "academy": "Our Lady of Tears",
        "environment": os.getenv("ENVIRONMENT", "development")
    }