import pandas as pd
import os
import numpy as np

# --- CONFIGURATION ---
RAW_PATH = "data/raw/table_1.csv"
OUT_PATH = "data/processed/manufacturing_clean.csv"

def clean_data():
    print(f"📂 Reading raw data from: {RAW_PATH}")
    
    if not os.path.exists(RAW_PATH):
        print(f"❌ Error: File not found at {RAW_PATH}")
        return

    # Read with header=None to manually handle the complex structure
    df_raw = pd.read_csv(RAW_PATH, header=None)

    # Row 1 (index 1) contains Years (e.g., 2015, 2014)
    years_row = df_raw.iloc[1]
    
    cleaned_data = []
    
    # Iterate through data rows (Data starts at row 3)
    for index, row in df_raw.iloc[3:].iterrows():
        industry = row[1] # Column 1 is the Industry Name
        
        # Columns come in pairs starting at index 2: [Total, E-commerce]
        col_idx = 2
        while col_idx < df_raw.shape[1] - 1:
            # Extract Year from the 'Total' column header
            year_val = str(years_row[col_idx])
            
            # Clean year string (remove 'revised')
            if 'revised' in year_val:
                year = year_val.replace(' revised', '')
            else:
                year = year_val
            
            # Skip invalid columns (like empty space or non-years)
            if not year.replace('.', '', 1).isdigit():
                col_idx += 2
                continue
                
            year = int(float(year))
            
            # Extract Values
            total_str = str(row[col_idx])      # Even column = Total
            ecom_str = str(row[col_idx+1])     # Odd column = E-commerce
            
            # Helper to clean numbers (remove commas, handle 'S'/'D' suppression codes)
            def clean_currency(x):
                if pd.isna(x) or x in ['nan', 'S', 'D', 'X']: return None
                x = x.replace(',', '').replace(' ', '')
                try:
                    return float(x)
                except:
                    return None

            total_val = clean_currency(total_str)
            ecom_val = clean_currency(ecom_str)
            
            # Only save if we have valid numbers
            if total_val is not None and ecom_val is not None:
                share = (ecom_val / total_val) * 100 if total_val > 0 else 0
                
                cleaned_data.append({
                    "industry": industry,
                    "year": year,
                    "total_value": total_val,       # CRITICAL: This is the column you were missing!
                    "ecommerce_value": ecom_val,
                    "ecommerce_share_pct": share
                })
            
            col_idx += 2

    # Save to CSV
    df_clean = pd.DataFrame(cleaned_data)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df_clean.to_csv(OUT_PATH, index=False)
    
    print(f"✅ Success! Fixed data saved to: {OUT_PATH}")
    print(f"📊 Columns: {df_clean.columns.tolist()}")

if __name__ == "__main__":
    clean_data()
