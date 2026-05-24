from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent / "raw"

df = pd.read_csv(RAW_DIR / "issues_raw.csv")
print(df.shape)
print(df.columns.tolist())
print(df.head(3))

df_prs = pd.read_csv(RAW_DIR / "prs_raw.csv")
print(df_prs.shape)
print(df_prs.columns.tolist())
