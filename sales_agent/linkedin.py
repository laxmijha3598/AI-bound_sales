from __future__ import annotations

import csv
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

from .models import OutreachRecord


def write_linkedin_queue(records: list[OutreachRecord], path: str | Path = "out/linkedin_queue.csv") -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "company", "linkedin_url", "note"])
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "name": record.lead.full_name,
                    "company": record.lead.company,
                    "linkedin_url": record.lead.linkedin_url,
                    "note": record.linkedin_note,
                }
            )


def open_profiles(records: list[OutreachRecord]) -> None:
    for record in records:
        if record.lead.linkedin_url:
            webbrowser.open(record.lead.linkedin_url)


def mark_linkedin_sent(records: list[OutreachRecord], lead_email_or_domain: str) -> list[OutreachRecord]:
    now = datetime.now(timezone.utc).isoformat()
    needle = lead_email_or_domain.lower()
    for record in records:
        if needle in record.lead.email.lower() or needle in record.lead.company_domain.lower():
            record.linkedin_sent_at = now
            record.updated_at = now
    return records

