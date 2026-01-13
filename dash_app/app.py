import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# --- LOAD DATA ---
DATA_PATH = "data/processed/manufacturing_clean.csv"

# Safe Data Loading
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    # Fallback if total_value is still missing (prevents crash)
    if "total_value" not in df.columns:
        df["total_value"] = df["ecommerce_value"] 
else:
    df = pd.DataFrame(columns=["industry", "year", "ecommerce_value", "total_value", "ecommerce_share_pct"])

# Prepare Lists
if not df.empty:
    df = df.sort_values("year")
    industries = sorted(df["industry"].unique())
    years = sorted(df["year"].unique())
    min_year, max_year = min(years), max(years)
else:
    industries, years, min_year, max_year = [], [], 2000, 2015

app = dash.Dash(__name__)
server = app.server

# --- LAYOUT ---
app.layout = html.Div(
    style={"padding": "20px", "maxWidth": "1600px", "margin": "auto"},
    children=[
        
        # 1. HEADER & FILTERS
        html.Div([
            html.Div([
                html.H2("🏭 Manufacturing E-commerce", style={"margin": "0", "color": "#1f2937"}),
                html.P("U.S. Census Bureau Data (1999-2015)", style={"margin": "0", "color": "#6b7280", "fontSize": "0.9rem"})
            ], style={"flex": "1"}),

            html.Div([
                dcc.Dropdown(
                    id="industry-dropdown",
                    options=[{"label": "All Industries", "value": "All"}] + [{"label": i, "value": i} for i in industries],
                    value="All",
                    clearable=False,
                    style={"width": "250px", "marginRight": "15px"}
                ),
                html.Div([
                    dcc.Slider(
                        id="year-slider",
                        min=min_year,
                        max=max_year,
                        value=max_year,
                        marks={str(y): str(y) for y in years if y % 5 == 0 or y == max_year},
                    )
                ], style={"width": "200px", "paddingTop": "5px"})
            ], style={"display": "flex", "alignItems": "center"})
        ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "20px", "background": "white", "padding": "15px", "borderRadius": "10px", "boxShadow": "0 2px 5px rgba(0,0,0,0.05)"}),

        # 2. KPI ROW
        html.Div(
            children=[
                html.Div(id="kpi-share", className="kpi-card"),
                html.Div(id="kpi-ecommerce", className="kpi-card"),
                html.Div(id="kpi-total", className="kpi-card"),
            ],
            style={"display": "flex", "gap": "20px", "marginBottom": "20px"}
        ),

        # 3. CHARTS GRID (2x2 Layout)
        html.Div(className="charts-grid", children=[
            html.Div(className="chart-container", children=[dcc.Graph(id="trend-line-chart", style={"height": "350px"})]),
            html.Div(className="chart-container", children=[dcc.Graph(id="stacked-area-chart", style={"height": "350px"})]),
            html.Div(className="chart-container", children=[dcc.Graph(id="sector-bar-chart", style={"height": "350px"})]),
            html.Div(className="chart-container", children=[dcc.Graph(id="top-bottom-chart", style={"height": "350px"})]),
        ])
    ]
)

# --- CALLBACKS ---
@app.callback(
    [Output("kpi-share", "children"), Output("kpi-ecommerce", "children"), Output("kpi-total", "children"),
     Output("trend-line-chart", "figure"), Output("sector-bar-chart", "figure"),
     Output("top-bottom-chart", "figure"), Output("stacked-area-chart", "figure")],
    [Input("industry-dropdown", "value"), Input("year-slider", "value")]
)
def update_charts(selected_industry, selected_year):
    if df.empty: return ["N/A"]*3 + [px.scatter()]*4

    # Filter Data
    if selected_industry == "All":
        dff_trend = df.groupby("year")[["ecommerce_value", "total_value"]].sum().reset_index()
        dff_trend["ecommerce_share_pct"] = (dff_trend["ecommerce_value"] / dff_trend["total_value"]) * 100
        title_prefix = "All Industries"
    else:
        dff_trend = df[df["industry"] == selected_industry].sort_values("year")
        title_prefix = selected_industry

    df_year = df[df["year"] == selected_year]
    
    # KPI Logic
    if selected_industry == "All":
        curr = df_year[["ecommerce_value", "total_value"]].sum()
        share, ecom, total = (curr["ecommerce_value"]/curr["total_value"])*100 if curr["total_value"] > 0 else 0, curr["ecommerce_value"], curr["total_value"]
    else:
        row = df_year[df_year["industry"] == selected_industry]
        if not row.empty:
            share, ecom, total = row["ecommerce_share_pct"].values[0], row["ecommerce_value"].values[0], row["total_value"].values[0]
        else:
            share, ecom, total = 0, 0, 0

    kpi_share = [html.Span("Digital Penetration"), html.Br(), html.Strong(f"{share:.1f}%")]
    kpi_ecom = [html.Span("E-commerce Sales"), html.Br(), html.Strong(f"${ecom:,.0f} M")]
    kpi_total = [html.Span("Total Market"), html.Br(), html.Strong(f"${total:,.0f} M")]

    layout_settings = dict(margin=dict(l=40, r=40, t=40, b=40), template="plotly_white")

    # Chart 1: Trend
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=dff_trend["year"], y=dff_trend["ecommerce_value"], name="E-commerce", line=dict(color="#2563EB", width=3)))
    fig_trend.add_trace(go.Scatter(x=dff_trend["year"], y=dff_trend["total_value"], name="Total", line=dict(color="#9CA3AF", dash="dot")))
    fig_trend.update_layout(title=f"Growth Trend ({title_prefix})", **layout_settings)

    # Chart 2: Stacked Area
    dff_trend["Traditional"] = dff_trend["total_value"] - dff_trend["ecommerce_value"]
    fig_stacked = px.area(dff_trend, x="year", y=["Traditional", "ecommerce_value"], color_discrete_map={"ecommerce_value": "#3B82F6", "Traditional": "#E5E7EB"})
    fig_stacked.update_layout(title="Market Composition", showlegend=False, **layout_settings)

    # Chart 3: Bar Chart
    if selected_industry == "All":
        fig_bar = px.bar(df_year.sort_values("ecommerce_value").tail(10), y="industry", x="ecommerce_value", orientation="h", title=f"Top 10 Sectors ({selected_year})")
    else:
        fig_bar = px.bar(x=[ecom], y=[selected_industry], orientation="h", title=f"Sector Value ({selected_year})")
    fig_bar.update_layout(**layout_settings)

    # Chart 4: Top/Bottom
    ranked = df_year.sort_values("ecommerce_share_pct", ascending=False)
    fig_tb = px.bar(pd.concat([ranked.head(3), ranked.tail(3)]), x="industry", y="ecommerce_share_pct", color="ecommerce_share_pct", title=f"High vs Low Adoption ({selected_year})", color_continuous_scale="Blues")
    fig_tb.update_layout(coloraxis_showscale=False, **layout_settings)

    return kpi_share, kpi_ecom, kpi_total, fig_trend, fig_bar, fig_tb, fig_stacked

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
