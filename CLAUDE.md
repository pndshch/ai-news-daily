# AI News Daily — Routine Instructions

This repo is updated by a Claude Code routine. When invoked, perform these steps:

## Daily Update Workflow

```
cd /Users/handa/260514_ai-news-daily
```

### 1. Fetch raw data
```
python3 scripts/fetch_all.py
```
This writes `data/raw-YYYY-MM-DD.json` with items from arXiv, HN, Reddit, GitHub Trending, and AI company blogs.

### 2. Read the raw JSON
Use the Read tool (or `python3 -c "import json; ..."` for compact summaries).

### 3. Write Japanese enrichment
For each item across all sources, add:
- `title_ja` — concise Japanese title (translation, can be loose)
- `summary_ja` — 1-2 sentence Japanese summary capturing the core point

For arXiv: read the abstract, summarize the contribution in plain Japanese.
For HN/Reddit: explain WHY the item is interesting in 1-2 sentences.
For GitHub: explain what the repo does and why it's trending today.
For blogs: capture the takeaway.

### 4. Pick highlights
Add a `highlights` array (3-5 items, can be 0 if nothing impressive today).
Each highlight needs:
- `source`, `title`, `title_ja`, `url`
- `hot_take_ja` — 2-3 sentences explaining why this matters, written so it could be material for an X tweet. Have a clear angle/perspective, not just a translation.

**Selection criteria**: subjective, impact-focused. Look for items that are:
- Surprising or counter-intuitive
- Genuinely novel research with broad implications
- Real-world AI events with social/business impact
- Anecdotal/viral material with cultural significance
- Skip mediocre items — better to have 2 strong highlights than 5 mid ones.

### 5. Save enriched JSON
Write to `data/YYYY-MM-DD.json` (NOT `raw-YYYY-MM-DD.json`).

The pattern: write a Python script (`scripts/enrich_today.py`) that reads the raw JSON, adds your translations inline, and saves the enriched version. See `scripts/enrich_today.py` for a working example from 2026-05-14.

### 6. Rebuild
```
python3 scripts/build_page.py
```
This injects `data/*.json` (excluding `raw-*.json`) into `template.html` and writes `index.html`.

### 7. Commit and push
```
git add -A
git commit -m "Update YYYY-MM-DD news"
git push
```

GitHub Pages serves `index.html` from main automatically.

## File map

- `template.html` — page HTML/CSS/JS (don't edit per-day; only when changing design)
- `scripts/fetch_all.py` — fetches from all 5 sources, writes raw JSON
- `scripts/build_page.py` — injects enriched JSON into template
- `scripts/enrich_today.py` — example enrichment script (overwrite each day)
- `data/YYYY-MM-DD.json` — enriched daily data (kept 14 days)
- `data/raw-YYYY-MM-DD.json` — raw pre-enrichment data (transient)

## Tips

- 1日あたり ~100件の項目があるので、上位25 arXiv + 全HN + 全Reddit + 全GitHub + 全blogsで十分。
- ハイライトは「Xでツイートしたくなる話か？」を基準に。理解促進が最優先。
- 原文タイトルが既に短く分かりやすければ、`title_ja`は無理に翻訳せずスキップしてOK（カードはEN原文を表示）。
