# Castleberry Church of Christ — Hymn Tools

## What this project is
A set of tools for Castleberry Church of Christ (Fort Worth, TX) worship ops:
1. **Hymn Tracker** — web app tracking every song sung, who led it, which service
2. **Hymn Downloader** — download slide decks (892 songs: HFWR, HFWS, eChoice)
3. **Service Deck Builder** — assembles a full Sunday-service .pptx from a lineup

Hosted at: https://noahrdunsmore-rgb.github.io/castleberry-hymns/
Local dev server: `python3 -m http.server 3400` (launch config in `.claude/launch.json`)

## Key people
- **Noah Dunsmore** (noahrdunsmore@gmail.com) — runs AV, leads 11 AM singing ~40% of Sundays
- **Parker Jennings** (parkerray@me.com / castleberryauditorium@gmail.com) — manages slides, sends weekly lineup PDFs
- **Chad Slone** (coslone@icloud.com) — also manages castleberry inbox
- **Song leaders**: Thomas Holder, Sawyer Gann, Larry Watkins, Jason Brackeen, Josh Jackson, Jim Colby, Coyte Greer, Brett Billingsley, Shawn Abraham, Nathan Hersey

## Critical: two Gmail accounts
- **noahrdunsmore@gmail.com** — connected to the Gmail MCP tool (can search/read emails here)
- **castleberryauditorium@gmail.com** — the shared church inbox. NOT connected to Gmail MCP.
  Access via Chrome browser tools at `mail.google.com/mail/u/1/` (it's the second logged-in account).
  **⚠ Reading the full inbox accessibility tree is ~50k tokens. Use `get_page_text` only. Ask before any large Gmail read.**

## Tracker data (castleberry_songs.json)
- 167 songs, 233 occurrences as of 2026-06-03
- Sources: `"email"` (confirmed from leader submissions — accurate) and `"youtube"` (transcript-based — approximate)
- Leaders email their song lists to castleberryauditorium@gmail.com each Saturday night
- To update: read the email → run a short Python script → git commit. See `rebuild_tracker_from_emails.py`.

## Service deck builder
- `build_service_deck.py` — assembles .pptx from a lineup JSON spec
- `service_app.py` — local Flask UI at http://127.0.0.1:5000 (paste order → build → download/email)
- `saturday_build.py` + `register_saturday_task.ps1` — Windows scheduled task, runs Sat 9 PM
- Deadline: deck ready by 11:50 PM CST each Saturday
- Delivery: local `service-decks/` + email via `notify.py` (configure `email_config.json`)
- See `SERVICE_BUILDER.md` for full docs

## Key files
| File | Purpose |
|------|---------|
| `index.html` | Single-page app: tracker + downloader + lookup bar |
| `castleberry_songs.json` | All tracked hymn occurrences |
| `hymn_catalogue.json` | 892-song download catalogue |
| `hymn_topics.json` | Topic tags for all hymns |
| `build_service_deck.py` | Service deck assembly engine |
| `service_app.py` | Local web UI ("the button") |
| `rebuild_tracker_from_emails.py` | Re-applies email-sourced song data |
| `castleberry_hymns.py` | YouTube transcript processor (runs weekly) |

## Current state (as of 2026-06-03)
- Dashboard redesign complete: side-by-side panels (tracker left, downloader right), viewport-filling, no tabs
- "When was this last sung?" lookup bar at top
- "Build Service Deck" button in header opens localhost:5000
- Hymn Downloader starts empty — search or click Show All
- Wednesday Evening services now tracked (in addition to Sunday AM services)

## What still needs doing
- Hymn 470 (Josh Jackson Apr 8) was the last inbox item captured
- March 2026 and earlier inbox submissions not yet read (lower priority)
- `saturday_build.py` not yet tested end-to-end
- `register_saturday_task.ps1` not yet run on Noah's PC
