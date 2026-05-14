import html
import time
from datetime import datetime, timezone

import requests


def fetch_with_retry(url, headers=None, timeout=30, retries=1, delay=2):
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code in (429, 500, 502, 503) and attempt < retries:
                time.sleep(delay)
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException:
            if attempt < retries:
                time.sleep(delay)
                continue
            raise
    return None


def sanitize(text):
    if not text:
        return ""
    return html.escape(text).strip()


def iso_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def unix_hours_ago(hours):
    return int(time.time()) - hours * 3600
