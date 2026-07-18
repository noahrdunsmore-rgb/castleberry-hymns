"""
tag_hymns.py
Assigns topic tags to every hymn in hymn_catalogue.json using Claude API.
Output: hymn_topics.json  ->  { "Hymn Name": ["Topic1", "Topic2"], ... }

Run once (takes ~3-5 minutes for 892 hymns):
    python tag_hymns.py
"""

import json, time, re
from pathlib import Path
import anthropic

# ── Config ───────────────────────────────────────────────────────────────────
CATALOGUE = Path(__file__).parent / 'hymn_catalogue.json'
OUTPUT    = Path(__file__).parent / 'hymn_topics.json'
MODEL     = 'claude-haiku-4-5-20251001'
BATCH     = 60          # hymns per API call
DELAY     = 1.0         # seconds between calls

# Canonical topic list — broad enough to cover most hymns
TOPICS = [
    "Grace", "Salvation", "Love", "Faith", "Trust", "Worship", "Praise",
    "Prayer", "Heaven", "Resurrection", "Easter", "The Cross", "Holy Spirit",
    "Scripture", "Forgiveness", "Repentance", "Community", "Service",
    "Comfort", "Peace", "Hope", "God's Power", "Thanksgiving",
    "Christmas", "Advent", "Baptism", "Commitment", "Encouragement",
    "Second Coming", "God's Majesty"
]

SYSTEM = (
    "You are a worship music expert. Given a list of hymn/worship song titles, "
    "assign 2–4 topic tags to each from the provided list. "
    "Return ONLY a JSON object — no markdown, no explanation."
)

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    hymns = json.loads(CATALOGUE.read_text(encoding='utf-8'))
    names = list({h['name'] for h in hymns})          # deduplicate
    print(f"Tagging {len(names)} unique hymns in batches of {BATCH}...")

    # Load existing results if resuming a partial run
    existing = {}
    if OUTPUT.exists():
        existing = json.loads(OUTPUT.read_text(encoding='utf-8'))
        print(f"  Resuming — {len(existing)} already tagged.")

    client  = anthropic.Anthropic()
    results = dict(existing)

    todo = [n for n in names if n not in results]
    print(f"  {len(todo)} remaining to tag.")

    for i in range(0, len(todo), BATCH):
        batch = todo[i : i + BATCH]
        prompt = (
            f"Topic list: {', '.join(TOPICS)}\n\n"
            "Hymns to tag (return JSON object with hymn name as key, "
            "array of 2-4 topics as value):\n"
            + "\n".join(f"{j+1}. {n}" for j, n in enumerate(batch))
        )

        try:
            resp = client.messages.create(
                model   = MODEL,
                max_tokens = 2048,
                system  = SYSTEM,
                messages = [{"role": "user", "content": prompt}]
            )
            text = resp.content[0].text.strip()
            # Strip any accidental markdown fences
            text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text, flags=re.S).strip()
            batch_result = json.loads(text)
            results.update(batch_result)
            print(f"  {min(i+BATCH, len(todo))}/{len(todo)} tagged")
        except Exception as e:
            print(f"  ERROR on batch {i//BATCH+1}: {e}")

        # Save incrementally so we can resume if interrupted
        OUTPUT.write_text(
            json.dumps(results, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        time.sleep(DELAY)

    print(f"\nDone — {len(results)} hymns tagged -> {OUTPUT}")

if __name__ == '__main__':
    main()
