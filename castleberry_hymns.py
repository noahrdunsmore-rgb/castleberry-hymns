"""
Castleberry Church of Christ — Hymn Tracker
Fetches NEW worship service videos from YouTube, extracts transcripts,
and uses Claude to identify hymns sung AND who led each song.
Updates incrementally — skips already-processed videos.
"""

import os
import json
import re
import time
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, IpBlocked
import anthropic

# ── Config ───────────────────────────────────────────────────────────────────
YOUTUBE_API_KEY   = "AIzaSyArD-dHJ7Or_UNsOMcdn1-Q21kbCO3TloI"
CHANNEL_ID        = "UCIvjPR5lGI39VtzyNz05lSw"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL             = "claude-haiku-4-5-20251001"

SCRIPT_DIR     = Path(__file__).parent
OUTPUT_FILE    = SCRIPT_DIR / "castleberry_songs.json"
PROCESSED_FILE = SCRIPT_DIR / "processed_videos.json"

ONE_YEAR_AGO = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Persistence ───────────────────────────────────────────────────────────────

def load_processed_videos() -> set:
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_processed_videos(processed: set) -> None:
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(processed), f, indent=2)


def load_existing_hymns() -> dict:
    """Returns {hymn_name: [{"date": ..., "leader": ...}, ...]}"""
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return {item["name"]: list(item.get("occurrences", [])) for item in data}
    return {}


def save_hymns(hymn_occurrences: dict) -> None:
    output = [
        {
            "name": name,
            "occurrences": sorted(occs, key=lambda x: x["date"]),
        }
        for name, occs in sorted(hymn_occurrences.items())
    ]
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

# ── YouTube ───────────────────────────────────────────────────────────────────

def get_channel_videos() -> list:
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
                "date":  item["snippet"]["publishedAt"][:10],
            })
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    print(f"  Found {len(videos)} videos in the past year.")
    return videos


class YouTubeBlocked(Exception):
    """Raised when YouTube is actively blocking requests — video should NOT be marked processed."""
    pass


def get_transcript(video_id: str, retries: int = 3) -> str | None:
    """
    Returns transcript text, None if genuinely unavailable, or raises
    YouTubeBlocked if the IP is being rate-limited (so the caller can skip
    marking the video as processed and retry it next run).
    """
    ytt = YouTubeTranscriptApi()
    for attempt in range(1, retries + 1):
        try:
            tlist = ytt.list(video_id)
            try:
                t = tlist.find_manually_created_transcript(["en"])
            except Exception:
                t = tlist.find_generated_transcript(["en"])
            return " ".join(s.text for s in t.fetch())
        except IpBlocked:
            if attempt < retries:
                wait = 30 * attempt
                print(f"    IP blocked — waiting {wait}s before retry {attempt}/{retries - 1}...")
                time.sleep(wait)
            else:
                print(f"    IP still blocked after {retries} attempts — will retry this video next run.")
                raise YouTubeBlocked()
        except (NoTranscriptFound, TranscriptsDisabled) as e:
            print(f"    No transcript available (captions disabled): {e}")
            return None
        except Exception as e:
            msg = str(e).lower()
            if "blocking" in msg or "ipblocked" in msg or "requestblocked" in msg:
                if attempt < retries:
                    wait = 30 * attempt
                    print(f"    Rate limited — waiting {wait}s (retry {attempt}/{retries - 1})...")
                    time.sleep(wait)
                else:
                    print(f"    Still blocked — will retry next run.")
                    raise YouTubeBlocked()
            else:
                print(f"    Transcript error: {e}")
                return None
    return None

# ── Claude ────────────────────────────────────────────────────────────────────

def identify_hymns_and_leaders(client, transcript: str, title: str, date: str) -> list:
    """
    Returns a list of dicts: [{"hymn": "Amazing Grace", "leader": "John Smith"}, ...]
    Leader is "" if not identifiable.
    """
    prompt = f"""You are analyzing a transcript from a Church of Christ worship service video.

Video title: {title}
Date: {date}

Transcript:
{transcript[:14000]}

Your task:
1. Identify any Christian hymns or worship songs that were actually SUNG during this service \
(not just mentioned or read). Church of Christ services are a cappella (no instruments), \
so look for song lyrics being transcribed.
2. For each hymn, try to identify WHO LED the song. Song leaders are often announced before \
the song (e.g. "John will lead us in Amazing Grace", or someone says "I'll lead us in..."). \
Use the person's name as it appears. If the leader is not mentioned, use "".

Return ONLY a valid JSON array of objects. Use standard/canonical hymn titles. \
If no hymns can be identified, return [].

Valid output examples:
[
  {{"hymn": "Amazing Grace", "leader": "John Smith"}},
  {{"hymn": "Holy, Holy, Holy", "leader": ""}}
]
[]

Return only the JSON array, no other text."""

    msg = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()

    # Try direct parse
    try:
        result = json.loads(raw)
        if isinstance(result, list):
            out = []
            for item in result:
                if isinstance(item, dict) and "hymn" in item:
                    out.append({
                        "hymn":   str(item["hymn"]).strip(),
                        "leader": str(item.get("leader", "")).strip(),
                    })
                elif isinstance(item, str):
                    # Graceful fallback if model returned plain strings
                    out.append({"hymn": item.strip(), "leader": ""})
            return out
    except json.JSONDecodeError:
        pass

    # Fallback: find first [...] block in the response
    m = re.search(r"\[.*?\]", raw, re.DOTALL)
    if m:
        try:
            result = json.loads(m.group())
            if isinstance(result, list):
                out = []
                for item in result:
                    if isinstance(item, dict) and "hymn" in item:
                        out.append({
                            "hymn":   str(item["hymn"]).strip(),
                            "leader": str(item.get("leader", "")).strip(),
                        })
                return out
        except Exception:
            pass

    print(f"    Could not parse response: {raw[:200]}")
    return []

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not ANTHROPIC_API_KEY:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable is not set.")

    client          = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    processed       = load_processed_videos()
    hymn_occurrences = load_existing_hymns()

    all_videos  = get_channel_videos()

    # Only process worship services — skip Wednesday Bible class / devotion videos
    WORSHIP_KEYWORDS = ("sunday", "worship", "5th sunday", "fifth sunday")
    worship_videos = [
        v for v in all_videos
        if any(kw in v["title"].lower() for kw in WORSHIP_KEYWORDS)
    ]
    skipped_non_worship = len(all_videos) - len(worship_videos)
    print(f"  Filtered to {len(worship_videos)} worship services"
          f" (skipped {skipped_non_worship} non-worship videos).")

    new_videos  = [v for v in worship_videos if v["id"] not in processed]
    skipped     = len(worship_videos) - len(new_videos)
    print(f"  {len(new_videos)} new video(s) to process  ({skipped} already done).")

    if not new_videos:
        print("Nothing new — exiting.")
        return

    for i, video in enumerate(new_videos, 1):
        vid_id, title, date = video["id"], video["title"], video["date"]
        print(f"\n[{i}/{len(new_videos)}] {date} — {title}")

        try:
            transcript = get_transcript(vid_id)
        except YouTubeBlocked:
            print("  IP blocked — skipping WITHOUT marking processed (will retry next run).")
            time.sleep(60)   # back off a full minute before trying the next video
            continue          # do not add to processed

        if transcript:
            print(f"  Transcript: {len(transcript):,} chars — asking Claude...")
            findings = identify_hymns_and_leaders(client, transcript, title, date)
            if findings:
                for f in findings:
                    leader = f["leader"] or ""
                    print(f"  ♪ {f['hymn']}" + (f" (led by {leader})" if leader else ""))
                    hymn_occurrences.setdefault(f["hymn"], []).append({
                        "date": date, "leader": leader
                    })
            else:
                print("  No hymns identified.")
        else:
            print("  Skipping (captions unavailable).")

        processed.add(vid_id)
        save_hymns(hymn_occurrences)        # save after every video — never lose progress
        save_processed_videos(processed)
        time.sleep(5)                        # 5s gap — gentler on YouTube

    print(f"\n✓ Done! {len(hymn_occurrences)} unique hymns across all tracked services.")
    print(f"  Saved → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
