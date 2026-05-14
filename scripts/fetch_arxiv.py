import sys, os, time
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))

from config import ARXIV_CATEGORIES, ARXIV_MAX_RESULTS
from utils import fetch_with_retry, unix_hours_ago

NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def fetch():
    from urllib.parse import quote
    cat_query = quote(" OR ".join(f"cat:{c}" for c in ARXIV_CATEGORIES))
    url = (
        f"http://export.arxiv.org/api/query"
        f"?search_query={cat_query}"
        f"&sortBy=submittedDate&sortOrder=descending"
        f"&max_results={ARXIV_MAX_RESULTS}"
    )

    time.sleep(3)
    resp = fetch_with_retry(url, timeout=60, retries=2, delay=5)
    if not resp:
        return []

    root = ET.fromstring(resp.content)
    items = []

    for entry in root.findall("atom:entry", NS):
        title_el = entry.find("atom:title", NS)
        title = title_el.text.strip().replace("\n", " ") if title_el is not None and title_el.text else ""

        paper_id = ""
        for link in entry.findall("atom:link", NS):
            href = link.get("href", "")
            if "abs/" in href:
                paper_id = href.split("abs/")[-1]
                break

        authors = []
        for author in entry.findall("atom:author", NS):
            name_el = author.find("atom:name", NS)
            if name_el is not None and name_el.text:
                authors.append(name_el.text.strip())

        abstract_el = entry.find("atom:summary", NS)
        abstract = abstract_el.text.strip().replace("\n", " ") if abstract_el is not None and abstract_el.text else ""

        categories = []
        for cat in entry.findall("atom:category", NS):
            term = cat.get("term", "")
            if term:
                categories.append(term)

        published_el = entry.find("atom:published", NS)
        published = published_el.text if published_el is not None and published_el.text else ""

        items.append({
            "id": paper_id,
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "categories": categories,
            "url": f"https://arxiv.org/abs/{paper_id}",
            "pdf_url": f"https://arxiv.org/pdf/{paper_id}",
            "published": published,
        })

    return items


if __name__ == "__main__":
    import json
    print(json.dumps(fetch(), indent=2, ensure_ascii=False))
