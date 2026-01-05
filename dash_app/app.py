import dash
import os
import sys
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# --------------------------------------------------
# Fix Python path so Railway can find src/
# --------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --------------------------------------------------
# Load or generate processed data
# --------------------------------------------------
DATA_PATH = "data/processed/manufacturing_clean.csv"

if not os.path.exists(DATA_PATH):
    from src.data_cleaning import clean_manufacturing_data
    os.makedirs("data/processed", exist_ok=True)
    df_clean = clean_manufacturing_data()
    df_clean.to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH)

# --------------------------------------------------
# Initialize Dash app
# --------------------------------------------------
app = Dash(__name__)
server = app.server  # required for Railway

# --------------------------------------------------
# Layout
# --------------------------------------------------
app.layout = html.Div(
    style={"width": "90%", "margin": "auto"},
    children=[

        html.H1(
            "Manufacturing E-commerce Dashboard",
            style={"textAlign": "center"}
        ),

        dcc.Dropdown(
            id="industry-dropdown",
            options=[
                {"label": i, "value": i}
                for i in sorted(df["industry"].dropna().unique())
            ],
            value=sorted(df["industry"].dropna().unique())[0],
            clearable=False,
            placeholder="Select an industry",
            style={"marginBottom": "20px"}
        ),

        dcc.Graph(id="line-chart")
    ]
)

# --------------------------------------------------
# Callback
# --------------------------------------------------
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
        yaxis_title="E-commerce Penetration (%)",
        template="plotly_white"
    )

    return fig

# --------------------------------------------------
# Run server
# --------------------------------------------------
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))

