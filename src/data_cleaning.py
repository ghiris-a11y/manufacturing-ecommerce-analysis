import os   
import pandas as pd
import numpy as np
import re

def clean_manufacturing_data(file_path="data/raw/table_1.csv"):
    """Load table_1.csv and return cleaned long-format DataFrame"""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Put table_1.csv in {file_path}")

    # Load raw file
    df_raw = pd.read_csv(file_path, header=None)

    # Extract NAICS codes and industry names
    naics_codes = df_raw.iloc[0::2, 0].dropna().astype(str)
    industry_names = df_raw.iloc[0::2, 1].dropna().astype(str)

    # Years (1999–2015)
    years = list(range(1999, 2016))

    # Extract shipment columns
    total_cols = df_raw.iloc[0::2, 2::4].values.flatten()
    ecommerce_cols = df_raw.iloc[0::2, 3::4].values.flatten()

    # Create base DataFrame
    df = pd.DataFrame({
        "naics": naics_codes.values,
        "industry": industry_names.values,
        "total_shipments": pd.to_numeric(total_cols, errors="coerce"),
        "ecommerce_shipments": pd.to_numeric(ecommerce_cols, errors="coerce")
    })

    # Convert to long format
    df_long = pd.DataFrame({
        "naics": np.repeat(df["naics"], len(years)),
        "industry": np.repeat(df["industry"], len(years)),
        "year": np.tile(years, len(df)),
        "total_shipments": np.tile(df["total_shipments"].fillna(0), len(years)),
        "ecommerce_shipments": np.tile(df["ecommerce_shipments"].fillna(0), len(years))
    })

    # Penetration %
    df_long["penetration_pct"] = (
        df_long["ecommerce_shipments"] / df_long["total_shipments"] * 100
    ).round(2)

    # Keep valid rows only
    df_long = df_long[df_long["total_shipments"] > 0].copy()

    return df_long


if __name__ == "__main__":
    df_clean = clean_manufacturing_data()
    os.makedirs("data/processed", exist_ok=True)
    df_clean.to_csv("data/processed/manufacturing_clean.csv", index=False)
    print(df_clean.head())
    print("Shape:", df_clean.shape)

