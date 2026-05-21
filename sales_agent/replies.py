from __future__ import annotations

from datetime import datetime, timezone

from .emailer import fetch_recent_replies, send_calendly_reply
from .models import OutreachRecord


def classify_reply(text: str, positive_terms: list[str]) -> str:
    normalized = text.lower()
    negative_terms = ["not interested", "unsubscribe", "remove me", "no thanks", "stop emailing"]
    if any(term in normalized for term in negative_terms):
        return "negative"
    if any(term.lower() in normalized for term in positive_terms):
        return "positive"
    return "neutral"


def update_reply_status(records: list[OutreachRecord], config: dict, auto_reply: bool = False) -> list[OutreachRecord]:
    replies = fetch_recent_replies()
    positive_terms = config["email"]["positive_reply_terms"]
    campaign = config["campaign"]
    now = datetime.now(timezone.utc).isoformat()

    for record in records:
        if not record.lead.email:
            continue
        matching = [reply for reply in replies if record.lead.email.lower() in reply[0].lower()]
        if not matching:
            continue
        _sender, subject, body = matching[-1]
        status = classify_reply(body, positive_terms)
        record.reply_status = status
        record.reply_excerpt = " ".join(body.split())[:240]
        record.updated_at = now
        if status == "positive" and auto_reply and not record.calendly_sent_at:
            send_calendly_reply(
                record.lead.email,
                subject or record.email_subject,
                campaign["calendly_link"],
                campaign["sender_name"],
            )
            record.calendly_sent_at = datetime.now(timezone.utc).isoformat()
    return records

