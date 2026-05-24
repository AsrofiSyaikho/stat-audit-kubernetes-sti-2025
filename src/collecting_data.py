import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────
load_dotenv()

REPO    = "kubernetes/kubernetes"
BASE    = f"https://api.github.com/repos/{REPO}"
HEADERS = {
    "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
    "Accept"       : "application/vnd.github+json",
}
OUTPUT  = "data/raw"
ISSUE_LIMIT   = 50   # max pages per endpoint (100 items/page = 5000 rows)
PR_LIMIT = 50

os.makedirs(OUTPUT, exist_ok=True)


# ── Helpers ───────────────────────────────────────────────────────
def fetch_pages(endpoint: str, params: dict, max_pages: int) -> list:
    """Paginate a GitHub endpoint and return all items as a list."""
    results, page = [], 1

    while page <= max_pages:
        response = requests.get(
            f"{BASE}/{endpoint}",
            headers=HEADERS,
            params={**params, "page": page, "per_page": 100},
        )
        batch = response.json()

        if not batch:
            break

        results.extend(batch)
        print(f"  page {page:>3} — collected {len(results):,}")
        page += 1
        time.sleep(1)

    return results


def save(df: pd.DataFrame, filename: str) -> None:
    path = os.path.join(OUTPUT, filename)
    df.to_csv(path, index=False)
    print(f"  saved -> {path}  ({len(df):,} rows, {df.shape[1]} cols)")


# ── Collectors ────────────────────────────────────────────────────
def get_issues() -> pd.DataFrame:
    print("Fetching issues...")
    # Ubah "state": "closed" menjadi "state": "all"
    raw = fetch_pages("issues", {"state": "all", "filter": "all"}, ISSUE_LIMIT)

    # /issues also returns PRs — keep only pure issues
    issues = [item for item in raw if "pull_request" not in item]
    return pd.DataFrame(issues)


def get_prs() -> pd.DataFrame:
    print("Fetching pull requests...")
    # Lakukan hal yang sama di sini jika ingin PR open & closed
    raw = fetch_pages("pulls", {"state": "all"}, PR_LIMIT)
    return pd.DataFrame(raw)


# ── Main ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    df_issues = get_issues()
    save(df_issues, "dataset_issues_raw.csv")

    df_prs = get_prs()
    save(df_prs, "dataset_prs_raw.csv")

    print(f"\nDone. {len(df_issues):,} issues + {len(df_prs):,} PRs -> {OUTPUT}/")