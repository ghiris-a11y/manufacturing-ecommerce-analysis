import os   
import pandas as pd
import numpy as np
import re


# src/data_cleaning.py

import pandas as pd
import os

RAW_PATH = "data/raw/table_1.csv"
OUT_PATH = "data/processed/manufacturing_clean.csv"

def clean_manufacturing_data():
    print("Reading raw CSV...")
    df = pd.read_csv(RAW_PATH)

    # Row 0 = years, Row 1 = Total / E-commerce
    year_row = df.iloc[0]
    type_row = df.iloc[1]

    # Build column mapping
    col_map = {}
    current_year = None

    for col in df.columns[2:]:
        year_val = year_row[col]
        type_val = type_row[col]

        if pd.notna(year_val):
            # Handle "2014 revised"
            current_year = str(year_val).split()[0]

        if type_val == "E-commerce":
            col_map[col] = current_year

    # Keep only relevant rows (actual industries)
    data = df.iloc[4:].copy()
    data = data[data["NAICS Code"].notna()]
    data["NAICS Code"] = data["NAICS Code"].astype(int)

    records = []

    for _, row in data.iterrows():
        industry = row["Description"]

        for col, year in col_map.items():
            value = row[col]
            if pd.notna(value):
                records.append({
                    "industry": industry,
                    "year": int(year),
                    "ecommerce_value": float(str(value).replace(",", ""))
                })

    clean_df = pd.DataFrame(records)

    os.makedirs("data/processed", exist_ok=True)
    clean_df.to_csv(OUT_PATH, index=False)

    print("Rows after cleaning:", len(clean_df))
    print(clean_df.head())
    print("CSV GENERATED:", OUT_PATH)

    return clean_df


if __name__ == "__main__":
    clean_manufacturing_data()
