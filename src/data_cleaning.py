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

    year_row = df.iloc[0]
    type_row = df.iloc[1]

    ecommerce_cols = {}
    total_cols = {}
    current_year = None

    for col in df.columns[2:]:
        year_val = year_row[col]
        type_val = type_row[col]

        if pd.notna(year_val):
            current_year = str(year_val).split()[0]

        if type_val == "E-commerce":
            ecommerce_cols[col] = int(current_year)
        elif type_val == "Total":
            total_cols[col] = int(current_year)

    data = df.iloc[4:].copy()
    data = data[data["NAICS Code"].notna()]
    data["NAICS Code"] = data["NAICS Code"].astype(int)

    records = []

    for _, row in data.iterrows():
        industry = row["Description"]

        for col, year in ecommerce_cols.items():
            ecom = row[col]
            total = row[[k for k, v in total_cols.items() if v == year][0]]

            if pd.notna(ecom) and pd.notna(total):
                ecom = float(str(ecom).replace(",", ""))
                total = float(str(total).replace(",", ""))

                records.append({
                    "industry": industry,
                    "year": year,
                    "ecommerce_value": ecom,
                    "total_value": total,
                    "ecommerce_share_pct": (ecom / total) * 100
                })
                
    df_clean["non_ecommerce_value"] = (
    df_clean["total_shipments"] - df_clean["ecommerce_value"]
     )
    
    df_clean["non_ecommerce_value"] = df_clean["non_ecommerce_value"].clip(lower=0)

    clean_df = pd.DataFrame(records)

    os.makedirs("data/processed", exist_ok=True)
    clean_df.to_csv(OUT_PATH, index=False)

    print("Rows after cleaning:", len(clean_df))
    print(clean_df.head())
    print("CSV GENERATED:", OUT_PATH)

    return clean_df

if __name__ == "__main__":
    clean_manufacturing_data()


