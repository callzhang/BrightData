#!/usr/bin/env python3
"""
Test script for the updated Competitive Intelligence Dashboard

This script tests the updated competitive intelligence dashboard that now includes
the Recent Good Selling Products Strategy as the second query instead of the old
"New Product Launches" query.

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

def test_competitive_intelligence_dashboard():
    """Test the updated competitive intelligence dashboard"""
    
    print("🧪 Testing Updated Competitive Intelligence Dashboard")
    print("=" * 60)
    
    # Initialize strategy queries
    strategy_queries = WalmartStrategyQueries()
    
    if not strategy_queries.brightdata_filter:
        print("❌ Error: Could not initialize BrightData filter")
        print("Please check your API key in secrets.yaml")
        return False
    
    print("✅ BrightData filter initialized successfully")
    print()
    
    # Test the competitive intelligence dashboard
    print("📊 Testing Competitive Intelligence Dashboard...")
    print("Expected queries:")
    print("1. Price Advantage Analysis")
    print("2. Recent Good Selling Products Strategy (NEW)")
    print("3. Stockout Opportunities")
    print()
    
    intelligence_queries = strategy_queries.competitive_intelligence_dashboard()
    
    if isinstance(intelligence_queries, dict) and "error" not in intelligence_queries:
        print("✅ Competitive Intelligence Dashboard executed successfully!")
        print()
        print("📋 Generated Queries:")
        
        for query_name, result in intelligence_queries.items():
            if isinstance(result, dict) and "snapshot_id" in result:
                snapshot_id = result["snapshot_id"]
                print(f"  • {query_name.replace('_', ' ').title()}: {snapshot_id}")
            else:
                print(f"  • {query_name.replace('_', ' ').title()}: {result}")
        
        print()
        
        # Verify the new query is present
        if "recent_good_selling" in intelligence_queries:
            print("✅ Recent Good Selling Products Strategy is included!")
        else:
            print("❌ Recent Good Selling Products Strategy is missing!")
            return False
        
        # Verify the old query is not present
        if "new_products" not in intelligence_queries:
            print("✅ Old 'New Product Launches' query has been replaced!")
        else:
            print("❌ Old 'New Product Launches' query still exists!")
            return False
        
        return True
    else:
        print(f"❌ Competitive Intelligence Dashboard failed: {intelligence_queries}")
        return False

def main():
    """Run the test"""
    
    print("🚀 Updated Competitive Intelligence Dashboard Test")
    print("=" * 60)
    
    success = test_competitive_intelligence_dashboard()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Updated dashboard test: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        print("\n🎉 Test passed! The Recent Good Selling Products Strategy")
        print("   has been successfully integrated into the Competitive")
        print("   Intelligence Dashboard as the second query.")
        print("\n📋 Next Steps:")
        print("1. Download the snapshot data using the provided snapshot IDs")
        print("2. Analyze the Recent Good Selling Products results")
        print("3. Compare with other intelligence queries")
        print("4. Implement strategic recommendations")
    else:
        print("\n⚠️  Test failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
