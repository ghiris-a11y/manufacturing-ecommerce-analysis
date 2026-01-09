

import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

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

        dcc.Graph(id="line-chart")
    ]
)
@app.callback(
    Output("line-chart", "figure"),
    Output("kpi-share", "children"),
    Output("kpi-ecommerce", "children"),
    Output("kpi-growth", "children"),
    Input("industry-dropdown", "value"),
)
def update_dashboard(industry):

    dff = df[df["industry"] == industry] if industry else df
    dff = dff.sort_values("year")

    fig = px.line(
        dff,
        x="year",
        y="ecommerce_value",
        title=f"E-commerce Value Trend: {industry}" if industry else "E-commerce Value Trend"
    )

    if len(dff) < 2:
        return fig, "N/A", "N/A", "N/A"

    latest = dff.iloc[-1]
    prev = dff.iloc[-2]

    ecommerce = latest["ecommerce_value"]

    # SAFE share calculation (no missing column)
    share_value = (ecommerce / dff["ecommerce_value"].max()) * 100

    growth = ((ecommerce - prev["ecommerce_value"]) / prev["ecommerce_value"]) * 100

    return (
        fig,
        f"E-commerce Share: {share_value:.2f}%",
        f"E-commerce Value: ${ecommerce:,.0f}M",
        f"YoY Growth: {growth:.2f}%",
    )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)

