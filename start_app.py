#!/usr/bin/env python3
"""
Traffic Safety Analytics Dashboard - Startup Script
"""

import webbrowser
import time
import sys
import os

def main():
    print("🚗 Traffic Safety Analytics Dashboard")
    print("=" * 50)
    
    # Check if required packages are installed
    try:
        import flask
        import pandas
        import numpy
        import plotly
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return
    
    # Start the Flask application
    print("🚀 Starting Flask application...")
    
    # Import and run the main application
    try:
        from main import app
        print("✅ Flask application loaded successfully")
        print("🌐 Opening browser in 3 seconds...")
        print("📊 Dashboard will be available at: http://localhost:5000")
        
        # Open browser after a short delay
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return

if __name__ == "__main__":
    main() 