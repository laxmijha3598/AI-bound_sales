from __future__ import annotations

from textwrap import dedent

from .models import Lead, OutreachRecord


def draft_email(lead: Lead, config: dict) -> tuple[str, str]:
    campaign = config["campaign"]
    subject = config["email"]["subject_template"].format(company=lead.company)
    signal = lead.hiring_signal.rstrip(".")
    basis = lead.personalization_basis.rstrip(".")
    offer = campaign["offer"].rstrip(".")
    sender_name = campaign["sender_name"]

    body = dedent(
        f"""\
        Hi {lead.first_name},

        I noticed {lead.company} is {signal.lower()}. The detail that stood out was: {basis}.

        That kind of growth usually creates a lot of repetitive engineering-adjacent work around sourcing, qualification, internal ops, and follow-up. I built a small agentic workflow for {offer}, and thought it might be relevant while your team is scaling.

        Worth a quick look next week?

        Best,
        {sender_name}
        """
    )
    return subject, body


def draft_linkedin_note(lead: Lead) -> str:
    basis = lead.personalization_basis.split(".")[0]
    note = (
        f"Hi {lead.first_name}, saw {lead.company}'s {lead.hiring_signal.lower()}. "
        f"{basis}. Would enjoy connecting."
    )
    if len(note) <= 300:
        return note
    shorter = f"Hi {lead.first_name}, saw {lead.company} is {lead.hiring_signal.lower()}. Relevant to AI workflows while eng is scaling. Would enjoy connecting."
    return shorter[:300]


def build_records(leads: list[Lead], config: dict) -> list[OutreachRecord]:
    records: list[OutreachRecord] = []
    for lead in leads:
        subject, body = draft_email(lead, config)
        records.append(
            OutreachRecord(
                lead=lead,
                email_subject=subject,
                email_body=body,
                linkedin_note=draft_linkedin_note(lead),
            )
        )
    return records

