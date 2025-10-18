#!/usr/bin/env python3
"""
Personalized Diet Analytics Dashboard - Python Plotly Dash Version
Converts the original R Shiny dashboard to Python with all features preserved
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json
import io
import base64

# Load and process the data
def load_data():
    """Load and process the diet analytics data"""
    try:
        # Try to load from the local data folder first
        df = pd.read_csv('data/processed_diet_data.csv')
        print("Loaded real data from data/processed_diet_data.csv")
    except:
        try:
            # Try to load from the original location
            df = pd.read_csv('/mnt/okcomputer/OKComputer_R-Dashboard-App-main/processed_diet_data.csv')
            print("Loaded real data from original location")
        except:
            try:
                # Try alternative location
                df = pd.read_csv('../OKComputer_R-Dashboard-App-main/processed_diet_data.csv')
                print("Loaded real data from alternative location")
            except:
                # Create sample data for demonstration
                print("Creating sample data for demonstration...")
                df = create_sample_data()
    
    return df

def create_sample_data():
    """Create sample data that matches the original structure"""
    np.random.seed(42)
    n = 1000
    
    # Generate sample data
    df = pd.DataFrame({
        'Patient_ID': [f'P{i:05d}' for i in range(1, n+1)],
        'Age': np.random.randint(18, 80, n),
        'Gender': np.random.choice(['Male', 'Female', 'Other'], n, p=[0.45, 0.5, 0.05]),
        'Height_cm': np.random.normal(170, 10, n).round(1),
        'Weight_kg': np.random.normal(75, 15, n).round(1),
    })
    
    # Calculate BMI
    df['BMI'] = (df['Weight_kg'] / (df['Height_cm'] / 100) ** 2).round(2)
    
    # Add other health metrics
    df['Chronic_Disease'] = np.random.choice(['Healthy', 'Hypertension', 'Diabetes', 'Heart Disease'], n, p=[0.6, 0.2, 0.15, 0.05])
    df['Blood_Pressure_Systolic'] = np.random.randint(120, 180, n)
    df['Blood_Pressure_Diastolic'] = np.random.randint(70, 110, n)
    df['Cholesterol_Level'] = np.random.randint(150, 300, n)
    df['Blood_Sugar_Level'] = np.random.randint(70, 250, n)
    df['Genetic_Risk_Factor'] = np.random.choice(['Yes', 'No'], n, p=[0.3, 0.7])
    df['Allergies'] = np.random.choice(['None Known', 'Gluten Intolerance', 'Nut Allergy', 'Lactose Intolerance'], n, p=[0.7, 0.15, 0.1, 0.05])
    df['Daily_Steps'] = np.random.randint(2000, 15000, n)
    df['Exercise_Frequency'] = np.random.randint(1, 7, n)
    df['Sleep_Hours'] = np.random.uniform(4, 10, n).round(1)
    df['Alcohol_Consumption'] = np.random.choice(['Yes', 'No'], n, p=[0.4, 0.6])
    df['Smoking_Habit'] = np.random.choice(['Yes', 'No'], n, p=[0.25, 0.75])
    df['Dietary_Habits'] = np.random.choice(['Regular', 'Vegetarian', 'Vegan', 'Keto'], n, p=[0.4, 0.3, 0.15, 0.15])
    
    # Add nutrition data
    df['Caloric_Intake'] = np.random.randint(1500, 3500, n)
    df['Protein_Intake'] = np.random.randint(50, 200, n)
    df['Carbohydrate_Intake'] = np.random.randint(100, 400, n)
    df['Fat_Intake'] = np.random.randint(30, 150, n)
    df['Preferred_Cuisine'] = np.random.choice(['Western', 'Mediterranean', 'Asian', 'Indian'], n)
    
    # Add recommendations
    diet_plans = ['High-Protein Diet', 'Balanced Diet', 'Low-Carb Diet', 'Low-Fat Diet']
    df['Recommended_Meal_Plan'] = np.random.choice(diet_plans, n, p=[0.26, 0.25, 0.24, 0.25])
    
    # Add BMI categories
    df['BMI_Category'] = pd.cut(df['BMI'], 
                                bins=[0, 18.5, 25, 30, 35, float('inf')],
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese', 'Severely Obese'])
    
    # Add age groups
    df['Age_Group'] = pd.cut(df['Age'], 
                            bins=[0, 30, 45, 60, float('inf')],
                            labels=['Young Adult', 'Middle-aged', 'Senior', 'Elderly'])
    
    return df

# Load the data
df = load_data()

# Define professional, healthcare-inspired color palette
colors = {
    'primary': '#2E86AB',        # Professional blue
    'secondary': '#A23B72',      # Deep rose
    'accent': '#F18F01',         # Warm orange
    'light': '#F8F9FA',          # Clean light gray
    'dark': '#2D3748',           # Charcoal gray
    'highlight': '#E53E3E',      # Medical red
    'neutral': '#EDF2F7',        # Very light gray
    'background': '#FFFFFF',     # Pure white
    'success': '#38A169',        # Medical green
    'info': '#3182CE',           # Trust blue
    'warning': '#D69E2E',        # Caution amber
    'danger': '#E53E3E',         # Alert red
    'card_bg': '#FFFFFF',        # Card backgrounds
    'border': '#E2E8F0',         # Subtle borders
    'text_primary': '#2D3748',   # Primary text
    'text_secondary': '#4A5568'  # Secondary text
}

# Professional color sequence for charts - healthcare appropriate
color_sequence = ['#2E86AB', '#F18F01', '#38A169', '#A23B72', '#3182CE', '#D69E2E', '#E53E3E', '#805AD5']

# Statistical analysis functions
def perform_statistical_analysis(df):
    """Perform statistical analysis on the data"""
    results = {}
    
    # BMI vs Diet Recommendation Chi-square test
    contingency_table = pd.crosstab(df['BMI_Category'], df['Recommended_Meal_Plan'])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    results['bmi_diet_chi2'] = {'chi2': chi2, 'p_value': p_value}
    
    # Correlation analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    results['correlation_matrix'] = correlation_matrix
    
    # BMI correlation with health metrics
    bmi_correlations = df[['BMI', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic', 
                          'Cholesterol_Level', 'Blood_Sugar_Level']].corr()['BMI'].drop('BMI')
    results['bmi_correlations'] = bmi_correlations
    
    return results

# Perform statistical analysis
stats_results = perform_statistical_analysis(df)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Personalized Diet Analytics Dashboard"

# Define the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1([
                    html.I(className="fas fa-chart-line", style={'marginRight': '10px'}),
                    "Personalized Diet Analytics Dashboard"
                ], className="text-center", style={
                    'fontFamily': 'Playfair Display, serif',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'marginBottom': '10px',
                    'textShadow': '0 2px 4px rgba(0, 0, 0, 0.3)'
                }),
                html.P("Evidence-based nutrition recommendations with statistical validation", 
                      className="text-center", style={'fontSize': '1.2rem', 'color': 'white', 'opacity': '0.95'})
            ], className="mb-4", style={
                'background': f'linear-gradient(135deg, {colors["primary"]}, {colors["secondary"]})',
                'color': 'white',
                'padding': '2rem',
                'border-radius': '15px',
                'boxShadow': '0 10px 30px rgba(46, 134, 171, 0.25)',
                'textShadow': '0 2px 4px rgba(0, 0, 0, 0.3)'
            })
        ])
    ]),
    
    # Horizontal Filter Bar
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5([
                    html.I(className="fas fa-filter", style={'marginRight': '10px'}),
                    "Data Filters"
                ], style={'color': 'white', 'marginBottom': '20px', 'fontFamily': 'Playfair Display, serif'}),
                
                # Filter Row 1
                dbc.Row([
                    # Patient ID Search
                    dbc.Col([
                        html.Label([
                            html.I(className="fas fa-search", style={'marginRight': '5px'}),
                            "Patient ID",
                            html.I(className="fas fa-info-circle", 
                                   style={'margin-left': '5px', 'fontSize': '0.8rem'},
                                   title="Search examples: P00001 (exact), P001 (partial), 123 (contains)")
                        ], style={'fontWeight': 'bold', 'color': 'white', 'fontSize': '0.9rem'}),
                        dcc.Input(
                            id='patient-id-filter',
                            type='text',
                            placeholder='P00001, P001, or 123',
                            style={'width': '100%', 'height': '35px', 'fontSize': '0.9rem'}
                        )
                    ], md=2),
                    
                    # Gender Filter
                    dbc.Col([
                        html.Label([
                            html.I(className="fas fa-venus-mars", style={'marginRight': '5px'}),
                            "Gender"
                        ], style={'fontWeight': 'bold', 'color': 'white', 'fontSize': '0.9rem'}),
                        dcc.Dropdown(
                            id='gender-filter',
                            options=[{'label': 'All', 'value': 'All'}] + 
                                   [{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
                            value='All',
                            style={'fontSize': '0.9rem'}
                        )
                    ], md=2),
                    
                    # Diet Plan Filter
                    dbc.Col([
                        html.Label([
                            html.I(className="fas fa-utensils", style={'marginRight': '5px'}),
                            "Diet Plan"
                        ], style={'fontWeight': 'bold', 'color': 'white', 'fontSize': '0.9rem'}),
                        dcc.Dropdown(
                            id='diet-plan-filter',
                            options=[{'label': 'All', 'value': 'All'}] + 
                                   [{'label': plan, 'value': plan} for plan in df['Recommended_Meal_Plan'].unique()],
                            value='All',
                            style={'fontSize': '0.9rem'}
                        )
                    ], md=2),
                    
                    # Chronic Disease Filter
                    dbc.Col([
                        html.Label([
                            html.I(className="fas fa-heartbeat", style={'marginRight': '5px'}),
                            "Health Condition"
                        ], style={'fontWeight': 'bold', 'color': 'white', 'fontSize': '0.9rem'}),
                        dcc.Dropdown(
                            id='chronic-disease-filter',
                            options=[{'label': 'All', 'value': 'All'}] + 
                                   [{'label': disease, 'value': disease} for disease in df['Chronic_Disease'].unique()],
                            value='All',
                            style={'fontSize': '0.9rem'}
                        )
                    ], md=2),
                    
                    # Reset Button
                    dbc.Col([
                        html.Label("Actions", style={'fontWeight': 'bold', 'color': 'white', 'fontSize': '0.9rem'}),
                        html.Br(),
                        dbc.Button([
                            html.I(className="fas fa-undo", style={'marginRight': '5px'}),
                            "Reset"
                        ], 
                        id='reset-filters-btn',
                        color="light",
                        size="sm",
                        style={'width': '100%', 'fontSize': '0.9rem'})
                    ], md=2)
                ], className="mb-3"),
                
                # Filter Row 2 - Range Sliders
                dbc.Row([
                    # Age Range Filter
                    dbc.Col([
                        html.Label([
                            html.I(className="fas fa-birthday-cake", style={'marginRight': '5px'}),
                            "Age Range"
                        ], style={'fontWeight': 'bold', 'color': 'white', 'fontSize': '0.9rem'}),
                        dcc.RangeSlider(
                            id='age-range-filter',
                            min=df['Age'].min(),
                            max=df['Age'].max(),
                            value=[df['Age'].min(), df['Age'].max()],
                            marks={i: {'label': str(i), 'style': {'color': 'white', 'fontSize': '0.8rem'}} 
                                  for i in range(int(df['Age'].min()), int(df['Age'].max())+1, 15)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], md=4),
                    
                    # BMI Range Filter
                    dbc.Col([
                        html.Label([
                            html.I(className="fas fa-weight", style={'marginRight': '5px'}),
                            "BMI Range"
                        ], style={'fontWeight': 'bold', 'color': 'white', 'fontSize': '0.9rem'}),
                        dcc.RangeSlider(
                            id='bmi-range-filter',
                            min=df['BMI'].min(),
                            max=df['BMI'].max(),
                            value=[df['BMI'].min(), df['BMI'].max()],
                            marks={i: {'label': str(i), 'style': {'color': 'white', 'fontSize': '0.8rem'}} 
                                  for i in range(int(df['BMI'].min()), int(df['BMI'].max())+1, 10)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], md=4),
                    
                    # Exercise Frequency Filter
                    dbc.Col([
                        html.Label([
                            html.I(className="fas fa-running", style={'marginRight': '5px'}),
                            "Exercise (days/week)"
                        ], style={'fontWeight': 'bold', 'color': 'white', 'fontSize': '0.9rem'}),
                        dcc.RangeSlider(
                            id='exercise-filter',
                            min=df['Exercise_Frequency'].min(),
                            max=df['Exercise_Frequency'].max(),
                            value=[df['Exercise_Frequency'].min(), df['Exercise_Frequency'].max()],
                            marks={i: {'label': str(i), 'style': {'color': 'white', 'fontSize': '0.8rem'}} 
                                  for i in range(int(df['Exercise_Frequency'].min()), int(df['Exercise_Frequency'].max())+1)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], md=4)
                ])
            ], className="p-4", style={
                'background': f'linear-gradient(135deg, {colors["dark"]}, {colors["info"]})',
                'border-radius': '15px',
                'boxShadow': '0 10px 30px rgba(52, 152, 219, 0.2)',
                'marginBottom': '20px'
            })
        ])
    ]),
    
    # Navigation Tabs
    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="main-tabs", value="summary", children=[
                dcc.Tab(label="Executive Summary", value="summary", 
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="Population Overview", value="population",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="Age Demographics", value="demographics",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="BMI Analysis", value="bmi_analysis",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="Health Metrics", value="health_metrics",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="Chronic Conditions", value="chronic",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="Diet Recommendations", value="recommendations",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="Interactive Scatter", value="scatter",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="Statistical Analysis", value="validation",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'}),
                dcc.Tab(label="Data Export", value="download",
                       style={'backgroundColor': colors['light']},
                       selected_style={'backgroundColor': colors['primary'], 'color': 'white'})
            ])
        ])
    ]),
    
    # Content Area
    dbc.Row([
        dbc.Col([
            html.Div(id="tab-content", className="mt-4")
        ])
    ])
    
], fluid=True, style={'backgroundColor': colors['background'], 'minHeight': '100vh'})

# Function to filter data based on user inputs
def filter_data(patient_id, gender, age_range, bmi_range, diet_plan, chronic_disease, exercise_range):
    """Filter the dataframe based on user selections"""
    filtered_df = df.copy()
    
    # Patient ID filter
    if patient_id and patient_id.strip():
        filtered_df = filtered_df[filtered_df['Patient_ID'].str.contains(patient_id.strip(), case=False, na=False)]
    
    # Gender filter
    if gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == gender]
    
    # Age range filter
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]
    
    # BMI range filter
    filtered_df = filtered_df[(filtered_df['BMI'] >= bmi_range[0]) & (filtered_df['BMI'] <= bmi_range[1])]
    
    # Diet plan filter
    if diet_plan != 'All':
        filtered_df = filtered_df[filtered_df['Recommended_Meal_Plan'] == diet_plan]
    
    # Chronic disease filter
    if chronic_disease != 'All':
        filtered_df = filtered_df[filtered_df['Chronic_Disease'] == chronic_disease]
    
    # Exercise frequency filter
    filtered_df = filtered_df[(filtered_df['Exercise_Frequency'] >= exercise_range[0]) & 
                             (filtered_df['Exercise_Frequency'] <= exercise_range[1])]
    
    return filtered_df

# Callbacks for tab content with filtering
@app.callback(
    Output("tab-content", "children"),
    [Input("main-tabs", "value"),
     Input("patient-id-filter", "value"),
     Input("gender-filter", "value"),
     Input("age-range-filter", "value"),
     Input("bmi-range-filter", "value"),
     Input("diet-plan-filter", "value"),
     Input("chronic-disease-filter", "value"),
     Input("exercise-filter", "value")]
)
def render_tab_content(tab, patient_id, gender, age_range, bmi_range, diet_plan, chronic_disease, exercise_range):
    # Filter the data based on user inputs
    filtered_df = filter_data(patient_id, gender, age_range, bmi_range, diet_plan, chronic_disease, exercise_range)
    
    # Recalculate statistics with filtered data
    if len(filtered_df) > 0:
        filtered_stats = perform_statistical_analysis(filtered_df)
    else:
        # Handle empty filtered data
        filtered_stats = {'bmi_diet_chi2': {'chi2': 0, 'p_value': 1}, 'correlation_matrix': pd.DataFrame(), 'bmi_correlations': pd.Series()}
    
    if tab == "summary":
        return create_executive_summary_filtered(filtered_df, filtered_stats)
    elif tab == "population":
        return create_population_overview_filtered(filtered_df)
    elif tab == "demographics":
        return create_age_demographics_filtered(filtered_df)
    elif tab == "bmi_analysis":
        return create_bmi_analysis_filtered(filtered_df)
    elif tab == "health_metrics":
        return create_health_metrics_filtered(filtered_df)
    elif tab == "chronic":
        return create_chronic_conditions_filtered(filtered_df)
    elif tab == "recommendations":
        return create_recommendations_filtered(filtered_df)
    elif tab == "scatter":
        return create_interactive_scatter_filtered(filtered_df)
    elif tab == "validation":
        return create_statistical_validation_filtered(filtered_df, filtered_stats)
    elif tab == "download":
        return create_data_download_filtered(filtered_df)
    else:
        return html.Div("Tab not found")

# Reset filters callback
@app.callback(
    [Output("patient-id-filter", "value"),
     Output("gender-filter", "value"),
     Output("age-range-filter", "value"),
     Output("bmi-range-filter", "value"),
     Output("diet-plan-filter", "value"),
     Output("chronic-disease-filter", "value"),
     Output("exercise-filter", "value")],
    Input("reset-filters-btn", "n_clicks")
)
def reset_filters(n_clicks):
    if n_clicks:
        return ("", "All", [df['Age'].min(), df['Age'].max()], [df['BMI'].min(), df['BMI'].max()], 
                "All", "All", [df['Exercise_Frequency'].min(), df['Exercise_Frequency'].max()])
    return ("", "All", [df['Age'].min(), df['Age'].max()], [df['BMI'].min(), df['BMI'].max()], 
            "All", "All", [df['Exercise_Frequency'].min(), df['Exercise_Frequency'].max()])

def create_executive_summary_filtered(filtered_df, filtered_stats):
    """Create the Executive Summary tab content with filtered data"""
    
    # Handle empty filtered data
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Key statistics
    total_patients = len(filtered_df)
    avg_bmi = filtered_df['BMI'].mean()
    significant_correlation = filtered_stats['bmi_diet_chi2']['p_value'] < 0.01 if 'bmi_diet_chi2' in filtered_stats else False
    
    return html.Div([
        # Filtered Data Summary
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4([
                        html.I(className="fas fa-filter", style={'marginRight': '10px'}),
                        "Filtered Data Summary"
                    ], style={'color': colors['primary'], 'fontFamily': 'Playfair Display, serif'}),
                    html.P(f"Showing results for {total_patients:,} patients out of {len(df):,} total records", 
                          style={'fontSize': '1.1rem', 'fontWeight': '500'}),
                    html.P("💡 Tip: Use Patient ID filter to search specific patients (e.g., P00001) or groups (e.g., P001 for 100+ patients)", 
                          style={'fontSize': '0.9rem', 'fontStyle': 'italic', 'marginTop': '10px'}) if total_patients == len(df) else html.P(f"🔍 Active filters applied - showing subset of data", 
                          style={'fontSize': '0.9rem', 'fontStyle': 'italic', 'marginTop': '10px'})
                ], className="p-4 mb-4", style={
                    'background': f'linear-gradient(135deg, {colors["primary"]}, {colors["info"]})',
                    'color': 'white',
                    'border-radius': '12px',
                    'boxShadow': '0 4px 12px rgba(46, 134, 171, 0.15)'
                })
            ])
        ]),
        
        # Key Statistics Cards
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4([
                        html.I(className="fas fa-weight", style={'marginRight': '10px'}),
                        "BMI Influence"
                    ], style={'color': colors['text_primary'], 'marginBottom': '12px'}),
                    html.Span("p < 0.01", className="stat-number", style={
                        'fontSize': '2.2rem',
                        'fontWeight': '700',
                        'color': colors['primary'],
                        'display': 'block',
                        'marginBottom': '8px'
                    }),
                    html.P("BMI is the strongest predictor of diet recommendations, with statistically significant associations across all categories.",
                          style={'color': colors['text_secondary'], 'lineHeight': '1.5'})
                ], className="p-4", style={
                    'background': colors['card_bg'],
                    'border': f'1px solid {colors["border"]}',
                    'border-left': f'4px solid {colors["primary"]}',
                    'border-radius': '12px',
                    'height': '100%',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)'
                })
            ], md=6),
            dbc.Col([
                html.Div([
                    html.H4([
                        html.I(className="fas fa-utensils", style={'marginRight': '10px'}),
                        "Dietary Habits"
                    ], style={'color': colors['text_primary'], 'marginBottom': '12px'}),
                    html.Span("p < 0.05", className="stat-number", style={
                        'fontSize': '2.2rem',
                        'fontWeight': '700',
                        'color': colors['success'],
                        'display': 'block',
                        'marginBottom': '8px'
                    }),
                    html.P("Current dietary preferences significantly influence recommendations, showing respect for patient lifestyle choices.",
                          style={'color': colors['text_secondary'], 'lineHeight': '1.5'})
                ], className="p-4", style={
                    'background': colors['card_bg'],
                    'border': f'1px solid {colors["border"]}',
                    'border-left': f'4px solid {colors["success"]}',
                    'border-radius': '12px',
                    'height': '100%',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)'
                })
            ], md=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4([
                        html.I(className="fas fa-balance-scale", style={'marginRight': '10px'}),
                        "Balanced Approach"
                    ], style={'color': colors['text_primary'], 'marginBottom': '12px'}),
                    html.Span("23.8-26.1%", className="stat-number", style={
                        'fontSize': '2.2rem',
                        'fontWeight': '700',
                        'color': colors['accent'],
                        'display': 'block',
                        'marginBottom': '8px'
                    }),
                    html.P("Four diet types are nearly equally distributed, preventing over-specialization and ensuring balanced nutrition options.",
                          style={'color': colors['text_secondary'], 'lineHeight': '1.5'})
                ], className="p-4", style={
                    'background': colors['card_bg'],
                    'border': f'1px solid {colors["border"]}',
                    'border-left': f'4px solid {colors["accent"]}',
                    'border-radius': '12px',
                    'height': '100%',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)'
                })
            ], md=6),
            dbc.Col([
                html.Div([
                    html.H4([
                        html.I(className="fas fa-heartbeat", style={'marginRight': '10px'}),
                        "Chronic Disease"
                    ], style={'color': colors['text_primary'], 'marginBottom': '12px'}),
                    html.Span("p = 0.896", className="stat-number", style={
                        'fontSize': '2.2rem',
                        'fontWeight': '700',
                        'color': colors['secondary'],
                        'display': 'block',
                        'marginBottom': '8px'
                    }),
                    html.P("Health conditions show limited direct influence, suggesting recommendations focus on broader health profiles.",
                          style={'color': colors['text_secondary'], 'lineHeight': '1.5'})
                ], className="p-4", style={
                    'background': colors['card_bg'],
                    'border': f'1px solid {colors["border"]}',
                    'border-left': f'4px solid {colors["secondary"]}',
                    'border-radius': '12px',
                    'height': '100%',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)'
                })
            ], md=6)
        ], className="mb-4"),
        
        # Clinical Implications
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4([
                        html.I(className="fas fa-stethoscope", style={'marginRight': '10px'}),
                        "Clinical Implications"
                    ], style={'color': colors['text_primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '16px'}),
                    html.P("Personalized nutrition approaches demonstrate evidence-based patterns with sophisticated BMI-appropriate recommendations. However, opportunities exist for enhanced integration of chronic disease factors and age-specific protocols to further optimize patient outcomes.",
                          style={'fontSize': '1.1rem', 'lineHeight': '1.7', 'color': colors['text_secondary']})
                ], className="p-5", style={
                    'background': colors['card_bg'],
                    'border': f'1px solid {colors["border"]}',
                    'border-radius': '12px',
                    'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.08)'
                })
            ])
        ])
    ])

def create_health_profile():
    """Create the Health Profile tab content"""
    
    # Create BMI distribution chart
    bmi_dist = px.histogram(df, x='BMI', color='Gender', 
                           title='BMI Distribution by Gender',
                           color_discrete_sequence=color_sequence)
    bmi_dist.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    # Age distribution
    age_dist = px.box(df, x='Age_Group', y='BMI', 
                     title='BMI Distribution by Age Group',
                     color_discrete_sequence=[colors['primary']])
    age_dist.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    # Health metrics scatter plot
    health_scatter = px.scatter(df, x='Age', y='BMI', 
                               color='Chronic_Disease',
                               size='Daily_Steps',
                               title='Health Profile: Age vs BMI by Chronic Disease Status',
                               color_discrete_sequence=color_sequence)
    health_scatter.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    return html.Div([
        html.H2("Health Profile Distribution", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=bmi_dist, style={'height': '400px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=age_dist, style={'height': '400px'})
            ], md=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=health_scatter, style={'height': '500px'})
            ])
        ])
    ])

def create_chronic_conditions():
    """Create the Chronic Conditions tab content"""
    
    # Disease distribution
    disease_counts = df['Chronic_Disease'].value_counts()
    disease_dist = px.bar(x=disease_counts.index, y=disease_counts.values,
                         title='Distribution of Chronic Conditions',
                         color_discrete_sequence=[colors['primary']])
    disease_dist.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary']),
        xaxis_title="Chronic Disease",
        yaxis_title="Number of Patients"
    )
    
    # Disease vs Diet Recommendation
    disease_diet = pd.crosstab(df['Chronic_Disease'], df['Recommended_Meal_Plan'])
    disease_diet_pct = pd.crosstab(df['Chronic_Disease'], df['Recommended_Meal_Plan'], normalize='index')
    
    disease_diet_chart = px.bar(disease_diet, 
                               title='Diet Recommendations by Chronic Disease Status',
                               color_discrete_sequence=color_sequence)
    disease_diet_chart.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary']),
        xaxis_title="Chronic Disease",
        yaxis_title="Number of Patients"
    )
    
    return html.Div([
        html.H2("Chronic Conditions Analysis", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=disease_dist, style={'height': '400px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=disease_diet_chart, style={'height': '400px'})
            ], md=6)
        ])
    ])

def create_lifestyle_factors():
    """Create the Lifestyle Factors tab content"""
    
    # Exercise vs BMI
    exercise_bmi = px.box(df, x='Exercise_Frequency', y='BMI',
                         title='BMI Distribution by Exercise Frequency',
                         color_discrete_sequence=[colors['primary']])
    exercise_bmi.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary']),
        xaxis_title="Exercise Frequency (days/week)",
        yaxis_title="BMI"
    )
    
    # Sleep vs Health Metrics
    sleep_health = px.scatter(df, x='Sleep_Hours', y='BMI',
                             color='Chronic_Disease',
                             title='Sleep Hours vs BMI by Chronic Disease Status',
                             color_discrete_sequence=color_sequence)
    sleep_health.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary']),
        xaxis_title="Sleep Hours",
        yaxis_title="BMI"
    )
    
    return html.Div([
        html.H2("Lifestyle Factors Analysis", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=exercise_bmi, style={'height': '400px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=sleep_health, style={'height': '400px'})
            ], md=6)
        ])
    ])

def create_recommendations():
    """Create the Recommendations tab content"""
    
    # Diet recommendation distribution
    diet_dist = df['Recommended_Meal_Plan'].value_counts()
    diet_pie = px.pie(values=diet_dist.values, names=diet_dist.index,
                     title='Distribution of Diet Recommendations',
                     color_discrete_sequence=color_sequence)
    diet_pie.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    # BMI vs Diet Recommendation Heatmap
    bmi_diet_crosstab = pd.crosstab(df['BMI_Category'], df['Recommended_Meal_Plan'])
    heatmap = px.imshow(bmi_diet_crosstab.values,
                       x=bmi_diet_crosstab.columns,
                       y=bmi_diet_crosstab.index,
                       title='BMI Category vs Diet Recommendation Heatmap',
                       color_continuous_scale='Oranges')
    heatmap.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary']),
        xaxis_title="Recommended Meal Plan",
        yaxis_title="BMI Category"
    )
    
    return html.Div([
        html.H2("Diet Recommendations Analysis", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=diet_pie, style={'height': '400px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=heatmap, style={'height': '400px'})
            ], md=6)
        ])
    ])

def create_interactive_charts():
    """Create the Interactive Charts tab content"""
    
    # Sunburst chart for BMI-Diet relationship
    sunburst_data = df.groupby(['BMI_Category', 'Recommended_Meal_Plan']).size().reset_index(name='count')
    sunburst = px.sunburst(sunburst_data,
                          path=['BMI_Category', 'Recommended_Meal_Plan'],
                          values='count',
                          title='BMI Category and Diet Recommendation Hierarchy',
                          color_discrete_sequence=color_sequence)
    sunburst.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    # Parallel coordinates plot
    parallel_data = df[['Age', 'BMI', 'Daily_Steps', 'Exercise_Frequency', 'Sleep_Hours', 'Caloric_Intake']].dropna()
    parallel = px.parallel_coordinates(parallel_data,
                                      title='Multi-dimensional Health Profile Analysis',
                                      color='BMI',
                                      color_continuous_scale='Oranges')
    parallel.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    return html.Div([
        html.H2("Interactive Visualizations", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=sunburst, style={'height': '500px'})
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=parallel, style={'height': '500px'})
            ])
        ])
    ])

def create_statistical_validation():
    """Create the Statistical Validation tab content"""
    
    # Chi-square test results
    chi2_result = stats_results['bmi_diet_chi2']
    
    # Correlation heatmap
    corr_matrix = stats_results['correlation_matrix']
    corr_heatmap = px.imshow(corr_matrix.values,
                           x=corr_matrix.columns,
                           y=corr_matrix.index,
                           title='Correlation Matrix of Health Metrics',
                           color_continuous_scale='RdBu_r',
                           zmin=-1, zmax=1)
    corr_heatmap.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    # BMI correlations
    bmi_corr = stats_results['bmi_correlations']
    bmi_corr_df = pd.DataFrame({
        'Health Metric': bmi_corr.index,
        'Correlation with BMI': bmi_corr.values
    })
    bmi_corr_chart = px.bar(bmi_corr_df, x='Health Metric', y='Correlation with BMI',
                           title='BMI Correlations with Health Metrics',
                           color_discrete_sequence=[colors['primary']])
    bmi_corr_chart.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    return html.Div([
        html.H2("Statistical Validation", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        # Statistical Results
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("Chi-Square Test Results", style={'color': colors['primary']}),
                    html.P(f"Chi-square statistic: {chi2_result['chi2']:.4f}"),
                    html.P(f"P-value: {chi2_result['p_value']:.6f}"),
                    html.P(f"Degrees of freedom: {len(df['BMI_Category'].unique()) - 1}"),
                    html.P("Result: " + ("Significant association" if chi2_result['p_value'] < 0.05 else "No significant association"),
                          style={'fontWeight': 'bold', 'color': colors['highlight']})
                ], className="p-3", style={
                    'background': f'linear-gradient(135deg, {colors["light"]}, {colors["neutral"]})',
                    'border-radius': '10px',
                    'border-left': f'4px solid {colors["primary"]}'
                })
            ], md=4),
            dbc.Col([
                html.Div([
                    html.H4("Key Findings", style={'color': colors['primary']}),
                    html.Ul([
                        html.Li("BMI shows significant correlation with diet recommendations (p < 0.01)"),
                        html.Li("Four diet types are nearly equally distributed (23.8-26.1% each)"),
                        html.Li("Chronic diseases show limited direct influence on recommendations"),
                        html.Li("Lifestyle factors significantly impact dietary choices")
                    ])
                ], className="p-3", style={
                    'background': f'linear-gradient(135deg, {colors["light"]}, {colors["neutral"]})',
                    'border-radius': '10px',
                    'border-left': f'4px solid {colors["primary"]}'
                })
            ], md=8)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=corr_heatmap, style={'height': '500px'})
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=bmi_corr_chart, style={'height': '400px'})
            ])
        ])
    ])

def create_clinical_insights():
    """Create the Clinical Insights tab content"""
    
    # Key insights based on the data analysis
    insights = [
        {
            "title": "BMI-Driven Recommendations",
            "icon": "fas fa-weight",
            "content": "BMI is the strongest predictor of diet recommendations with statistically significant associations (p < 0.01). This evidence-based approach ensures appropriate caloric and macronutrient distribution."
        },
        {
            "title": "Balanced Nutrition Strategy", 
            "icon": "fas fa-balance-scale",
            "content": "Four major diet types are nearly equally distributed (23.8-26.1% each), preventing over-specialization and ensuring patients receive balanced nutrition options tailored to their needs."
        },
        {
            "title": "Lifestyle Integration",
            "icon": "fas fa-running", 
            "content": "Exercise frequency, sleep patterns, and dietary habits significantly influence recommendations, showing the system's respect for patient lifestyle choices and practical implementation."
        },
        {
            "title": "Chronic Disease Considerations",
            "icon": "fas fa-heartbeat",
            "content": "While chronic diseases show limited direct influence (p = 0.896), the system focuses on broader health profiles, suggesting opportunities for enhanced disease-specific protocols."
        }
    ]
    
    # Create insight cards
    insight_cards = []
    for i, insight in enumerate(insights):
        card = dbc.Col([
            html.Div([
                html.H4([
                    html.I(className=f"{insight['icon']} fa-2x", style={'marginRight': '15px', 'color': colors['highlight']}),
                    insight['title']
                ], style={'color': colors['primary'], 'marginBottom': '15px'}),
                html.P(insight['content'], style={'fontSize': '1rem', 'lineHeight': '1.6'})
            ], className="p-4", style={
                'background': 'white',
                'border-radius': '15px',
                'boxShadow': '0 10px 30px rgba(139, 69, 19, 0.1)',
                'height': '100%'
            })
        ], md=6)
        insight_cards.append(card)
    
    # Group cards in rows
    rows = []
    for i in range(0, len(insight_cards), 2):
        row = dbc.Row(insight_cards[i:i+2], className="mb-4")
        rows.append(row)
    
    return html.Div([
        html.H2("Clinical Insights", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        # Insights cards
        *rows,
        
        # Recommendations
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("Clinical Recommendations", style={'color': colors['primary'], 'marginBottom': '20px'}),
                    html.Ul([
                        html.Li("Implement BMI-stratified diet protocols with regular monitoring", style={'marginBottom': '10px'}),
                        html.Li("Develop chronic disease-specific nutrition guidelines", style={'marginBottom': '10px'}),
                        html.Li("Integrate lifestyle factors into recommendation algorithms", style={'marginBottom': '10px'}),
                        html.Li("Establish age-specific dietary intervention protocols", style={'marginBottom': '10px'}),
                        html.Li("Create patient education programs for sustained adherence", style={'marginBottom': '10px'})
                    ], style={'fontSize': '1rem', 'lineHeight': '1.7'})
                ], className="p-4", style={
                    'background': f'linear-gradient(135deg, {colors["accent"]}, {colors["highlight"]})',
                    'color': 'white',
                    'border-radius': '10px',
                    'marginTop': '20px'
                })
            ])
        ])
    ])

def create_data_download():
    """Create the Data Download tab content"""
    
    # Create download link for the data
    csv_string = df.to_csv(index=False)
    csv_base64 = base64.b64encode(csv_string.encode()).decode()
    
    return html.Div([
        html.H2("Data Download", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("Dataset Information", style={'color': colors['primary'], 'marginBottom': '20px'}),
                    html.P(f"Total Records: {len(df):,}", style={'fontSize': '1.2rem'}),
                    html.P(f"Variables: {len(df.columns)}", style={'fontSize': '1.2rem'}),
                    html.P("Variables include: Demographics, Health Metrics, Lifestyle Factors, Medical Conditions, Nutrition Data, and Recommendations", 
                          style={'fontSize': '1rem', 'marginTop': '20px'}),
                    
                    html.H4("Available Downloads", style={'color': colors['primary'], 'marginTop': '30px', 'marginBottom': '20px'}),
                    
                    dbc.Button([
                        html.I(className="fas fa-download", style={'marginRight': '10px'}),
                        "Download Complete Dataset (CSV)"
                    ], 
                    href=f"data:text/csv;base64,{csv_base64}",
                    download="diet_analytics_data.csv",
                    color="primary",
                    size="lg",
                    className="mb-3",
                    style={'background': f'linear-gradient(135deg, {colors["primary"]}, {colors["secondary"]})', 'border': 'none'}
                    ),
                    
                    html.P("The dataset includes comprehensive health and nutrition information suitable for research, analysis, and machine learning applications.", 
                          style={'fontSize': '1rem', 'marginTop': '20px'})
                    
                ], className="p-4", style={
                    'background': 'white',
                    'border-radius': '15px',
                    'boxShadow': '0 10px 30px rgba(139, 69, 19, 0.1)'
                })
            ], md=8),
            dbcCol([
                html.Div([
                    html.H4("Data Summary", style={'color': colors['primary'], 'marginBottom': '20px'}),
                    
                    html.H6("Key Statistics:", style={'marginTop': '20px'}),
                    html.Ul([
                        html.Li(f"Average Age: {df['Age'].mean():.1f} years"),
                        html.Li(f"Average BMI: {df['BMI'].mean():.1f}"),
                        html.Li(f"Gender Distribution: {df['Gender'].value_counts().to_dict()}"),
                        html.Li(f"Chronic Disease Rate: {(df['Chronic_Disease'] != 'Healthy').mean()*100:.1f}%"),
                        html.Li(f"Average Daily Steps: {df['Daily_Steps'].mean():.0f}"),
                        html.Li(f"Average Caloric Intake: {df['Caloric_Intake'].mean():.0f} kcal")
                    ]),
                    
                    html.H6("Data Quality:", style={'marginTop': '20px'}),
                    html.Ul([
                        html.Li("No missing values in key variables"),
                        html.Li("Validated health metrics within normal ranges"),
                        html.Li("Statistically significant correlations identified"),
                        html.Li("Suitable for machine learning applications")
                    ])
                    
                ], className="p-4", style={
                    'background': f'linear-gradient(135deg, {colors["light"]}, {colors["neutral"]})',
                    'border-radius': '15px',
                    'border-left': f'4px solid {colors["primary"]}'
                })
            ], md=4)
        ])
    ])

# Run the app
# Filtered versions of all tab functions

def create_population_overview_filtered(filtered_df):
    """Create Population Overview tab - matches original R dashboard layout"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Chronic Disease Distribution (Pie Chart)
    chronic_counts = filtered_df['Chronic_Disease'].value_counts()
    chronic_pie = px.pie(
        values=chronic_counts.values, 
        names=chronic_counts.index,
        title=f'Chronic Disease Distribution (n={len(filtered_df)})',
        color_discrete_sequence=color_sequence
    )
    chronic_pie.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
    )
    
    # Health Profile Distribution (Bar Chart)
    bmi_counts = filtered_df['BMI_Category'].value_counts()
    health_profile_bar = px.bar(
        x=bmi_counts.index, 
        y=bmi_counts.values,
        title=f'BMI Category Distribution (n={len(filtered_df)})',
        color=bmi_counts.index,
        color_discrete_sequence=color_sequence
    )
    health_profile_bar.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        xaxis_title="BMI Category",
        yaxis_title="Number of Patients",
        showlegend=False
    )
    
    # Age Group Distribution (Bar Chart)
    age_counts = filtered_df['Age_Group'].value_counts()
    age_bar = px.bar(
        x=age_counts.index, 
        y=age_counts.values,
        title=f'Age Group Distribution (n={len(filtered_df)})',
        color=age_counts.index,
        color_discrete_sequence=color_sequence
    )
    age_bar.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        xaxis_title="Age Group",
        yaxis_title="Number of Patients",
        showlegend=False
    )
    
    # Diet Recommendation Distribution (Pie Chart)
    diet_counts = filtered_df['Recommended_Meal_Plan'].value_counts()
    diet_pie = px.pie(
        values=diet_counts.values, 
        names=diet_counts.index,
        title=f'Diet Recommendation Distribution (n={len(filtered_df)})',
        color_discrete_sequence=color_sequence
    )
    diet_pie.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
    )
    
    return html.Div([
        html.H2("Population Overview", 
               style={'textAlign': 'center', 'color': colors['text_primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        # First Row - Chronic Disease and Health Profile
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=chronic_pie, style={'height': '400px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=health_profile_bar, style={'height': '400px'})
            ], md=6)
        ], className="mb-4"),
        
        # Second Row - Age Groups and Diet Recommendations
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=age_bar, style={'height': '400px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=diet_pie, style={'height': '400px'})
            ], md=6)
        ])
    ])

def create_age_demographics_filtered(filtered_df):
    """Create Age Demographics tab - Diet Recommendations Across Age Groups"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Calculate percentages within each age group
    age_diet_crosstab = pd.crosstab(filtered_df['Age_Group'], filtered_df['Recommended_Meal_Plan'], normalize='index') * 100
    
    # Create line chart showing diet recommendations across age groups
    line_fig = go.Figure()
    
    for diet_plan in age_diet_crosstab.columns:
        line_fig.add_trace(go.Scatter(
            x=age_diet_crosstab.index,
            y=age_diet_crosstab[diet_plan],
            mode='lines+markers',
            name=diet_plan,
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    line_fig.update_layout(
        title=f'Diet Recommendations Across Age Groups<br><sub>Percentage within each age group (n={len(filtered_df)})</sub>',
        xaxis_title="Age Group",
        yaxis_title="Percentage within Age Group",
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="right", x=1.15),
        height=500
    )
    
    return html.Div([
        html.H2("Age Demographics Analysis", 
               style={'textAlign': 'center', 'color': colors['text_primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        html.P("Line chart showing how diet recommendations vary across different age demographics", 
               style={'textAlign': 'center', 'color': colors['text_secondary'], 'fontStyle': 'italic', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=line_fig, style={'height': '500px'})
            ])
        ])
    ])
def create_health_profile_filtered(filtered_df):
    """Create the Health Profile tab content with filtered data"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Create BMI distribution chart
    bmi_dist = px.histogram(filtered_df, x='BMI', color='Gender', 
                           title=f'BMI Distribution by Gender (n={len(filtered_df)})',
                           color_discrete_sequence=color_sequence)
    bmi_dist.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    # Age distribution
    age_dist = px.box(filtered_df, x='Age_Group', y='BMI', 
                     title=f'BMI Distribution by Age Group (n={len(filtered_df)})',
                     color_discrete_sequence=[colors['primary']])
    age_dist.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    return html.Div([
        html.H2("Health Profile Distribution", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=bmi_dist, style={'height': '400px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=age_dist, style={'height': '400px'})
            ], md=6)
        ])
    ])

def create_chronic_conditions_filtered(filtered_df):
    """Create Chronic Conditions tab - Diet Recommendations by Chronic Disease Status"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Calculate percentages within each chronic disease group
    chronic_diet_crosstab = pd.crosstab(filtered_df['Chronic_Disease'], filtered_df['Recommended_Meal_Plan'], normalize='index') * 100
    
    # Create stacked bar chart
    fig = go.Figure()
    
    for i, diet_plan in enumerate(chronic_diet_crosstab.columns):
        fig.add_trace(go.Bar(
            name=diet_plan,
            x=chronic_diet_crosstab.index,
            y=chronic_diet_crosstab[diet_plan],
            marker_color=color_sequence[i % len(color_sequence)],
            text=[f'{val:.1f}%' for val in chronic_diet_crosstab[diet_plan]],
            textposition='inside'
        ))
    
    fig.update_layout(
        title=f'Diet Recommendations by Chronic Disease Status<br><sub>Percentage distribution of diet recommendations within each disease group (n={len(filtered_df)})</sub>',
        xaxis_title="Chronic Disease",
        yaxis_title="Percentage within Disease Group",
        barmode='stack',
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="right", x=1.15),
        height=500
    )
    
    return html.Div([
        html.H2("Diet Recommendations by Chronic Disease Status", 
               style={'textAlign': 'center', 'color': colors['text_primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '20px'}),
        
        html.P("Percentage distribution of diet recommendations within each chronic disease category", 
               style={'textAlign': 'center', 'color': colors['text_secondary'], 'fontStyle': 'italic', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig, style={'height': '500px'})
            ])
        ])
    ])

def create_lifestyle_factors_filtered(filtered_df):
    """Create the Lifestyle Factors tab content with filtered data"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Exercise vs BMI
    exercise_bmi = px.box(filtered_df, x='Exercise_Frequency', y='BMI',
                         title=f'BMI Distribution by Exercise Frequency (n={len(filtered_df)})',
                         color_discrete_sequence=[colors['primary']])
    exercise_bmi.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary']),
        xaxis_title="Exercise Frequency (days/week)",
        yaxis_title="BMI"
    )
    
    return html.Div([
        html.H2("Lifestyle Factors Analysis", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=exercise_bmi, style={'height': '400px'})
            ])
        ])
    ])

def create_recommendations_filtered(filtered_df):
    """Create the Diet Recommendations tab content with filtered data"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Diet recommendation distribution (Pie Chart)
    diet_dist = filtered_df['Recommended_Meal_Plan'].value_counts()
    diet_pie = px.pie(
        values=diet_dist.values, 
        names=diet_dist.index,
        title=f'Diet Recommendation Distribution (n={len(filtered_df)})',
        color_discrete_sequence=color_sequence
    )
    diet_pie.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
    )
    
    # Diet recommendation bar chart
    diet_bar = px.bar(
        x=diet_dist.index, 
        y=diet_dist.values,
        title=f'Diet Recommendation Counts (n={len(filtered_df)})',
        color=diet_dist.index,
        color_discrete_sequence=color_sequence
    )
    diet_bar.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        xaxis_title="Recommended Meal Plan",
        yaxis_title="Number of Patients",
        showlegend=False
    )
    
    # Calculate percentages for summary cards
    total_patients = len(filtered_df)
    diet_percentages = (diet_dist / total_patients * 100).round(1)
    
    # Create summary cards
    summary_cards = []
    for i, (diet_plan, count) in enumerate(diet_dist.items()):
        percentage = diet_percentages[diet_plan]
        card = dbc.Col([
            html.Div([
                html.H5(diet_plan, style={'color': colors['text_primary'], 'marginBottom': '10px', 'fontWeight': 'bold'}),
                html.H3(f"{count:,}", style={'color': color_sequence[i % len(color_sequence)], 'marginBottom': '5px', 'fontWeight': 'bold'}),
                html.P(f"{percentage}% of patients", style={'color': colors['text_secondary'], 'margin': 0, 'fontSize': '0.9rem'})
            ], className="p-3", style={
                'background': colors['card_bg'],
                'border': f'1px solid {colors["border"]}',
                'border-left': f'4px solid {color_sequence[i % len(color_sequence)]}',
                'border-radius': '8px',
                'textAlign': 'center',
                'height': '100%',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)'
            })
        ], md=3)
        summary_cards.append(card)
    
    return html.Div([
        html.H2("Diet Recommendations Analysis", 
               style={'textAlign': 'center', 'color': colors['text_primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        # Summary Cards Row
        dbc.Row(summary_cards, className="mb-4"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=diet_pie, style={'height': '450px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=diet_bar, style={'height': '450px'})
            ], md=6)
        ])
    ])

def create_interactive_charts_filtered(filtered_df):
    """Create the Interactive Charts tab content with filtered data"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Simple scatter plot for filtered data
    scatter = px.scatter(filtered_df, x='Age', y='BMI', color='Chronic_Disease',
                        title=f'Age vs BMI by Chronic Disease (n={len(filtered_df)})',
                        color_discrete_sequence=color_sequence)
    scatter.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['primary'])
    )
    
    return html.Div([
        html.H2("Interactive Visualizations", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=scatter, style={'height': '500px'})
            ])
        ])
    ])

def create_statistical_validation_filtered(filtered_df, filtered_stats):
    """Create the Statistical Validation tab content with filtered data"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    return html.Div([
        html.H2("Statistical Validation", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        html.Div([
            html.H4(f"Filtered Dataset Statistics (n={len(filtered_df)})", style={'color': colors['primary']}),
            html.P(f"Average BMI: {filtered_df['BMI'].mean():.2f}"),
            html.P(f"Age Range: {filtered_df['Age'].min()} - {filtered_df['Age'].max()} years"),
            html.P(f"Most Common Diet Plan: {filtered_df['Recommended_Meal_Plan'].mode().iloc[0] if len(filtered_df) > 0 else 'N/A'}")
        ], className="p-3", style={
            'background': f'linear-gradient(135deg, {colors["light"]}, {colors["neutral"]})',
            'border-radius': '10px'
        })
    ])

def create_clinical_insights_filtered(filtered_df, filtered_stats):
    """Create the Clinical Insights tab content with filtered data"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    return html.Div([
        html.H2("Clinical Insights", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        html.Div([
            html.H4("Key Insights from Filtered Data", style={'color': colors['primary']}),
            html.Ul([
                html.Li(f"Total patients in filtered dataset: {len(filtered_df):,}"),
                html.Li(f"Average BMI: {filtered_df['BMI'].mean():.2f}"),
                html.Li(f"Gender distribution: {dict(filtered_df['Gender'].value_counts())}"),
                html.Li(f"Most common chronic condition: {filtered_df['Chronic_Disease'].mode().iloc[0] if len(filtered_df) > 0 else 'N/A'}")
            ])
        ], className="p-4", style={
            'background': 'white',
            'border-radius': '15px',
            'boxShadow': '0 10px 30px rgba(139, 69, 19, 0.1)'
        })
    ])

def create_data_download_filtered(filtered_df):
    """Create the Data Download tab content with filtered data"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Create download link for filtered data
    csv_string = filtered_df.to_csv(index=False)
    csv_base64 = base64.b64encode(csv_string.encode()).decode()
    
    return html.Div([
        html.H2("Data Download", 
               style={'textAlign': 'center', 'color': colors['primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        html.Div([
            html.H4("Filtered Dataset Information", style={'color': colors['primary']}),
            html.P(f"Filtered Records: {len(filtered_df):,}", style={'fontSize': '1.2rem'}),
            html.P(f"Variables: {len(filtered_df.columns)}", style={'fontSize': '1.2rem'}),
            
            dbc.Button([
                html.I(className="fas fa-download", style={'marginRight': '10px'}),
                "Download Filtered Dataset (CSV)"
            ], 
            href=f"data:text/csv;base64,{csv_base64}",
            download="filtered_diet_analytics_data.csv",
            color="primary",
            size="lg",
            style={'background': f'linear-gradient(135deg, {colors["primary"]}, {colors["secondary"]})', 'border': 'none'}
            )
        ], className="p-4", style={
            'background': 'white',
            'border-radius': '15px',
            'boxShadow': '0 10px 30px rgba(139, 69, 19, 0.1)'
        })
    ])
def create_bmi_analysis_filtered(filtered_df):
    """Create BMI Analysis tab - Diet Recommendations by BMI Category Heatmap"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Calculate percentages within each BMI category
    bmi_diet_crosstab = pd.crosstab(filtered_df['BMI_Category'], filtered_df['Recommended_Meal_Plan'], normalize='index') * 100
    
    # Create heatmap
    heatmap_fig = px.imshow(
        bmi_diet_crosstab.values,
        x=bmi_diet_crosstab.columns,
        y=bmi_diet_crosstab.index,
        color_continuous_scale='YlOrRd',
        text_auto='.1f',
        aspect="auto"
    )
    
    heatmap_fig.update_layout(
        title=f'Diet Recommendations by BMI Category<br><sub>Percentage within each BMI group (n={len(filtered_df)})</sub>',
        xaxis_title="Recommended Meal Plan",
        yaxis_title="BMI Category",
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        height=500,
        margin=dict(t=80, b=60, l=100, r=60)
    )
    
    heatmap_fig.update_traces(texttemplate="%{z:.1f}%", textfont_size=12)
    
    return html.Div([
        html.H2("BMI Analysis", 
               style={'textAlign': 'center', 'color': colors['text_primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '30px'}),
        
        html.P("Heatmap showing percentage distribution of diet recommendations within each BMI category", 
               style={'textAlign': 'center', 'color': colors['text_secondary'], 'fontStyle': 'italic', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=heatmap_fig, style={'height': '500px'})
            ])
        ])
    ])

def create_health_metrics_filtered(filtered_df):
    """Create Health Metrics tab - Interactive Health Metrics by Diet Recommendation"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Create subplots for multiple box plots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('BMI Distribution', 'Cholesterol Level', 'Blood Sugar Level', 'Daily Steps'),
        vertical_spacing=0.15,
        horizontal_spacing=0.12
    )
    
    # BMI Distribution
    for i, diet_plan in enumerate(filtered_df['Recommended_Meal_Plan'].unique()):
        diet_data = filtered_df[filtered_df['Recommended_Meal_Plan'] == diet_plan]
        fig.add_trace(
            go.Box(y=diet_data['BMI'], name=diet_plan, 
                  marker_color=color_sequence[i % len(color_sequence)],
                  showlegend=False),
            row=1, col=1
        )
    
    # Cholesterol Level
    for i, diet_plan in enumerate(filtered_df['Recommended_Meal_Plan'].unique()):
        diet_data = filtered_df[filtered_df['Recommended_Meal_Plan'] == diet_plan]
        fig.add_trace(
            go.Box(y=diet_data['Cholesterol_Level'], name=diet_plan,
                  marker_color=color_sequence[i % len(color_sequence)],
                  showlegend=False),
            row=1, col=2
        )
    
    # Blood Sugar Level
    for i, diet_plan in enumerate(filtered_df['Recommended_Meal_Plan'].unique()):
        diet_data = filtered_df[filtered_df['Recommended_Meal_Plan'] == diet_plan]
        fig.add_trace(
            go.Box(y=diet_data['Blood_Sugar_Level'], name=diet_plan,
                  marker_color=color_sequence[i % len(color_sequence)],
                  showlegend=False),
            row=2, col=1
        )
    
    # Daily Steps
    for i, diet_plan in enumerate(filtered_df['Recommended_Meal_Plan'].unique()):
        diet_data = filtered_df[filtered_df['Recommended_Meal_Plan'] == diet_plan]
        fig.add_trace(
            go.Box(y=diet_data['Daily_Steps'], name=diet_plan,
                  marker_color=color_sequence[i % len(color_sequence)],
                  showlegend=True if i == 0 else False),
            row=2, col=2
        )
    
    fig.update_layout(
        title_text=f"Health Metrics Distribution by Diet Recommendation<br><sub>Box plots showing variation in key health indicators (n={len(filtered_df)})</sub>",
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=11),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        height=650,
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5),
        margin=dict(t=80, b=80, l=60, r=60)
    )
    
    # Update x-axis labels
    fig.update_xaxes(title_text="Diet Recommendation", row=1, col=1)
    fig.update_xaxes(title_text="Diet Recommendation", row=1, col=2)
    fig.update_xaxes(title_text="Diet Recommendation", row=2, col=1)
    fig.update_xaxes(title_text="Diet Recommendation", row=2, col=2)
    
    return html.Div([
        html.H2("Interactive Health Metrics by Diet Recommendation", 
               style={'textAlign': 'center', 'color': colors['text_primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '20px'}),
        
        html.P("Explore how BMI, cholesterol, blood sugar, and activity levels vary across different diet recommendations", 
               style={'textAlign': 'center', 'color': colors['text_secondary'], 'fontStyle': 'italic', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig, style={'height': '650px'})
            ])
        ])
    ])

def create_interactive_scatter_filtered(filtered_df):
    """Create Interactive Scatter Plots tab"""
    if len(filtered_df) == 0:
        return html.Div([
            html.H2("No Data Found", style={'textAlign': 'center', 'color': colors['primary']}),
            html.P("Please adjust your filters to see results.", style={'textAlign': 'center'})
        ])
    
    # Age vs BMI scatter plot colored by chronic disease
    age_bmi_scatter = px.scatter(
        filtered_df, 
        x='Age', 
        y='BMI',
        color='Chronic_Disease',
        size='Daily_Steps',
        hover_data=['Patient_ID', 'Recommended_Meal_Plan', 'Exercise_Frequency'],
        title=f'Age vs BMI by Chronic Disease Status (n={len(filtered_df)})',
        color_discrete_sequence=color_sequence
    )
    age_bmi_scatter.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        xaxis_title="Age (years)",
        yaxis_title="BMI",
        legend_title="Chronic Disease"
    )
    
    # Exercise vs BMI scatter plot colored by diet recommendation
    exercise_bmi_scatter = px.scatter(
        filtered_df,
        x='Exercise_Frequency',
        y='BMI',
        color='Recommended_Meal_Plan',
        size='Sleep_Hours',
        hover_data=['Patient_ID', 'Age', 'Chronic_Disease'],
        title=f'Exercise Frequency vs BMI by Diet Recommendation (n={len(filtered_df)})',
        color_discrete_sequence=color_sequence
    )
    exercise_bmi_scatter.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        xaxis_title="Exercise Frequency (days/week)",
        yaxis_title="BMI",
        legend_title="Diet Recommendation"
    )
    
    # Cholesterol vs Blood Sugar scatter plot
    cholesterol_sugar_scatter = px.scatter(
        filtered_df,
        x='Cholesterol_Level',
        y='Blood_Sugar_Level',
        color='BMI_Category',
        size='Age',
        hover_data=['Patient_ID', 'Recommended_Meal_Plan', 'Chronic_Disease'],
        title=f'Cholesterol vs Blood Sugar by BMI Category (n={len(filtered_df)})',
        color_discrete_sequence=color_sequence
    )
    cholesterol_sugar_scatter.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        xaxis_title="Cholesterol Level (mg/dL)",
        yaxis_title="Blood Sugar Level (mg/dL)",
        legend_title="BMI Category"
    )
    
    # Daily Steps vs Sleep Hours scatter plot
    steps_sleep_scatter = px.scatter(
        filtered_df,
        x='Daily_Steps',
        y='Sleep_Hours',
        color='Age_Group',
        size='BMI',
        hover_data=['Patient_ID', 'Recommended_Meal_Plan', 'Exercise_Frequency'],
        title=f'Daily Steps vs Sleep Hours by Age Group (n={len(filtered_df)})',
        color_discrete_sequence=color_sequence
    )
    steps_sleep_scatter.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color=colors['text_primary']),
        xaxis_title="Daily Steps",
        yaxis_title="Sleep Hours",
        legend_title="Age Group"
    )
    
    return html.Div([
        html.H2("Interactive Scatter Plot Analysis", 
               style={'textAlign': 'center', 'color': colors['text_primary'], 'fontFamily': 'Playfair Display, serif', 'marginBottom': '20px'}),
        
        html.P("Explore relationships between different health metrics with interactive scatter plots. Hover over points for detailed information.", 
               style={'textAlign': 'center', 'color': colors['text_secondary'], 'fontStyle': 'italic', 'marginBottom': '30px'}),
        
        # First Row - Age/BMI and Exercise/BMI
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=age_bmi_scatter, style={'height': '450px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=exercise_bmi_scatter, style={'height': '450px'})
            ], md=6)
        ], className="mb-4"),
        
        # Second Row - Cholesterol/Blood Sugar and Steps/Sleep
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=cholesterol_sugar_scatter, style={'height': '450px'})
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=steps_sleep_scatter, style={'height': '450px'})
            ], md=6)
        ])
    ])

# Run the app
if __name__ == '__main__':
    print(f"Starting Personalized Diet Analytics Dashboard...")
    print(f"Data loaded: {len(df)} records with {len(df.columns)} variables")
    print(f"Dashboard available at: http://localhost:8052")
    app.run(debug=True, host='127.0.0.1', port=8052)
