import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from src.analysis import load_data, calculate_growth, top_growers

# Load and prepare data
df = load_data()
df = calculate_growth(df)

# Layout
app = dash.Dash(__name__, title="Manufacturing E-commerce Analysis")

app.layout = html.Div([
    html.H1("U.S. Manufacturing E-commerce Penetration (1999-2015)", 
            style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select Industries:"),
        dcc.Dropdown(
            id='industry-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['industry'].unique())],
            value=df['industry'].value_counts().head(8).index.tolist(),
            multi=True
        ),
    ], style={'width': '50%', 'margin': 'auto'}),
    
    dcc.Graph(id='trend-chart'),
    
    html.Hr(),
    
    html.H3("Fastest Growing Industries (CAGR 1999-2015)"),
    dcc.Graph(id='growth-bar'),
    
    html.Hr(),
    
    html.Div(id='kpi-container', style={'textAlign': 'center'})
], style={'padding': '20px'})

@callback(
    [Output('trend-chart', 'figure'),
     Output('growth-bar', 'figure'),
     Output('kpi-container', 'children')],
    [Input('industry-dropdown', 'value')]
)
def update_charts(selected_industries):
    filtered = df[df['industry'].isin(selected_industries)]
    
    # Trend chart
    trend_fig = px.line(filtered, x='year', y='penetration_pct', 
                       color='industry',
                       title='E-commerce Penetration Trends',
                       markers=True)
    
    # Growth bar (top growers among selected)
    growth_selected = top_growers(filtered, len(selected_industries))
    growth_fig = px.bar(growth_selected.reset_index(), 
                       x='cdirectory_1999_2015', y='industry',
                       title='Growth Ranking')
    
    # KPIs
    latest_avg = filtered[filtered['year']==2015]['penetration_pct'].mean()
    kpis = [
        html.Div(f"Avg 2015 Penetration: {latest_avg:.1f}%", 
                className="kpi"),
        html.Div(f"Industries: {len(selected_industries)}", className="kpi")
    ]
    
    return trend_fig, growth_fig, kpis

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
