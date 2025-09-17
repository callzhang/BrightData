#!/usr/bin/env python3
"""
Example: Recent Good Selling Products Strategy

This example demonstrates how to use the new strategy for finding products that are:
1. Recently launched (less than 50 reviews on Amazon)
2. High sales volume (>100 last month)
3. Good quality (rating >= 4.0)
4. Not available on Walmart (opportunity)

This strategy helps identify emerging products before they become mainstream,
giving Walmart a competitive advantage in early-stage product adoption.

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

def main():
    """Demonstrate the Recent Good Selling Products Strategy"""
    
    print("🚀 Recent Good Selling Products Strategy Example")
    print("=" * 60)
    print()
    print("This strategy identifies products that are:")
    print("• Recently launched (less than 50 reviews)")
    print("• High sales volume (>100 last month)")
    print("• Good quality (rating >= 4.0)")
    print("• Not available on Walmart (opportunity)")
    print()
    
    # Initialize strategy queries
    strategy_queries = WalmartStrategyQueries()
    
    if not strategy_queries.brightdata_filter:
        print("❌ Error: Could not initialize BrightData filter")
        print("Please check your API key in secrets.yaml")
        return
    
    print("✅ BrightData filter initialized successfully")
    print()
    
    # Example 1: Default parameters
    print("📊 Example 1: Default Parameters")
    print("-" * 40)
    print("Parameters:")
    print("  • Max reviews: 50")
    print("  • Min sales: 100")
    print("  • Min rating: 4.0")
    print()
    
    snapshot_id_1 = strategy_queries.recent_good_selling_products()
    
    if snapshot_id_1 and not snapshot_id_1.startswith("Error"):
        print(f"✅ Query submitted successfully!")
        print(f"📋 Snapshot ID: {snapshot_id_1}")
        print()
    else:
        print(f"❌ Query failed: {snapshot_id_1}")
        return
    
    # Example 2: More restrictive parameters
    print("📊 Example 2: More Restrictive Parameters")
    print("-" * 40)
    print("Parameters:")
    print("  • Max reviews: 30")
    print("  • Min sales: 200")
    print("  • Min rating: 4.0")
    print()
    
    snapshot_id_2 = strategy_queries.recent_good_selling_products(max_reviews=30, min_sales=200)
    
    if snapshot_id_2 and not snapshot_id_2.startswith("Error"):
        print(f"✅ Query submitted successfully!")
        print(f"📋 Snapshot ID: {snapshot_id_2}")
        print()
    else:
        print(f"❌ Query failed: {snapshot_id_2}")
        return
    
    # Example 3: Very restrictive parameters for premium products
    print("📊 Example 3: Premium Product Focus")
    print("-" * 40)
    print("Parameters:")
    print("  • Max reviews: 20")
    print("  • Min sales: 500")
    print("  • Min rating: 4.5")
    print()
    
    snapshot_id_3 = strategy_queries.recent_good_selling_products(max_reviews=20, min_sales=500)
    
    if snapshot_id_3 and not snapshot_id_3.startswith("Error"):
        print(f"✅ Query submitted successfully!")
        print(f"📋 Snapshot ID: {snapshot_id_3}")
        print()
    else:
        print(f"❌ Query failed: {snapshot_id_3}")
        return
    
    # Summary
    print("📋 Summary of Generated Snapshots")
    print("=" * 40)
    print(f"1. Default parameters:     {snapshot_id_1}")
    print(f"2. Restrictive parameters: {snapshot_id_2}")
    print(f"3. Premium focus:          {snapshot_id_3}")
    print()
    
    print("🎯 Next Steps:")
    print("1. Download snapshot data using the snapshot IDs above")
    print("2. Analyze the results to identify specific products")
    print("3. Research suppliers and pricing for these products")
    print("4. Prioritize products based on:")
    print("   • Revenue potential")
    print("   • Supplier availability")
    print("   • Competitive landscape")
    print("   • Category fit")
    print("5. Add top products to Walmart's catalog")
    print()
    
    print("💡 Strategy Benefits:")
    print("• Early market entry for trending products")
    print("• Lower competition due to newness")
    print("• Higher margins on emerging products")
    print("• Brand partnership opportunities")
    print("• Customer acquisition through unique offerings")

if __name__ == "__main__":
    main()
