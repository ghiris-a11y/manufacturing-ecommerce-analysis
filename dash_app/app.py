import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# dash_app/app.py

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
    Input("industry-dropdown", "value")
)
def update_chart(selected_industry):

    if selected_industry is None or df.empty:
        return px.line(title="No data available")

    filtered = df[df["industry"] == selected_industry]

    fig = px.line(
        filtered,
        x="year",
        y="ecommerce_value",
        markers=True,
        title=f"E-commerce Value Trend: {selected_industry}"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="E-commerce Value (Million USD)",
        template="plotly_white"
    )

    return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)

