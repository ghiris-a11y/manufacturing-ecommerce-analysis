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

    # Clean column names
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Assume first column is industry
    industry_col = df.columns[0]

    # Remaining columns should be years
    year_cols = []
    for c in df.columns[1:]:
        try:
            int(c)
            year_cols.append(c)
        except:
            pass

    if not year_cols:
        raise ValueError("No year columns found (1999–2015 expected)")

    print("Detected year columns:", year_cols[:5], "...")

    # Convert wide → long
    df_long = df.melt(
        id_vars=[industry_col],
        value_vars=year_cols,
        var_name="year",
        value_name="penetration_pct"
    )

    df_long = df_long.rename(columns={industry_col: "industry"})

    # Clean values
    df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce")
    df_long["penetration_pct"] = (
        df_long["penetration_pct"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    df_long["penetration_pct"] = pd.to_numeric(
        df_long["penetration_pct"], errors="coerce"
    )

    # Drop invalid rows
    df_long = df_long.dropna(
        subset=["year", "industry", "penetration_pct"]
    )

    print("Rows after cleaning:", len(df_long))
    print(df_long.head())

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_long.to_csv(output_path, index=False)

    print("CSV GENERATED:", os.path.exists(output_path))
    print("Rows:", len(df_long))

    return df_long


if __name__ == "__main__":
    clean_manufacturing_data()

