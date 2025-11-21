from typing import Sequence

import smtplib
from email.mime.text import MIMEText

from app.core.config import get_settings

settings = get_settings()


def send_email(subject: str, body: str, to_addresses: Sequence[str]) -> None:
    """Send a simple text email using SMTP settings.

    This is a basic implementation and should be improved for production use.
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = ", ".join(to_addresses)

    with smtplib.SMTP(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT) as server:
        try:
            server.starttls()
        except Exception:
            # Some SMTP servers might not support STARTTLS
            pass

        if settings.EMAIL_SMTP_USER and settings.EMAIL_SMTP_PASSWORD:
            server.login(settings.EMAIL_SMTP_USER, settings.EMAIL_SMTP_PASSWORD)

        server.sendmail(settings.EMAIL_FROM, list(to_addresses), msg.as_string())
