from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application State
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev_secret_key_change_in_production_123456789"

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Cookie Security Settings
    COOKIE_SECURE: bool = False     # Set to False for local http://localhost
    COOKIE_HTTPONLY: bool = True    # Prevent JavaScript access (XSS defense)
    COOKIE_SAMESITE: str = "lax"    # CSRF protection

    # Path Settings
    MANUSCRIPT_PATH: str = "app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()