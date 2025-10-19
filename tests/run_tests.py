#!/usr/bin/env python3
"""
Main Test Runner for BrightData Manager

This script runs all tests for the BrightData Manager project.
Run this from the project root directory.

Author: BrightData Manager Team
Date: 2025-01-17
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_brightdata_filter_tests():
    """Run BrightDataFilter core functionality tests."""
    print("🧪 Running BrightDataFilter Core Tests...")
    try:
        from tests.test_brightdata_filter import main as run_brightdata_tests
        return run_brightdata_tests()
    except Exception as e:
        print(f"❌ Error running BrightDataFilter tests: {e}")
        return False

def run_streamlit_app_tests():
    """Run Streamlit application tests."""
    print("🧪 Running Streamlit App Tests...")
    try:
        from tests.test_streamlit_app import main as run_app_tests
        return run_app_tests()
    except Exception as e:
        print(f"❌ Error running Streamlit app tests: {e}")
        return False

def main():
    """Run all BrightData Manager tests."""
    print("🚀 BrightData Manager Test Suite")
    print("=" * 60)
    
    # Run core functionality tests
    print("\n🔧 Testing Core Functionality...")
    core_result = run_brightdata_filter_tests()
    
    # Run Streamlit app tests
    print("\n🖥️  Testing Streamlit Application...")
    app_result = run_streamlit_app_tests()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print(f"   Core Functionality: {'✅ PASSED' if core_result else '❌ FAILED'}")
    print(f"   Streamlit App: {'✅ PASSED' if app_result else '❌ FAILED'}")
    
    if core_result and app_result:
        print("\n🎉 All tests passed! BrightData Manager is ready to use.")
        print("\n📋 Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt -r requirements_ui.txt")
        print("2. Configure API key: cp secrets.example.yaml secrets.yaml")
        print("3. Launch the app: python launch_viewer.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit(main())
