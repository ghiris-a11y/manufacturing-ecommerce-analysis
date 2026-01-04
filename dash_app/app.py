import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('data/processed/manufacturing_clean.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Manufacturing E-commerce Dashboard", style={'textAlign':'center'}),
    
    dcc.Dropdown(
        id='industry-select',
        options=[{'label': i, 'value': i} for i in df['industry'].unique()],
        value=df['industry'].unique()[:5],
        multi=True
    ),
    
    dcc.Graph(id='main-chart')
])

@app.callback(
    Output('main-chart', 'figure'),
    Input('industry-select', 'value'))
def update_chart(selected):
    filtered = df[df['industry'].isin(selected)]
    fig = px.line(filtered, x='year', y='penetration_pct', color='industry')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

