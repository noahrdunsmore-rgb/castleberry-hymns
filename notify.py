"""
Email delivery for finished service decks.
==========================================
Sends the built .pptx to a recipient via Gmail SMTP. Used by both the local
build app and the Saturday-night scheduled task.

Credentials are read from (in order) environment variables or a local
`email_config.json` (git-ignored). NOTHING is hard-coded — you supply your own
Gmail address + App Password:

    email_config.json
    {
      "gmail_address": "you@gmail.com",
      "app_password":  "abcd efgh ijkl mnop",   // Gmail App Password, not your login
      "notify_to":     "you@gmail.com"
    }

Create the App Password at https://myaccount.google.com/apppasswords (requires
2-Step Verification). Gmail caps attachments at 25 MB; decks larger than that are
emailed as a notification with the local file path instead of an attachment.
"""

from __future__ import annotations

import json
import mimetypes
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

ROOT          = Path(__file__).parent
CONFIG_PATH   = ROOT / "email_config.json"
ATTACH_LIMIT  = 24 * 1024 * 1024        # stay under Gmail's 25 MB ceiling


def load_config() -> dict | None:
    cfg = {}
    if CONFIG_PATH.exists():
        cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    addr = os.environ.get("GMAIL_ADDRESS", cfg.get("gmail_address"))
    pw   = os.environ.get("GMAIL_APP_PASSWORD", cfg.get("app_password"))
    to   = os.environ.get("NOTIFY_TO", cfg.get("notify_to", addr))
    if not addr or not pw:
        return None
    return {"gmail_address": addr, "app_password": pw, "notify_to": to}


def is_configured() -> bool:
    return load_config() is not None


def send_deck(deck_path: Path, subject: str, body: str,
              to: str | None = None) -> tuple[bool, str]:
    """
    Email the deck (attached if small enough, otherwise a notification).
    Returns (ok, human-readable status).
    """
    cfg = load_config()
    if cfg is None:
        return False, ("Email not configured — set GMAIL_ADDRESS + "
                       "GMAIL_APP_PASSWORD or create email_config.json.")

    deck_path = Path(deck_path)
    recipient = to or cfg["notify_to"]

    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = cfg["gmail_address"], recipient, subject

    attached = False
    if deck_path.exists() and deck_path.stat().st_size <= ATTACH_LIMIT:
        ctype, _ = mimetypes.guess_type(str(deck_path))
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        msg.set_content(body)
        msg.add_attachment(deck_path.read_bytes(), maintype=maintype,
                           subtype=subtype, filename=deck_path.name)
        attached = True
    else:
        size_mb = deck_path.stat().st_size / 1e6 if deck_path.exists() else 0
        note = (f"\n\n(The deck is {size_mb:.0f} MB — too large to attach. "
                f"It's saved locally at:\n{deck_path})") if deck_path.exists() else \
               f"\n\n(Deck not found at {deck_path}.)"
        msg.set_content(body + note)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
            s.login(cfg["gmail_address"], cfg["app_password"])
            s.send_message(msg)
    except Exception as e:
        return False, f"Email failed: {e}"

    return True, (f"Emailed deck to {recipient}"
                  + (" (attached)." if attached else " (link/path only — too big to attach)."))
