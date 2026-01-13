

import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = "data/processed/manufacturing_clean.csv"

print("=== DASH STARTUP DEBUG ===")
print("Working directory:", os.getcwd())
print("Looking for:", DATA_PATH)
print("File exists:", os.path.exists(DATA_PATH))

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    print("CSV shape:", df.shape)
else:
    df = pd.DataFrame(columns=["industry", "year", "ecommerce_value"])
    print("CSV NOT FOUND — dashboard will be empty")
    
if "ecommerce_share_pct" not in df.columns:
    if "total_value" in df.columns:
        df["ecommerce_share_pct"] = (df["ecommerce_value"] / df["total_value"]) * 100
    else:
        # Fallback: relative share (prevents crash)
        df["ecommerce_share_pct"] = (
            df["ecommerce_value"] / df["ecommerce_value"].max()
        ) * 100

if "total_value" not in df.columns:
    df["total_value"] = df["ecommerce_value"]

print("==========================")

app = dash.Dash(__name__)
server = app.server

industries = sorted(df["industry"].unique())

app.layout = html.Div(
    style={"width": "90%", "margin": "auto"},
    children=[

        html.H1(
            "U.S. Manufacturing E-commerce Dashboard",
            style={"textAlign": "center"}
        ),

        html.Div(
            [
                html.Div(id="kpi-share", className="kpi-card"),
                html.Div(id="kpi-ecommerce", className="kpi-card"),
                html.Div(id="kpi-growth", className="kpi-card"),
            ],
            style={"display": "flex", "gap": "25px", "marginBottom": "20px"}
        ),

        dcc.Dropdown(
            id="industry-dropdown",
            options=[{"label": i, "value": i} for i in industries],
            value=industries[0] if industries else None,
            placeholder="Select an industry",
            style={"marginBottom": "20px"}
        ),

        dcc.Graph(id="line-chart"),

        html.Hr(),

        dcc.Graph(id="industry-bar-chart"),

        html.Hr(),

        dcc.Graph(id="top-bottom-chart"),

        html.Hr(),

        dcc.Graph(id="stacked-area-chart"),
    ]
)

@app.callback(
    Output("line-chart", "figure"),
    Output("industry-bar-chart", "figure"),
    Output("top-bottom-chart", "figure"),
    Output("stacked-area-chart", "figure"),
    Output("kpi-share", "children"),
    Output("kpi-ecommerce", "children"),
    Output("kpi-growth", "children"),
    Input("industry-dropdown", "value"),
)
def update_dashboard(industry):

    # Filter data
    dff = df[df["industry"] == industry] if industry else df
    dff = dff.sort_values("year")

    # ---------- LINE CHART ----------
    line_fig = px.line(
        dff,
        x="year",
        y="ecommerce_value",
        title=f"E-commerce Value Trend: {industry}" if industry else "E-commerce Value Trend"
    )

    # ---------- SAFETY CHECK ----------
    if len(dff) < 2:
        empty_fig = px.bar(title="No data available")
        return line_fig, empty_fig, empty_fig, empty_fig, "N/A", "N/A", "N/A"

    latest = dff.iloc[-1]
    prev = dff.iloc[-2]

    # -------- KPI VALUES --------
    share = f"{latest['ecommerce_share_pct']:.2f}%"
    ecommerce = f"${latest['ecommerce_value']:,.0f}M"
    growth_val = ((latest['ecommerce_value'] - prev['ecommerce_value']) / prev['ecommerce_value']) * 100
    growth = f"{growth_val:.2f}%"
    # ---------- INDUSTRY BAR (LATEST YEAR) ----------
    latest_year = df["year"].max()
    latest_df = df[df["year"] == latest_year]

    bar_fig = px.bar(
        latest_df,
        x="industry",
        y="ecommerce_share_pct",
        title=f"E-commerce Share by Industry ({latest_year})",
    )
    bar_fig.update_layout(xaxis_tickangle=-45)

    # ---------- TOP 5 vs BOTTOM 5 ----------
    ranked = latest_df.sort_values("ecommerce_share_pct", ascending=False)
    top_bottom = pd.concat([ranked.head(5), ranked.tail(5)])

    top_bottom_fig = px.bar(
        top_bottom,
        x="industry",
        y="ecommerce_share_pct",
        color="industry",
        title="Top 5 vs Bottom 5 Industries (E-commerce Share)",
    )
    top_bottom_fig.update_layout(showlegend=False, xaxis_tickangle=-45)

    # ---------- STACKED AREA ----------
    stacked = dff.copy()

    if "total_value" in stacked.columns:
         stacked["non_ecommerce"] = stacked["total_value"] - stacked["ecommerce_value"]
    else:
         stacked["non_ecommerce"] = 0

    stacked_fig = go.Figure()
    stacked_fig.add_trace(go.Scatter(
        x=stacked["year"],
        y=stacked["ecommerce_value"],
        stackgroup="one",
        name="E-commerce"
    ))
    stacked_fig.add_trace(go.Scatter(
        x=stacked["year"],
        y=stacked["non_ecommerce"],
        stackgroup="one",
        name="Non E-commerce"
    ))

    stacked_fig.update_layout(
        title="E-commerce vs Non E-commerce Shipments",
        xaxis_title="Year",
        yaxis_title="Value (USD Millions)"
    )

    # ---------- RETURN (ORDER MUST MATCH OUTPUTS) ----------
    return (
        line_fig,
        bar_fig,
        top_bottom_fig,
        stacked_fig,
        f"E-commerce Share: {share}",
        f"E-commerce Value: {ecommerce}",
        f"YoY Growth: {growth}",
    )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)

