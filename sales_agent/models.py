from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Lead:
    first_name: str
    last_name: str
    title: str
    company: str
    company_domain: str
    geography: str
    linkedin_url: str = ""
    email: str = ""
    source_url: str = ""
    hiring_signal: str = ""
    personalization_basis: str = ""
    fit_notes: str = ""

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class OutreachRecord:
    lead: Lead
    email_subject: str = ""
    email_body: str = ""
    linkedin_note: str = ""
    email_sent_at: str = ""
    linkedin_sent_at: str = ""
    reply_status: str = "not_checked"
    reply_excerpt: str = ""
    calendly_sent_at: str = ""
    meeting_booked: str = "unknown"
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

