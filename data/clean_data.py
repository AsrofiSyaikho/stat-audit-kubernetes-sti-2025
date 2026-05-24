from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
RAW_DIR = SCRIPT_DIR / "raw"
CLEAN_DIR = SCRIPT_DIR / "clean"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

ISSUES_RAW = RAW_DIR / "issues_raw.csv"
PRS_RAW = RAW_DIR / "prs_raw.csv"
ISSUES_CLEAN = CLEAN_DIR / "issues_clean.csv"
PRS_CLEAN = CLEAN_DIR / "prs_clean.csv"


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not ISSUES_RAW.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {ISSUES_RAW}")
    if not PRS_RAW.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {PRS_RAW}")
    return pd.read_csv(ISSUES_RAW), pd.read_csv(PRS_RAW)


def clean_issues(df: pd.DataFrame) -> pd.DataFrame:
    clean = df[[
        "number", "title", "state", "created_at",
        "closed_at", "comments", "author_association", "labels",
    ]].copy()

    clean["created_at"] = pd.to_datetime(clean["created_at"], utc=True)
    clean["closed_at"] = pd.to_datetime(clean["closed_at"], utc=True)

    clean["duration_days"] = (clean["closed_at"] - clean["created_at"]).dt.days
    clean["month_year"] = clean["created_at"].dt.tz_convert(None).dt.to_period("M").astype(str)

    return clean.dropna(subset=["closed_at"])


def clean_prs(df: pd.DataFrame) -> pd.DataFrame:
    clean = df[[
        "number", "title", "state", "created_at",
        "closed_at", "comments", "author_association", "pull_request",
    ]].copy()

    clean["created_at"] = pd.to_datetime(clean["created_at"], utc=True)
    clean["closed_at"] = pd.to_datetime(clean["closed_at"], utc=True)

    clean["duration_days"] = (clean["closed_at"] - clean["created_at"]).dt.days
    clean["is_merged"] = clean["pull_request"].apply(
        lambda x: 1 if "merged_at" in str(x) and "None" not in str(x) else 0
    )
    clean["month_year"] = clean["created_at"].dt.tz_convert(None).dt.to_period("M").astype(str)

    return clean.dropna(subset=["closed_at"])


def main() -> None:
    df_issues, df_prs = load_raw()

    issues_clean = clean_issues(df_issues)
    prs_clean = clean_prs(df_prs)

    issues_clean.to_csv(ISSUES_CLEAN, index=False)
    prs_clean.to_csv(PRS_CLEAN, index=False)

    print(f"Issues bersih: {len(issues_clean)} baris -> {ISSUES_CLEAN}")
    print(f"PRs bersih: {len(prs_clean)} baris -> {PRS_CLEAN}")
    print(f"PRs merged: {prs_clean['is_merged'].sum()}")
    print(f"Selesai! Cek folder {CLEAN_DIR}")


if __name__ == "__main__":
    main()
