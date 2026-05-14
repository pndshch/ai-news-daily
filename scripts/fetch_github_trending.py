import sys, os, re

sys.path.insert(0, os.path.dirname(__file__))

from bs4 import BeautifulSoup
from config import GITHUB_MAX_RESULTS
from utils import fetch_with_retry

AI_KEYWORDS = re.compile(
    r"(ai|llm|gpt|transformer|neural|machine.?learn|deep.?learn|diffusion|"
    r"nlp|computer.?vision|reinforcement|rag|embedding|vector|agent|"
    r"anthropic|openai|hugging.?face|langchain|ollama|vllm|gguf|lora)",
    re.IGNORECASE,
)


def fetch():
    url = "https://github.com/trending?since=daily"
    headers = {"User-Agent": "ai-news-daily/1.0"}

    resp = fetch_with_retry(url, headers=headers)
    if not resp:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    seen = set()

    for row in soup.select("article.Box-row"):
        try:
            name_el = row.select_one("h2 a")
            if not name_el:
                continue
            full_name = name_el.get("href", "").strip("/")
            if not full_name or full_name in seen:
                continue

            desc_el = row.select_one("p")
            description = desc_el.get_text(strip=True) if desc_el else ""

            text_to_check = f"{full_name} {description}"
            if not AI_KEYWORDS.search(text_to_check):
                continue

            seen.add(full_name)

            lang_el = row.select_one("[itemprop='programmingLanguage']")
            language = lang_el.get_text(strip=True) if lang_el else ""

            stars_total = 0
            stars_today = 0
            for link in row.select("a.Link--muted"):
                text = link.get_text(strip=True).replace(",", "")
                if "/stargazers" in link.get("href", ""):
                    try:
                        stars_total = int(text)
                    except ValueError:
                        pass

            today_el = row.select_one("span.d-inline-block.float-sm-right")
            if today_el:
                m = re.search(r"([\d,]+)\s+stars?\s+today", today_el.get_text())
                if m:
                    stars_today = int(m.group(1).replace(",", ""))

            forks = 0
            for link in row.select("a.Link--muted"):
                if "/forks" in link.get("href", ""):
                    text = link.get_text(strip=True).replace(",", "")
                    try:
                        forks = int(text)
                    except ValueError:
                        pass

            items.append({
                "name": full_name.split("/")[-1],
                "full_name": full_name,
                "description": description,
                "url": f"https://github.com/{full_name}",
                "language": language,
                "stars": stars_total,
                "stars_today": stars_today,
                "forks": forks,
            })
        except Exception as e:
            print(f"[github] Error parsing row: {e}")
            continue

    items.sort(key=lambda x: x["stars_today"], reverse=True)
    return items[:GITHUB_MAX_RESULTS]


if __name__ == "__main__":
    import json
    print(json.dumps(fetch(), indent=2, ensure_ascii=False))
