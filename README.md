# Personalized Diet Analytics Dashboard - Python Implementation

This repository provides a Python-based analytics dashboard for personalized diet recommendations, converted from the original R Shiny application.

## Overview

This Python Dash application provides sophisticated analytics for personalized diet recommendations with:

- **9 comprehensive analysis tabs** covering health profiles, chronic conditions, lifestyle factors, and statistical validation
- **15+ interactive visualizations** using Plotly and Dash
- **Evidence-based insights** with statistical significance testing (p < 0.01 for BMI correlations)
- **BMI-driven recommendations** with balanced distribution across four major diet types

## Quick Start

### Option 1: Using the Shell Script (Recommended)

```bash
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

3. **Start the dashboard:**

   ```bash
   python dashboard_app.py
   ```

4. **Access the dashboard:**
   - Open your browser to `http://localhost:8050`
   - Navigate through the different analysis tabs

## Features

### Dashboard Features

- **Executive Summary**: BMI-driven recommendations with statistical validation
- **Health Profile Analysis**: Demographic distributions and risk factor correlations
- **Chronic Conditions**: Disease-diet relationship mapping
- **Lifestyle Integration**: Exercise, sleep, and behavioral factor analysis
- **Interactive Visualizations**: Sunburst charts, parallel coordinates, dynamic filtering
- **Statistical Validation**: Chi-square tests, correlation matrices, significance testing
- **Clinical Insights**: Evidence-based recommendations and findings
- **Data Download**: Export functionality for datasets

## System Requirements

### Minimum Requirements

- **Python 3.7+**
- **2GB RAM** minimum
- **500MB disk space** for packages and data

### Required Python Packages

- pandas, numpy, plotly, dash
- dash-bootstrap-components, scipy, scikit-learn
- flask (for alternative web interface)

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

1. **R Package Installation Fails**

   ```bash
   # Install packages manually
   R -e "install.packages(c('shiny', 'shinydashboard', 'tidyverse'), dependencies=TRUE)"
   ```

2. **Port Already in Use**

   ```bash
   # Use different port
   Rscript -e "shiny::runApp('app.R', port=3839)"
   ```

3. **Permission Issues**

   ```bash
   # Make scripts executable
   chmod +x setup.R test_setup.R
   ```

4. **Memory Issues**
   ```bash
   # Check available memory
   free -h
   # Close other applications if needed
   ```

### Getting Help

- **Check System Logs**: Use the web interface log viewer
- **Verify Installation**: Run `Rscript test_setup.R`
- **Check File Permissions**: Ensure app.R and data files are readable
- **Network Issues**: Verify firewall settings for ports 3838, 5000

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

1. **R Dashboard**: Modify `app.R` to add new analysis tabs
2. **Web Interface**: Update `app.py` and templates for new controls
3. **Data Processing**: Extend the dataset in `processed_diet_data.csv`

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

**Access the enhanced dashboard at: http://localhost:8052**

## Design & Color Scheme

### 🎨 Modern Color Palette
The dashboard features a vibrant, healthcare-inspired color scheme:

- **Primary Orange** (#FF8C00) - Bright, energetic headers and highlights
- **Coral Accents** (#FF6B35) - Warm secondary elements  
- **Fresh Teal** (#4ECDC4) - Cool balance and data points
- **Success Green** (#2ECC71) - Positive indicators and healthy metrics
- **Modern Blue** (#3498DB) - Information and navigation elements
- **Clean Whites** (#FFFFFF) - Pure backgrounds for clarity
- **Professional Dark** (#2C3E50) - Text and contrast elements

This palette provides excellent contrast, accessibility, and visual appeal while maintaining a professional healthcare aesthetic.