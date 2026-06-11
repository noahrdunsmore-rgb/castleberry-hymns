"""
Append the June 7 (Sun 11 AM, Sawyer Gann) and June 10 (Wed Evening,
Josh Jackson) email-sourced services to castleberry_songs.json.

Source emails (castleberryauditorium@gmail.com):
  - Sawyer Gann, "Sun 6/7 - 11 AM Songs" (Jun 4) — service order; liturgical
    lines (Prayer, LS, Lesson) and the post-"I.C.O.B." standby-baptism songs
    (117/110/125/104) are excluded.
  - jrjackson (Josh Jackson), "Songs 06-10-26" (Jun 10) — Wednesday songs.

Run: python add_jun7_jun10.py
"""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT  = ROOT / "castleberry_songs.json"

NEW_RECORDS = [
    ("2026-06-07", "Sunday 11:00 AM", "Sawyer Gann", [
        "Lamb of God",
        "Mended and Whole",
        "Beautiful Lamb of God",
        "Are You Washed in the Blood",
        "We Will Glorify the King of Kings",
    ]),
    ("2026-06-10", "Wednesday Evening", "Josh Jackson", [
        "I Want to Be a Worker",
        "What Will Your Answer Be?",
    ]),
]


def normalize(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def main():
    shutil.copy(OUT, OUT.with_suffix(".bak3.json"))

    songs = json.loads(OUT.read_text(encoding="utf-8"))
    idx = {normalize(s["name"]): s for s in songs}

    added_occ = added_song = 0
    for date, service, leader, titles in NEW_RECORDS:
        for title in titles:
            key = normalize(title)
            occ = {"date": date, "service": service, "leader": leader, "source": "email"}
            if key in idx:
                entry = idx[key]
                existing = {(o["date"], o.get("leader", ""), o.get("service", ""))
                            for o in entry["occurrences"]}
                if (date, leader, service) not in existing:
                    entry["occurrences"].append(occ)
                    added_occ += 1
            else:
                entry = {"name": title, "occurrences": [occ]}
                songs.append(entry)
                idx[key] = entry
                added_song += 1
                added_occ += 1

    for entry in songs:
        entry["occurrences"].sort(key=lambda o: o["date"])
    songs.sort(key=lambda s: s["name"].lower())

    OUT.write_text(json.dumps(songs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Done. {added_song} new songs, {added_occ} new occurrences.")


if __name__ == "__main__":
    main()
