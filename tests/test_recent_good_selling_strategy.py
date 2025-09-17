#!/usr/bin/env python3
"""
Test script for the Recent Good Selling Products Strategy

This script tests the new strategy for finding products with:
1. Less than 50 reviews on Amazon
2. High sales volume: > 100 last month
3. Good ratings (>= 4.0)
4. Not available on Walmart (opportunity)

Author: Derek
Date: 2025-01-16
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import util modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from walmart_strategy_queries import WalmartStrategyQueries

def test_recent_good_selling_strategy():
    """Test the recent good selling products strategy"""
    
    print("🧪 Testing Recent Good Selling Products Strategy")
    print("=" * 60)
    
    # Initialize strategy queries
    strategy_queries = WalmartStrategyQueries()
    
    if not strategy_queries.brightdata_filter:
        print("❌ Error: Could not initialize BrightData filter")
        print("Please check your API key in secrets.yaml")
        return False
    
    print("✅ BrightData filter initialized successfully")
    print()
    
    # Test with default parameters
    print("📊 Testing with default parameters:")
    print("   - Max reviews: 50")
    print("   - Min sales: 100")
    print("   - Min rating: 4.0")
    print()
    
    snapshot_id = strategy_queries.recent_good_selling_products()
    
    if snapshot_id and not snapshot_id.startswith("Error"):
        print(f"✅ Strategy executed successfully!")
        print(f"📋 Snapshot ID: {snapshot_id}")
        print()
        print("🎯 Strategy Details:")
        print("   - Target: Products with <50 reviews but >100 sales last month")
        print("   - Quality filter: Rating >= 4.0")
        print("   - Opportunity: Not available on Walmart")
        print("   - Records limit: 1000")
        return True
    else:
        print(f"❌ Strategy failed: {snapshot_id}")
        return False

def test_custom_parameters():
    """Test the strategy with custom parameters"""
    
    print("\n🔧 Testing with custom parameters:")
    print("   - Max reviews: 30")
    print("   - Min sales: 200")
    print("   - Min rating: 4.0")
    print()
    
    strategy_queries = WalmartStrategyQueries()
    
    if not strategy_queries.brightdata_filter:
        print("❌ Error: Could not initialize BrightData filter")
        return False
    
    snapshot_id = strategy_queries.recent_good_selling_products(max_reviews=30, min_sales=200)
    
    if snapshot_id and not snapshot_id.startswith("Error"):
        print(f"✅ Custom parameters test successful!")
        print(f"📋 Snapshot ID: {snapshot_id}")
        return True
    else:
        print(f"❌ Custom parameters test failed: {snapshot_id}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 Recent Good Selling Products Strategy Test Suite")
    print("=" * 60)
    
    # Test 1: Default parameters
    test1_success = test_recent_good_selling_strategy()
    
    # Test 2: Custom parameters
    test2_success = test_custom_parameters()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Default parameters test: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Custom parameters test: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! Strategy is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Download the snapshot data using the provided snapshot IDs")
        print("2. Analyze the results to identify specific products")
        print("3. Research suppliers and pricing for these products")
        print("4. Add these products to Walmart's catalog")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
    
    return test1_success and test2_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
