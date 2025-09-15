"""
Multi-Dataset Usage Examples

This module demonstrates how to use the BrightData API filter system
with multiple datasets including Amazon Products and Amazon-Walmart Comparison.
"""

from util import (
    BrightDataFilter, 
    AMAZON_FIELDS as AF, 
    AMAZON_WALMART_FIELDS as AW,
    list_available_datasets,
    get_brightdata_api_key
)


def example_1_list_datasets():
    """Example 1: List all available datasets"""
    print("=== Available Datasets ===")
    datasets = BrightDataFilter.list_available_datasets()
    
    for dataset in datasets:
        print(f"• {dataset['name']}")
        print(f"  ID: {dataset['dataset_id']}")
        print(f"  Description: {dataset['description']}")
        print(f"  Fields: {dataset['field_count']}")
        print()


def example_2_amazon_products_filter():
    """Example 2: Filter Amazon Products dataset"""
    print("=== Amazon Products Filter ===")
    
    # Initialize filter for Amazon dataset
    api_key = get_brightdata_api_key()
    amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")
    
    # Create filter using Amazon-specific fields
    high_rated_electronics = (
        AF.rating >= 4.5 &
        AF.categories.includes("Electronics") &
        AF.final_price < 500 &
        AF.is_available.is_true()
    )
    
    print("Filter created for Amazon Products:")
    print(high_rated_electronics)
    print()
    
    # Get dataset info
    info = amazon_filter.get_dataset_info()
    print(f"Dataset: {info['name']}")
    print(f"Available fields: {len(info['available_fields'])}")
    print()


def example_3_amazon_walmart_comparison():
    """Example 3: Filter Amazon-Walmart Comparison dataset"""
    print("=== Amazon-Walmart Comparison Filter ===")
    
    # Initialize filter for Amazon-Walmart dataset
    api_key = get_brightdata_api_key()
    aw_filter = BrightDataFilter(api_key, "gd_m4l6s4mn2g2rkx9lia")
    
    # Create filter using Amazon-Walmart specific fields
    cross_platform_analysis = (
        AW.platform.in_list(["Amazon", "Walmart"]) &
        AW.rating >= 4.0 &
        AW.availability_match.is_true() &
        AW.price_difference_percentage > 10
    )
    
    print("Filter created for Amazon-Walmart Comparison:")
    print(cross_platform_analysis)
    print()
    
    # Get dataset info
    info = aw_filter.get_dataset_info()
    print(f"Dataset: {info['name']}")
    print(f"Available fields: {len(info['available_fields'])}")
    print()


def example_4_field_validation():
    """Example 4: Demonstrate field validation"""
    print("=== Field Validation ===")
    
    api_key = get_brightdata_api_key()
    
    # Test with Amazon dataset
    amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")
    
    try:
        # This should work - ASIN exists in Amazon dataset
        valid_filter = amazon_filter.create_filter("asin", "=", "B123456789")
        print("✓ Valid filter created for Amazon dataset")
    except ValueError as e:
        print(f"✗ Error: {e}")
    
    try:
        # This should fail - platform doesn't exist in Amazon dataset
        invalid_filter = amazon_filter.create_filter("platform", "=", "Amazon")
        print("✗ This should have failed!")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    print()


def example_5_dataset_specific_fields():
    """Example 5: Show dataset-specific field differences"""
    print("=== Dataset-Specific Fields ===")
    
    # Amazon-specific fields
    amazon_fields = AF.get_field_names()
    amazon_unique = [f for f in amazon_fields if f not in AW.get_field_names()]
    
    # Amazon-Walmart specific fields
    aw_fields = AW.get_field_names()
    aw_unique = [f for f in aw_fields if f not in amazon_fields]
    
    # Common fields
    common_fields = [f for f in amazon_fields if f in aw_fields]
    
    print(f"Amazon Products unique fields ({len(amazon_unique)}):")
    for field in amazon_unique:
        print(f"  • {field}")
    print()
    
    print(f"Amazon-Walmart unique fields ({len(aw_unique)}):")
    for field in aw_unique:
        print(f"  • {field}")
    print()
    
    print(f"Common fields ({len(common_fields)}):")
    for field in common_fields[:10]:  # Show first 10
        print(f"  • {field}")
    if len(common_fields) > 10:
        print(f"  ... and {len(common_fields) - 10} more")
    print()


def example_6_complex_cross_platform_analysis():
    """Example 6: Complex cross-platform analysis"""
    print("=== Complex Cross-Platform Analysis ===")
    
    api_key = get_brightdata_api_key()
    aw_filter = BrightDataFilter(api_key, "gd_m4l6s4mn2g2rkx9lia")
    
    # Find products where Amazon is significantly more expensive
    amazon_expensive = (
        AW.platform == "Amazon" &
        AW.price_difference > 0 &
        AW.price_difference_percentage > 20 &
        AW.availability_match.is_true() &
        AW.rating >= 4.0
    )
    
    # Find products where Walmart is more expensive
    walmart_expensive = (
        AW.platform == "Walmart" &
        AW.price_difference < 0 &
        AW.price_difference_percentage < -10 &
        AW.availability_match.is_true() &
        AW.rating >= 4.0
    )
    
    # Combine with OR
    price_analysis = amazon_expensive | walmart_expensive
    
    print("Cross-platform price analysis filter:")
    print(price_analysis)
    print()


def run_all_examples():
    """Run all examples"""
    try:
        example_1_list_datasets()
        example_2_amazon_products_filter()
        example_3_amazon_walmart_comparison()
        example_4_field_validation()
        example_5_dataset_specific_fields()
        example_6_complex_cross_platform_analysis()
        
        print("=== All Examples Completed Successfully! ===")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have a valid API key in secrets.yaml")


if __name__ == "__main__":
    run_all_examples()
