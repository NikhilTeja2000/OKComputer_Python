#!/usr/bin/env python3
"""
Personalized Diet Analytics Dashboard - Startup Script
This script provides an easy way to start the dashboard with various options.
"""

import os
import sys
import subprocess
import argparse
import webbrowser
import time
import platform

def check_python_dependencies():
    """Check if required Python packages are installed"""
    try:
        import flask
        import psutil
        print("✓ Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing Python dependency: {e}")
        print("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✓ Python dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install Python dependencies")
            return False

def check_r_installation():
    """Check if R is installed and available"""
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['where', 'R'], capture_output=True, text=True)
        else:
            result = subprocess.run(['which', 'R'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ R is installed")
            return True
        else:
            print("✗ R is not installed or not in PATH")
            return False
    except Exception as e:
        print(f"✗ Error checking R installation: {e}")
        return False

def check_r_packages():
    """Check if required R packages are installed"""
    r_app_path = os.path.join('..', 'OKComputer_R-Dashboard-App-main', 'test_setup.R')
    if not os.path.exists(r_app_path):
        print("✗ R test script not found")
        return False
    
    try:
        result = subprocess.run(['Rscript', r_app_path], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✓ R packages are installed")
            return True
        else:
            print("✗ R packages are not installed or test failed")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ R package check timed out")
        return False
    except Exception as e:
        print(f"✗ Error checking R packages: {e}")
        return False

def install_r_packages():
    """Install required R packages"""
    setup_script = os.path.join('..', 'OKComputer_R-Dashboard-App-main', 'setup.R')
    if not os.path.exists(setup_script):
        print("✗ R setup script not found")
        return False
    
    print("Installing R packages (this may take several minutes)...")
    try:
        result = subprocess.run(['Rscript', setup_script], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ R packages installed successfully")
            return True
        else:
            print("✗ Failed to install R packages")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error installing R packages: {e}")
        return False

def start_r_shiny_direct(port=3838):
    """Start the R Shiny application directly"""
    r_app_path = os.path.join('..', 'OKComputer_R-Dashboard-App-main', 'app.R')
    if not os.path.exists(r_app_path):
        print("✗ R Shiny app file not found")
        return False
    
    print(f"Starting R Shiny dashboard on port {port}...")
    try:
        cmd = ['Rscript', '-e', f'shiny::runApp("{r_app_path}", port={port}, launch.browser=TRUE, host="0.0.0.0")']
        subprocess.Popen(cmd)
        print(f"✓ R Shiny dashboard started")
        print(f"Dashboard will open in your browser at http://localhost:{port}")
        return True
    except Exception as e:
        print(f"✗ Error starting R Shiny dashboard: {e}")
        return False

def start_web_interface(port=5000):
    """Start the Python web interface"""
    print(f"Starting web interface on port {port}...")
    try:
        subprocess.Popen([sys.executable, 'app.py'])
        print(f"✓ Web interface started")
        print(f"Access the dashboard manager at http://localhost:{port}")
        return True
    except Exception as e:
        print(f"✗ Error starting web interface: {e}")
        return False

def show_help():
    """Show help information"""
    print("""
Personalized Diet Analytics Dashboard - Startup Script

Usage: python start_dashboard.py [OPTIONS]

Options:
    --web-only          Start only the web interface
    --r-only            Start only the R Shiny dashboard directly
    --install           Install R packages and exit
    --check             Check system requirements and exit
    --port PORT         Specify port for web interface (default: 5000)
    --r-port PORT       Specify port for R Shiny app (default: 3838)
    --no-browser        Don't open browser automatically
    --help              Show this help message

Examples:
    python start_dashboard.py              # Start everything with checks
    python start_dashboard.py --web-only   # Start only web interface
    python start_dashboard.py --r-only     # Start R Shiny directly
    python start_dashboard.py --install    # Install packages only
    python start_dashboard.py --check      # Check requirements only
    """)

def main():
    parser = argparse.ArgumentParser(description='Start the Personalized Diet Analytics Dashboard')
    parser.add_argument('--web-only', action='store_true', help='Start only the web interface')
    parser.add_argument('--r-only', action='store_true', help='Start only the R Shiny dashboard directly')
    parser.add_argument('--install', action='store_true', help='Install R packages and exit')
    parser.add_argument('--check', action='store_true', help='Check system requirements and exit')
    parser.add_argument('--port', type=int, default=5000, help='Port for web interface (default: 5000)')
    parser.add_argument('--r-port', type=int, default=3838, help='Port for R Shiny app (default: 3838)')
    parser.add_argument('--no-browser', action='store_true', help='Don\'t open browser automatically')
    parser.add_argument('--help', action='store_true', help='Show help message')
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
        return
    
    print("=" * 60)
    print("Personalized Diet Analytics Dashboard - Startup Script")
    print("=" * 60)
    
    # Check Python dependencies first
    if not check_python_dependencies():
        print("✗ Cannot continue without Python dependencies")
        sys.exit(1)
    
    # Check R installation
    r_installed = check_r_installation()
    if not r_installed and not args.web_only:
        print("⚠ R is not installed. Some features may not work.")
        print("Please install R from https://cran.r-project.org/")
    
    # Check R packages if R is installed
    packages_installed = False
    if r_installed:
        packages_installed = check_r_packages()
        if not packages_installed:
            print("⚠ R packages are not installed.")
    
    # Handle different modes
    if args.check:
        print("\nSystem check complete.")
        if r_installed and packages_installed:
            print("✓ System is ready to run the dashboard!")
        else:
            print("⚠ Some requirements are missing. Use --install to fix.")
        return
    
    if args.install:
        if not r_installed:
            print("✗ Cannot install packages: R is not installed")
            sys.exit(1)
        
        if install_r_packages():
            print("✓ Installation complete!")
        else:
            print("✗ Installation failed!")
            sys.exit(1)
        return
    
    if args.r_only:
        if not r_installed:
            print("✗ Cannot start R Shiny: R is not installed")
            sys.exit(1)
        
        if not packages_installed:
            print("⚠ R packages not installed. Installing now...")
            if not install_r_packages():
                print("✗ Failed to install packages")
                sys.exit(1)
        
        start_r_shiny_direct(args.r_port)
        print("\nPress Ctrl+C to stop the dashboard")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping dashboard...")
        return
    
    # Default mode: start web interface (and R Shiny if available)
    print("\nStarting dashboard in web interface mode...")
    
    # Start web interface
    if not start_web_interface(args.port):
        print("✗ Failed to start web interface")
        sys.exit(1)
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    # Open browser if not disabled
    if not args.no_browser:
        webbrowser.open(f'http://localhost:{args.port}')
    
    print("\nDashboard manager is running!")
    print("Use the web interface to control the R Shiny dashboard")
    print("\nPress Ctrl+C to stop the web interface")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping web interface...")

if __name__ == '__main__':
    main()