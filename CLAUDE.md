# Castleberry Hymn Tools

Web app: hymn tracker + downloader + service deck builder.
Hosted: https://noahrdunsmore-rgb.github.io/castleberry-hymns/
Dev: `python3 -m http.server 3400`

## Key people
- Noah Dunsmore — AV, leads 11 AM singing ~40% of Sundays
- Parker Jennings / castleberryauditorium@gmail.com — manages slides, sends weekly lineup PDFs
- Song leaders: Thomas Holder, Sawyer Gann, Larry Watkins, Jason Brackeen, Josh Jackson, Jim Colby, Coyte Greer, Brett Billingsley, Shawn Abraham, Nathan Hersey

## Gmail — IMPORTANT
- `noahrdunsmore@gmail.com` → Gmail MCP tool (cheap, use this)
- `castleberryauditorium@gmail.com` → Chrome browser at `mail.google.com/mail/u/1/`
  **⚠ Always use `get_page_text`, NEVER `read_page` on Gmail — accessibility trees = ~50k tokens. Ask before any inbox sweep.**

## Tracker (castleberry_songs.json)
167 songs, 233 occurrences. Sources: `email` (accurate) and `youtube` (approximate).
Leaders email song lists to castleberry inbox each Saturday night.
Update path: read email → short Python script → git commit. See `rebuild_tracker_from_emails.py`.

## Service deck builder
- `service_app.py` → local Flask UI at http://127.0.0.1:5000
- Deadline: deck ready by 11:50 PM CST Saturday
- `register_saturday_task.ps1` → register Windows scheduled task (not yet run)
- See `SERVICE_BUILDER.md` for full docs

## What still needs doing
- Saturday scheduled task not yet registered on Noah's PC
- March 2026 and earlier inbox submissions not captured (low priority)
