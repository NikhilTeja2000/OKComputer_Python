#!/usr/bin/env python3
"""
Personalized Diet Analytics Dashboard - Python Wrapper
This Flask application provides a web interface to manage and run the R Shiny dashboard.
"""

import os
import subprocess
import json
import time
from flask import Flask, render_template, jsonify, request, send_file
from threading import Thread
import psutil

app = Flask(__name__)

# Configuration
R_APP_PATH = os.path.join(os.path.dirname(__file__), '..', 'OKComputer_R-Dashboard-App-main', 'app.R')
SETUP_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'OKComputer_R-Dashboard-App-main', 'setup.R')
TEST_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'OKComputer_R-Dashboard-App-main', 'test_setup.R')

# Global variables to track R Shiny process
r_process = None
r_process_info = {
    'is_running': False,
    'port': None,
    'pid': None,
    'status': 'Stopped',
    'last_error': None
}

def check_r_installation():
    """Check if R is installed and available"""
    try:
        result = subprocess.run(['which', 'R'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_r_packages():
    """Check if required R packages are installed"""
    try:
        test_cmd = ['Rscript', TEST_SCRIPT_PATH]
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except:
        return False

def install_r_packages():
    """Install required R packages"""
    try:
        install_cmd = ['Rscript', SETUP_SCRIPT_PATH]
        result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=300)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def start_r_shiny_app(port=3838):
    """Start the R Shiny application"""
    global r_process, r_process_info
    
    try:
        # Check if R is installed
        if not check_r_installation():
            r_process_info['last_error'] = "R is not installed. Please install R first."
            return False
        
        # Check if packages are installed
        if not check_r_packages():
            r_process_info['last_error'] = "Required R packages are not installed."
            return False
        
        # Start the R Shiny app
        cmd = ['Rscript', '-e', f'shiny::runApp("{R_APP_PATH}", port={port}, launch.browser=FALSE, host="0.0.0.0")']
        r_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment to see if it starts successfully
        time.sleep(3)
        
        if r_process.poll() is None:
            r_process_info.update({
                'is_running': True,
                'port': port,
                'pid': r_process.pid,
                'status': 'Running',
                'last_error': None
            })
            return True
        else:
            stdout, stderr = r_process.communicate()
            r_process_info.update({
                'last_error': f"Failed to start R Shiny app: {stderr.decode('utf-8')}"
            })
            return False
            
    except Exception as e:
        r_process_info['last_error'] = f"Exception starting R Shiny app: {str(e)}"
        return False

def stop_r_shiny_app():
    """Stop the R Shiny application"""
    global r_process, r_process_info
    
    try:
        if r_process and r_process.poll() is None:
            # Try to terminate gracefully
            r_process.terminate()
            try:
                r_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate
                r_process.kill()
                r_process.wait()
        
        r_process_info.update({
            'is_running': False,
            'port': None,
            'pid': None,
            'status': 'Stopped',
            'last_error': None
        })
        
        return True
    except Exception as e:
        r_process_info['last_error'] = f"Error stopping R Shiny app: {str(e)}"
        return False

@app.route('/')
def index():
    """Main dashboard interface"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """Get the current status of the R Shiny application"""
    return jsonify(r_process_info)

@app.route('/api/start', methods=['POST'])
def start_app():
    """Start the R Shiny application"""
    global r_process_info
    
    if r_process_info['is_running']:
        return jsonify({'success': False, 'message': 'R Shiny app is already running'})
    
    port = request.json.get('port', 3838) if request.json else 3838
    
    # Start in a separate thread to avoid blocking
    def start_in_thread():
        start_r_shiny_app(port)
    
    thread = Thread(target=start_in_thread)
    thread.start()
    
    # Wait a moment and check status
    time.sleep(2)
    
    if r_process_info['is_running']:
        return jsonify({
            'success': True, 
            'message': f'R Shiny app started successfully on port {port}',
            'port': port,
            'pid': r_process_info['pid']
        })
    else:
        return jsonify({
            'success': False, 
            'message': 'Failed to start R Shiny app',
            'error': r_process_info.get('last_error', 'Unknown error')
        })

@app.route('/api/stop', methods=['POST'])
def stop_app():
    """Stop the R Shiny application"""
    if stop_r_shiny_app():
        return jsonify({'success': True, 'message': 'R Shiny app stopped successfully'})
    else:
        return jsonify({
            'success': False, 
            'message': 'Failed to stop R Shiny app',
            'error': r_process_info.get('last_error', 'Unknown error')
        })

@app.route('/api/install', methods=['POST'])
def install_packages():
    """Install required R packages"""
    try:
        success, stdout, stderr = install_r_packages()
        if success:
            return jsonify({
                'success': True, 
                'message': 'R packages installed successfully',
                'output': stdout
            })
        else:
            return jsonify({
                'success': False, 
                'message': 'Failed to install some R packages',
                'output': stdout,
                'error': stderr
            })
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': 'Exception during package installation',
            'error': str(e)
        })

@app.route('/api/check')
def check_environment():
    """Check if the environment is ready"""
    r_installed = check_r_installation()
    packages_installed = check_r_packages() if r_installed else False
    
    return jsonify({
        'r_installed': r_installed,
        'packages_installed': packages_installed,
        'ready': r_installed and packages_installed,
        'app_path_exists': os.path.exists(R_APP_PATH),
        'setup_path_exists': os.path.exists(SETUP_SCRIPT_PATH)
    })

@app.route('/api/app-url')
def get_app_url():
    """Get the URL of the running R Shiny application"""
    if r_process_info['is_running'] and r_process_info['port']:
        return jsonify({
            'url': f'http://localhost:{r_process_info["port"]}',
            'is_running': True
        })
    else:
        return jsonify({
            'url': None,
            'is_running': False,
            'message': 'R Shiny app is not running'
        })

@app.route('/api/logs')
def get_logs():
    """Get recent logs from the R Shiny application"""
    # This would need to be implemented to capture stdout/stderr
    return jsonify({
        'logs': ['Log functionality to be implemented'],
        'last_error': r_process_info.get('last_error', None)
    })

@app.route('/download/data')
def download_data():
    """Download the processed diet data"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'OKComputer_R-Dashboard-App-main', 'processed_diet_data.csv')
    if os.path.exists(data_path):
        return send_file(data_path, as_attachment=True, download_name='diet_analytics_data.csv')
    else:
        return jsonify({'error': 'Data file not found'}), 404

if __name__ == '__main__':
    # Check if R app files exist
    if not os.path.exists(R_APP_PATH):
        print(f"Warning: R app file not found at {R_APP_PATH}")
    if not os.path.exists(SETUP_SCRIPT_PATH):
        print(f"Warning: Setup script not found at {SETUP_SCRIPT_PATH}")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)