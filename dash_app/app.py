

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
    [
        Output("line-chart", "figure"),
        Output("kpi-share", "children"),
        Output("kpi-ecommerce", "children"),
        Output("kpi-growth", "children"),
    ],
    Input("industry-dropdown", "value"),
)
def update_dashboard(industry):

    if industry is None or df.empty:
        fig = px.line(title="No data available")
        return fig, "—", "—", "—"

    dff = df[df["industry"] == industry].sort_values("year")

    if len(dff) < 2:
        fig = px.line(title="Not enough data")
        return fig, "—", "—", "—"

    # KPI calculations
    latest = dff.iloc[-1]
    prev = dff.iloc[-2]

    ecommerce_value = latest["ecommerce_value"]

    growth = (
        (latest["ecommerce_value"] - prev["ecommerce_value"])
        / prev["ecommerce_value"]
    ) * 100

    # Approximate share (relative to industry max)
    share = (latest["ecommerce_value"] / dff["ecommerce_value"].max()) * 100

    # Line chart
    fig = px.line(
        dff,
        x="year",
        y="ecommerce_value",
        markers=True,
        title=f"E-commerce Value Trend: {industry}",
    )

    fig.add_annotation(
        x=2008,
        y=dff[dff["year"] == 2008]["ecommerce_value"].values[0],
        text="2008 Financial Crisis",
        showarrow=True,
        arrowhead=2,
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="E-commerce Value (Million USD)",
        template="plotly_white",
    )

    return (
        fig,
        f"E-commerce Share: {share:.2f}%",
        f"E-commerce Value: ${ecommerce_value:,.0f}M",
        f"YoY Growth: {growth:.2f}%",
    )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)

