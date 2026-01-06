import os   
import pandas as pd
import numpy as np
import re

def clean_manufacturing_data(
    file_path="data/raw/table_1.csv",
    output_path="data/processed/manufacturing_clean.csv"
):
    print("Reading raw CSV...")
    df = pd.read_csv(file_path)

    # --- Inspect columns ---
    df.columns = [c.strip().lower() for c in df.columns]

    # Expected columns (based on Census table format)
    # year | industry | ecommerce_percent (or similar)
    possible_pct_cols = [
        c for c in df.columns if "percent" in c or "penetration" in c
    ]

    if not possible_pct_cols:
        raise ValueError("No penetration/percent column found")

    pct_col = possible_pct_cols[0]

    # --- Clean & normalize ---
    df = df.rename(columns={
        pct_col: "penetration_pct"
    })

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["penetration_pct"] = (
        df["penetration_pct"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    df["penetration_pct"] = pd.to_numeric(
        df["penetration_pct"], errors="coerce"
    )

    df["industry"] = df["industry"].astype(str).str.strip()

    # --- Drop invalid rows ---
    df_clean = df.dropna(subset=["year", "penetration_pct", "industry"])

    print("Rows after cleaning:", len(df_clean))
    print(df_clean.head())

    # --- Save ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_clean.to_csv(output_path, index=False)

    print("CSV GENERATED:", os.path.exists(output_path))
    print("Rows:", len(df_clean))

    return df_clean


if __name__ == "__main__":
    clean_manufacturing_data()

