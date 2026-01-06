import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# src/analysis.py

import os
import pandas as pd
import plotly.express as px


def load_data():
    """
    Load processed manufacturing e-commerce data
    """
    path = "data/processed/manufacturing_clean.csv"
    if not os.path.exists(path):
        raise FileNotFoundError("Processed data not found. Run data_cleaning.py first.")
    
    return pd.read_csv(path)


def calculate_growth_metrics(df):
    """
    Calculate growth metrics for TOTAL manufacturing e-commerce value
    """
    df_total = (
        df.groupby("year", as_index=False)["ecommerce_value"]
        .sum()
        .sort_values("year")
    )

    start_val = df_total.iloc[0]["ecommerce_value"]
    end_val = df_total.iloc[-1]["ecommerce_value"]
    years = df_total["year"].nunique() - 1

    cagr = None
    if start_val > 0 and years > 0:
        cagr = ((end_val / start_val) ** (1 / years) - 1) * 100

    return {
        "start_year": int(df_total.iloc[0]["year"]),
        "end_year": int(df_total.iloc[-1]["year"]),
        "start_value": round(start_val, 2),
        "end_value": round(end_val, 2),
        "cagr_percent": round(cagr, 2) if cagr else None
    }


def create_figures(df):
    """
    Create figures for analysis
    """

    df_total = (
        df.groupby("year", as_index=False)["ecommerce_value"]
        .sum()
        .sort_values("year")
    )

    fig = px.line(
        df_total,
        x="year",
        y="ecommerce_value",
        markers=True,
        title="Total U.S. Manufacturing E-commerce Value (1999–2015)"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="E-commerce Value (Million USD)",
        template="plotly_white"
    )

    return fig


if __name__ == "__main__":
    df = load_data()
    metrics = calculate_growth_metrics(df)

    print("Manufacturing E-commerce Growth Summary")
    print("-------------------------------------")
    print(f"Period: {metrics['start_year']}–{metrics['end_year']}")
    print(f"Start value: {metrics['start_value']}")
    print(f"End value: {metrics['end_value']}")
    print(f"CAGR: {metrics['cagr_percent']}%")

    fig = create_figures(df)
    fig.show()
