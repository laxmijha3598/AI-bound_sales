from __future__ import annotations

from dataclasses import asdict

from .config import env
from .storage import LOG_FIELDS
from .models import OutreachRecord


def sync_to_google_sheet(records: list[OutreachRecord]) -> None:
    try:
        import gspread
    except ImportError as exc:
        raise RuntimeError("Install optional dependency gspread to sync Google Sheets.") from exc

    json_path = env("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = env("GOOGLE_SHEET_ID")
    if not json_path or not sheet_id:
        raise RuntimeError("Set GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SHEET_ID to sync Google Sheets.")

    client = gspread.service_account(filename=json_path)
    sheet = client.open_by_key(sheet_id).sheet1
    rows = [LOG_FIELDS]
    for record in records:
        row = asdict(record.lead)
        row.update(
            {
                "email_subject": record.email_subject,
                "email_body": record.email_body,
                "linkedin_note": record.linkedin_note,
                "email_sent_at": record.email_sent_at,
                "linkedin_sent_at": record.linkedin_sent_at,
                "reply_status": record.reply_status,
                "reply_excerpt": record.reply_excerpt,
                "calendly_sent_at": record.calendly_sent_at,
                "meeting_booked": record.meeting_booked,
                "updated_at": record.updated_at,
            }
        )
        rows.append([row.get(field, "") for field in LOG_FIELDS])
    sheet.clear()
    sheet.update(rows)
