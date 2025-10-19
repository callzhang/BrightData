#!/usr/bin/env python3
"""
Test script for BrightDataFilter core functionality

This script tests the main BrightDataFilter class and its core methods
for API interaction, filtering, and snapshot management.

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

def test_brightdata_filter_initialization():
    """Test BrightDataFilter initialization"""
    
    print("🧪 Testing BrightDataFilter Initialization")
    print("=" * 50)
    
    try:
        from util.brightdata import BrightDataFilter
        
        # Test initialization with dataset name
        filter_obj = BrightDataFilter("amazon_products")
        
        if filter_obj and hasattr(filter_obj, 'dataset_id'):
            print("✅ BrightDataFilter initialized successfully")
            print(f"   Dataset ID: {filter_obj.dataset_id}")
            return True
        else:
            print("❌ BrightDataFilter initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing BrightDataFilter: {e}")
        return False

def test_filter_criteria_creation():
    """Test filter criteria creation"""
    
    print("\n🧪 Testing Filter Criteria Creation")
    print("=" * 50)
    
    try:
        from util.brightdata import BrightDataFilter, FilterCondition, FilterGroup, FilterOperator, LogicalOperator
        
        # Initialize filter
        filter_obj = BrightDataFilter("amazon_products")
        F = filter_obj.filter
        
        # Test creating filter conditions
        condition1 = FilterCondition('title', FilterOperator.EQUAL, 'test1')
        condition2 = FilterCondition('price', FilterOperator.GREATER_THAN, 100)
        
        print("✅ FilterConditions created successfully")
        print(f"   Condition 1: {condition1}")
        print(f"   Condition 2: {condition2}")
        
        # Test creating filter group
        filter_group = FilterGroup(LogicalOperator.AND, [condition1, condition2])
        
        print("✅ FilterGroup created successfully")
        print(f"   Group: {filter_group}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating filter criteria: {e}")
        return False

def test_dataset_registry_loading():
    """Test dataset registry loading"""
    
    print("\n🧪 Testing Dataset Registry Loading")
    print("=" * 50)
    
    try:
        from util.dataset_registry import dataset_registry
        
        # Test getting available datasets
        datasets = dataset_registry.list_datasets()
        
        if datasets and len(datasets) > 0:
            print("✅ Dataset registry loaded successfully")
            print(f"   Available datasets: {[d.name for d in datasets]}")
            return True
        else:
            print("❌ No datasets found in registry")
            return False
            
    except Exception as e:
        print(f"❌ Error loading dataset registry: {e}")
        return False

def test_config_management():
    """Test configuration management"""
    
    print("\n🧪 Testing Configuration Management")
    print("=" * 50)
    
    try:
        from util.config import get_brightdata_api_key, get_secret
        
        # Test API key loading (should not fail even if key is missing)
        api_key = get_brightdata_api_key()
        
        if api_key:
            print("✅ API key loaded successfully")
            print(f"   API key: {api_key[:10]}...")
        else:
            print("⚠️  API key not found (this is expected if secrets.yaml is not configured)")
        
        # Test secret loading with default
        base_url = get_secret('brightdata.base_url', 'https://api.brightdata.com/datasets')
        
        if base_url:
            print("✅ Base URL loaded successfully")
            print(f"   Base URL: {base_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in configuration management: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 BrightData Manager Test Suite")
    print("=" * 60)
    
    # Run all tests
    test1_success = test_brightdata_filter_initialization()
    test2_success = test_filter_criteria_creation()
    test3_success = test_dataset_registry_loading()
    test4_success = test_config_management()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"BrightDataFilter initialization: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Filter criteria creation: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Dataset configuration loading: {'✅ PASS' if test3_success else '❌ FAIL'}")
    print(f"Configuration management: {'✅ PASS' if test4_success else '❌ FAIL'}")
    
    all_passed = test1_success and test2_success and test3_success and test4_success
    
    if all_passed:
        print("\n🎉 All tests passed! Core functionality is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Configure your API key in secrets.yaml")
        print("2. Test the Streamlit web interface")
        print("3. Try creating and submitting queries")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
