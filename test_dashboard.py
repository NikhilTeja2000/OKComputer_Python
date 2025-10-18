#!/usr/bin/env python3
"""
Simple test version of the dashboard to check if basic functionality works
"""

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load data
try:
    df = pd.read_csv('data/processed_diet_data.csv')
    print(f"Loaded {len(df)} records from real data")
except:
    print("Could not load real data, creating sample")
    df = pd.DataFrame({
        'BMI': [22, 25, 30, 35],
        'Age': [25, 35, 45, 55],
        'Gender': ['Male', 'Female', 'Male', 'Female']
    })

# Create simple app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Diet Analytics Dashboard - Test Version"),
    html.P(f"Data loaded: {len(df)} records"),
    dcc.Graph(
        figure=px.histogram(df, x='BMI', title='BMI Distribution')
    )
])

if __name__ == '__main__':
    print("Starting test dashboard on http://localhost:8051")
    app.run(debug=True, host='0.0.0.0', port=8051)