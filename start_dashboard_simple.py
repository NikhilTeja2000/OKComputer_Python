#!/usr/bin/env python3
"""
Simple launcher for the Personalized Diet Analytics Dashboard
"""

import sys
import os

def main():
    print("=" * 60)
    print("Personalized Diet Analytics Dashboard")
    print("=" * 60)
    print("Loading data and starting server...")
    print("Dashboard will be available at: http://localhost:8050")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Import and run the dashboard
    try:
        from dashboard_app import app
        app.run(debug=True, host='0.0.0.0', port=8050)
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    except ImportError as e:
        print(f"Missing dependencies. Please install requirements: pip install -r requirements.txt")
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error starting dashboard: {e}")

if __name__ == '__main__':
    main()