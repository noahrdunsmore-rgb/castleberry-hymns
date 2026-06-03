# Worship Service Deck Builder

Assembles a complete Sunday-service PowerPoint from a **lineup spec**, following
the worship leader's service order. It stitches together the per-song decks this
project already builds (HFWR / HFWS / eChoice / hand-made) and inserts the
recurring liturgical "frame" slides (Call to Worship, Communion, Giving, Prayer,
scripture readings, …).

Every source slide in the project is a single full-bleed picture, so the songs
come through pixel-identical to their original decks; only the frame and
scripture slides are freshly rendered (Century Schoolbook on Castleberry red).

## Files

| File | What it is |
|------|------------|
| `build_service_deck.py` | The engine. Reads a lineup → writes a combined `.pptx`. |
| `service-template/template.json` | Editable definitions + styling for every frame slide. |
| `lineups/example-service.json` | A worked example modeled on Parker's 11:00 order. |
| `parse_lineup.py` | Turns a worship leader's free-form order into a lineup spec. |
| `service_app.py` | **The button** — local web app: paste order → build → download/email. |
| `notify.py` + `email_config.example.json` | Emails the finished deck (Gmail SMTP). |
| `saturday_build.py` + `register_saturday_task.ps1` | Saturday-night safety net (auto-build/remind). |
| `service-decks/` | Output decks land here (git-ignored). |

## How it gets kicked off

The deck must be built **on this PC** (it reads the local song assets, including
the ~700 HFWR/HFWS per-verse PNG folders that aren't in git). Two triggers:

### 1. The button (when the lineup's ready)
```bash
python service_app.py        # then open http://127.0.0.1:5000
```
Paste the worship leader's order → **Parse with AI** → review the lineup →
**Build Deck**. The deck saves to `service-decks/`, offers a download, and (if
email is set up) emails you a copy. Tip: make a desktop shortcut to
`pythonw service_app.py` so it's one double-click.

### 2. Saturday-night safety net (so the 11:50 PM deadline is never missed)
Register a Windows scheduled task once:
```powershell
powershell -ExecutionPolicy Bypass -File register_saturday_task.ps1
```
Every Saturday at 9:00 PM it runs `saturday_build.py`, which:
- builds + emails the deck if this week's lineup is prepared but no current deck exists;
- does nothing if a current deck is already built (idempotent);
- emails you a **reminder** if no lineup has been prepared yet — leaving time to
  build manually before 11:50 PM.

Change the time with `-Time "21:30"`, or remove it with `-Unregister`.

## Email setup (optional but needed for delivery)

Copy `email_config.example.json` to `email_config.json` and fill in your Gmail
address + an [App Password](https://myaccount.google.com/apppasswords) (not your
login). `email_config.json` is git-ignored. Decks over 25 MB are emailed as a
notification with the local path instead of an attachment (Gmail's limit).

## Quick start

```bash
# Build the example
python build_service_deck.py lineups/example-service.json

# Build a real one to a chosen path
python build_service_deck.py lineups/6.7.26.json -o "service-decks/CB 11 (6.7.26).pptx"

# See every song title the builder can resolve
python build_service_deck.py --list-songs
```

## The lineup spec

A JSON object with an ordered `items` list. Each item is one of three types:

```jsonc
{ "type": "frame", "frame": "call_to_worship" }       // a template slide

{ "type": "song",  "title": "The Gloryland Way",
  "source": "HFWR", "number": "574",                   // source/number optional — only to disambiguate
  "verses": "all" }                                    // "all" | 1 | [1,3] | "1-2"

{ "type": "scripture", "title": "Hosea's Amazing Act of Love",
  "reference": "Hosea 3:1-5",
  "text": ["1 And the LORD said…", "2 So I bought her…"] }   // list = one slide per verse
```

**Verse selection** works for HFWR & HFWS songs (their per-verse source images
are on disk). For eChoice / hand-made decks the whole song is included and a
warning is printed if specific verses were requested.

**Frames** available out of the box (edit `template.json` to add/restyle):
`countdown, welcome, please_be_seated, please_stand, call_to_worship, prayer,
opening_prayer, closing_prayer, scripture_reading, lords_supper, communion,
giving, sermon, invitation, announcements, dismissal, blank`.

To use Parker's exact artwork for a frame instead of the solid background, add a
`"background"` path (relative to the project root) to that frame in
`template.json` — the builder will drop the image in full-bleed and skip the
generated text.

## Getting a lineup in from email

The worship leader emails the order to the shared inbox
(`castleberryauditorium@gmail.com`). Because the lineup arrives as a PDF
attachment that the current Gmail tool can't download, the reliable flow is:

1. Open the email (or its PDF) and copy the service order text into `order.txt`.
2. Convert it to a spec (requires `ANTHROPIC_API_KEY`):
   ```bash
   python parse_lineup.py order.txt --date 6.7.26
   ```
   Claude extracts the order; every song title is then matched **locally**
   against the real song index, so the spec only points at decks that exist.
   Unmatched titles are reported with close suggestions to fix by hand.
3. Review the generated `lineups/<date>.json` (fix any flagged songs, paste in
   the scripture text), then build it.

## How songs are resolved

`build_song_index()` merges, in priority order:

1. **HFWR / HFWS Output** (from `hymn_catalogue.json`) — verse-selectable.
2. **eChoice Output** (`hymn-slides/eChoice Output/<name>/<name>.pptx`).
3. **Hand-made decks** (`hymn-slides/*.pptx`).

Titles are matched on a normalized (lowercase, punctuation-stripped) key. When a
title exists in more than one hymnal, add `"source"` and/or `"number"` to the
lineup item to pick the right one.
