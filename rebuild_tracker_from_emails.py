"""
Rebuild castleberry_songs.json from email-sourced song submissions.
================================================================
The ground truth for who led what is the emails that song leaders send
to the shared Castleberry inbox (castleberryauditorium@gmail.com).
This script encodes every email-derived service record collected from
inbox and merges it into the tracker, preserving YouTube-derived entries
for dates not covered by emails.

Run: python rebuild_tracker_from_emails.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent
OUT  = ROOT / "castleberry_songs.json"

# ---------------------------------------------------------------------------
# Email-derived service records
# Format: (date, service_type, leader, [song_titles])
# Songs that are liturgical elements (Prayer, Lord Supper, Sermon, Lesson,
# Closing Prayer, etc.) are stripped below.
# ---------------------------------------------------------------------------

SKIP = {
    "prayer", "lord supper", "lord's supper", "sermon", "lesson",
    "closing prayer", "opening prayer", "elders prayer", "elders prayers",
    "elders prayers for school kids",
}

def is_song(line):
    return line.lower().strip() not in SKIP and line.strip()

EMAIL_RECORDS = [
    # ── 2025 ──────────────────────────────────────────────────────────────
    ("2025-06-22", "Sunday 11:00 AM", "Noah Dunsmore", [
        "The Unclouded Day",
        "Shine, Jesus, Shine",
        "Near the Cross",
        "Rise Up Again",
        "Give Me the Bible",       # updated from Lord I'm Coming Home
    ]),
    ("2025-06-29", "5th Sunday PM", "Noah Dunsmore", [
        "Shout Hallelujah",
        "Today Is the Day",
        "The Walls Came Tumbling Down",
        "I Have Decided to Follow Jesus",
        "In His Time",
    ]),
    ("2025-07-13", "Sunday 11:00 AM", "Noah Dunsmore", [
        "King of Kings",
        "The Lord Is in His Holy Temple",
        "He Carried My Sorrows",
        "Salvation Has Been Brought Down",
        "He Gave Me a Song",
        "Walk Beside Me",
    ]),
    ("2025-08-10", "Sunday 11:00 AM", "Noah Dunsmore", [
        "How Can I Keep From Singing",
        "Calvary",
        "I Want to Be a Worker",
        "I Will Call Upon the Lord",
        "In Need",
    ]),
    ("2025-09-07", "Sunday 11:00 AM", "Noah Dunsmore", [
        "He's My King",
        "Calvary",
        "Guide Me, O Thou Great Jehovah",
        "Jesus Paid It All",
        "When All of God's Singers Get Home",
    ]),
    # Oct 4, 2025 — Saturday Gospel Meeting (Thomas sent the full table)
    ("2025-10-04", "Gospel Meeting", "Thomas Holder", [
        "Be Thou My Vision",
        "Shout Hallelujah",
        "Praise the Lord",
    ]),
    ("2025-10-04", "Gospel Meeting", "Sawyer Gann", [
        "The Great Redeemer",
        "Jesus, Only Jesus",
        "Where No One Stands Alone",
        "In the Service of My King",
    ]),
    ("2025-10-04", "Gospel Meeting", "Noah Dunsmore", [
        "10,000 Reasons",
        "At the Cross (Love Ran Red)",
        "Ancient Words",
        "A Shield About Me",
    ]),
    # Oct 5, 2025 — Sunday 11 AM (Noah led the Sunday morning service of the GM)
    ("2025-10-05", "Sunday 11:00 AM", "Noah Dunsmore", [
        "Jesus Draw Me Ever Nearer",
        "Calvary",
        "Christian, Remember Who You Are",
        "Coming Home",
        "You Are the Song That I Sing",
    ]),
    ("2025-11-09", "Sunday 11:00 AM", "Noah Dunsmore", [
        "Each Step I Take",
        "Exalted",
        "Just a Closer Walk With Thee",
        "Hand in Hand With Jesus",
        "In Need",
    ]),
    ("2025-11-30", "5th Sunday PM", "Noah Dunsmore", [
        "Be Unto Your Name",
        "Shine, Jesus, Shine",
        "On Bended Knee I Come",
        "There's Something About That Name",
    ]),
    ("2025-12-07", "Sunday 11:00 AM", "Noah Dunsmore", [
        "Sweet Hour of Prayer",
        "Oh the Blood",
        "His Grace Reaches Me",
        "Burdens Are Lifted at Calvary",
        "Walk Beside Me",
    ]),
    # ── 2026 ──────────────────────────────────────────────────────────────
    ("2026-01-11", "Sunday 11:00 AM", "Noah Dunsmore", [
        "To God Be the Glory",
        "Come Just as You Are",
        "There Is a Green Hill Far Away",
        "Jesus Draw Me Ever Nearer",
        "I Surrender All",
        "Rock of Ages",
    ]),
    ("2026-02-08", "Sunday 11:00 AM", "Noah Dunsmore", [
        "Yet Not I But Through Christ in Me",
        "It Was Finished Upon That Cross",
        "On Jordan's Stormy Banks",
        "There's a Fountain Free",
        "Remember Who You Are",
    ]),
    ("2026-03-01", "Sunday 11:00 AM", "Noah Dunsmore", [
        "Soliloquy and Prayer",
        "A Shield About Me",
        "Calvary",
        "Where No One Stands Alone",
        "Come Just as You Are",
        "We Are One",
    ]),
    # Mar 7, 2026 — Saturday Gospel Meeting evening
    ("2026-03-07", "Gospel Meeting", "Sawyer Gann", [
        "Wonderful City of God",
        "The Kingdoms of Earth Pass Away",
    ]),
    ("2026-03-07", "Gospel Meeting", "Noah Dunsmore", [
        "A Passion for My God",
        "Oh How Good It Is",
        "Come to Jesus Today",
    ]),
    ("2026-03-07", "Gospel Meeting", "Thomas Holder", [
        "10,000 Reasons",
        "Zion, Sing",
    ]),
    ("2026-05-18", "Sunday 11:00 AM", "Noah Dunsmore", [
        "There Is a Habitation",
        "There Is a Green Hill Far Away",
        "Oh to Be Like Thee",
        "Come Just as You Are",
        "Just a Closer Walk With Thee",
    ]),
]


# ---------------------------------------------------------------------------
# Merge into the tracker
# ---------------------------------------------------------------------------

def normalize(s):
    import re
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load():
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return []


def build_index(songs):
    """{ normalized_name -> song_entry (reference) }"""
    return {normalize(s["name"]): s for s in songs}


def main():
    import shutil
    shutil.copy(OUT, OUT.with_suffix(".bak2.json"))

    songs = load()
    idx   = build_index(songs)

    added_occ = 0
    added_song = 0
    updated_dates = set()

    for date, service, leader, song_titles in EMAIL_RECORDS:
        for title in song_titles:
            key = normalize(title)
            occ = {"date": date, "service": service, "leader": leader, "source": "email"}

            if key in idx:
                entry = idx[key]
                # Don't add a duplicate (same date + leader + service)
                existing_keys = {(o["date"], o.get("leader",""), o.get("service",""))
                                 for o in entry["occurrences"]}
                if (date, leader, service) not in existing_keys:
                    entry["occurrences"].append(occ)
                    added_occ += 1
                    updated_dates.add(date)
            else:
                new_entry = {"name": title, "occurrences": [occ]}
                songs.append(new_entry)
                idx[key] = new_entry
                added_song += 1
                added_occ  += 1
                updated_dates.add(date)

    # Tag all existing YouTube-sourced entries (those without a source field)
    for entry in songs:
        for occ in entry["occurrences"]:
            if "source" not in occ:
                occ["source"] = "youtube"

    # Remove the YouTube-derived "Where He Leads I'll Follow" on 2026-05-18
    # because the email for that service does NOT include that song — it was
    # a transcript mis-identification.
    corrected = 0
    for entry in songs:
        if normalize(entry["name"]) == normalize("Where He Leads, I'll Follow"):
            before = len(entry["occurrences"])
            entry["occurrences"] = [
                o for o in entry["occurrences"]
                if not (o["date"] == "2026-05-18" and o.get("source") == "youtube")
            ]
            corrected += before - len(entry["occurrences"])

    # Sort each song's occurrences by date
    for entry in songs:
        entry["occurrences"].sort(key=lambda o: o["date"])

    # Sort songs by name
    songs.sort(key=lambda s: s["name"].lower())

    OUT.write_text(json.dumps(songs, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Done.")
    print(f"  {added_song} new song entries added.")
    print(f"  {added_occ} new occurrences added across {len(updated_dates)} service dates.")
    print(f"  {corrected} incorrect YouTube occurrence(s) removed.")
    print(f"  All pre-existing entries tagged source=youtube.")
    print(f"  Saved -> {OUT}")


if __name__ == "__main__":
    main()
