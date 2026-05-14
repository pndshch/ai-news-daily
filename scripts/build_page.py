#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from config import DATA_DIR, TEMPLATE_FILE, OUTPUT_FILE, MAX_ARCHIVE_DAYS
from utils import iso_now, today_str

ROOT = Path(__file__).resolve().parent.parent


def run_fetcher(name, fetch_fn):
    try:
        print(f"[{name}] Fetching...")
        items = fetch_fn()
        print(f"[{name}] Got {len(items)} items")
        return items
    except Exception as e:
        print(f"[{name}] FAILED: {e}")
        return []


def build():
    from fetch_arxiv import fetch as fetch_arxiv
    from fetch_hn import fetch as fetch_hn
    from fetch_reddit import fetch as fetch_reddit
    from fetch_blogs import fetch as fetch_blogs
    from fetch_github_trending import fetch as fetch_github

    date = today_str()
    print(f"Building for {date}")

    sources = {
        "arxiv": run_fetcher("arxiv", fetch_arxiv),
        "hn": run_fetcher("hn", fetch_hn),
        "reddit": run_fetcher("reddit", fetch_reddit),
        "github": run_fetcher("github", fetch_github),
        "blogs": run_fetcher("blogs", fetch_blogs),
    }

    data = {
        "date": date,
        "generated_at": iso_now(),
        "sources": sources,
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
    data_file = data_dir / f"{date}.json"
    data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {data_file}")

    archive = collect_archive(data_dir, date)
    archive[date] = data

    template_path = ROOT / TEMPLATE_FILE
    template = template_path.read_text(encoding="utf-8")

    news_json = json.dumps(archive, ensure_ascii=False)
    output = template.replace("/* __NEWS_DATA__ */ null", news_json)

    output_path = ROOT / OUTPUT_FILE
    output_path.write_text(output, encoding="utf-8")
    print(f"Wrote {output_path} ({len(archive)} days)")

    prune_old(data_dir, date)


def collect_archive(data_dir, today):
    archive = {}
    cutoff = datetime.strptime(today, "%Y-%m-%d") - timedelta(days=MAX_ARCHIVE_DAYS)

    for f in sorted(data_dir.glob("*.json")):
        try:
            file_date = datetime.strptime(f.stem, "%Y-%m-%d")
            if file_date >= cutoff:
                archive[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, json.JSONDecodeError):
            continue
    return archive


def prune_old(data_dir, today):
    cutoff = datetime.strptime(today, "%Y-%m-%d") - timedelta(days=MAX_ARCHIVE_DAYS)
    for f in data_dir.glob("*.json"):
        try:
            file_date = datetime.strptime(f.stem, "%Y-%m-%d")
            if file_date < cutoff:
                f.unlink()
                print(f"Pruned {f.name}")
        except ValueError:
            continue


if __name__ == "__main__":
    build()
