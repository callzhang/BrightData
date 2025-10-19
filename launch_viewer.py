#!/usr/bin/env python3
"""
Launch script for the BrightData Snapshot Viewer
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Launching BrightData Manager...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("data/snapshots").exists():
        print("❌ data/snapshots directory not found!")
        print("💡 Make sure you're running this from the project root directory.")
        print("💡 The snapshots have been moved to data/snapshots/ during cleanup.")
        return
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_ui.txt"])
            print("✅ Requirements installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            return
    
    # Launch the app
    print("🌐 Starting multi-page web interface...")
    print("📱 The app will open in your default browser")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    print("📋 Available pages:")
    print("   • Query Builder - Create and submit data queries")
    print("   • Snapshot Viewer - View and analyze downloaded data")
    print("   • Settings - Manage API credentials and configuration")
    print()
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 BrightData Manager stopped")

if __name__ == "__main__":
    main()

