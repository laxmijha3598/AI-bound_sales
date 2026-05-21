from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config
from .emailer import mark_sent, send_email
from .linkedin import mark_linkedin_sent, open_profiles, write_linkedin_queue
from .personalization import build_records
from .replies import update_reply_status
from .sheets import sync_to_google_sheet
from .storage import read_leads, read_log, write_log


def main() -> None:
    parser = argparse.ArgumentParser(description="Outbound sales agent CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    draft = sub.add_parser("draft")
    draft.add_argument("--config", default="config.toml")
    draft.add_argument("--leads", default="data/starter_leads.csv")
    draft.add_argument("--limit", type=int, default=10)
    draft.add_argument("--log", default="out/outreach_log.csv")

    send = sub.add_parser("send-email")
    send.add_argument("--config", default="config.toml")
    send.add_argument("--log", default="out/outreach_log.csv")
    send.add_argument("--sync-sheets", action="store_true")

    li = sub.add_parser("linkedin-queue")
    li.add_argument("--log", default="out/outreach_log.csv")
    li.add_argument("--queue", default="out/linkedin_queue.csv")
    li.add_argument("--open-browser", action="store_true")

    mark_li = sub.add_parser("mark-linkedin-sent")
    mark_li.add_argument("identifier", help="Lead email or company domain")
    mark_li.add_argument("--log", default="out/outreach_log.csv")

    replies = sub.add_parser("watch-replies")
    replies.add_argument("--config", default="config.toml")
    replies.add_argument("--log", default="out/outreach_log.csv")
    replies.add_argument("--auto-reply", action=argparse.BooleanOptionalAction, default=True)
    replies.add_argument("--sync-sheets", action="store_true")

    run = sub.add_parser("run")
    run.add_argument("--config", default="config.toml")
    run.add_argument("--leads", default="data/starter_leads.csv")
    run.add_argument("--limit", type=int, default=10)
    run.add_argument("--log", default="out/outreach_log.csv")
    run.add_argument("--send-email", action="store_true")
    run.add_argument("--sync-sheets", action="store_true")

    args = parser.parse_args()
    command = args.command.replace("-", "_")
    globals()[f"{command}_command"](args)


def draft_command(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    records = build_records(read_leads(args.leads, args.limit), cfg)
    write_log(args.log, records)
    print(f"Drafted {len(records)} records to {args.log}")


def send_email_command(args: argparse.Namespace) -> None:
    load_config(args.config)
    records = read_log(args.log)
    sent = 0
    for record in records:
        if record.email_sent_at:
            continue
        send_email(record.lead.email, record.email_subject, record.email_body)
        mark_sent(record)
        sent += 1
    write_log(args.log, records)
    if args.sync_sheets:
        sync_to_google_sheet(records)
    print(f"Sent {sent} emails")


def linkedin_queue_command(args: argparse.Namespace) -> None:
    records = read_log(args.log)
    write_linkedin_queue(records, args.queue)
    if args.open_browser:
        open_profiles(records)
    print(f"Wrote LinkedIn review queue to {args.queue}")


def mark_linkedin_sent_command(args: argparse.Namespace) -> None:
    records = mark_linkedin_sent(read_log(args.log), args.identifier)
    write_log(args.log, records)
    print(f"Marked LinkedIn sent for {args.identifier}")


def watch_replies_command(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    records = update_reply_status(read_log(args.log), cfg, auto_reply=args.auto_reply)
    write_log(args.log, records)
    if args.sync_sheets:
        sync_to_google_sheet(records)
    print("Reply statuses updated")


def run_command(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    records = build_records(read_leads(args.leads, args.limit), cfg)
    if args.send_email:
        for record in records:
            send_email(record.lead.email, record.email_subject, record.email_body)
            mark_sent(record)
    write_log(args.log, records)
    write_linkedin_queue(records)
    if args.sync_sheets:
        sync_to_google_sheet(records)
    print(f"Prepared {len(records)} leads. Log: {args.log}. LinkedIn queue: out/linkedin_queue.csv")


if __name__ == "__main__":
    main()
