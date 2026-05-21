from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path

from .models import Lead, OutreachRecord


LEAD_FIELDS = [
    "first_name",
    "last_name",
    "title",
    "company",
    "company_domain",
    "geography",
    "linkedin_url",
    "email",
    "source_url",
    "hiring_signal",
    "personalization_basis",
    "fit_notes",
]

LOG_FIELDS = LEAD_FIELDS + [
    "email_subject",
    "email_body",
    "linkedin_note",
    "email_sent_at",
    "linkedin_sent_at",
    "reply_status",
    "reply_excerpt",
    "calendly_sent_at",
    "meeting_booked",
    "updated_at",
]


def read_leads(path: str | Path, limit: int | None = None) -> list[Lead]:
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    leads = [Lead(**{field: row.get(field, "").strip() for field in LEAD_FIELDS}) for row in rows]
    return leads[:limit] if limit else leads


def read_log(path: str | Path) -> list[OutreachRecord]:
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    records: list[OutreachRecord] = []
    for row in rows:
        lead = Lead(**{field: row.get(field, "") for field in LEAD_FIELDS})
        records.append(
            OutreachRecord(
                lead=lead,
                email_subject=row.get("email_subject", ""),
                email_body=row.get("email_body", ""),
                linkedin_note=row.get("linkedin_note", ""),
                email_sent_at=row.get("email_sent_at", ""),
                linkedin_sent_at=row.get("linkedin_sent_at", ""),
                reply_status=row.get("reply_status", "not_checked"),
                reply_excerpt=row.get("reply_excerpt", ""),
                calendly_sent_at=row.get("calendly_sent_at", ""),
                meeting_booked=row.get("meeting_booked", "unknown"),
                updated_at=row.get("updated_at", ""),
            )
        )
    return records


def write_log(path: str | Path, records: list[OutreachRecord]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writeheader()
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
            writer.writerow(row)

