# Outbound Sales Agent

A small, practical outbound agent for the AI Agent Engineer take-home.

It runs this workflow:

1. Find or import 10 ICP-matched leads from free public sources.
2. Draft genuinely personalized cold emails and LinkedIn notes.
3. Send email through Gmail.
4. Prepare LinkedIn connection notes for human review/send.
5. Watch Gmail replies and auto-send a Calendly link when a reply looks positive.
6. Log every step to CSV and, when credentials are present, Google Sheets.

LinkedIn is intentionally semi-manual. Automated connection sending can violate LinkedIn's rules and can get an account restricted, so the agent drafts notes, opens lead profiles, and logs the user-confirmed send.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
Copy-Item config.example.toml config.toml
python -m sales_agent.cli run --config config.toml --leads data/starter_leads.csv --limit 10
```

The first run uses local CSV logging only. To send real emails and sync Google Sheets, fill in `.env` and use:

```powershell
python -m sales_agent.cli run --config config.toml --leads data/starter_leads.csv --limit 10 --send-email --sync-sheets
```

## Gmail Setup

The simplest free option is Gmail SMTP plus an app password:

1. Turn on 2-step verification on the Gmail account.
2. Create an app password.
3. Put these in `.env`:

```text
GMAIL_ADDRESS=your.name@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
```

For reply monitoring, IMAP must be enabled in Gmail settings.

## Google Sheets Setup

Create a free Google Cloud project, enable Google Sheets API, create a service account, download the JSON key, and share your target Sheet with the service account email.

Then set:

```text
GOOGLE_SERVICE_ACCOUNT_JSON=C:\absolute\path\service-account.json
GOOGLE_SHEET_ID=your_sheet_id
```

If these are missing, the agent still writes `out/outreach_log.csv`.

## Commands

```powershell
python -m sales_agent.cli draft --config config.toml --leads data/starter_leads.csv --limit 10
python -m sales_agent.cli send-email --config config.toml --log out/outreach_log.csv
python -m sales_agent.cli linkedin-queue --log out/outreach_log.csv
python -m sales_agent.cli watch-replies --config config.toml --log out/outreach_log.csv
```

## Submission Notes

- Code: this repository.
- Sheet: run with `--sync-sheets`, or upload `out/outreach_log.csv` to Google Sheets.
- Loom: record `run`, one manual LinkedIn send, and `watch-replies` detecting a positive test reply.
- Scale paragraph: see [SCALE.md](SCALE.md).
