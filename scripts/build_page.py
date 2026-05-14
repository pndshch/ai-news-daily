#!/usr/bin/env python3
"""Build index.html from existing data/YYYY-MM-DD.json files.

This does NOT fetch. Run scripts/fetch_all.py first, have Claude add
Japanese summaries + highlights to the JSON, then run this.
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from config import DATA_DIR, TEMPLATE_FILE, OUTPUT_FILE, MAX_ARCHIVE_DAYS

ROOT = Path(__file__).resolve().parent.parent


def build():
    data_dir = ROOT / DATA_DIR
    data_dir.mkdir(exist_ok=True)

    archive = {}
    cutoff = datetime.now() - timedelta(days=MAX_ARCHIVE_DAYS)

    for f in sorted(data_dir.glob("*.json")):
        if f.name.startswith("raw-"):
            continue
        try:
            file_date = datetime.strptime(f.stem, "%Y-%m-%d")
            if file_date >= cutoff:
                archive[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, json.JSONDecodeError):
            continue

    if not archive:
        print("No data files found. Run fetch_all.py first.")
        return

    template = (ROOT / TEMPLATE_FILE).read_text(encoding="utf-8")
    news_json = json.dumps(archive, ensure_ascii=False)
    output = template.replace("/* __NEWS_DATA__ */ null", news_json)

    (ROOT / OUTPUT_FILE).write_text(output, encoding="utf-8")
    print(f"Built index.html with {len(archive)} day(s)")

    for f in data_dir.glob("*.json"):
        if f.name.startswith("raw-"):
            try:
                file_date = datetime.strptime(f.stem.replace("raw-", ""), "%Y-%m-%d")
                if file_date < cutoff - timedelta(days=2):
                    f.unlink()
            except ValueError:
                continue
        else:
            try:
                file_date = datetime.strptime(f.stem, "%Y-%m-%d")
                if file_date < cutoff:
                    f.unlink()
                    print(f"Pruned {f.name}")
            except ValueError:
                continue


if __name__ == "__main__":
    build()
