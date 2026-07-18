"""
Lineup ingestion — worship leader's order  ->  lineup JSON spec
================================================================
The worship leader emails the service order to the shared Castleberry inbox
(castleberryauditorium@gmail.com). This script turns that free-form order into
a structured lineup spec that build_service_deck.py can assemble.

Two-stage, so it is robust:
  1. Claude reads the raw order text and extracts a structured lineup (songs,
     verses, frames, scripture) using its best guess at each song title.
  2. We resolve every song title *locally* against the real song index, so the
     final spec always points at decks that actually exist. Titles that can't
     be matched are reported with the closest suggestions for you to fix.

Getting the order text in:
  The connected Gmail tool can read Parker's emails but cannot download PDF
  attachments, and the *shared* inbox is a different account. So the simple,
  reliable flow is: open the lineup email (or its PDF), copy the order, paste
  it into a .txt file, and run:

      python parse_lineup.py order.txt
      python parse_lineup.py order.txt -o lineups/6.7.26.json --date 6.7.26

  You can also pipe text in:   type order.txt | python parse_lineup.py -

Requires ANTHROPIC_API_KEY (same as castleberry_hymns.py).
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from pathlib import Path

import anthropic

from build_service_deck import build_song_index, normalize, resolve_song

ROOT          = Path(__file__).parent
TEMPLATE_PATH = ROOT / "service-template" / "template.json"
MODEL         = os.environ.get("LINEUP_MODEL", "claude-haiku-4-5-20251001")


def known_frames() -> list[str]:
    tpl = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    return sorted(tpl.get("frames", {}).keys())


EXTRACT_PROMPT = """You convert a Church of Christ worship service order into a structured JSON lineup.

The service is a cappella. A typical order: a countdown/welcome slide, Call to Worship, \
an opening prayer, several songs (often with specific verses noted, e.g. "vs. 1 & 3" or \
"verse 1 only"), a scripture reading tied to the sermon, the Lord's Supper (communion), \
giving, more songs, and a closing prayer / dismissal.

Output ONLY a JSON object of this exact shape:
{{
  "service": "CB 11 Service line-up",
  "date": "",
  "worship_leader": "",
  "items": [ ... ]
}}

Each item is one of:
  {{"type":"frame","frame":"<one of: {frames}>"}}
  {{"type":"song","title":"<song title as written>","verses":"all" | [1,3] | "1-2"}}
  {{"type":"scripture","title":"<heading>","reference":"<e.g. Hosea 3:1-5>","text":""}}

Rules:
- Keep the items in the same order they appear in the service.
- For songs, copy the title as faithfully as you can; do NOT invent hymnal numbers.
- If verses aren't specified for a song, use "all".
- Map liturgical elements to the closest frame key from the allowed list. If an element \
has no good match, use "blank".
- Leave scripture "text" empty (it will be filled in later); still capture title/reference.
- Do not add commentary. Output only the JSON object.

SERVICE ORDER:
---
{order}
---"""


def extract_lineup(order_text: str) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = EXTRACT_PROMPT.format(frames=", ".join(known_frames()), order=order_text)
    msg = client.messages.create(
        model=MODEL, max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            return json.loads(m.group())
        raise SystemExit(f"Could not parse model output as JSON:\n{raw[:500]}")


def resolve_titles(lineup: dict, index: dict) -> list[str]:
    """Annotate each song with the matched source/number; return unresolved notes."""
    all_titles = sorted({m["name"] for ms in index.values() for m in ms})
    norm_map = {normalize(t): t for t in all_titles}
    notes = []
    for it in lineup.get("items", []):
        if it.get("type") != "song":
            continue
        title = it.get("title", "")
        entry = resolve_song(it, index)
        if entry:
            it["title"]  = entry["name"]          # canonicalize
            it["source"] = entry["source"]
            if entry["number"]:
                it["number"] = entry["number"]
        else:
            close = difflib.get_close_matches(normalize(title), list(norm_map), n=3, cutoff=0.6)
            sugg = [norm_map[c] for c in close]
            notes.append(f"'{title}' — no exact match"
                         + (f"; did you mean: {', '.join(sugg)}?" if sugg else ""))
    return notes


def main():
    for _s in (sys.stdout, sys.stderr):       # survive the Windows cp1252 console
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Convert a worship order into a lineup spec.")
    ap.add_argument("source", help="Path to the order text file, or '-' to read stdin.")
    ap.add_argument("-o", "--out", help="Output lineup JSON path.")
    ap.add_argument("--date", help="Service date label, e.g. 6.7.26")
    ap.add_argument("--service", default="CB 11 Service line-up")
    args = ap.parse_args()

    order_text = sys.stdin.read() if args.source == "-" \
        else Path(args.source).read_text(encoding="utf-8")
    if not order_text.strip():
        raise SystemExit("No order text provided.")

    print("Extracting lineup with Claude…", file=sys.stderr)
    lineup = extract_lineup(order_text)
    if args.date:
        lineup["date"] = args.date
    lineup.setdefault("service", args.service)

    index = build_song_index()
    notes = resolve_titles(lineup, index)

    out = Path(args.out) if args.out else (
        ROOT / "lineups" / (re.sub(r'[<>:"/\\|?*]', "", f"{lineup.get('date','lineup')}") + ".json"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(lineup, indent=2, ensure_ascii=False), encoding="utf-8")

    n_songs = sum(1 for it in lineup["items"] if it.get("type") == "song")
    print(f"\nWrote {out}  ({len(lineup['items'])} items, {n_songs} songs).")
    if notes:
        print("\n⚠ Songs needing review (edit the JSON to fix the title/source/number):")
        for nt in notes:
            print("  •", nt)
    print("\nNext: review the JSON, fill in any scripture text, then run:")
    print(f"    python build_service_deck.py \"{out}\"")


if __name__ == "__main__":
    main()
