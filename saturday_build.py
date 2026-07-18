"""
Saturday-night safety net.
==========================
Run unattended by Windows Task Scheduler each Saturday evening so a deck for the
upcoming Sunday is ready before the 11:50 PM CST deadline. Logic:

  • Find the most recent lineup spec in lineups/ (excluding the example).
  • No recent lineup?  ->  email a reminder to prepare/build the deck.
  • Lineup present but no up-to-date deck?  ->  build it and email it.
  • Deck already built and current?  ->  do nothing (idempotent) unless --force.

Everything is logged to saturday_build.log so each scheduled run is auditable.
Register it with register_saturday_task.ps1.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import build_service_deck as bsd
import notify

# Survive the Windows cp1252 console when run by Task Scheduler / a plain shell.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT     = Path(__file__).parent
LINEUPS  = ROOT / "lineups"
LOG_PATH = ROOT / "saturday_build.log"
RECENT_DAYS = 8          # only consider a lineup prepared within the past week


def log(msg: str):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def upcoming_sunday(today: datetime | None = None) -> datetime:
    today = today or datetime.now()
    days = (6 - today.weekday()) % 7        # Monday=0 … Sunday=6
    if days == 0:                           # today is Sunday → mean the next one
        days = 7
    return (today + timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)


def find_recent_lineup() -> Path | None:
    if not LINEUPS.is_dir():
        return None
    cutoff = datetime.now() - timedelta(days=RECENT_DAYS)
    cands = [p for p in LINEUPS.glob("*.json")
             if p.name != "example-service.json"
             and datetime.fromtimestamp(p.stat().st_mtime) >= cutoff]
    if not cands:
        return None
    return max(cands, key=lambda p: p.stat().st_mtime)


def main():
    ap = argparse.ArgumentParser(description="Saturday safety-net deck build.")
    ap.add_argument("--force", action="store_true", help="Rebuild even if a current deck exists.")
    ap.add_argument("--no-email", action="store_true", help="Build/log only; never send email.")
    args = ap.parse_args()

    sunday = upcoming_sunday()
    log(f"=== Safety-net run for Sunday {sunday:%Y-%m-%d} ===")

    lineup_path = find_recent_lineup()
    if lineup_path is None:
        msg = (f"No lineup prepared for this Sunday ({sunday:%b %d}) yet.\n\n"
               f"Please build the service deck before 11:50 PM tonight:\n"
               f"  • open the builder:  python service_app.py  →  http://127.0.0.1:5000\n"
               f"  • or run:  python build_service_deck.py lineups\\<your-lineup>.json")
        log("No recent lineup found — sending reminder.")
        if not args.no_email:
            ok, status = notify.send_deck(Path("none"),
                subject=f"⚠ No worship deck prepared for Sunday {sunday:%b %d}",
                body=msg)
            log(status)
        return

    lineup = json.loads(lineup_path.read_text(encoding="utf-8"))
    template = json.loads((ROOT / "service-template" / "template.json").read_text(encoding="utf-8"))
    out_path = bsd.default_out_name(lineup, lineup_path)

    spec_mtime = lineup_path.stat().st_mtime
    if out_path.exists() and out_path.stat().st_mtime >= spec_mtime and not args.force:
        log(f"Deck already current: {out_path.name} — nothing to do.")
        return

    log(f"Building from {lineup_path.name} -> {out_path.name}")
    index = bsd.build_song_index()
    report = bsd.build(lineup, out_path, template, index)
    log(f"Built {report['total_slides']} slides.")
    for w in report.get("warnings", []):
        log("  warning: " + w)

    if not args.no_email:
        ok, status = notify.send_deck(
            Path(report["out"]),
            subject=f"Service deck ready — {lineup.get('service','CB Service')} ({lineup.get('date','')})",
            body=(f"The worship slide deck for Sunday {sunday:%b %d} is built "
                  f"({report['total_slides']} slides)."
                  + ("\n\nNote — some items need attention:\n• " + "\n• ".join(report["warnings"])
                     if report.get("warnings") else "")))
        log(status)


if __name__ == "__main__":
    main()
