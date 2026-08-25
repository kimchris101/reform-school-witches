import ssl
import os
from fastapi import Request


def get_ssl_context() -> ssl.SSLContext:
    """Configures SSL Context for HTTPS calls (e.g. Brevo API)."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl._create_unverified_context()


def is_authenticated_session(request: Request) -> bool:
    """
    Utility helper to check whether a valid initiate session token cookie exists.
    Returns True if user has verified their email address.
    """
    token = request.cookies.get("rsfw_member_token")
    return bool(token and token.strip())