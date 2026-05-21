from sales_agent.models import Lead
from sales_agent.personalization import draft_email, draft_linkedin_note
from sales_agent.replies import classify_reply


def _config():
    return {
        "campaign": {
            "sender_name": "Sam",
            "offer": "deploying AI agents for outbound ops",
        },
        "email": {
            "subject_template": "Quick thought after seeing {company}'s engineering hiring",
            "positive_reply_terms": ["interested", "let's talk"],
        },
    }


def _lead():
    return Lead(
        first_name="Rob",
        last_name="Williams",
        title="CTO",
        company="Read AI",
        company_domain="read.ai",
        geography="US",
        hiring_signal="Hiring Senior Software Engineer, Backend",
        personalization_basis="The role touches FastAPI, SQLAlchemy, AWS, integrations, auth, and enterprise security.",
    )


def test_email_uses_specific_personalization():
    subject, body = draft_email(_lead(), _config())
    assert "Read AI" in subject
    assert "FastAPI" in body
    assert "Senior Software Engineer" in body


def test_linkedin_note_under_300_chars():
    assert len(draft_linkedin_note(_lead())) <= 300


def test_reply_classifier():
    assert classify_reply("Interested, send times", ["interested"]) == "positive"
    assert classify_reply("Please remove me", ["interested"]) == "negative"
    assert classify_reply("Maybe later", ["interested"]) == "neutral"

