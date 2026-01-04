import pandas as pd
import numpy as np
import re

def clean_manufacturing_data(file_path):
    """Parse messy Census table_1.csv to tidy format"""
    
    # Raw read handles commas in numbers
    df_raw = pd.read_csv(file_path, header=None)
    
    # Extract NAICS codes (first column)
    naics_codes = df_raw.iloc[0::2, 0].dropna().astype(str)
    
    # Extract industry names (next to NAICS)
    industry_names = df_raw.iloc[0::2, 1].dropna().astype(str)
    
    # Years from column headers (hardcoded from data pattern)
    years = list(range(1999, 2016))
    
    # Extract total shipments (odd columns after NAICS/industry)
    total_cols = df_raw.iloc[0::2, 2::4].values.flatten()
    
    # Extract ecommerce shipments (even columns after NAICS/industry)  
    ecommerce_cols = df_raw.iloc[0::2, 3::4].values.flatten()
    
    # Create clean DataFrame
    data = {
        'naics': naics_codes.values,
        'industry': industry_names.values,
        'total_shipments': pd.to_numeric(total_cols, errors='coerce'),
        'ecommerce_shipments': pd.to_numeric(ecommerce_cols, errors='coerce')
    }
    
    df = pd.DataFrame(data)
    
    # Explode to long format (one row per year)
    df_long = pd.DataFrame({
        'naics': np.repeat(df['naics'], len(years)),
        'industry': np.repeat(df['industry'], len(years)),
        'year': np.tile(years, len(df)),
        'total_shipments': np.tile(df['total_shipments'].fillna(0), len(years)),
        'ecommerce_shipments': np.tile(df['ecommerce_shipments'].fillna(0), len(years))
    })
    
    # Calculate penetration rate
    df_long['penetration_pct'] = (df_long['ecommerce_shipments'] / 
                                df_long['total_shipments'] * 100).round(2)
    
    # Filter valid data
    df_long = df_long[df_long['total_shipments'] > 0].copy()
    
    return df_long

# Run cleaning
if __name__ == "__main__":
    df_clean = clean_manufacturing_data('data/raw/table_1.csv')
    df_clean.to_csv('data/processed/manufacturing_clean.csv', index=False)
    print(df_clean.head())
    print(f"Shape: {df_clean.shape}")
