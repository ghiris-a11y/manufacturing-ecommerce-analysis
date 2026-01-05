import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data():
    path = "data/processed/manufacturing_clean.csv"
    if not os.path.exists(path):
        raise FileNotFoundError("Processed data not found. Run data cleaning first.")
    return pd.read_csv(path)
    
def calculate_growth(df):
    pivot_pen = df.pivot_table('penetration_pct', 'naics', 'year', aggfunc='mean')

    start = pivot_pen.iloc[:, 0].replace(0, pd.NA)
    end = pivot_pen.iloc[:, -1]

    cagr = ((end / start) ** (1/15) - 1) * 100
    cagr = cagr.replace([pd.NA, float("inf"), -float("inf")], None)

    df['cagr_1999_2015'] = df['naics'].map(cagr)
    return df

def top_growers(df, n=10):
    """Get top n industries by CAGR"""
    growth = df.groupby('industry')['cagr_1999_2015'].first().sort_values(ascending=False)
    return growth.head(n)

def create_figures(df):
    """Pre-generate key figures"""
    
    # 1. Overall trend
    overall = df.groupby('year')['penetration_pct'].mean().reset_index()
    fig1 = px.line(overall, x='year', y='penetration_pct',
                   title='Manufacturing E-commerce Penetration (1999-2015)')
    
    # 2. Top industries heatmap
    top_ind = df['industry'].value_counts().head(12).index
    heatmap_data = df[df['industry'].isin(top_ind)].pivot_table(
        'penetration_pct', 'industry', 'year', aggfunc='mean')
    fig2 = px.imshow(
         heatmap_data,
         title='E-commerce Penetration Heatmap: Top Industries',
         color_continuous_scale='Viridis',
         aspect='auto'
    )
    
    # 3. Growth ranking
    growth_df = top_growers(df).reset_index()
    fig3 = px.bar(growth_df, x='cagr_1999_2015', y='industry',
                  title='Fastest Growing Industries (CAGR 1999-2015)')
    
    return [fig1, fig2, fig3]
