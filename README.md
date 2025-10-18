# Personalized Diet Analytics Dashboard - Python Implementation

This repository provides a comprehensive Python-based analytics dashboard for personalized diet recommendations, converted and enhanced from the original R Shiny application.

## Overview

This modern Python Dash application provides sophisticated analytics for personalized diet recommendations with:

- **9 specialized analysis tabs** with professional healthcare design
- **20+ interactive visualizations** using Plotly and Dash with real-time filtering
- **Evidence-based insights** with statistical significance testing (p < 0.01 for BMI correlations)
- **Advanced filtering system** with horizontal filter bar for dynamic data exploration
- **Professional color scheme** designed for healthcare applications
- **Real-time analytics** with 4,355 patient records and 32 health variables

## Quick Start

### Option 1: One-Command Setup (Recommended)

```bash
# Make script executable and run
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### Option 2: Manual Setup

1. **Create and activate virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Verify setup (optional but recommended):**

   ```bash
   python test_setup.py
   ```

4. **Start the dashboard:**

   ```bash
   python dashboard_app.py
   ```

5. **Access the dashboard:**
   - Open your browser to `http://localhost:8052`
   - Use the horizontal filter bar to explore different patient subsets
   - Navigate through the 9 specialized analysis tabs

## Features

### 📊 Dashboard Tabs & Features

1. **Executive Summary** - Key insights with professional statistics cards and clinical implications
2. **Population Overview** - 4-panel comprehensive demographic analysis (pie charts, bar charts)
3. **Age Demographics** - Line chart analysis of diet recommendations across age groups
4. **BMI Analysis** - Interactive heatmap showing diet recommendations by BMI category
5. **Health Metrics** - 4-panel box plots (BMI, cholesterol, blood sugar, daily steps by diet type)
6. **Chronic Conditions** - Stacked bar chart analysis of diet recommendations by disease status
7. **Diet Recommendations** - Enhanced analysis with summary cards, pie chart, and bar chart
8. **Statistical Analysis** - Chi-square tests, correlation matrices, significance testing
9. **Data Export** - Download filtered datasets with comprehensive metadata

### 🎛️ Advanced Filtering System

**Horizontal Filter Bar with Real-time Updates:**
- **Patient ID Search** - Exact match (P00001) or partial search (P001, 123)
- **Gender Selection** - Male/Female/Other dropdown
- **Diet Plan Filter** - Filter by recommended meal plans
- **Health Condition Filter** - Filter by chronic disease status
- **Age Range Slider** - Dynamic age filtering (18-79 years)
- **BMI Range Slider** - Body mass index filtering (12-53)
- **Exercise Frequency Slider** - Activity level filtering (0-7 days/week)
- **Reset Button** - One-click filter clearing

## System Requirements

### Minimum Requirements

- **Python 3.7+**
- **2GB RAM** minimum
- **500MB disk space** for packages and data

### Required Python Packages

**Core Analytics:**
- `pandas>=2.0.0` - Data manipulation and analysis
- `numpy>=1.24.0` - Numerical computing
- `scipy>=1.11.0` - Statistical analysis
- `scikit-learn>=1.3.0` - Machine learning utilities

**Visualization & Dashboard:**
- `plotly>=5.15.0` - Interactive charts and graphs
- `dash>=2.11.0` - Web application framework
- `dash-bootstrap-components>=1.4.0` - UI components

**Optional (for legacy Flask interface):**
- `flask>=2.3.0` - Alternative web framework
- `psutil>=5.9.0` - System monitoring
- `requests>=2.31.0` - HTTP requests

## Data Overview

The dashboard analyzes a comprehensive dataset of **4,355 patient records** with 32 variables:

- **Demographics**: Age, Gender, BMI Categories, Height, Weight
- **Health Metrics**: Blood Pressure, Cholesterol, Blood Sugar Levels
- **Lifestyle Factors**: Exercise Frequency, Sleep Hours, Dietary Habits
- **Medical Conditions**: Chronic Diseases, Genetic Risk Factors, Allergies
- **Nutrition Data**: Caloric Intake, Macronutrient Distribution, Meal Plans

## Key Findings

- **BMI is the strongest predictor** of diet recommendations (p < 0.01)
- **Balanced distribution** across four major diet types (23.8-26.1% each)
- **Lifestyle factors** show significant correlations with dietary preferences
- **Chronic conditions** have limited direct influence, suggesting broader health focus

## Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   # Check what's using port 8052
   lsof -i :8052
   # Kill the process or use different port in dashboard_app.py
   ```

2. **Missing Dependencies**

   ```bash
   # Reinstall requirements
   pip install -r requirements.txt
   ```

3. **Virtual Environment Issues**

   ```bash
   # Recreate virtual environment
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Data Loading Issues**
   ```bash
   # Verify data files exist
   ls -la data/
   # Should show processed_diet_data.csv (4,355 records)
   ```

### Getting Help

- **Check Console**: Browser developer tools show any JavaScript errors
- **Verify Data**: Dashboard shows "Data loaded: 4355 records" in terminal
- **Test Filters**: Try Patient ID search with "P00001" to verify functionality
- **Network Issues**: Ensure firewall allows access to port 8052

## Development

### Project Structure

```
├── dashboard_app.py           # Main Python Dash application
├── run_dashboard.sh           # Shell script launcher (recommended)
├── start_dashboard_simple.py  # Python launcher script
├── app.py                     # Alternative Flask wrapper (legacy)
├── requirements.txt           # Python dependencies
├── data/                      # Real dataset files
│   ├── processed_diet_data.csv    # Main patient dataset (4,355 records)
│   └── disease_diet_contingency.csv # Additional analysis data
├── venv/                      # Virtual environment (created after setup)
├── templates/                 # HTML templates (for Flask app)
└── README.md                  # This file
```

### Adding New Features

1. **New Analysis Tab**: Add function in `dashboard_app.py` following the `create_*_filtered()` pattern
2. **Update Navigation**: Add new tab to the `dcc.Tabs` component in the layout
3. **Update Callback**: Add new tab handling in the `render_tab_content()` callback
4. **Data Processing**: Extend analysis using the existing 32 variables in the dataset

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. The original R Shiny application and this web interface are provided as-is for educational and research purposes.

## Acknowledgments

- **R Shiny Team** for the excellent dashboard framework
- **Plotly Team** for interactive visualization capabilities
- **Tidyverse Community** for data processing tools
- **Original Dataset Contributors** for the comprehensive health data

---

For more information, visit the [original repository](https://github.com/NikhilTeja2000/OKComputer_R-Dashboard-App) or check the [detailed report](https://eqq3pylpyaib6.ok.kimi.link).

## Interactive Features

### 🎛️ Horizontal Filter Bar
The dashboard includes a comprehensive horizontal filter system:

**Row 1 - Dropdown Filters:**
- 🔍 **Patient ID Search** - Find specific patients
- 👥 **Gender Filter** - Male/Female/Other selection
- 🍽️ **Diet Plan Filter** - Filter by meal plan recommendations  
- 💓 **Health Condition Filter** - Filter by chronic diseases
- 🔄 **Reset Button** - Clear all filters instantly

**Row 2 - Range Sliders:**
- 🎂 **Age Range** - Adjust age demographics (18-79 years)
- ⚖️ **BMI Range** - Filter by body mass index (12-53)
- 🏃 **Exercise Frequency** - Filter by activity level (0-7 days/week)

### 📊 Real-time Analytics
- All charts and statistics update instantly when filters change
- Dynamic patient count and statistics recalculation
- Export filtered datasets as CSV files
- Smart handling of empty filter results

**🚀 Access the enhanced dashboard at: http://localhost:8052**

## Design & Color Scheme

### 🎨 Professional Healthcare Color Palette
The dashboard features a carefully designed, healthcare-appropriate color scheme:

- **Professional Blue** (#2E86AB) - Primary headers and navigation
- **Deep Rose** (#A23B72) - Secondary accents and highlights  
- **Warm Orange** (#F18F01) - Energy and nutrition focus
- **Medical Green** (#38A169) - Positive health indicators
- **Trust Blue** (#3182CE) - Information and data elements
- **Clean White** (#FFFFFF) - Pure backgrounds for clarity
- **Charcoal Gray** (#2D3748) - Professional text and contrast

This palette provides excellent contrast, accessibility, and visual appeal while maintaining a trustworthy healthcare aesthetic.

### 🎨 Enhanced Header Design
- **Gradient Background**: Professional blue to deep rose gradient
- **White Text**: High contrast white text with subtle shadow for readability
- **Professional Typography**: Playfair Display serif font for elegance
- **Enhanced Visibility**: Text shadow ensures readability across all devices#
# New Chart Features (Based on Original R Dashboard)

### 📊 **Recreated Visualizations:**

1. **Population Overview** - 4-panel dashboard showing:
   - Chronic Disease Distribution (Pie Chart)
   - BMI Category Distribution (Bar Chart) 
   - Age Group Distribution (Bar Chart)
   - Diet Recommendation Distribution (Pie Chart)

2. **Age Demographics** - Line chart showing diet recommendation trends across age groups

3. **BMI Analysis** - Heatmap displaying percentage distribution of diet recommendations within each BMI category

4. **Health Metrics** - Interactive 4-panel box plots showing:
   - BMI Distribution by Diet Type
   - Cholesterol Levels by Diet Type
   - Blood Sugar Levels by Diet Type
   - Daily Steps by Diet Type

5. **Chronic Conditions** - Stacked bar chart showing diet recommendation percentages within each chronic disease group

6. **Interactive Scatter Plots** - 4-panel scatter plot analysis showing:
   - Age vs BMI by Chronic Disease Status
   - Exercise Frequency vs BMI by Diet Recommendation
   - Cholesterol vs Blood Sugar by BMI Category
   - Daily Steps vs Sleep Hours by Age Group

### 🔄 Real-time Interactivity

- **Dynamic Filtering**: All charts update instantly when filters change
- **Smart Data Handling**: Graceful handling of empty filter results
- **Export Functionality**: Download filtered datasets as CSV
- **Professional Styling**: Consistent healthcare-appropriate design
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Performance Optimized**: Handles 4,355 patient records smoothly

### 📈 Key Analytics Features

- **Statistical Significance Testing**: Chi-square tests with p-values
- **Correlation Analysis**: BMI relationships with health metrics
- **Percentage Calculations**: Within-group distributions
- **Trend Analysis**: Diet recommendations across demographics
- **Clinical Insights**: Evidence-based recommendations
- **Data Validation**: Real-time patient count updates

All visualizations use the professional healthcare color scheme and are fully interactive with the comprehensive filter system.
## Quick R
eference

### 🚀 **Getting Started**
```bash
# Clone and setup
git clone <repository-url>
cd OKComputer_Python

# Option 1: One command (recommended)
chmod +x run_dashboard.sh && ./run_dashboard.sh

# Option 2: Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python test_setup.py  # Verify setup
python dashboard_app.py

# Open http://localhost:8052
```

### 🔍 **Filter Examples**
- **Single Patient**: `P00001`
- **Patient Group**: `P001` (gets ~93 patients)
- **Number Pattern**: `123` (finds all IDs with 123)
- **Age Range**: Slide to 25-45 years
- **BMI Range**: Slide to 18.5-25 (normal weight)

### 📊 **Navigation Guide**
1. **Executive Summary** → Key insights and statistics
2. **Population Overview** → 4-panel demographic analysis  
3. **Age Demographics** → Diet trends by age
4. **BMI Analysis** → Heatmap of recommendations
5. **Health Metrics** → Box plots by diet type
6. **Chronic Conditions** → Disease-diet relationships
7. **Diet Recommendations** → Comprehensive meal plan analysis
8. **Statistical Analysis** → Correlation and significance tests
9. **Data Export** → Download filtered results

### 🎯 **Key Features**
- ✅ **4,355 real patient records** with 32 health variables
- ✅ **Real-time filtering** with horizontal filter bar
- ✅ **Professional healthcare design** with appropriate colors
- ✅ **Statistical validation** with p-values and correlations
- ✅ **Export functionality** for filtered datasets
- ✅ **Responsive design** for all devices
- ✅ **No R dependencies** - pure Python implementation

---

**🏥 Ready for healthcare analytics? Start exploring at http://localhost:8052**
##
 Project Status

### ✅ **Production Ready**
- **Fully Functional**: All features tested and working
- **Complete Documentation**: Setup, usage, and troubleshooting guides
- **Professional Design**: Healthcare-appropriate color scheme and layout
- **Real Data**: 4,355 patient records with 32 health variables
- **Performance Optimized**: Handles large datasets smoothly

### 🔄 **Recent Updates**
- ✅ Converted from R Shiny to Python Dash
- ✅ Added horizontal filter bar with real-time updates
- ✅ Implemented 9 specialized analysis tabs
- ✅ Enhanced with professional healthcare color scheme
- ✅ Added comprehensive export functionality
- ✅ Optimized for performance and usability

### 📊 **Analytics Capabilities**
- **Statistical Analysis**: Chi-square tests, correlations, p-values
- **Demographic Analysis**: Age, gender, BMI distributions
- **Health Metrics**: Blood pressure, cholesterol, blood sugar analysis
- **Diet Recommendations**: Evidence-based meal plan analysis
- **Interactive Filtering**: Real-time data exploration
- **Export Functions**: CSV download of filtered datasets

---

**🎯 This dashboard is ready for healthcare analytics and research applications.**