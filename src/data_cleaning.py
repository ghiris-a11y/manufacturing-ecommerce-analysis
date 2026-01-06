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

    # ---------------------------------
    # Row definitions (from inspection)
    # ---------------------------------
    YEAR_ROW = 3
    TYPE_ROW = 4
    DATA_START_ROW = 7

    year_labels = df.iloc[YEAR_ROW]
    type_labels = df.iloc[TYPE_ROW]

    # ---------------------------------
    # Identify E-commerce columns
    # ---------------------------------
    ecommerce_cols = []

    for idx, (year, typ) in enumerate(zip(year_labels, type_labels)):
        if isinstance(year, str) and isinstance(typ, str):
            year_match = re.search(r"(19\d{2}|20\d{2})", year)
            if year_match and "E-commerce" in typ:
                ecommerce_cols.append((idx, year_match.group(1)))

    if not ecommerce_cols:
        raise ValueError("No E-commerce columns detected")

    print("Detected E-commerce columns:", ecommerce_cols)

    # ---------------------------------
    # Extract data rows
    # ---------------------------------
    records = []

    for _, row in df.iloc[DATA_START_ROW:].iterrows():
        industry = row[1]

        if pd.isna(industry):
            continue

        for col_idx, year in ecommerce_cols:
            value = row[col_idx]

            if pd.isna(value):
                continue

            value = str(value).replace(",", "")

            try:
                value = float(value)
            except:
                continue

            records.append({
                "industry": industry,
                "year": int(year),
                "ecommerce_value": value
            })

    df_long = pd.DataFrame(records)

    print("Rows after cleaning:", len(df_long))
    print(df_long.head())

    # ---------------------------------
    # Save output
    # ---------------------------------
    os.makedirs("data/processed", exist_ok=True)
    df_long.to_csv(OUT_PATH, index=False)

    print("CSV GENERATED:", OUT_PATH)
    return df_long


if __name__ == "__main__":
    clean_manufacturing_data()
