#!/usr/bin/env python3
"""
Test script for Streamlit application components

This script tests the multi-page Streamlit application structure
and key components without requiring a full Streamlit session.

Author: BrightData Manager Team
Date: 2025-01-17
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import util modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

def test_app_imports():
    """Test that all app components can be imported"""
    
    print("🧪 Testing Streamlit App Imports")
    print("=" * 50)
    
    try:
        # Test main app import
        import app
        print("✅ Main app.py imported successfully")
        
        # Test page imports (using importlib for numeric module names)
        import importlib.util
        
        # Test Query Builder page
        query_builder_path = parent_dir / "pages" / "1_Query_Builder.py"
        if query_builder_path.exists():
            spec = importlib.util.spec_from_file_location("query_builder", query_builder_path)
            query_builder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(query_builder)
            print("✅ Query Builder page imported successfully")
        else:
            print("❌ Query Builder page not found")
            return False
        
        # Test Snapshot Viewer page
        snapshot_viewer_path = parent_dir / "pages" / "2_Snapshot_Viewer.py"
        if snapshot_viewer_path.exists():
            spec = importlib.util.spec_from_file_location("snapshot_viewer", snapshot_viewer_path)
            snapshot_viewer = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(snapshot_viewer)
            print("✅ Snapshot Viewer page imported successfully")
        else:
            print("❌ Snapshot Viewer page not found")
            return False
        
        # Test Settings page
        settings_path = parent_dir / "pages" / "3_Settings.py"
        if settings_path.exists():
            spec = importlib.util.spec_from_file_location("settings", settings_path)
            settings = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings)
            print("✅ Settings page imported successfully")
        else:
            print("❌ Settings page not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing app components: {e}")
        return False

def test_launch_script():
    """Test launch script functionality"""
    
    print("\n🧪 Testing Launch Script")
    print("=" * 50)
    
    try:
        import launch_viewer
        
        # Check if launch script has main function
        if hasattr(launch_viewer, 'main'):
            print("✅ Launch script has main function")
        else:
            print("❌ Launch script missing main function")
            return False
        
        # Check if launch script has proper imports
        if hasattr(launch_viewer, 'subprocess'):
            print("✅ Launch script has subprocess import")
        else:
            print("❌ Launch script missing subprocess import")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing launch script: {e}")
        return False

def test_config_files():
    """Test configuration files exist and are valid"""
    
    print("\n🧪 Testing Configuration Files")
    print("=" * 50)
    
    try:
        # Test datasets.yaml
        datasets_config_path = parent_dir / "config" / "datasets.yaml"
        if datasets_config_path.exists():
            print("✅ datasets.yaml exists")
            
            # Try to load the YAML
            import yaml
            with open(datasets_config_path, 'r') as f:
                datasets_config = yaml.safe_load(f)
            
            if 'datasets' in datasets_config:
                print(f"✅ datasets.yaml contains {len(datasets_config['datasets'])} datasets")
            else:
                print("❌ datasets.yaml missing 'datasets' key")
                return False
        else:
            print("❌ datasets.yaml not found")
            return False
        
        # Test secrets.example.yaml
        secrets_example_path = parent_dir / "secrets.example.yaml"
        if secrets_example_path.exists():
            print("✅ secrets.example.yaml exists")
        else:
            print("❌ secrets.example.yaml not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing configuration files: {e}")
        return False

def test_requirements_files():
    """Test requirements files exist and are valid"""
    
    print("\n🧪 Testing Requirements Files")
    print("=" * 50)
    
    try:
        # Test requirements.txt
        requirements_path = parent_dir / "requirements.txt"
        if requirements_path.exists():
            print("✅ requirements.txt exists")
            
            # Check if it has basic dependencies
            with open(requirements_path, 'r') as f:
                content = f.read()
            
            if 'requests' in content and 'pyyaml' in content:
                print("✅ requirements.txt contains expected dependencies")
            else:
                print("❌ requirements.txt missing expected dependencies")
                return False
        else:
            print("❌ requirements.txt not found")
            return False
        
        # Test requirements_ui.txt
        requirements_ui_path = parent_dir / "requirements_ui.txt"
        if requirements_ui_path.exists():
            print("✅ requirements_ui.txt exists")
            
            # Check if it has Streamlit
            with open(requirements_ui_path, 'r') as f:
                content = f.read()
            
            if 'streamlit' in content:
                print("✅ requirements_ui.txt contains Streamlit")
            else:
                print("❌ requirements_ui.txt missing Streamlit")
                return False
        else:
            print("❌ requirements_ui.txt not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing requirements files: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 BrightData Manager Streamlit App Test Suite")
    print("=" * 60)
    
    # Run all tests
    test1_success = test_app_imports()
    test2_success = test_launch_script()
    test3_success = test_config_files()
    test4_success = test_requirements_files()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"App imports: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Launch script: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Configuration files: {'✅ PASS' if test3_success else '❌ FAIL'}")
    print(f"Requirements files: {'✅ PASS' if test4_success else '❌ FAIL'}")
    
    all_passed = test1_success and test2_success and test3_success and test4_success
    
    if all_passed:
        print("\n🎉 All tests passed! Streamlit app is properly configured.")
        print("\n📋 Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt -r requirements_ui.txt")
        print("2. Configure API key: cp secrets.example.yaml secrets.yaml")
        print("3. Launch the app: python launch_viewer.py")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
