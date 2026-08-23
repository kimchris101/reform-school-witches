from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services.lore_engine import initialize_pdf_lore_index
from app.routes import intake, dossier, media, interactive, vault, industry, legal


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Pre-index the manuscript PDF into memory
    initialize_pdf_lore_index()
    yield
    # Shutdown logic (if required in future)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend engine for interactive visual novel choices, archetype intake diagnostics, cinematic unlocks, classified book vault, and industry pitch portal.",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS Configuration
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.onrender.com",
    settings.SITE_URL
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
app.include_router(industry.router, prefix="/industry", tags=["Industry Pitch"])
app.include_router(legal.router, prefix="/legal", tags=["Legal"])


# Custom 404 Exception Handler
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={
            "page_title": "Archival Record Not Found | RSFW",
            "meta_description": "The requested diocesan record does not exist or has been restricted."
        },
        status_code=status.HTTP_404_NOT_FOUND
    )


# Custom 500 Exception Handler
@app.exception_handler(500)
async def custom_500_handler(request: Request, exc):
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={
            "page_title": "Tribunal Signal Anomaly | RSFW",
            "meta_description": "An internal system anomaly was encountered during archival retrieval."
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


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


@app.get("/sitemap.xml", include_in_schema=False)
async def get_sitemap():
    """Dynamically generates an XML sitemap for search engines."""
    domain = settings.SITE_URL.rstrip('/')
    
    pages = [
        {"loc": "/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": "/intake", "changefreq": "monthly", "priority": "0.8"},
        {"loc": "/dossiers", "changefreq": "weekly", "priority": "0.9"},
        {"loc": "/vault", "changefreq": "weekly", "priority": "0.9"},
        {"loc": "/media", "changefreq": "weekly", "priority": "0.8"},
        {"loc": "/interactive", "changefreq": "monthly", "priority": "0.7"},
        {"loc": "/industry", "changefreq": "monthly", "priority": "0.6"},
    ]

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml_content += "  <url>\n"
        xml_content += f"    <loc>{domain}{page['loc']}</loc>\n"
        xml_content += f"    <changefreq>{page['changefreq']}</changefreq>\n"
        xml_content += f"    <priority>{page['priority']}</priority>\n"
        xml_content += "  </url>\n"
        
    xml_content += "</urlset>"

    return Response(content=xml_content, media_type="application/xml")


@app.get("/robots.txt", include_in_schema=False)
async def get_robots():
    """Returns robots.txt rules for web crawlers."""
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Allow: /dossiers\n"
        "Allow: /vault\n"
        "Allow: /media\n"
        "Allow: /interactive\n"
        "Allow: /industry\n"
        "Disallow: /dossiers/easter-egg/\n"
        "Disallow: /vault/download/\n\n"
        f"Sitemap: {settings.SITE_URL.rstrip('/')}/sitemap.xml\n"
    )
    return Response(content=content, media_type="text/plain")


@app.get("/healthz", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "academy": "Our Lady of Tears",
        "environment": settings.APP_ENV
    }