"""
Utility modules for BrightData API filtering and analysis.

This package contains core functionality for data filtering, analysis, and strategy development
using the BrightData API across multiple datasets.
"""

from .brightdata_filter import (
    BrightDataFilter,
    FilterOperator,
    LogicalOperator,
    FilterCondition,
    FilterGroup,
    export_filter_to_json,
    load_filter_from_json,
    analyze_filter_results
)


from .config import (
    ConfigManager,
    config_manager,
    get_secret,
    get_config,
    get_brightdata_api_key,
    validate_required_secrets
)

from .filter_criteria import (
    FilterFields,
    DatasetFilterFields,
    AMAZON_FIELDS,
    AMAZON_WALMART_FIELDS,
    SHOPEE_FIELDS,
    # Direct callable fields (backward compatibility)
    TITLE, ASIN, BRAND, DESCRIPTION, CATEGORIES,
    INITIAL_PRICE, FINAL_PRICE, CURRENCY, DISCOUNT,
    RATING, REVIEWS_COUNT, AVAILABILITY, DELIVERY, IS_AVAILABLE,
    SELLER_NAME, BUYBOX_SELLER, NUMBER_OF_SELLERS,
    BS_RANK, ROOT_BS_RANK, DEPARTMENT, ITEM_WEIGHT,
    PRODUCT_DIMENSIONS, MODEL_NUMBER, MANUFACTURER, UPC
)

from .dataset_registry import (
    dataset_registry,
    get_dataset_schema,
    list_available_datasets,
    get_field_reference,
    validate_field_operator,
    get_dataset_id,
    list_dataset_names
)

__all__ = [
    'BrightDataFilter',
    'FilterOperator', 
    'LogicalOperator',
    'FilterCondition',
    'FilterGroup',
    'export_filter_to_json',
    'load_filter_from_json',
    'analyze_filter_results',
    'ConfigManager',
    'config_manager',
    'get_secret',
    'get_config',
    'get_brightdata_api_key',
    'validate_required_secrets',
    'FilterFields',
    'DatasetFilterFields',
    'AMAZON_FIELDS',
    'AMAZON_WALMART_FIELDS',
    'SHOPEE_FIELDS',
    'dataset_registry',
    'get_dataset_schema',
    'list_available_datasets',
    'get_field_reference',
    'validate_field_operator',
    'get_dataset_id',
    'list_dataset_names',
    'list_datasets_comprehensive',
    # Direct callable fields (backward compatibility)
    'TITLE', 'ASIN', 'BRAND', 'DESCRIPTION', 'CATEGORIES',
    'INITIAL_PRICE', 'FINAL_PRICE', 'CURRENCY', 'DISCOUNT',
    'RATING', 'REVIEWS_COUNT', 'AVAILABILITY', 'DELIVERY', 'IS_AVAILABLE',
    'SELLER_NAME', 'BUYBOX_SELLER', 'NUMBER_OF_SELLERS',
    'BS_RANK', 'ROOT_BS_RANK', 'DEPARTMENT', 'ITEM_WEIGHT',
    'PRODUCT_DIMENSIONS', 'MODEL_NUMBER', 'MANUFACTURER', 'UPC'
]
