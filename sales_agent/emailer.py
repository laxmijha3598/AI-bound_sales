from __future__ import annotations

import imaplib
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default

from .config import env
from .models import OutreachRecord


def send_email(to_email: str, subject: str, body: str) -> None:
    gmail = env("GMAIL_ADDRESS")
    password = env("GMAIL_APP_PASSWORD")
    if not gmail or not password:
        raise RuntimeError("Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env before sending.")
    if not to_email:
        raise RuntimeError("Lead has no email address.")

    msg = EmailMessage()
    msg["From"] = gmail
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail, password)
        smtp.send_message(msg)


def send_calendly_reply(to_email: str, subject: str, calendly_link: str, sender_name: str) -> None:
    body = (
        "Thanks for the reply. Glad this is relevant.\n\n"
        f"Here is my Calendly link: {calendly_link}\n\n"
        "Feel free to grab any slot that works.\n\n"
        f"Best,\n{sender_name}"
    )
    send_email(to_email, subject if subject.lower().startswith("re:") else f"Re: {subject}", body)


def mark_sent(record: OutreachRecord) -> OutreachRecord:
    record.email_sent_at = datetime.now(timezone.utc).isoformat()
    record.updated_at = record.email_sent_at
    return record


def fetch_recent_replies(limit: int = 50) -> list[tuple[str, str, str]]:
    gmail = env("GMAIL_ADDRESS")
    password = env("GMAIL_APP_PASSWORD")
    if not gmail or not password:
        raise RuntimeError("Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env before reply monitoring.")

    replies: list[tuple[str, str, str]] = []
    with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
        imap.login(gmail, password)
        imap.select("INBOX")
        _, data = imap.search(None, "ALL")
        ids = data[0].split()[-limit:]
        for msg_id in ids:
            _, msg_data = imap.fetch(msg_id, "(RFC822)")
            raw = msg_data[0][1]
            msg = BytesParser(policy=default).parsebytes(raw)
            sender = msg.get("From", "")
            subject = msg.get("Subject", "")
            body = _plain_body(msg)
            replies.append((sender, subject, body))
    return replies


def _plain_body(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_content()
        return ""
    return msg.get_content() if msg.get_content_type() == "text/plain" else ""

