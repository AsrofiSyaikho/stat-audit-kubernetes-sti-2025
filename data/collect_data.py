import os
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    raise SystemExit(
        "GITHUB_TOKEN belum diset. Jalankan: set GITHUB_TOKEN=ghp_xxxxxxxx\n"
        "PowerShell: $env:GITHUB_TOKEN=\"ghp_xxxxxxxxxxx\""
    )

HEADERS = {"Authorization": f"Bearer {TOKEN}"}
REPO = "pandas-dev/pandas"
COLLECT_YEAR: Optional[int] = 2025

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REQUEST_DELAY = 0.5
SEARCH_MAX_PAGES = 10


def github_get(url, params):
    while True:
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = int(r.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(reset - int(time.time()), 1) + 1
            print(f"Rate limit, tunggu {wait}s...")
            time.sleep(wait)
            continue
        if r.status_code != 200:
            raise RuntimeError(f"GitHub API error {r.status_code}: {r.text}")
        return r


def fetch_search(query: str) -> list:
    url = "https://api.github.com/search/issues"
    results = []
    page = 1
    total_count = 0

    while page <= SEARCH_MAX_PAGES:
        r = github_get(url, {"q": query, "per_page": 100, "page": page})
        data = r.json()
        items = data.get("items", [])
        total_count = data.get("total_count", len(items))
        if not items:
            break
        results.extend(items)
        if len(results) >= total_count:
            break
        page += 1
        time.sleep(REQUEST_DELAY)

    if total_count > 1000:
        print(f"Peringatan: {total_count} hasil, GitHub search max 1000 — data terpotong.")

    return results


def fetch_paginated_list(url: str, params: dict) -> list:
    results = []
    page = 1
    while True:
        r = github_get(url, {**params, "page": page})
        data = r.json()
        if not isinstance(data, list) or not data:
            break
        results.extend(data)
        page += 1
        time.sleep(REQUEST_DELAY)
    return results


def fetch_issues() -> list:
    if COLLECT_YEAR:
        query = (
            f"repo:{REPO} is:issue is:closed "
            f"closed:{COLLECT_YEAR}-01-01..{COLLECT_YEAR}-12-31"
        )
        return fetch_search(query)

    url = f"https://api.github.com/repos/{REPO}/issues"
    raw = fetch_paginated_list(url, {"state": "closed", "per_page": 100})
    return [item for item in raw if "pull_request" not in item]


def fetch_pull_requests() -> list:
    if COLLECT_YEAR:
        query = (
            f"repo:{REPO} is:pr is:closed "
            f"closed:{COLLECT_YEAR}-01-01..{COLLECT_YEAR}-12-31"
        )
        return fetch_search(query)

    url = f"https://api.github.com/repos/{REPO}/pulls"
    return fetch_paginated_list(url, {"state": "closed", "per_page": 100})


# ── Ambil Issues ──────────────────────────────
print(f"Mengambil issues dari {REPO} (tahun {COLLECT_YEAR or 'semua'})...")
issues = fetch_issues()
df_issues = pd.DataFrame(issues)
df_issues.to_csv(OUTPUT_DIR / "issues_raw.csv", index=False)
print(f"Issues tersimpan: {len(df_issues)} baris")

# ── Ambil Pull Requests ───────────────────────
print(f"Mengambil pull requests dari {REPO} (tahun {COLLECT_YEAR or 'semua'})...")
prs = fetch_pull_requests()
df_prs = pd.DataFrame(prs)
df_prs.to_csv(OUTPUT_DIR / "prs_raw.csv", index=False)
print(f"PRs tersimpan: {len(df_prs)} baris")

print(f"Selesai! Cek folder {OUTPUT_DIR}")
