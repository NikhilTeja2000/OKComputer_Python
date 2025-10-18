#!/usr/bin/env python3
"""
Simple launcher for the Personalized Diet Analytics Dashboard
"""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("Personalized Diet Analytics Dashboard")
    print("=" * 60)
    print("Loading data and starting server...")
    
    # Change to the correct directory
    os.chdir('/mnt/okcomputer/output')
    
    # Run the dashboard
    try:
        subprocess.run([sys.executable, 'dashboard_app.py'])
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()