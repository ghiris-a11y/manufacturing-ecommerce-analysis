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
    
    # Read raw file WITHOUT headers
    df = pd.read_csv(RAW_PATH, header=None)

    # --- STEP 1: Identify header rows ---
    year_row = 3        # contains years like 2015, 2014 revised, etc.
    subheader_row = 4   # contains Total / E-commerce
    data_start = 7      # first NAICS row starts here

    years = df.iloc[year_row].ffill()
    subs = df.iloc[subheader_row]

    # --- STEP 2: Build usable column names ---
    columns = []
    for y, s in zip(years, subs):
        if pd.isna(y):
            columns.append(None)
        else:
            y = str(y).strip()
            s = str(s).strip()
            columns.append(f"{y}_{s}")

    df.columns = columns

    # --- STEP 3: Keep only needed columns ---
    keep_cols = ["NAICS", "Description"]
    ecommerce_cols = [
        c for c in df.columns
        if c and "E-commerce" in c
    ]

    df = df.iloc[data_start:].copy()
    df = df[["NAICS", "Description"] + ecommerce_cols]

    df.columns = ["naics", "industry"] + ecommerce_cols

    # --- STEP 4: Clean values ---
    for col in ecommerce_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

    # --- STEP 5: Convert to long format ---
    df_long = df.melt(
        id_vars=["industry"],
        value_vars=ecommerce_cols,
        var_name="year",
        value_name="ecommerce_value"
    )

    # Extract year number
    df_long["year"] = df_long["year"].str.extract(r"(\d{4})").astype(int)

    df_long = df_long.dropna(subset=["ecommerce_value"])

    print("Rows after cleaning:", len(df_long))
    print(df_long.head())

    # --- STEP 6: Save ---
    os.makedirs("data/processed", exist_ok=True)
    df_long.to_csv(OUT_PATH, index=False)

    print("CSV GENERATED:", OUT_PATH)
    return df_long


if __name__ == "__main__":
    clean_manufacturing_data()

