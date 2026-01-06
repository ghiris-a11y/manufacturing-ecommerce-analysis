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

    # Normalize column names
    df.columns = [str(c).strip() for c in df.columns]

    # First column = industry
    industry_col = df.columns[0]

    # Detect year columns using regex (1999–2015)
    year_map = {}
    for col in df.columns[1:]:
        match = re.search(r"(19|20)\d{2}", col)
        if match:
            year_map[col] = int(match.group())

    if not year_map:
        raise ValueError("No year columns detected in CSV")

    print("Detected year columns:", list(year_map.values())[:5], "...")

    # Rename columns to clean year numbers
    df = df.rename(columns=year_map)

    # Melt to long format
    df_long = df.melt(
        id_vars=[industry_col],
        value_vars=list(year_map.values()),
        var_name="year",
        value_name="penetration_pct"
    )

    df_long = df_long.rename(columns={industry_col: "industry"})

    # Clean values
    df_long["penetration_pct"] = (
        df_long["penetration_pct"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    df_long["penetration_pct"] = pd.to_numeric(
        df_long["penetration_pct"], errors="coerce"
    )

    df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce")

    # Drop invalid rows
    df_long = df_long.dropna(
        subset=["industry", "year", "penetration_pct"]
    )

    print("Rows after cleaning:", len(df_long))
    print(df_long.head())

    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_long.to_csv(output_path, index=False)

    print("CSV GENERATED:", os.path.exists(output_path))
    print("Rows:", len(df_long))

    return df_long


if __name__ == "__main__":
    clean_manufacturing_data()
