import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data():
    return pd.read_csv('data/processed/manufacturing_clean.csv')

def calculate_growth(df):
    """Add CAGR and ranking columns"""
    pivot_pen = df.pivot_table('penetration_pct', 'naics', 'year', aggfunc='mean')
    cagr = ((pivot_pen.iloc[:, -1] / pivot_pen.iloc[:, 0]) ** (1/15) - 1) * 100
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
    fig2 = px.imshow(heatmap_data.T, 
                     title='E-commerce Penetration Heatmap: Top Industries',
                     color_continuous_scale='Viridis')
    
    # 3. Growth ranking
    growth_df = top_growers(df).reset_index()
    fig3 = px.bar(growth_df, x='cagr_1999_2015', y='industry',
                  title='Fastest Growing Industries (CAGR 1999-2015)')
    
    return [fig1, fig2, fig3]
