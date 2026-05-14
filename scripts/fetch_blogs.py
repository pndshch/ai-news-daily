import sys, os
from datetime import datetime, timezone, timedelta
import time

sys.path.insert(0, os.path.dirname(__file__))

import feedparser
from config import BLOG_FEEDS, BLOG_LOOKBACK_DAYS


def fetch():
    cutoff = datetime.now(timezone.utc) - timedelta(days=BLOG_LOOKBACK_DAYS)
    items = []

    for source, feed_url in BLOG_FEEDS.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

                if published and published < cutoff:
                    continue

                summary = ""
                if hasattr(entry, "summary"):
                    summary = entry.summary[:300].replace("<br>", " ").replace("<br/>", " ")
                    import re
                    summary = re.sub(r"<[^>]+>", "", summary).strip()

                items.append({
                    "title": getattr(entry, "title", ""),
                    "url": getattr(entry, "link", ""),
                    "source": source,
                    "summary": summary,
                    "published": published.strftime("%Y-%m-%dT%H:%M:%SZ") if published else "",
                })
        except Exception as e:
            print(f"[blogs] Error fetching {source}: {e}")

    items.sort(key=lambda x: x.get("published", ""), reverse=True)
    return items


if __name__ == "__main__":
    import json
    print(json.dumps(fetch(), indent=2, ensure_ascii=False))
