import os
import logging
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("uvicorn.error")

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip().strip('"').strip("'")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "admin@anomik.io").strip()
SENDER_NAME = os.getenv("SENDER_NAME", "Our Lady of Tears Academy").strip()


def send_diocesan_assessment_email(
    recipient_email: str,
    recipient_alias: str,
    archetype_title: str,
    letter_obj: object,
    verify_url: str = ""
) -> bool:
    """Dispatches a Diocesan Assessment Letter with verification link via Brevo REST API."""
    if not BREVO_API_KEY:
        print("[BREVO ERROR]: BREVO_API_KEY environment variable is missing or empty. Check your .env file.")
        logger.error("[BREVO ERROR]: BREVO_API_KEY is missing from environment. Skipping email dispatch.")
        return False

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    def get_val(obj, key, default):
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    classification = get_val(letter_obj, "classification_class", "Academy Initiate")
    patron = get_val(letter_obj, "patron_example", "St. Michael the Archangel")
    summary = get_val(letter_obj, "file_summary", "Record pending classification.")
    warning = get_val(letter_obj, "warning_notice", "Maintain spiritual vigilance.")
    seal_code = get_val(letter_obj, "diocesan_seal_code", "OLT-ARCHIVE-RESTRICTED")

    # Verification CTA Button
    verify_button_html = f"""
    <div style="text-align: center; margin: 28px 0;">
        <a href="{verify_url}" style="background-color: #a30f2e; color: #ffffff; padding: 14px 28px; text-decoration: none; font-weight: bold; font-family: 'Courier New', monospace; font-size: 12px; letter-spacing: 2px; border: 1px solid #dc2626; display: inline-block;">
            ✝ VERIFY EMAIL & UNLOCK CLEARANCE
        </a>
    </div>
    """ if verify_url else ""

    full_html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                background-color: #0b0809;
                color: #e5dfd5;
                font-family: Georgia, 'Times New Roman', serif;
                padding: 20px 10px;
                margin: 0;
            }}
            .container {{
                max-width: 580px;
                margin: 0 auto;
                background-color: #120d0f;
                border: 2px solid #5c0a1a;
                padding: 32px 28px;
                box-shadow: 0 0 20px rgba(0,0,0,0.8);
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #5c0a1a;
                padding-bottom: 18px;
                margin-bottom: 24px;
            }}
            .seal {{
                font-size: 28px;
                color: #a30f2e;
                margin-bottom: 6px;
            }}
            .sub-title {{
                font-family: 'Courier New', Courier, monospace;
                font-size: 10px;
                color: #a30f2e;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 4px;
            }}
            .title {{
                color: #f2ece4;
                font-size: 20px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin: 0;
            }}
            .meta-grid {{
                background-color: #1a1215;
                border-left: 3px solid #a30f2e;
                padding: 12px 16px;
                margin-bottom: 24px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 11px;
                line-height: 1.8;
                color: #c4b9ad;
            }}
            .meta-label {{
                color: #a30f2e;
                font-weight: bold;
                text-transform: uppercase;
            }}
            .content-section {{
                font-size: 14px;
                line-height: 1.7;
                color: #d6ccc0;
                margin-bottom: 20px;
            }}
            .warning-box {{
                background-color: #24080e;
                border: 1px dashed #a30f2e;
                padding: 14px 16px;
                margin-top: 24px;
                font-size: 13px;
                color: #fca5a5;
                line-height: 1.5;
            }}
            .warning-header {{
                font-family: 'Courier New', Courier, monospace;
                font-size: 10px;
                color: #ef4444;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 6px;
            }}
            .footer {{
                margin-top: 32px;
                border-top: 1px solid #2e1a1e;
                padding-top: 16px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 9px;
                color: #6b5e56;
                text-align: center;
                line-height: 1.5;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="seal">✝</div>
                <div class="sub-title">Archdiocese of New Orleans • Official Registry</div>
                <h1 class="title">Disciplinary Assessment File</h1>
            </div>

            <div class="meta-grid">
                <div><span class="meta-label">INITIATE ALIAS:</span> {recipient_alias}</div>
                <div><span class="meta-label">CLASSIFICATION:</span> {classification}</div>
                <div><span class="meta-label">AFFINITY PATRON:</span> {patron}</div>
                <div><span class="meta-label">RECORD SEAL:</span> {seal_code}</div>
            </div>

            <div class="content-section">
                <p style="margin-top: 0;"><strong>Initiate {recipient_alias},</strong></p>
                <p>{summary}</p>
            </div>

            {verify_button_html}

            <div class="warning-box">
                <div class="warning-header">⚠️ ARCHIVAL DISCIPLINARY NOTICE</div>
                <div>{warning}</div>
            </div>

            <div class="footer">
                CONFIDENTIAL DIOCESAN TRANSMISSION • OUR LADY OF TEARS ACADEMY<br>
                THE REFORM SCHOOL FOR WITCHES (rsfwseries.com)<br>
                Do not forward this disciplinary record outside consecrated channels.
            </div>
        </div>
    </body>
    </html>
    """

    payload = {
        "sender": {
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        },
        "to": [
            {
                "email": recipient_email,
                "name": recipient_alias
            }
        ],
        "subject": f"✝ [Diocesan File] Verify Email & Official Disciplinary Record: Initiate {recipient_alias}",
        "htmlContent": full_html_content
    }

    try:
        with httpx.Client(timeout=12.0) as client:
            response = client.post(BREVO_API_URL, headers=headers, json=payload)
            
            if response.status_code in (200, 201, 202):
                print(f"[BREVO DISPATCH SUCCESS]: Email delivered to {recipient_email}")
                logger.info(f"[BREVO SUCCESS]: Diocesan Assessment email dispatched to {recipient_email}")
                return True
            else:
                print(f"[BREVO API ERROR] ({response.status_code}): {response.text}")
                logger.error(f"[BREVO API ERROR] ({response.status_code}): {response.text}")
                return False

    except Exception as exc:
        print(f"[BREVO DISPATCH FAILED]: Exception: {exc}")
        logger.error(f"[BREVO DISPATCH FAILED]: Exception sending email to {recipient_email}: {exc}")
        return False