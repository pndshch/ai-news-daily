#!/usr/bin/env python3
"""Fetch raw data from all sources. Writes data/raw-YYYY-MM-DD.json.

This is called first by Claude Code during a daily routine run.
After this, Claude reads the raw JSON, writes Japanese summaries
and picks highlights, then runs build_page.py.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from config import DATA_DIR
from utils import iso_now, today_str

ROOT = Path(__file__).resolve().parent.parent


def run(name, fn):
    try:
        print(f"[{name}] Fetching...")
        items = fn()
        print(f"[{name}] Got {len(items)} items")
        return items
    except Exception as e:
        print(f"[{name}] FAILED: {e}")
        return []


def fetch_all():
    from fetch_arxiv import fetch as fetch_arxiv
    from fetch_hn import fetch as fetch_hn
    from fetch_reddit import fetch as fetch_reddit
    from fetch_blogs import fetch as fetch_blogs
    from fetch_github_trending import fetch as fetch_github

    date = today_str()
    print(f"Fetching for {date}")

    sources = {
        "arxiv": run("arxiv", fetch_arxiv),
        "hn": run("hn", fetch_hn),
        "reddit": run("reddit", fetch_reddit),
        "github": run("github", fetch_github),
        "blogs": run("blogs", fetch_blogs),
    }

    data = {
        "date": date,
        "generated_at": iso_now(),
        "sources": sources,
        "highlights": [],
        "stats": {
            "arxiv_count": len(sources["arxiv"]),
            "hn_count": len(sources["hn"]),
            "reddit_count": len(sources["reddit"]),
            "github_count": len(sources["github"]),
            "blogs_count": len(sources["blogs"]),
            "total": sum(len(v) for v in sources.values()),
        },
    }

    data_dir = ROOT / DATA_DIR
    data_dir.mkdir(exist_ok=True)
    raw_file = data_dir / f"raw-{date}.json"
    raw_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {raw_file}")
    print(f"\nNext: Claude reads {raw_file}, adds title_ja/summary_ja/highlights, saves to data/{date}.json, runs build_page.py")


if __name__ == "__main__":
    fetch_all()
