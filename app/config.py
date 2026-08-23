from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application Config
    PROJECT_NAME: str = "The Reform School for Witches - Reader Portal"
    APP_ENV: str = "development"  # development, staging, production
    DEBUG: bool = True
    PORT: int = 8000
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    SITE_URL: str = "http://localhost:8000"

    # Cookie Security Settings
    COOKIE_SECURE: bool = False     # False for http://localhost, True for staging HTTPS
    COOKIE_HTTPONLY: bool = True    # XSS Protection
    COOKIE_SAMESITE: str = "lax"    # CSRF Protection

    # Manuscript Path
    MANUSCRIPT_PATH: str = "app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf"

    # Supabase Credentials (Optional if relying solely on zero-db cookie session tracking)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None

    # Brevo Email Credentials
    BREVO_API_KEY: Optional[str] = None
    BREVO_SENDER_EMAIL: str = "diocesan-registry@reformschoolforwitches.com"
    BREVO_SENDER_NAME: str = "Diocesan Tribunal Authority"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()