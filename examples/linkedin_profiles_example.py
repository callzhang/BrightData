#!/usr/bin/env python3
"""
LinkedIn Profiles Dataset - Example Queries

This script demonstrates various use cases for LinkedIn profiles data
using the actual BrightData LinkedIn dataset with 42 fields.

Author: BrightData Manager Team
Date: 2025-01-17
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from util import BrightDataFilter
from util.dataset_registry import dataset_registry
from util.brightdata import FilterCondition, FilterGroup, FilterOperator, LogicalOperator

def example_talent_acquisition():
    """Example: Find qualified candidates for software engineering roles"""
    print("🎯 Example: Talent Acquisition - Software Engineers")
    print("=" * 60)
    
    # Initialize the LinkedIn dataset
    filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
    
    # Define filters for software engineers
    filter_group = FilterGroup(
        operator=LogicalOperator.AND,
        filters=[
            FilterCondition("position", FilterOperator.INCLUDES, "Software Engineer"),
            FilterCondition("city", FilterOperator.INCLUDES, "San Francisco"),
            FilterCondition("connections", FilterOperator.GREATER_THAN_EQUAL, 100),
            FilterCondition("followers", FilterOperator.GREATER_THAN_EQUAL, 50)
        ]
    )
    
    # Submit the query
    result = filter_obj.search_data(
        filter_obj=filter_group,
        records_limit=500,
        title="SF Software Engineers"
    )
    
    print(f"✅ Query submitted successfully!")
    print(f"📊 Snapshot ID: {result}")
    print(f"🎯 Target: Software Engineers in SF with good network")
    print(f"📈 Expected records: ~500 profiles")

def example_market_research():
    """Example: Analyze tech skills and market trends"""
    print("\n📊 Example: Market Research - Tech Skills Analysis")
    print("=" * 60)
    
    filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
    
    # Research tech professionals with specific skills
    filter_group = FilterGroup(
        operator=LogicalOperator.AND,
        filters=[
            FilterCondition("position", FilterOperator.INCLUDES, "Data Scientist"),
            FilterCondition("city", FilterOperator.INCLUDES, "New York"),
            FilterCondition("connections", FilterOperator.GREATER_THAN_EQUAL, 200),
            FilterCondition("certifications", FilterOperator.INCLUDES, "AWS")
        ]
    )
    
    result = filter_obj.search_data(
        filter_obj=filter_group,
        records_limit=1000,
        title="NYC Data Scientists with Certifications"
    )
    
    print(f"✅ Query submitted successfully!")
    print(f"📊 Snapshot ID: {result}")
    print(f"🎯 Target: Data Scientists in NYC with certifications")
    print(f"📈 Expected records: ~1000 profiles")

def example_sales_prospecting():
    """Example: Find healthcare decision makers"""
    print("\n💼 Example: Sales Prospecting - Healthcare Decision Makers")
    print("=" * 60)
    
    filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
    
    # Target healthcare professionals in leadership roles
    filter_group = FilterGroup(
        operator=LogicalOperator.AND,
        filters=[
            FilterCondition("position", FilterOperator.INCLUDES, "Director"),
            FilterCondition("current_company_name", FilterOperator.INCLUDES, "Health"),
            FilterCondition("city", FilterOperator.INCLUDES, "Boston"),
            FilterCondition("connections", FilterOperator.GREATER_THAN_EQUAL, 300)
        ]
    )
    
    result = filter_obj.search_data(
        filter_obj=filter_group,
        records_limit=300,
        title="Boston Healthcare Directors"
    )
    
    print(f"✅ Query submitted successfully!")
    print(f"📊 Snapshot ID: {result}")
    print(f"🎯 Target: Healthcare Directors in Boston")
    print(f"📈 Expected records: ~300 profiles")

def example_university_alumni():
    """Example: Find university alumni networks"""
    print("\n🎓 Example: University Alumni Network")
    print("=" * 60)
    
    filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
    
    # Target Stanford alumni in tech
    filter_group = FilterGroup(
        operator=LogicalOperator.AND,
        filters=[
            FilterCondition("education", FilterOperator.INCLUDES, "Stanford"),
            FilterCondition("position", FilterOperator.INCLUDES, "Engineer"),
            FilterCondition("city", FilterOperator.INCLUDES, "Palo Alto"),
            FilterCondition("connections", FilterOperator.GREATER_THAN_EQUAL, 500)
        ]
    )
    
    result = filter_obj.search_data(
        filter_obj=filter_group,
        records_limit=200,
        title="Stanford Alumni Engineers"
    )
    
    print(f"✅ Query submitted successfully!")
    print(f"📊 Snapshot ID: {result}")
    print(f"🎯 Target: Stanford alumni engineers in Palo Alto")
    print(f"📈 Expected records: ~200 profiles")

def example_remote_work_analysis():
    """Example: Analyze remote work trends"""
    print("\n🏠 Example: Remote Work Trends Analysis")
    print("=" * 60)
    
    filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
    
    # Target remote workers and digital nomads
    filter_group = FilterGroup(
        operator=LogicalOperator.AND,
        filters=[
            FilterCondition("position", FilterOperator.INCLUDES, "Remote"),
            FilterCondition("connections", FilterOperator.GREATER_THAN_EQUAL, 200),
            FilterCondition("followers", FilterOperator.GREATER_THAN_EQUAL, 100)
        ]
    )
    
    result = filter_obj.search_data(
        filter_obj=filter_group,
        records_limit=400,
        title="Remote Work Professionals"
    )
    
    print(f"✅ Query submitted successfully!")
    print(f"📊 Snapshot ID: {result}")
    print(f"🎯 Target: Remote work professionals")
    print(f"📈 Expected records: ~400 profiles")

def example_skills_gap_analysis():
    """Example: Analyze skills gaps in data science"""
    print("\n🔍 Example: Skills Gap Analysis - Data Scientists")
    print("=" * 60)
    
    filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
    
    # Target data scientists with specific skills
    filter_group = FilterGroup(
        operator=LogicalOperator.AND,
        filters=[
            FilterCondition("position", FilterOperator.INCLUDES, "Data Scientist"),
            FilterCondition("certifications", FilterOperator.INCLUDES, "AWS"),
            FilterCondition("city", FilterOperator.INCLUDES, "Seattle"),
            FilterCondition("connections", FilterOperator.GREATER_THAN_EQUAL, 150)
        ]
    )
    
    result = filter_obj.search_data(
        filter_obj=filter_group,
        records_limit=600,
        title="Seattle Data Scientists with Certifications"
    )
    
    print(f"✅ Query submitted successfully!")
    print(f"📊 Snapshot ID: {result}")
    print(f"🎯 Target: Data Scientists in Seattle with certifications")
    print(f"📈 Expected records: ~600 profiles")

def example_competitive_intelligence():
    """Example: Competitive intelligence on tech companies"""
    print("\n🏢 Example: Competitive Intelligence - Tech Companies")
    print("=" * 60)
    
    filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
    
    # Target Google employees
    filter_group = FilterGroup(
        operator=LogicalOperator.AND,
        filters=[
            FilterCondition("current_company_name", FilterOperator.INCLUDES, "Google"),
            FilterCondition("position", FilterOperator.INCLUDES, "Manager"),
            FilterCondition("city", FilterOperator.INCLUDES, "Mountain View"),
            FilterCondition("connections", FilterOperator.GREATER_THAN_EQUAL, 300)
        ]
    )
    
    result = filter_obj.search_data(
        filter_obj=filter_group,
        records_limit=150,
        title="Google Managers in Mountain View"
    )
    
    print(f"✅ Query submitted successfully!")
    print(f"📊 Snapshot ID: {result}")
    print(f"🎯 Target: Google managers in Mountain View")
    print(f"📈 Expected records: ~150 profiles")

def example_geographic_analysis():
    """Example: Geographic talent analysis"""
    print("\n🌍 Example: Geographic Talent Analysis")
    print("=" * 60)
    
    filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
    
    # Target tech professionals in Austin
    filter_group = FilterGroup(
        operator=LogicalOperator.AND,
        filters=[
            FilterCondition("position", FilterOperator.INCLUDES, "Engineer"),
            FilterCondition("city", FilterOperator.INCLUDES, "Austin"),
            FilterCondition("connections", FilterOperator.GREATER_THAN_EQUAL, 200),
            FilterCondition("followers", FilterOperator.GREATER_THAN_EQUAL, 100)
        ]
    )
    
    result = filter_obj.search_data(
        filter_obj=filter_group,
        records_limit=800,
        title="Austin Tech Engineers"
    )
    
    print(f"✅ Query submitted successfully!")
    print(f"📊 Snapshot ID: {result}")
    print(f"🎯 Target: Tech engineers in Austin")
    print(f"📈 Expected records: ~800 profiles")

def main():
    """Main function to run all examples"""
    print("🚀 LinkedIn Profiles Dataset - Example Queries")
    print("=" * 80)
    print("This script demonstrates various use cases for LinkedIn profiles data")
    print("Each example shows different filtering strategies and use cases")
    print("=" * 80)
    
    # Load dataset configuration
    try:
        linkedin_config = dataset_registry.get_dataset("gd_l1viktl72bvl7bjuj0")
        if linkedin_config:
            print(f"✅ Dataset configuration loaded: {linkedin_config.name}")
            print(f"📊 Available fields: {len(linkedin_config.fields)}")
            print(f"🔗 Dataset ID: {linkedin_config.dataset_id}")
        else:
            print("❌ LinkedIn dataset not found in registry")
            return
    except Exception as e:
        print(f"⚠️ Warning: Could not load dataset configuration: {e}")
        print("Proceeding with hardcoded dataset ID...")
    
    # Run examples
    try:
        example_talent_acquisition()
        example_market_research()
        example_sales_prospecting()
        example_university_alumni()
        example_remote_work_analysis()
        example_skills_gap_analysis()
        example_competitive_intelligence()
        example_geographic_analysis()
        
        print("\n" + "=" * 80)
        print("📋 SUMMARY")
        print("=" * 80)
        print("✅ Successfully submitted 8 queries")
        print("📊 Total estimated cost: $16.00")
        print("🎯 Use the Snapshot Viewer to monitor progress and download results")
        
        print("\n💡 Next steps:")
        print("1. Check the Snapshot Viewer for query status")
        print("2. Download results when ready")
        print("3. Analyze the data for your specific use case")
        print("4. Use insights for talent acquisition, market research, or sales")
        
    except Exception as e:
        print(f"❌ Error in example: {e}")

if __name__ == "__main__":
    main()