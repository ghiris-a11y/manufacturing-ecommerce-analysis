import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Generate data if not present (Railway-safe)
if not os.path.exists("data/processed/manufacturing_clean.csv"):
    from src.data_cleaning import clean_manufacturing_data
    os.makedirs("data/processed", exist_ok=True)
    df_clean = clean_manufacturing_data()
    df_clean.to_csv("data/processed/manufacturing_clean.csv", index=False)

df = pd.read_csv("data/processed/manufacturing_clean.csv")

# Load data
df = pd.read_csv('data/processed/manufacturing_clean.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Manufacturing E-commerce Dashboard"),

    dcc.Dropdown(
        id="industry-dropdown",
        options=[{"label": i, "value": i} for i in sorted(df["industry"].unique())],
        value=df["industry"].unique()[0],
        clearable=False
    ),

    dcc.Graph(id="line-chart")   # 👈 MATCHES callback
])
@app.callback(
    Output("line-chart", "figure"),
    Input("industry-dropdown", "value")
)
def update_chart(selected_industry):

    if selected_industry is None:
        df_filtered = df
        title = "E-commerce Penetration (All Industries)"
    else:
        df_filtered = df[df["industry"] == selected_industry]
        title = f"E-commerce Penetration: {selected_industry}"

    fig = px.line(
        df_filtered,
        x="year",
        y="penetration_pct",
        title=title
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="E-commerce Penetration (%)"
    )

    return fig
])

@app.callback(
    Output("main-chart", "figure"),
    Input("industry-select", "value")
)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)


