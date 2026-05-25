"""
Castleberry Church of Christ — Hymn Tracker
Fetches NEW worship service videos from YouTube, extracts transcripts,
and uses Claude to identify hymns sung. Updates incrementally (skips
already-processed videos) so it can run weekly without re-doing old work.
"""

import os
import json
import re
import time
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import anthropic

# ── Config ──────────────────────────────────────────────────────────────────
YOUTUBE_API_KEY = "AIzaSyArD-dHJ7Or_UNsOMcdn1-Q21kbCO3TloI"
CHANNEL_ID      = "UCIvjPR5lGI39VtzyNz05lSw"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL           = "claude-sonnet-4-20250514"

SCRIPT_DIR      = Path(__file__).parent
OUTPUT_FILE     = SCRIPT_DIR / "castleberry_songs.json"
PROCESSED_FILE  = SCRIPT_DIR / "processed_videos.json"

ONE_YEAR_AGO = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Persistence helpers ──────────────────────────────────────────────────────

def load_processed_videos() -> set:
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_processed_videos(processed: set) -> None:
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(processed), f, indent=2)


def load_existing_hymns() -> dict:
    """Returns {hymn_name: set_of_dates}."""
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return {item["name"]: set(item["dates"]) for item in data}
    return {}


def save_hymns(hymn_dates: dict) -> None:
    output = [
        {"name": name, "dates": sorted(dates)}
        for name, dates in sorted(hymn_dates.items())
    ]
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

# ── YouTube helpers ──────────────────────────────────────────────────────────

def get_channel_videos() -> list:
    """Fetch all videos uploaded to the channel in the past year."""
    videos, page_token = [], None
    url = "https://www.googleapis.com/youtube/v3/search"

    print("Fetching video list from YouTube...")
    while True:
        params = {
            "key": YOUTUBE_API_KEY,
            "channelId": CHANNEL_ID,
            "part": "snippet",
            "type": "video",
            "order": "date",
            "publishedAfter": ONE_YEAR_AGO,
            "maxResults": 50,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get("items", []):
            videos.append({
                "id":    item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "date":  item["snippet"]["publishedAt"][:10],   # YYYY-MM-DD
            })

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    print(f"  Found {len(videos)} videos in the past year.")
    return videos


def get_transcript(video_id: str) -> str | None:
    """Return the English transcript text for a video, or None if unavailable."""
    ytt = YouTubeTranscriptApi()
    try:
        tlist = ytt.list(video_id)
        try:
            t = tlist.find_manually_created_transcript(["en"])
        except Exception:
            t = tlist.find_generated_transcript(["en"])
        return " ".join(s.text for s in t.fetch())
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        print(f"    No transcript: {e}")
        return None
    except Exception as e:
        print(f"    Transcript error: {e}")
        return None

# ── Claude helper ────────────────────────────────────────────────────────────

def identify_hymns(client, transcript: str, title: str, date: str) -> list:
    """Ask Claude to return a JSON array of hymn titles sung in the service."""
    prompt = f"""You are analyzing a transcript from a Church of Christ worship service video.

Video title: {title}
Date: {date}

Transcript:
{transcript[:12000]}

Your task: Identify any Christian hymns or worship songs that were actually SUNG during \
this service (not just mentioned or read). Church of Christ services are a cappella (no \
instruments), so look for song lyrics being transcribed.

Return ONLY a JSON array of hymn title strings. Use the standard/canonical hymn title \
(e.g., "Amazing Grace" not "amazing grace"). If no hymns can be identified, return [].

Examples of valid output:
["Amazing Grace", "How Great Thou Art", "Blessed Assurance"]
[]

Return only the JSON array, no other text."""

    msg = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()

    try:
        hymns = json.loads(raw)
        if isinstance(hymns, list):
            return [h for h in hymns if isinstance(h, str)]
    except json.JSONDecodeError:
        m = re.search(r"\[.*?\]", raw, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
    print(f"    Could not parse hymn list: {raw[:200]}")
    return []

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not ANTHROPIC_API_KEY:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable is not set.")

    client    = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    processed = load_processed_videos()
    hymn_dates = load_existing_hymns()

    all_videos = get_channel_videos()
    new_videos = [v for v in all_videos if v["id"] not in processed]

    skipped = len(all_videos) - len(new_videos)
    print(f"  {len(new_videos)} new video(s) to process  ({skipped} already done).")

    if not new_videos:
        print("Nothing new — exiting.")
        return

    for i, video in enumerate(new_videos, 1):
        vid_id, title, date = video["id"], video["title"], video["date"]
        print(f"\n[{i}/{len(new_videos)}] {date} — {title}")

        transcript = get_transcript(vid_id)
        if transcript:
            print(f"  Transcript: {len(transcript):,} chars — asking Claude...")
            hymns = identify_hymns(client, transcript, title, date)
            if hymns:
                print(f"  Hymns found: {hymns}")
                for hymn in hymns:
                    hymn_dates.setdefault(hymn, set()).add(date)
            else:
                print("  No hymns identified.")
        else:
            print("  Skipping (no transcript).")

        processed.add(vid_id)
        time.sleep(0.5)   # be polite to the APIs

    save_hymns(hymn_dates)
    save_processed_videos(processed)

    print(f"\nDone! {len(hymn_dates)} unique hymns across all tracked services.")
    print(f"Saved → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
