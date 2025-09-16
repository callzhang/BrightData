"""
Type-aware filter criteria for BrightData API datasets.

Callable field classes with type-specific methods for intuitive filter creation
across multiple datasets including Amazon, Walmart, and other product data sources.
"""

from typing import Any, Union, Optional, Dict
from .brightdata import FilterCondition, FilterOperator
from .dataset_registry import dataset_registry, get_dataset_schema


class FilterField:
    """Base class for filter fields that can be called with operators"""
    
    def __init__(self, field_name: str):
        self.field_name = field_name
    
    def __call__(self, operator: str, value: Any = None) -> FilterCondition:
        """
        Create a filter condition using string operator.
        
        Args:
            operator: String operator (e.g., ">=", "=", "in", "array_includes")
            value: Filter value
            
        Returns:
            FilterCondition object
        """
        # Map string operators to FilterOperator enum
        op_map = {
            "=": FilterOperator.EQUAL,
            "!=": FilterOperator.NOT_EQUAL,
            "<": FilterOperator.LESS_THAN,
            "<=": FilterOperator.LESS_THAN_EQUAL,
            ">": FilterOperator.GREATER_THAN,
            ">=": FilterOperator.GREATER_THAN_EQUAL,
            "in": FilterOperator.IN,
            "not_in": FilterOperator.NOT_IN,
            "includes": FilterOperator.INCLUDES,
            "not_includes": FilterOperator.NOT_INCLUDES,
            "array_includes": FilterOperator.ARRAY_INCLUDES,
            "not_array_includes": FilterOperator.NOT_ARRAY_INCLUDES,
            "is_null": FilterOperator.IS_NULL,
            "is_not_null": FilterOperator.IS_NOT_NULL
        }
        
        if operator not in op_map:
            raise ValueError(f"Unknown operator: {operator}. Available: {list(op_map.keys())}")
        
        return FilterCondition(self.field_name, op_map[operator], value)
    
    def __str__(self):
        return self.field_name
    
    def __repr__(self):
        return f"FilterField('{self.field_name}')"


class NumericalFilterField(FilterField):
    """Filter field for numerical values with comparison methods"""
    
    def __gt__(self, value: Union[int, float, str]) -> FilterCondition:
        """Greater than: field > value"""
        return FilterCondition(self.field_name, FilterOperator.GREATER_THAN, str(value))
    
    def __ge__(self, value: Union[int, float, str]) -> FilterCondition:
        """Greater than or equal: field >= value"""
        return FilterCondition(self.field_name, FilterOperator.GREATER_THAN_EQUAL, str(value))
    
    def __lt__(self, value: Union[int, float, str]) -> FilterCondition:
        """Less than: field < value"""
        return FilterCondition(self.field_name, FilterOperator.LESS_THAN, str(value))
    
    def __le__(self, value: Union[int, float, str]) -> FilterCondition:
        """Less than or equal: field <= value"""
        return FilterCondition(self.field_name, FilterOperator.LESS_THAN_EQUAL, str(value))
    
    def __eq__(self, value: Union[int, float, str]) -> FilterCondition:
        """Equal: field = value"""
        return FilterCondition(self.field_name, FilterOperator.EQUAL, str(value))
    
    def __ne__(self, value: Union[int, float, str]) -> FilterCondition:
        """Not equal: field != value"""
        return FilterCondition(self.field_name, FilterOperator.NOT_EQUAL, str(value))
    
    def in_range(self, min_val: Union[int, float, str], max_val: Union[int, float, str]) -> 'FilterGroup':
        """Create a range filter: min_val <= field <= max_val"""
        from .brightdata import FilterGroup, LogicalOperator
        return FilterGroup(LogicalOperator.AND, [
            FilterCondition(self.field_name, FilterOperator.GREATER_THAN_EQUAL, str(min_val)),
            FilterCondition(self.field_name, FilterOperator.LESS_THAN_EQUAL, str(max_val))
        ])


class BooleanFilterField(FilterField):
    """Filter field for boolean values with boolean-specific methods"""
    
    def is_true(self) -> FilterCondition:
        """Field is true"""
        return FilterCondition(self.field_name, FilterOperator.EQUAL, True)
    
    def is_false(self) -> FilterCondition:
        """Field is false"""
        return FilterCondition(self.field_name, FilterOperator.EQUAL, False)
    
    def __eq__(self, value: bool) -> FilterCondition:
        """Equal: field = value (uses actual boolean)"""
        return FilterCondition(self.field_name, FilterOperator.EQUAL, value)
    
    def __ne__(self, value: bool) -> FilterCondition:
        """Not equal: field != value (uses actual boolean)"""
        return FilterCondition(self.field_name, FilterOperator.NOT_EQUAL, value)


class StringFilterField(FilterField):
    """Filter field for string values with string-specific methods"""
    
    def contains(self, value: str) -> FilterCondition:
        """String contains value"""
        return FilterCondition(self.field_name, FilterOperator.INCLUDES, value)
    
    def not_contains(self, value: str) -> FilterCondition:
        """String does not contain value"""
        return FilterCondition(self.field_name, FilterOperator.NOT_INCLUDES, value)
    
    def includes(self, value: Union[str, list]) -> FilterCondition:
        """
        String includes value (supports both single string and array of strings).
        
        According to BrightData API docs:
        - If filter value is a single string, matches records where field value contains that string
        - If filter value is an array of strings, matches records where field value contains at least one string from the array
        """
        return FilterCondition(self.field_name, FilterOperator.INCLUDES, value)
    
    def not_includes(self, value: Union[str, list]) -> FilterCondition:
        """
        String does not include value (supports both single string and array of strings).
        
        According to BrightData API docs:
        - If filter value is a single string, matches records where field value does not contain that string
        - If filter value is an array of strings, matches records where field value does not contain any of the strings from the array
        """
        return FilterCondition(self.field_name, FilterOperator.NOT_INCLUDES, value)
    
    def __eq__(self, value: str) -> FilterCondition:
        """Equal: field = value"""
        return FilterCondition(self.field_name, FilterOperator.EQUAL, value)
    
    def __ne__(self, value: str) -> FilterCondition:
        """Not equal: field != value"""
        return FilterCondition(self.field_name, FilterOperator.NOT_EQUAL, value)
    
    def in_list(self, values: list) -> FilterCondition:
        """Field value is in list"""
        return FilterCondition(self.field_name, FilterOperator.IN, values)
    
    def not_in_list(self, values: list) -> FilterCondition:
        """Field value is not in list"""
        return FilterCondition(self.field_name, FilterOperator.NOT_IN, values)


class ArrayFilterField(FilterField):
    """Filter field for array values with array-specific methods"""
    
    def includes(self, value: Union[str, list]) -> FilterCondition:
        """
        Array includes value(s).
        
        Args:
            value: Single string value or list of values to check for inclusion
        """
        if isinstance(value, list):
            # For lists, we need to create multiple conditions and combine them with OR
            from .brightdata import FilterGroup, LogicalOperator
            conditions = [FilterCondition(self.field_name, FilterOperator.ARRAY_INCLUDES, v) for v in value]
            return FilterGroup(LogicalOperator.OR, conditions)
        else:
            # Single value
            return FilterCondition(self.field_name, FilterOperator.ARRAY_INCLUDES, value)
    
    def not_includes(self, value: Union[str, list]) -> FilterCondition:
        """
        Array does not include value(s).
        
        Args:
            value: Single string value or list of values to check for exclusion
        """
        if isinstance(value, list):
            # For lists, we need to create multiple conditions and combine them with AND
            from .brightdata import FilterGroup, LogicalOperator
            conditions = [FilterCondition(self.field_name, FilterOperator.NOT_ARRAY_INCLUDES, v) for v in value]
            return FilterGroup(LogicalOperator.AND, conditions)
        else:
            # Single value
            return FilterCondition(self.field_name, FilterOperator.NOT_ARRAY_INCLUDES, value)
    
    def __eq__(self, value: str) -> FilterCondition:
        """Equal: field = value"""
        return FilterCondition(self.field_name, FilterOperator.EQUAL, value)
    
    def __ne__(self, value: str) -> FilterCondition:
        """Not equal: field != value"""
        return FilterCondition(self.field_name, FilterOperator.NOT_EQUAL, value)


class DatasetFilterFields:
    """Dataset-aware filter fields factory"""
    
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id
        self.schema = get_dataset_schema(dataset_id)
        if not self.schema:
            raise ValueError(f"Unknown dataset ID: {dataset_id}")
        
        # Create field instances based on schema
        self._fields: Dict[str, FilterField] = {}
        self._create_fields()
    
    def _create_fields(self):
        """Create field instances based on dataset schema"""
        for field_name, field_def in self.schema.fields.items():
            if field_def.field_type.value == "numeric":
                self._fields[field_name] = NumericalFilterField(field_name)
            elif field_def.field_type.value == "boolean":
                self._fields[field_name] = BooleanFilterField(field_name)
            elif field_def.field_type.value == "array":
                self._fields[field_name] = ArrayFilterField(field_name)
            else:  # string, object
                self._fields[field_name] = StringFilterField(field_name)
    
    def __getattr__(self, name: str) -> FilterField:
        """Get field by name (uppercase convention)"""
        # Convert uppercase to lowercase for field names
        field_name = name.lower()
        if field_name in self._fields:
            return self._fields[field_name]
        raise AttributeError(f"Field '{name}' not found in dataset '{self.dataset_id}'")
    
    def get_field(self, field_name: str) -> Optional[FilterField]:
        """Get field by name"""
        return self._fields.get(field_name)
    
    def list_fields(self) -> Dict[str, FilterField]:
        """List all available fields"""
        return self._fields.copy()
    
    def get_field_names(self) -> list:
        """Get all field names"""
        return list(self._fields.keys())


# Create dataset-specific field instances
# Amazon Products Dataset (gd_l7q7dkf244hwjntr0)
AMAZON_FIELDS = DatasetFilterFields("gd_l7q7dkf244hwjntr0")

# Amazon-Walmart Comparison Dataset (gd_m4l6s4mn2g2rkx9lia)
AMAZON_WALMART_FIELDS = DatasetFilterFields("gd_m4l6s4mn2g2rkx9lia")

# Shopee Products Dataset (gd_lk122xxgf86xf97py)
SHOPEE_FIELDS = DatasetFilterFields("gd_lk122xxgf86xf97py")

# Backward compatibility - use Amazon fields as default
# This maintains existing code compatibility
RATING = AMAZON_FIELDS.rating
REVIEWS_COUNT = AMAZON_FIELDS.reviews_count
INITIAL_PRICE = AMAZON_FIELDS.initial_price
FINAL_PRICE = AMAZON_FIELDS.final_price
DISCOUNT = AMAZON_FIELDS.discount
NUMBER_OF_SELLERS = AMAZON_FIELDS.number_of_sellers
BS_RANK = AMAZON_FIELDS.bs_rank
ROOT_BS_RANK = AMAZON_FIELDS.root_bs_rank
ITEM_WEIGHT = AMAZON_FIELDS.item_weight

# Boolean fields
IS_AVAILABLE = AMAZON_FIELDS.is_available

# String fields
TITLE = AMAZON_FIELDS.title
ASIN = AMAZON_FIELDS.asin
BRAND = AMAZON_FIELDS.brand
DESCRIPTION = AMAZON_FIELDS.description
CURRENCY = AMAZON_FIELDS.currency
AVAILABILITY = AMAZON_FIELDS.availability
SELLER_NAME = AMAZON_FIELDS.seller_name
BUYBOX_SELLER = AMAZON_FIELDS.buybox_seller
DEPARTMENT = AMAZON_FIELDS.department
PRODUCT_DIMENSIONS = AMAZON_FIELDS.product_dimensions
MODEL_NUMBER = AMAZON_FIELDS.model_number
MANUFACTURER = AMAZON_FIELDS.manufacturer
UPC = AMAZON_FIELDS.upc

# Array fields
CATEGORIES = AMAZON_FIELDS.categories
DELIVERY = AMAZON_FIELDS.delivery

# Keep the old enum for backward compatibility
class FilterFields:
    """Legacy enum for backward compatibility"""
    TITLE = TITLE
    ASIN = ASIN
    BRAND = BRAND
    DESCRIPTION = DESCRIPTION
    CATEGORIES = CATEGORIES
    INITIAL_PRICE = INITIAL_PRICE
    FINAL_PRICE = FINAL_PRICE
    CURRENCY = CURRENCY
    DISCOUNT = DISCOUNT
    RATING = RATING
    REVIEWS_COUNT = REVIEWS_COUNT
    AVAILABILITY = AVAILABILITY
    DELIVERY = DELIVERY
    IS_AVAILABLE = IS_AVAILABLE
    SELLER_NAME = SELLER_NAME
    BUYBOX_SELLER = BUYBOX_SELLER
    NUMBER_OF_SELLERS = NUMBER_OF_SELLERS
    BS_RANK = BS_RANK
    ROOT_BS_RANK = ROOT_BS_RANK
    DEPARTMENT = DEPARTMENT
    ITEM_WEIGHT = ITEM_WEIGHT
    PRODUCT_DIMENSIONS = PRODUCT_DIMENSIONS
    MODEL_NUMBER = MODEL_NUMBER
    MANUFACTURER = MANUFACTURER
    UPC = UPC
    
    @classmethod
    def __iter__(cls):
        """Make FilterFields iterable for backward compatibility"""
        return iter([
            cls.TITLE, cls.ASIN, cls.BRAND, cls.DESCRIPTION, cls.CATEGORIES,
            cls.INITIAL_PRICE, cls.FINAL_PRICE, cls.CURRENCY, cls.DISCOUNT,
            cls.RATING, cls.REVIEWS_COUNT, cls.AVAILABILITY, cls.DELIVERY, cls.IS_AVAILABLE,
            cls.SELLER_NAME, cls.BUYBOX_SELLER, cls.NUMBER_OF_SELLERS,
            cls.BS_RANK, cls.ROOT_BS_RANK, cls.DEPARTMENT, cls.ITEM_WEIGHT,
            cls.PRODUCT_DIMENSIONS, cls.MODEL_NUMBER, cls.MANUFACTURER, cls.UPC
        ])
    
    @classmethod
    def get_all_fields(cls):
        """Get all field instances"""
        return [
            cls.TITLE, cls.ASIN, cls.BRAND, cls.DESCRIPTION, cls.CATEGORIES,
            cls.INITIAL_PRICE, cls.FINAL_PRICE, cls.CURRENCY, cls.DISCOUNT,
            cls.RATING, cls.REVIEWS_COUNT, cls.AVAILABILITY, cls.DELIVERY, cls.IS_AVAILABLE,
            cls.SELLER_NAME, cls.BUYBOX_SELLER, cls.NUMBER_OF_SELLERS,
            cls.BS_RANK, cls.ROOT_BS_RANK, cls.DEPARTMENT, cls.ITEM_WEIGHT,
            cls.PRODUCT_DIMENSIONS, cls.MODEL_NUMBER, cls.MANUFACTURER, cls.UPC
        ]
    
    @classmethod
    def get_field_count(cls):
        """Get the number of fields"""
        return 25
