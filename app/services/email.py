import os
import logging
import httpx

logger = logging.getLogger("uvicorn.error")

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "hello@rsfwseries.com")
SENDER_NAME = os.getenv("SENDER_NAME", "Our Lady of Tears Academy")


async def send_diocesan_assessment_email(
    recipient_email: str,
    recipient_alias: str,
    archetype_title: str,
    letter_body_html: str
) -> bool:
    """Dispatches the official Diocesan Assessment Letter to an initiate via Brevo REST API."""
    if not BREVO_API_KEY:
        logger.warning("BREVO_API_KEY is missing. Email dispatch skipped.")
        return False

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    full_html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                background-color: #0d0a0b;
                color: #e6dfd5;
                font-family: Georgia, 'Times New Roman', serif;
                padding: 20px;
                margin: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #140f11;
                border: 2px solid #5c0a1a;
                padding: 30px;
            }}
            .header {{
                text-align: center;
                border-bottom: 1px solid #5c0a1a;
                padding-bottom: 15px;
                margin-bottom: 20px;
            }}
            .seal {{
                font-size: 24px;
                color: #a30f2e;
            }}
            .sub-title {{
                font-family: monospace;
                font-size: 10px;
                color: #a30f2e;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            .title {{
                color: #e6dfd5;
                font-size: 20px;
                text-transform: uppercase;
                margin: 5px 0;
            }}
            .content {{
                font-size: 14px;
                line-height: 1.6;
                color: #c9c0b5;
            }}
            .archetype {{
                color: #f59e0b;
                font-weight: bold;
            }}
            .footer {{
                margin-top: 30px;
                border-top: 1px solid #332226;
                padding-top: 15px;
                font-family: monospace;
                font-size: 10px;
                color: #786d65;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="seal">✝</div>
                <div class="sub-title">Our Lady of Tears Academy — Diagnostic Record</div>
                <h1 class="title">Official Disciplinary Clearance</h1>
            </div>
            <div class="content">
                <p><strong>Initiate {recipient_alias},</strong></p>
                <p>Your diagnostic submission has been logged into the Academy Registry.</p>
                <p>Assigned Frequency Profile: <span class="archetype">{archetype_title}</span></p>
                <hr style="border: 0; border-top: 1px solid #5c0a1a; margin: 20px 0;">
                <div>
                    {letter_body_html}
                </div>
            </div>
            <div class="footer">
                CONFIDENTIAL DIOCESAN TRANSMISSION • THE REFORM SCHOOL FOR WITCHES (rsfwseries.com)<br>
                Do not forward this record outside consecrated channels.
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
        "subject": f"✝ [Academy Diagnostic File] Assessment Record for Initiate {recipient_alias}",
        "htmlContent": full_html_content
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(BREVO_API_URL, headers=headers, json=payload)
            
            if response.status_code in (200, 201, 202):
                logger.info(f"Diocesan Assessment email dispatched successfully to {recipient_email}")
                return True
            else:
                logger.error(f"Brevo API error ({response.status_code}): {response.text}")
                return False

    except Exception as exc:
        logger.error(f"Failed to send email via Brevo API: {exc}")
        return False