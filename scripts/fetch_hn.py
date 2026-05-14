import sys, os
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))

from config import HN_MIN_POINTS, HN_MAX_RESULTS
from utils import fetch_with_retry, unix_hours_ago

SEARCH_TERMS = ["AI", "LLM", "machine learning", "GPT", "Claude", "deep learning"]


def fetch():
    ts = unix_hours_ago(36)
    all_items = {}

    for term in SEARCH_TERMS:
        url = (
            f"https://hn.algolia.com/api/v1/search"
            f"?query={quote(term)}"
            f"&tags=story"
            f"&numericFilters=points>={HN_MIN_POINTS},created_at_i>={ts}"
            f"&hitsPerPage=30"
        )
        try:
            resp = fetch_with_retry(url)
            if not resp:
                continue
            data = resp.json()
            for hit in data.get("hits", []):
                oid = hit.get("objectID")
                if oid and oid not in all_items:
                    all_items[oid] = {
                        "id": oid,
                        "title": hit.get("title", ""),
                        "url": hit.get("url") or f"https://news.ycombinator.com/item?id={oid}",
                        "points": hit.get("points", 0),
                        "comments": hit.get("num_comments", 0),
                        "comments_url": f"https://news.ycombinator.com/item?id={oid}",
                        "author": hit.get("author", ""),
                        "created_at": hit.get("created_at", ""),
                    }
        except Exception as e:
            print(f"[hn] Error for '{term}': {e}")

    items = sorted(all_items.values(), key=lambda x: x["points"], reverse=True)
    return items[:HN_MAX_RESULTS]


if __name__ == "__main__":
    import json
    print(json.dumps(fetch(), indent=2, ensure_ascii=False))
