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

    # ---- STEP 1: Extract years from header row ----
    # Row 3 contains years (2015, 2014 revised, 2013, ..., 1999)
    year_row = df.iloc[3].astype(str)

    years = []
    for val in year_row:
        match = re.search(r"(19\d{2}|20\d{2})", val)
        years.append(match.group(1) if match else None)

    # ---- STEP 2: Extract subheaders (Total / E-commerce) ----
    subheader_row = df.iloc[4].astype(str)

    columns = []
    for y, s in zip(years, subheader_row):
        if y and "E-commerce" in s:
            columns.append(f"{y}_ecom")
        else:
            columns.append(None)

    # First two columns = NAICS + Industry
    columns[0] = "naics"
    columns[1] = "industry"

    df.columns = columns

    # ---- STEP 3: Drop junk rows above industries ----
    df = df.iloc[7:].copy()

    # Keep only industry + e-commerce columns
    keep_cols = ["industry"] + [c for c in df.columns if c and c.endswith("_ecom")]
    df = df[keep_cols]

    # ---- STEP 4: Wide → Long ----
    df_long = df.melt(
        id_vars="industry",
        var_name="year",
        value_name="ecommerce_value"
    )

    df_long["year"] = df_long["year"].str.replace("_ecom", "")
    df_long["ecommerce_value"] = (
        df_long["ecommerce_value"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df_long["ecommerce_value"] = pd.to_numeric(
        df_long["ecommerce_value"], errors="coerce"
    )

    # ---- STEP 5: Clean ----
    df_long = df_long.dropna(subset=["industry", "year", "ecommerce_value"])

    print("Rows after cleaning:", len(df_long))
    print(df_long.head())

    # ---- STEP 6: Save ----
    os.makedirs("data/processed", exist_ok=True)
    df_long.to_csv(OUT_PATH, index=False)
    print("CSV GENERATED:", OUT_PATH)

    return df_long


if __name__ == "__main__":
    clean_manufacturing_data()
