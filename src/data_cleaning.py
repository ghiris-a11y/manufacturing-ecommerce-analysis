import os   
import pandas as pd
import numpy as np
import re
def clean_manufacturing_data(file_path="data/raw/table_1.csv"):
    # Load raw Census table
    df = pd.read_csv(file_path)

    # Rename first column to something usable
    df.rename(columns={df.columns[0]: "metric"}, inplace=True)

    # Keep only the penetration row
    df = df[df["metric"].str.contains("E-commerce", case=False, na=False)]

    # Drop metric column and reshape
    df_long = df.drop(columns=["metric"]).melt(
        var_name="year",
        value_name="penetration_pct"
    )

    # Clean data types
    df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce")
    df_long["penetration_pct"] = pd.to_numeric(df_long["penetration_pct"], errors="coerce")

    # Drop invalid rows
    df_long = df_long.dropna()

    # Add industry label (single industry dataset)
    df_long["industry"] = "Manufacturing (Total)"

    print("Rows after cleaning:", len(df_long))
    print(df_long.head())

    return df_long


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    df_clean = clean_manufacturing_data()
    df_clean.to_csv("data/processed/manufacturing_clean.csv", index=False)


