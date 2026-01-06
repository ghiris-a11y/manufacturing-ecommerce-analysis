import os   
import pandas as pd
import numpy as np
import re


import pandas as pd
import os
import re

RAW_PATH = "data/raw/table_1.csv"
OUT_PATH = "data/processed/manufacturing_clean.csv"


def clean_manufacturing_data():
    print("Reading raw CSV...")
    df = pd.read_csv(RAW_PATH, header=None)

    # =============================
    # STEP 1: Extract year labels
    # =============================
    year_row = df.iloc[3]
    subheader_row = df.iloc[4]

    new_columns = []

    for y, s in zip(year_row, subheader_row):
        if isinstance(y, str):
            match = re.search(r"(19\d{2}|20\d{2})", y)
        else:
            match = None

        if match and isinstance(s, str) and "E-commerce" in s:
            new_columns.append(match.group(1))
        else:
            new_columns.append(None)

    # First columns = NAICS + Industry name
    new_columns[0] = "naics"
    new_columns[1] = "industry"

    df.columns = new_columns

    # =============================
    # STEP 2: Keep only valid rows
    # =============================
    df = df.iloc[7:].copy()

    # Keep industry + year columns
    year_cols = [c for c in df.columns if c and c.isdigit()]
    df = df[["industry"] + year_cols]

    # =============================
    # STEP 3: Wide → Long
    # =============================
    df_long = df.melt(
        id_vars="industry",
        var_name="year",
        value_name="ecommerce_value"
    )

    # =============================
    # STEP 4: Clean values
    # =============================
    df_long["ecommerce_value"] = (
        df_long["ecommerce_value"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df_long["ecommerce_value"] = pd.to_numeric(
        df_long["ecommerce_value"], errors="coerce"
    )

    df_long = df_long.dropna(subset=["industry", "year", "ecommerce_value"])

    print("Rows after cleaning:", len(df_long))
    print(df_long.head())

    # =============================
    # STEP 5: Save
    # =============================
    os.makedirs("data/processed", exist_ok=True)
    df_long.to_csv(OUT_PATH, index=False)
    print("CSV GENERATED:", OUT_PATH)

    return df_long


if __name__ == "__main__":
    clean_manufacturing_data()

