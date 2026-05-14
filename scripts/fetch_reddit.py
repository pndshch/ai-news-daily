import sys, os
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

from config import REDDIT_SUBS, REDDIT_USER_AGENT, REDDIT_MIN_SCORE, REDDIT_MAX_RESULTS
from utils import fetch_with_retry, unix_hours_ago


def fetch():
    cutoff = unix_hours_ago(48)
    headers = {"User-Agent": REDDIT_USER_AGENT}
    items = []

    for sub in REDDIT_SUBS:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit=50"
        try:
            resp = fetch_with_retry(url, headers=headers)
            if not resp:
                continue
            data = resp.json()
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                created = post.get("created_utc", 0)
                if created < cutoff:
                    continue
                if post.get("score", 0) < REDDIT_MIN_SCORE:
                    continue
                items.append({
                    "id": post.get("id", ""),
                    "title": post.get("title", ""),
                    "url": post.get("url", ""),
                    "subreddit": sub,
                    "score": post.get("score", 0),
                    "comments": post.get("num_comments", 0),
                    "comments_url": f"https://www.reddit.com{post.get('permalink', '')}",
                    "author": post.get("author", ""),
                    "created_at": datetime.fromtimestamp(created, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                })
        except Exception as e:
            print(f"[reddit] Error fetching r/{sub}: {e}")

    items.sort(key=lambda x: x["score"], reverse=True)
    return items[:REDDIT_MAX_RESULTS]


if __name__ == "__main__":
    import json
    print(json.dumps(fetch(), indent=2, ensure_ascii=False))
