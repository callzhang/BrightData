"""
Import utility for notebooks in the amazon/ directory.
This handles the path setup to import from the parent directory's util package.
"""

import sys
from pathlib import Path

def setup_util_imports():
    """Set up the Python path to import from the util package."""
    # Get the current file's directory (amazon/)
    current_dir = Path(__file__).parent
    
    # Get the parent directory (project root)
    project_root = current_dir.parent
    
    # Add project root to Python path if not already there
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    return project_root

# Automatically set up imports when this module is imported
project_root = setup_util_imports()

# Now import everything from util
from util import (
    AmazonProductFilter,
    WalmartInsightsFilter,
    FilterOperator,
    LogicalOperator,
    FilterCondition,
    FilterGroup,
    create_walmart_strategy_filters,
    export_filter_to_json,
    load_filter_from_json,
    analyze_filter_results,
    get_brightdata_api_key,
    get_secret,
    validate_required_secrets,
    FilterFields,
    # Direct callable fields
    TITLE, ASIN, BRAND, DESCRIPTION, CATEGORIES,
    INITIAL_PRICE, FINAL_PRICE, CURRENCY, DISCOUNT,
    RATING, REVIEWS_COUNT, AVAILABILITY, DELIVERY, IS_AVAILABLE,
    SELLER_NAME, BUYBOX_SELLER, NUMBER_OF_SELLERS,
    BS_RANK, ROOT_BS_RANK, DEPARTMENT, ITEM_WEIGHT,
    PRODUCT_DIMENSIONS, MODEL_NUMBER, MANUFACTURER, UPC
)

print("✅ Successfully imported all modules from util package")
print(f"📁 Project root: {project_root}")
print(f"🐍 Python path includes: {[p for p in sys.path if 'walmart insights' in p]}")

# Test that the imports work
print("\n🧪 Testing imports:")
print(f"  FilterFields.RATING = {FilterFields.RATING}")
print(f"  RATING = {RATING}")
print(f"  FilterOperator.EQUAL = {FilterOperator.EQUAL.value}")
print(f"  Available fields: {FilterFields.get_field_count()}")
print("✅ All imports working correctly!")
