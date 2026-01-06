import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data():
    """
    Load processed manufacturing e-commerce data
    """
    path = "data/processed/manufacturing_clean.csv"
    if not os.path.exists(path):
        raise FileNotFoundError("Processed data not found. Run data_cleaning.py first.")
    
    df = pd.read_csv(path)
    return df


def calculate_growth_metrics(df):
    """
    Calculate overall growth metrics for manufacturing
    """
    df = df.sort_values("year")

    start_val = df.iloc[0]["penetration_pct"]
    end_val = df.iloc[-1]["penetration_pct"]
    years = df["year"].nunique() - 1

    if start_val <= 0 or years <= 0:
        cagr = None
    else:
        cagr = ((end_val / start_val) ** (1 / years) - 1) * 100

    return {
        "start_year": int(df.iloc[0]["year"]),
        "end_year": int(df.iloc[-1]["year"]),
        "start_penetration": start_val,
        "end_penetration": end_val,
        "cagr_percent": round(cagr, 2) if cagr is not None else None
    }


def create_figures(df):
    """
    Create all figures used in dashboard or analysis
    """

    # 1. Line chart: E-commerce penetration over time
    fig_line = px.line(
        df,
        x="year",
        y="penetration_pct",
        title="Manufacturing E-commerce Penetration (1999–2015)",
        markers=True
    )
    fig_line.update_layout(
        xaxis_title="Year",
        yaxis_title="E-commerce Penetration (%)"
    )

    return {
        "trend_chart": fig_line
    }


if __name__ == "__main__":
    df = load_data()
    metrics = calculate_growth_metrics(df)

    print("Manufacturing E-commerce Growth Summary")
    print("--------------------------------------")
    print(f"Period: {metrics['start_year']}–{metrics['end_year']}")
    print(f"Start penetration: {metrics['start_penetration']:.2f}%")
    print(f"End penetration: {metrics['end_penetration']:.2f}%")
    print(f"CAGR: {metrics['cagr_percent']}%")

    figs = create_figures(df)
    figs["trend_chart"].show()

