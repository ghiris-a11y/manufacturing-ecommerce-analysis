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
    print(df.head())
else:
    df = pd.DataFrame()
    print("CSV NOT FOUND — dashboard will be empty")

print("==========================")
