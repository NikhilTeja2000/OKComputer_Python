#!/usr/bin/env python3
"""
Simple HTTP server to serve the dashboard files
This allows accessing the dashboard through a web interface
"""

import http.server
import socketserver
import threading
import webbrowser
import time
import os

PORT = 8000

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    """Start the HTTP server"""
    os.chdir('/mnt/okcomputer/output')
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Serving dashboard at http://localhost:{PORT}")
        httpd.serve_forever()

def main():
    print("=" * 60)
    print("Personalized Diet Analytics Dashboard - HTTP Server")
    print("=" * 60)
    
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait a moment for server to start
    time.sleep(2)
    
    print(f"\nDashboard is now accessible at:")
    print(f"  http://localhost:{PORT}")
    print(f"  http://0.0.0.0:{PORT}")
    
    print("\nFiles available:")
    print(f"  /dashboard_app.py - Main working dashboard")
    print(f"  /working_dashboard.html - Dashboard landing page")
    print(f"  /index.html - Main interface")
    print(f"  /processed_diet_data.csv - Complete dataset")
    
    print("\nPress Ctrl+C to stop the server")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")

if __name__ == '__main__':
    main()