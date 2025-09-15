# BrightData API Filter Syntax Documentation

This project provides a comprehensive Python library for filtering data using the BrightData API across multiple datasets. The filter system is designed to be intuitive, type-safe, and powerful for complex data analysis with built-in support for Amazon Products, Amazon-Walmart Comparison, Shopee Products, and other datasets.

## Table of Contents

- [Quick Start](#quick-start)
- [Multi-Dataset Support](#multi-dataset-support)
- [Filter Syntax Overview](#filter-syntax-overview)
- [Type-Aware Filter Fields](#type-aware-filter-fields)
- [Operators](#operators)
- [Logical Operations](#logical-operations)
- [Configuration](#configuration)
- [Examples](#examples)
- [API Reference](#api-reference)

## Quick Start

```python
from util import BrightDataFilter, AMAZON_FIELDS as AF, AMAZON_WALMART_FIELDS as AW, SHOPEE_FIELDS as SF, get_brightdata_api_key

# Initialize the filter for Amazon Products dataset
api_key = get_brightdata_api_key()
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")

# Create a simple filter using dataset-specific fields
high_rated_products = AF.rating >= 4.5

# Execute the search
result = amazon_filter.search_data(high_rated_products, records_limit=1000)
print(f"Found products with snapshot ID: {result['snapshot_id']}")
```

## Multi-Dataset Support

The system supports multiple datasets with dataset-specific field definitions and validation:

### Available Datasets

```python
from util import BrightDataFilter

# List all available datasets
datasets = BrightDataFilter.list_available_datasets()
for dataset in datasets:
    print(f"• {dataset['name']} ({dataset['dataset_id']})")
    print(f"  {dataset['description']}")
    print(f"  Fields: {dataset['field_count']}")
```

### Dataset-Specific Fields

```python
from util import AMAZON_FIELDS as AF, AMAZON_WALMART_FIELDS as AW, SHOPEE_FIELDS as SF

# Amazon Products dataset fields
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")
amazon_query = (
    AF.rating >= 4.5 &
    AF.categories.includes("Electronics") &
    AF.asin.is_not_null()  # Amazon-specific field
)

# Amazon-Walmart Comparison dataset fields
aw_filter = BrightDataFilter(api_key, "gd_m4l6s4mn2g2rkx9lia")
aw_query = (
    AW.platform == "Amazon" &
    AW.price_difference > 0 &
    AW.availability_match.is_true()  # Cross-platform field
)

# Shopee Products dataset fields
shopee_filter = BrightDataFilter(api_key, "gd_lk122xxgf86xf97py")
shopee_query = (
    SF.rating >= 4.5 &
    SF.units_sold > 1000 &
    SF.country == "Singapore"  # Shopee-specific field
)
```

### Field Validation

The system automatically validates fields and operators for each dataset:

```python
try:
    # This works - ASIN exists in Amazon dataset
    filter = amazon_filter.create_filter("asin", "=", "B123456789")
except ValueError as e:
    print(f"Error: {e}")

try:
    # This fails - platform doesn't exist in Amazon dataset
    filter = amazon_filter.create_filter("platform", "=", "Amazon")
except ValueError as e:
    print(f"Error: {e}")  # Field 'platform' not found in dataset 'gd_l7q7dkf244hwjntr0'
```

### Dataset Information

```python
# Get information about the current dataset
info = amazon_filter.get_dataset_info()
print(f"Dataset: {info['name']}")
print(f"Available fields: {len(info['available_fields'])}")

# Get field reference for current dataset
field_ref = amazon_filter.get_field_reference()
for field_name, description in field_ref.items():
    print(f"{field_name}: {description}")
```

## Filter Syntax Overview

The filter system provides multiple ways to create filters, from simple comparisons to complex nested conditions:

### 1. Type-Aware Field Syntax (Recommended)
```python
# Numerical fields support comparison operators
RATING >= 4.5
PRICE < 100.0
REVIEWS_COUNT.in_range(50, 500)

# String fields support equality and contains
TITLE.contains("iPhone")
BRAND == "Apple"
DEPARTMENT.in_list(["Electronics", "Computers"])

# Boolean fields have specific methods
IS_AVAILABLE.is_true()
IS_AVAILABLE == True

# Array fields support inclusion checks
CATEGORIES.includes("Electronics")
CATEGORIES.not_includes("Books")
```

### 2. Generic Filter Creation
```python
# Using the filter method
filter_tool.filter("rating", ">=", "4.5")
filter_tool.filter("title", "includes", "iPhone")
filter_tool.filter("categories", "array_includes", "Electronics")
```

### 3. Direct FilterCondition Creation
```python
from util import FilterCondition, FilterOperator

condition = FilterCondition("rating", FilterOperator.GREATER_THAN_EQUAL, "4.5")
```

## Type-Aware Filter Fields

The system provides type-aware field classes that offer intuitive methods for each data type:

### Numerical Fields
```python
from util import RATING, PRICE, REVIEWS_COUNT, BS_RANK

# Comparison operators
RATING >= 4.5
PRICE < 100.0
REVIEWS_COUNT > 100

# Range filtering
PRICE.in_range(50, 200)  # 50 <= price <= 200
RATING.in_range(4.0, 5.0)

# Available numerical fields:
# RATING, REVIEWS_COUNT, INITIAL_PRICE, FINAL_PRICE, DISCOUNT
# NUMBER_OF_SELLERS, BS_RANK, ROOT_BS_RANK, ITEM_WEIGHT
```

### String Fields
```python
from util import AMAZON_FIELDS as AF

# Equality
AF.brand == "Apple"
AF.department == "Electronics"

# Contains/Not contains
AF.title.contains("iPhone")
AF.description.not_contains("refurbished")

# Includes (supports single string or array of strings)
AF.availability.includes("FREE")  # Single string
AF.availability.includes(["only", "within", "limited"])  # Array of strings

# List operations
AF.brand.in_list(["Apple", "Samsung", "Sony"])
AF.department.not_in_list(["Books", "Movies"])

# Available string fields:
# TITLE, ASIN, BRAND, DESCRIPTION, CURRENCY, AVAILABILITY
# SELLER_NAME, BUYBOX_SELLER, DEPARTMENT, PRODUCT_DIMENSIONS
# MODEL_NUMBER, MANUFACTURER, UPC
```

### Boolean Fields
```python
from util import IS_AVAILABLE

# Boolean methods
IS_AVAILABLE.is_true()
IS_AVAILABLE.is_false()

# Equality (converts to string)
IS_AVAILABLE == True   # becomes "true"
IS_AVAILABLE == False  # becomes "false"
```

### Array Fields
```python
from util import CATEGORIES, DELIVERY

# Single value inclusion
CATEGORIES.includes("Electronics")
DELIVERY.not_includes("Prime")

# Multiple value inclusion (creates OR condition)
CATEGORIES.includes(["Electronics", "Computers"])

# Available array fields:
# CATEGORIES, DELIVERY
```

## Operators

The system supports all Bright Data API operators:

| Operator | String | Description | Field Types |
|----------|--------|-------------|-------------|
| `=` | `"="` | Equal to | Any |
| `!=` | `"!="` | Not equal to | Any |
| `<` | `"<"` | Less than | Number, Date |
| `<=` | `"<="` | Less than or equal | Number, Date |
| `>` | `">"` | Greater than | Number, Date |
| `>=` | `">="` | Greater than or equal | Number, Date |
| `in` | `"in"` | Value in list | Any |
| `not_in` | `"not_in"` | Value not in list | Any |
| `includes` | `"includes"` | String contains | String |
| `not_includes` | `"not_includes"` | String does not contain | String |
| `array_includes` | `"array_includes"` | Array contains value | Array |
| `not_array_includes` | `"not_array_includes"` | Array does not contain value | Array |
| `is_null` | `"is_null"` | Field is null | Any |
| `is_not_null` | `"is_not_null"` | Field is not null | Any |

## Logical Operations

Combine filters using logical operators:

### AND Operations
```python
# Using & operator
high_rated_affordable = (RATING >= 4.5) & (PRICE < 100)

# Using + operator (alternative)
high_rated_affordable = (RATING >= 4.5) + (PRICE < 100)

# Multiple conditions
complex_filter = (RATING >= 4.0) & (PRICE < 200) & (CATEGORIES.includes("Electronics"))
```

### OR Operations
```python
# Using | operator
apple_or_samsung = (BRAND == "Apple") | (BRAND == "Samsung")

# Multiple OR conditions
electronics_or_computers = (CATEGORIES.includes("Electronics")) | (CATEGORIES.includes("Computers"))
```

### Complex Nested Logic
```python
# Complex nested conditions
strategy_filter = (
    (RATING >= 4.0) & 
    (PRICE < 100) & 
    (
        (CATEGORIES.includes("Electronics")) | 
        (CATEGORIES.includes("Home & Garden"))
    ) &
    (IS_AVAILABLE.is_true())
)
```


## Configuration

### Secrets Management
```python
from util import get_brightdata_api_key, validate_required_secrets

# Validate configuration
validate_required_secrets()

# Get API key
api_key = get_brightdata_api_key()
```

### Configuration File Structure
```yaml
# secrets.yaml
brightdata:
  api_key: "your_bright_data_api_key_here"
  dataset_id: "gd_l7q7dkf244hwjntr0"
  base_url: "https://api.brightdata.com/datasets"

environment:
  debug: false
  log_level: "INFO"
  max_retries: 3
  timeout: 30
```

## Examples

### Example 1: Find High-Quality Electronics Under $100 (Amazon Products)
```python
from util import BrightDataFilter, AMAZON_FIELDS as AF, get_brightdata_api_key

api_key = get_brightdata_api_key()
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")

# Create the filter using Amazon-specific fields
electronics_filter = (
    AF.rating >= 4.5 &
    AF.final_price < 100 &
    AF.categories.includes("Electronics") &
    AF.is_available.is_true()
)

# Execute search
result = amazon_filter.search_data(electronics_filter, records_limit=500)
print(f"Found products: {result['snapshot_id']}")
```

### Example 2: Cross-Platform Price Analysis (Amazon-Walmart Comparison)
```python
from util import BrightDataFilter, AMAZON_WALMART_FIELDS as AW, get_brightdata_api_key

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

result = aw_filter.search_data(amazon_expensive, records_limit=1000)
print(f"Found Amazon-expensive products: {result['snapshot_id']}")
```

### Example 3: Long Tail Opportunities (Amazon Products)
```python
from util import BrightDataFilter, AMAZON_FIELDS as AF, get_brightdata_api_key

api_key = get_brightdata_api_key()
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")

# Find long tail opportunities (good ratings, moderate competition)
long_tail_filter = (
    AF.rating >= 4.0 &
    AF.reviews_count >= 50 &
    AF.reviews_count < 500 &
    AF.final_price < 100 &
    AF.is_available.is_true() &
    AF.currency == "USD"
)

result = amazon_filter.search_data(long_tail_filter, records_limit=1000)
```

### Example 4: Complex Multi-Category Analysis (Amazon Products)
```python
from util import BrightDataFilter, AMAZON_FIELDS as AF, get_brightdata_api_key

api_key = get_brightdata_api_key()
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")

# Complex filter for multiple categories
multi_category_filter = (
    AF.rating >= 4.0 &
    AF.final_price.in_range(20, 150) &
    (
        AF.categories.includes("Electronics") |
        AF.categories.includes("Home & Garden") |
        AF.categories.includes("Sports & Outdoors")
    ) &
    AF.brand.not_in_list(["Generic", "Unbranded"])
)

result = amazon_filter.search_data(multi_category_filter, records_limit=2000)
```

### Example 5: Export and Import Filter Configurations
```python
from util import BrightDataFilter, AMAZON_FIELDS as AF, export_filter_to_json, load_filter_from_json

# Create a complex filter
my_filter = (AF.rating >= 4.5) & (AF.final_price < 100)

# Export to JSON
export_filter_to_json(my_filter, "my_filter_config.json")

# Load from JSON
filter_config = load_filter_from_json("my_filter_config.json")
print(filter_config)
```

### Example 6: Shopee Market Analysis
```python
from util import BrightDataFilter, SHOPEE_FIELDS as SF, get_brightdata_api_key

api_key = get_brightdata_api_key()
shopee_filter = BrightDataFilter(api_key, "gd_lk122xxgf86xf97py")

# Find trending products in Singapore
trending_singapore = (
    (SF.rating >= 4.0) &
    (SF.units_sold > 500) &
    (SF.favorites_count > 100) &
    (SF.country == "Singapore") &
    SF.is_available.is_true()
)

# Find best-selling electronics
best_electronics = (
    (SF.category == "Electronics") &
    (SF.units_sold > 1000) &
    (SF.rating >= 4.5) &
    (SF.final_price < 200)
)

result = shopee_filter.search_data(trending_singapore, records_limit=1000)
print(f"Found trending products: {result['snapshot_id']}")
```

### Example 7: Dataset Discovery and Information
```python
from util import BrightDataFilter, get_brightdata_api_key

# List all available datasets
datasets = BrightDataFilter.list_available_datasets()
print("Available datasets:")
for dataset in datasets:
    print(f"• {dataset['name']} ({dataset['dataset_id']})")
    print(f"  {dataset['description']}")
    print(f"  Fields: {dataset['field_count']}")

# Get detailed information about a specific dataset
api_key = get_brightdata_api_key()
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")

info = amazon_filter.get_dataset_info()
print(f"\nCurrent dataset: {info['name']}")
print(f"Available fields: {len(info['available_fields'])}")

# Get field reference
field_ref = amazon_filter.get_field_reference()
print("\nField reference:")
for field_name, description in list(field_ref.items())[:5]:  # Show first 5
    print(f"  {field_name}: {description}")
```

## API Reference

### Core Classes

#### `BrightDataFilter`
Main class for creating and executing data filters using the BrightData API.

```python
class BrightDataFilter:
    def __init__(self, api_key: str, dataset_id: str = "gd_l7q7dkf244hwjntr0")
    def create_filter(self, name: str, operator: FilterOperator, value: Any = None) -> FilterCondition
    def filter(self, field: str, op: str, value: Any = None) -> FilterCondition
    def create_filter_group(self, operator: LogicalOperator, filters: List) -> FilterGroup
    def search_data(self, filter_obj: Union[FilterCondition, FilterGroup], records_limit: int = 1000) -> Dict[str, Any]
    def get_dataset_info(self) -> Dict[str, Any]
    def get_field_reference(self) -> Dict[str, str]
    @staticmethod
    def list_available_datasets() -> List[Dict[str, Any]]
```

#### `DatasetFilterFields`
Dataset-aware filter fields factory for type-safe field access.

```python
class DatasetFilterFields:
    def __init__(self, dataset_id: str)
    def __getattr__(self, name: str) -> FilterField
    def get_field(self, field_name: str) -> Optional[FilterField]
    def list_fields(self) -> Dict[str, FilterField]
    def get_field_names(self) -> list
```

#### `FilterCondition`
Represents a single filter condition.

```python
@dataclass
class FilterCondition:
    name: str
    operator: FilterOperator
    value: Any = None
    
    def to_dict(self) -> Dict[str, Any]
    def __and__(self, other) -> FilterGroup  # AND operation
    def __or__(self, other) -> FilterGroup   # OR operation
    def __add__(self, other) -> FilterGroup  # Alternative AND syntax
```

#### `FilterGroup`
Represents a group of filters with logical operators.

```python
@dataclass
class FilterGroup:
    operator: LogicalOperator
    filters: List[Union[FilterGroup, FilterCondition]]
    
    def to_dict(self) -> Dict[str, Any]
    def pretty_print(self, indent: int = 0) -> str
    def __and__(self, other) -> FilterGroup  # AND operation
    def __or__(self, other) -> FilterGroup   # OR operation
```

### Type-Aware Field Classes

#### `NumericalFilterField`
```python
class NumericalFilterField:
    def __gt__(self, value) -> FilterCondition      # >
    def __ge__(self, value) -> FilterCondition      # >=
    def __lt__(self, value) -> FilterCondition      # <
    def __le__(self, value) -> FilterCondition      # <=
    def __eq__(self, value) -> FilterCondition      # ==
    def __ne__(self, value) -> FilterCondition      # !=
    def in_range(self, min_val, max_val) -> FilterGroup
```

#### `StringFilterField`
```python
class StringFilterField:
    def contains(self, value: str) -> FilterCondition
    def not_contains(self, value: str) -> FilterCondition
    def __eq__(self, value: str) -> FilterCondition
    def __ne__(self, value: str) -> FilterCondition
    def in_list(self, values: list) -> FilterCondition
    def not_in_list(self, values: list) -> FilterCondition
```

#### `BooleanFilterField`
```python
class BooleanFilterField:
    def is_true(self) -> FilterCondition
    def is_false(self) -> FilterCondition
    def __eq__(self, value: bool) -> FilterCondition
    def __ne__(self, value: bool) -> FilterCondition
```

#### `ArrayFilterField`
```python
class ArrayFilterField:
    def includes(self, value: Union[str, list]) -> FilterCondition
    def not_includes(self, value: Union[str, list]) -> FilterCondition
    def __eq__(self, value: str) -> FilterCondition
    def __ne__(self, value: str) -> FilterCondition
```

### Utility Functions

```python
def export_filter_to_json(filter_obj: Union[FilterCondition, FilterGroup], filename: str = "filter_config.json") -> None
def load_filter_from_json(filename: str) -> Dict[str, Any]
def analyze_filter_results(snapshot_id: str, api_key: str) -> Dict[str, Any]
```

### Configuration Functions

```python
def get_brightdata_api_key() -> str
def validate_required_secrets() -> None
def get_secret(key_path: str, default: Any = None) -> Any
def get_config(key_path: str, default: Any = None) -> Any
```

### Multi-Dataset Functions

```python
def list_available_datasets() -> List[DatasetSchema]
def get_dataset_schema(dataset_id: str) -> Optional[DatasetSchema]
def get_field_reference(dataset_id: str) -> Dict[str, str]
def validate_field_operator(dataset_id: str, field_name: str, operator: str) -> bool
```

### Pre-configured Dataset Fields

```python
# Amazon Products Dataset (gd_l7q7dkf244hwjntr0)
AMAZON_FIELDS = DatasetFilterFields("gd_l7q7dkf244hwjntr0")

# Amazon-Walmart Comparison Dataset (gd_m4l6s4mn2g2rkx9lia)
AMAZON_WALMART_FIELDS = DatasetFilterFields("gd_m4l6s4mn2g2rkx9lia")

# Shopee Products Dataset (gd_lk122xxgf86xf97py)
SHOPEE_FIELDS = DatasetFilterFields("gd_lk122xxgf86xf97py")
```

## Best Practices

### 1. Use Dataset-Specific Fields with Aliases
Prefer dataset-specific fields with aliases for cleaner, more readable code:
```python
# Good - Use aliases for cleaner code
from util import AMAZON_FIELDS as AF, AMAZON_WALMART_FIELDS as AW

AF.rating >= 4.5
AW.platform == "Amazon"

# Also good - Full names for clarity
AMAZON_FIELDS.rating >= 4.5
AMAZON_WALMART_FIELDS.platform == "Amazon"

# Avoid
filter_tool.filter("rating", ">=", "4.5")  # No dataset validation
```

### 2. Combine Filters Logically
Use parentheses to ensure correct operator precedence:
```python
# Good - With aliases
from util import AMAZON_FIELDS as AF
filter = (AF.rating >= 4.0) & (AF.final_price < 100) & (AF.categories.includes("Electronics"))

# Also good - Full names
filter = (AMAZON_FIELDS.rating >= 4.0) & (AMAZON_FIELDS.final_price < 100) & (AMAZON_FIELDS.categories.includes("Electronics"))

# Avoid
filter = AF.rating >= 4.0 & AF.final_price < 100 & AF.categories.includes("Electronics")
```

### 3. Validate Dataset Compatibility
Always ensure you're using the correct dataset and fields:
```python
# Good - Check available datasets first
datasets = BrightDataFilter.list_available_datasets()
for dataset in datasets:
    print(f"Available: {dataset['name']} ({dataset['dataset_id']})")

# Good - Use appropriate dataset-specific fields with aliases
from util import AMAZON_FIELDS as AF, AMAZON_WALMART_FIELDS as AW
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")
amazon_query = AF.rating >= 4.0  # Uses Amazon-specific fields

# Avoid - Mixing datasets
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0")
amazon_query = AW.platform == "Amazon"  # Wrong dataset fields
```

### 4. Export Complex Filters
Save complex filter configurations for reuse:
```python
from util import AMAZON_FIELDS as AF, export_filter_to_json
complex_filter = (AF.rating >= 4.5) & (AF.final_price < 100) & (AF.categories.includes("Electronics"))
export_filter_to_json(complex_filter, "electronics_high_quality.json")
```

### 5. Validate Configuration
Always validate your configuration before running filters:
```python
validate_required_secrets()
api_key = get_brightdata_api_key()
```

## Error Handling

The system provides clear error messages for common issues:

```python
# Invalid operator
try:
    filter_tool.filter("rating", "invalid_op", "4.5")
except ValueError as e:
    print(f"Error: {e}")  # "Unknown operator: invalid_op. Available: ['=', '!=', '<', ...]"

# Missing API key
try:
    get_brightdata_api_key()
except ValueError as e:
    print(f"Error: {e}")  # "Bright Data API key not found. Please set it in secrets.yaml"
```

## Performance Tips

1. **Limit Results**: Always set appropriate `records_limit` to avoid large result sets
2. **Use Specific Filters**: More specific filters return fewer results and are faster
3. **Cache Results**: Save snapshot IDs for later analysis instead of re-running filters
4. **Batch Operations**: Use filter groups to combine multiple conditions efficiently

## Troubleshooting

### Common Issues

1. **API Key Not Found**: Ensure `secrets.yaml` exists and contains valid API key
2. **Invalid Operators**: Check operator spelling and field type compatibility
3. **Large Result Sets**: Use more specific filters or lower `records_limit`
4. **Timeout Errors**: Reduce filter complexity or increase timeout in configuration

### Debug Mode

Enable debug mode for detailed logging:
```yaml
# secrets.yaml
environment:
  debug: true
  log_level: "DEBUG"
```

## Snapshot Management

After submitting filters, use the **Snapshot Manager** to track progress and handle downloads:

```bash
# List all snapshot records
python snapshot_manager.py --list

# Check status of all snapshots  
python snapshot_manager.py --status

# Download ready snapshots (incurs fees)
python snapshot_manager.py --download

# View downloaded data
python snapshot_manager.py --view <snapshot_id>

# Monitor processing snapshots
python snapshot_manager.py --monitor
```

The snapshot manager provides:
- **Local Record Storage**: All filter criteria and metadata saved as JSON files
- **Status Monitoring**: Real-time status checking from BrightData API
- **Download Management**: Handle ready snapshots and view downloaded data
- **Progress Tracking**: Monitor long-running jobs (30+ minutes)
- **Cost Tracking**: Monitor API costs per snapshot

See [SNAPSHOT_MANAGER_README.md](SNAPSHOT_MANAGER_README.md) for complete documentation.

## Conclusion

This comprehensive filter system provides powerful, intuitive tools for data analysis using the BrightData API across multiple datasets. The multi-dataset architecture with type-aware syntax makes complex filters readable and maintainable, enabling efficient analysis for various market research and product strategy applications. With built-in support for Amazon Products, Amazon-Walmart Comparison, Shopee Products, and extensible architecture for additional datasets, the system scales to meet diverse analytical needs across global e-commerce platforms.

The integrated snapshot management system ensures you never lose track of submitted filters and can efficiently handle the long processing times and download management required for large-scale data analysis.
