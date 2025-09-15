"""
Dataset registry for managing multiple BrightData datasets.

This module provides a centralized registry for different datasets, their schemas,
and field definitions to support multi-dataset filtering.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum


class FieldType(Enum):
    """Field data types"""
    STRING = "string"
    NUMERIC = "numeric"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


@dataclass
class FieldDefinition:
    """Definition of a dataset field"""
    name: str
    field_type: FieldType
    description: str
    example: Optional[str] = None
    operators: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.operators is None:
            # Set default operators based on field type
            if self.field_type == FieldType.STRING:
                self.operators = ["=", "!=", "includes", "not_includes", "in", "not_in", "is_null", "is_not_null"]
            elif self.field_type == FieldType.NUMERIC:
                self.operators = ["=", "!=", "<", "<=", ">", ">=", "in", "not_in", "is_null", "is_not_null"]
            elif self.field_type == FieldType.BOOLEAN:
                self.operators = ["=", "!=", "is_null", "is_not_null"]
            elif self.field_type == FieldType.ARRAY:
                self.operators = ["array_includes", "not_array_includes", "is_null", "is_not_null"]
            else:
                self.operators = ["is_null", "is_not_null"]


@dataclass
class DatasetSchema:
    """Schema definition for a dataset"""
    dataset_id: str
    name: str
    description: str
    fields: Dict[str, FieldDefinition]
    base_url: str = "https://api.brightdata.com/datasets"
    
    def get_field(self, field_name: str) -> Optional[FieldDefinition]:
        """Get field definition by name"""
        return self.fields.get(field_name)
    
    def get_fields_by_type(self, field_type: FieldType) -> List[FieldDefinition]:
        """Get all fields of a specific type"""
        return [field for field in self.fields.values() if field.field_type == field_type]
    
    def get_field_names(self) -> List[str]:
        """Get all field names"""
        return list(self.fields.keys())


class DatasetRegistry:
    """Registry for managing multiple datasets"""
    
    def __init__(self):
        self._datasets: Dict[str, DatasetSchema] = {}
        self._register_default_datasets()
    
    def register_dataset(self, schema: DatasetSchema) -> None:
        """Register a new dataset schema"""
        self._datasets[schema.dataset_id] = schema
    
    def get_dataset(self, dataset_id: str) -> Optional[DatasetSchema]:
        """Get dataset schema by ID"""
        return self._datasets.get(dataset_id)
    
    def list_datasets(self) -> List[DatasetSchema]:
        """List all registered datasets"""
        return list(self._datasets.values())
    
    def get_dataset_names(self) -> List[str]:
        """Get all dataset names"""
        return [schema.name for schema in self._datasets.values()]
    
    def _register_default_datasets(self):
        """Register default datasets"""
        # Amazon Products Dataset
        amazon_schema = DatasetSchema(
            dataset_id="gd_l7q7dkf244hwjntr0",
            name="Amazon Products",
            description="Amazon product data with pricing, reviews, and seller information",
            fields={
                # Core product info
                "title": FieldDefinition("title", FieldType.STRING, "Product title", "iPhone 15 Pro"),
                "asin": FieldDefinition("asin", FieldType.STRING, "Unique identifier for each product", "B0CHX1W1XY"),
                "parent_asin": FieldDefinition("parent_asin", FieldType.STRING, "Parent ASIN of the product", "B0CHX1W1XY"),
                "brand": FieldDefinition("brand", FieldType.STRING, "Product brand", "Apple"),
                "description": FieldDefinition("description", FieldType.STRING, "A brief description of the product", "Latest iPhone with advanced features"),
                "categories": FieldDefinition("categories", FieldType.ARRAY, "Product categories", '["Electronics", "Cell Phones"]'),
                
                # Pricing
                "initial_price": FieldDefinition("initial_price", FieldType.NUMERIC, "Initial price", "999.99"),
                "final_price": FieldDefinition("final_price", FieldType.NUMERIC, "Final price of the product", "899.99"),
                "final_price_high": FieldDefinition("final_price_high", FieldType.NUMERIC, "Highest value of the final price when it is a range", "999.99"),
                "currency": FieldDefinition("currency", FieldType.STRING, "Currency of the product", "USD"),
                "discount": FieldDefinition("discount", FieldType.STRING, "Product discount information", "20% off"),
                
                # Reviews & ratings
                "rating": FieldDefinition("rating", FieldType.NUMERIC, "Average rating (1-5)", "4.5"),
                "reviews_count": FieldDefinition("reviews_count", FieldType.NUMERIC, "Number of reviews", "1250"),
                "answered_questions": FieldDefinition("answered_questions", FieldType.NUMERIC, "Number of answered questions", "45"),
                "top_review": FieldDefinition("top_review", FieldType.STRING, "Top review for the product", "Great product, highly recommend!"),
                
                # Sales & Purchase Data
                "bought_past_month": FieldDefinition("bought_past_month", FieldType.NUMERIC, "Number of units bought in the past month", "150"),
                
                # Availability
                "availability": FieldDefinition("availability", FieldType.STRING, "Stock status", "In Stock"),
                "is_available": FieldDefinition("is_available", FieldType.BOOLEAN, "Boolean availability", "true"),
                
                # Seller info
                "seller_name": FieldDefinition("seller_name", FieldType.STRING, "Seller name", "Amazon.com"),
                "seller_id": FieldDefinition("seller_id", FieldType.STRING, "Unique identifier for each seller", "ATVPDKIKX0DER"),
                "seller_url": FieldDefinition("seller_url", FieldType.STRING, "Seller URL", "https://amazon.com/seller/ATVPDKIKX0DER"),
                "buybox_seller": FieldDefinition("buybox_seller", FieldType.STRING, "Seller in the buy box", "Amazon.com"),
                "number_of_sellers": FieldDefinition("number_of_sellers", FieldType.NUMERIC, "Number of sellers for the product", "5"),
                
                # Rankings
                "bs_rank": FieldDefinition("bs_rank", FieldType.NUMERIC, "Best seller rank in the specific category", "150"),
                "root_bs_rank": FieldDefinition("root_bs_rank", FieldType.NUMERIC, "Best sellers rank in the general category", "25"),
                "bs_category": FieldDefinition("bs_category", FieldType.STRING, "Best seller category", "Electronics"),
                "root_bs_category": FieldDefinition("root_bs_category", FieldType.STRING, "Best seller root category", "Electronics"),
                
                # URLs & Media
                "url": FieldDefinition("url", FieldType.STRING, "URL that links directly to the product", "https://amazon.com/dp/B0CHX1W1XY"),
                "domain": FieldDefinition("domain", FieldType.STRING, "URL of the product domain", "amazon.com"),
                "image_url": FieldDefinition("image_url", FieldType.STRING, "URL that links directly to the product image", "https://images.amazon.com/image.jpg"),
                "images": FieldDefinition("images", FieldType.ARRAY, "URLs of the product images", '["https://images.amazon.com/image1.jpg", "https://images.amazon.com/image2.jpg"]'),
                "images_count": FieldDefinition("images_count", FieldType.NUMERIC, "Number of images", "5"),
                "video": FieldDefinition("video", FieldType.BOOLEAN, "Boolean indicating the presence of videos", "true"),
                "video_count": FieldDefinition("video_count", FieldType.NUMERIC, "Number of videos", "2"),
                
                # Product Details
                "department": FieldDefinition("department", FieldType.STRING, "Department to which the product belongs", "Electronics"),
                "item_weight": FieldDefinition("item_weight", FieldType.STRING, "Weight of the product", "1.2 lbs"),
                "product_dimensions": FieldDefinition("product_dimensions", FieldType.STRING, "Dimensions of the product", "6.1 x 2.8 x 0.3 inches"),
                "model_number": FieldDefinition("model_number", FieldType.STRING, "Model number of the product", "A3108"),
                "manufacturer": FieldDefinition("manufacturer", FieldType.STRING, "Manufacturer of the product", "Apple"),
                "upc": FieldDefinition("upc", FieldType.STRING, "Universal Product Code", "194253000000"),
                "country_of_origin": FieldDefinition("country_of_origin", FieldType.STRING, "Country of origin of the product", "USA"),
                "date_first_available": FieldDefinition("date_first_available", FieldType.STRING, "Date when the product first became available", "2023-01-15"),
                
                # Features & Content
                "features": FieldDefinition("features", FieldType.ARRAY, "Product features", '["5G", "Face ID", "Wireless Charging"]'),
                "product_details": FieldDefinition("product_details", FieldType.ARRAY, "Full product details", '[{"type": "Weight", "value": "1.2 lbs"}]'),
                "plus_content": FieldDefinition("plus_content", FieldType.BOOLEAN, "Boolean indicating the presence of additional content", "true"),
                
                # Amazon Specific
                "amazon_choice": FieldDefinition("amazon_choice", FieldType.BOOLEAN, "Specifies if the product is amazon's choice", "true"),
                "amazon_prime": FieldDefinition("amazon_prime", FieldType.BOOLEAN, "Does it has amazon prime delivery", "true"),
                "badge": FieldDefinition("badge", FieldType.STRING, "Product badge", "#1 Best Seller"),
                "sponsered": FieldDefinition("sponsered", FieldType.BOOLEAN, "Is the product sponsored", "false"),
                "climate_pledge_friendly": FieldDefinition("climate_pledge_friendly", FieldType.BOOLEAN, "Climate pledge friendly product", "true"),
                
                # Delivery & Shipping
                "delivery": FieldDefinition("delivery", FieldType.ARRAY, "Delivery-related information", '["Free shipping", "Prime delivery"]'),
                "ships_from": FieldDefinition("ships_from", FieldType.STRING, "Location where product ships from", "Amazon Fulfillment Center"),
            }
        )
        
        # Amazon-Walmart Comparison Dataset
        amazon_walmart_schema = DatasetSchema(
            dataset_id="gd_m4l6s4mn2g2rkx9lia",
            name="Amazon Walmart Comparison",
            description="Cross-platform product comparison between Amazon and Walmart",
            fields={
                # Platform identification
                "platform": FieldDefinition("platform", FieldType.STRING, "E-commerce platform", "Amazon"),
                
                # Core product info
                "title": FieldDefinition("title", FieldType.STRING, "Product name", "Vital Farms, Large Grade A Eggs, 12 Count"),
                "product_id": FieldDefinition("product_id", FieldType.STRING, "Platform-specific product ID", "B0849MZ45Y"),
                "brand": FieldDefinition("brand", FieldType.STRING, "Product brand", "VITAL FARMS"),
                "description": FieldDefinition("description", FieldType.STRING, "Product description", "Pasture raised eggs from happy hens"),
                "categories": FieldDefinition("categories", FieldType.ARRAY, "Product categories", '["Grocery & Gourmet Food", "Eggs"]'),
                
                # Pricing
                "initial_price": FieldDefinition("initial_price", FieldType.NUMERIC, "Original price", "8.49"),
                "final_price": FieldDefinition("final_price", FieldType.NUMERIC, "Current price", "8.49"),
                "currency": FieldDefinition("currency", FieldType.STRING, "Currency code", "USD"),
                "discount": FieldDefinition("discount", FieldType.NUMERIC, "Discount amount", "0.00"),
                
                # Availability & Stock
                "availability": FieldDefinition("availability", FieldType.STRING, "Stock status", "In Stock"),
                "is_available": FieldDefinition("is_available", FieldType.BOOLEAN, "Boolean availability", "true"),
                
                # Seller Information
                "seller_name": FieldDefinition("seller_name", FieldType.STRING, "Seller name", "Amazon.com"),
                "seller_id": FieldDefinition("seller_id", FieldType.STRING, "Unique seller identifier", "ATVPDKIKX0DER"),
                "is_fulfilled_by_platform": FieldDefinition("is_fulfilled_by_platform", FieldType.BOOLEAN, "Platform fulfillment", "true"),
                
                # Customer Reviews & Ratings
                "reviews_count": FieldDefinition("reviews_count", FieldType.NUMERIC, "Number of reviews", "9024"),
                "rating": FieldDefinition("rating", FieldType.NUMERIC, "Average rating (1-5)", "4.9"),
                
                # Product Details & Specifications
                "item_weight": FieldDefinition("item_weight", FieldType.STRING, "Product weight", "1.77 Pounds"),
                "product_dimensions": FieldDefinition("product_dimensions", FieldType.STRING, "Product dimensions", "0.39 x 0.39 x 0.5 inches"),
                "model_number": FieldDefinition("model_number", FieldType.STRING, "Model number", "u-4c-7501"),
                "manufacturer": FieldDefinition("manufacturer", FieldType.STRING, "Manufacturer", "VITAL FARMS"),
                "department": FieldDefinition("department", FieldType.STRING, "Product department", "Grocery & Gourmet Food"),
                "upc": FieldDefinition("upc", FieldType.STRING, "Universal Product Code", "861745000010"),
                
                # Media & Images
                "images": FieldDefinition("images", FieldType.ARRAY, "Product image URLs", '["https://example.com/image1.jpg"]'),
                "images_count": FieldDefinition("images_count", FieldType.NUMERIC, "Number of images", "11"),
                "image_url": FieldDefinition("image_url", FieldType.STRING, "Primary image URL", "https://example.com/primary.jpg"),
                
                # Best Sellers & Rankings
                "best_seller_rank": FieldDefinition("best_seller_rank", FieldType.NUMERIC, "Best seller rank", "18745"),
                "category_rank": FieldDefinition("category_rank", FieldType.NUMERIC, "Category rank", "40"),
                "best_seller_category": FieldDefinition("best_seller_category", FieldType.STRING, "Best seller category", "Grocery & Gourmet Food"),
                
                # Additional Product Information
                "date_first_available": FieldDefinition("date_first_available", FieldType.STRING, "First available date", "December 12, 2023"),
                "url": FieldDefinition("url", FieldType.STRING, "Product URL", "https://www.amazon.com/product"),
                "domain": FieldDefinition("domain", FieldType.STRING, "Platform domain", "https://www.amazon.com/"),
                
                # Amazon-specific fields with _amazon suffix
                "title_amazon": FieldDefinition("title_amazon", FieldType.STRING, "Amazon product title", "iPhone 15 Pro"),
                "seller_name_amazon": FieldDefinition("seller_name_amazon", FieldType.STRING, "Amazon seller name", "Amazon.com"),
                "brand_amazon": FieldDefinition("brand_amazon", FieldType.STRING, "Amazon product brand", "Apple"),
                "description_amazon": FieldDefinition("description_amazon", FieldType.STRING, "Amazon product description", "Latest iPhone with advanced features"),
                "initial_price_amazon": FieldDefinition("initial_price_amazon", FieldType.NUMERIC, "Amazon initial price", "999.99"),
                "currency_amazon": FieldDefinition("currency_amazon", FieldType.STRING, "Amazon currency", "USD"),
                "availability_amazon": FieldDefinition("availability_amazon", FieldType.STRING, "Amazon availability", "In Stock"),
                "reviews_count_amazon": FieldDefinition("reviews_count_amazon", FieldType.NUMERIC, "Amazon reviews count", "1250"),
                "categories_amazon": FieldDefinition("categories_amazon", FieldType.ARRAY, "Amazon categories", '["Electronics", "Cell Phones"]'),
                "asin_amazon": FieldDefinition("asin_amazon", FieldType.STRING, "Amazon ASIN", "B0CHX1W1XY"),
                "parent_asin_amazon": FieldDefinition("parent_asin_amazon", FieldType.STRING, "Amazon parent ASIN", "B0CHX1W1XY"),
                "rating_amazon": FieldDefinition("rating_amazon", FieldType.NUMERIC, "Amazon rating", "4.5"),
                "final_price_amazon": FieldDefinition("final_price_amazon", FieldType.NUMERIC, "Amazon final price", "899.99"),
                "bought_past_month_amazon": FieldDefinition("bought_past_month_amazon", FieldType.NUMERIC, "Amazon bought past month", "150"),
                "is_available_amazon": FieldDefinition("is_available_amazon", FieldType.BOOLEAN, "Amazon is available", "true"),
                "amazon_choice_amazon": FieldDefinition("amazon_choice_amazon", FieldType.BOOLEAN, "Amazon's Choice", "true"),
                
                # Walmart-specific fields with _walmart suffix
                "url_walmart": FieldDefinition("url_walmart", FieldType.STRING, "Walmart product URL", "https://walmart.com/ip/product/123"),
                "final_price_walmart": FieldDefinition("final_price_walmart", FieldType.NUMERIC, "Walmart final price", "799.99"),
                "sku_walmart": FieldDefinition("sku_walmart", FieldType.STRING, "Walmart SKU", "123456789"),
                "currency_walmart": FieldDefinition("currency_walmart", FieldType.STRING, "Walmart currency", "USD"),
                "brand_walmart": FieldDefinition("brand_walmart", FieldType.STRING, "Walmart brand", "Apple"),
                "product_name_walmart": FieldDefinition("product_name_walmart", FieldType.STRING, "Walmart product name", "iPhone 15 Pro"),
                "rating_walmart": FieldDefinition("rating_walmart", FieldType.NUMERIC, "Walmart rating", "4.3"),
                "review_count_walmart": FieldDefinition("review_count_walmart", FieldType.NUMERIC, "Walmart review count", "850"),
                "available_for_delivery_walmart": FieldDefinition("available_for_delivery_walmart", FieldType.BOOLEAN, "Walmart available for delivery", "true"),
                "available_for_pickup_walmart": FieldDefinition("available_for_pickup_walmart", FieldType.BOOLEAN, "Walmart available for pickup", "true"),
                
                # Cross-Platform Comparison Fields
                "price_difference": FieldDefinition("price_difference", FieldType.NUMERIC, "Amazon final price - Walmart final price", "99.99"),
                
                # Complex Data Fields
                "product_details": FieldDefinition("product_details", FieldType.ARRAY, "Structured product details", '[{"type": "Weight", "value": "1.77 lbs"}]'),
                "variations": FieldDefinition("variations", FieldType.ARRAY, "Product variations", '[{"color": "Red", "size": "Large"}]'),
                "features": FieldDefinition("features", FieldType.ARRAY, "Product features", '["Organic", "Free Range"]'),
                "delivery": FieldDefinition("delivery", FieldType.ARRAY, "Delivery options", '["Free shipping", "Prime delivery"]'),
            }
        )
        
        # Shopee Products Dataset (gd_lk122xxgf86xf97py)
        shopee_schema = DatasetSchema(
            dataset_id="gd_lk122xxgf86xf97py",
            name="Shopee Products",
            description="Comprehensive product data from Shopee e-commerce platform in Southeast Asia.",
            fields={
                # Product Information
                "url": FieldDefinition("url", FieldType.STRING, "Product page URL"),
                "title": FieldDefinition("title", FieldType.STRING, "Product name/title"),
                "description": FieldDefinition("description", FieldType.STRING, "Product description"),
                "images": FieldDefinition("images", FieldType.ARRAY, "URLs to product images"),
                "image_url": FieldDefinition("image_url", FieldType.STRING, "Primary product image URL"),
                "images_count": FieldDefinition("images_count", FieldType.NUMERIC, "Number of product images"),
                
                # Pricing Information
                "initial_price": FieldDefinition("initial_price", FieldType.NUMERIC, "Original/listed price"),
                "final_price": FieldDefinition("final_price", FieldType.NUMERIC, "Current/sale price"),
                "currency": FieldDefinition("currency", FieldType.STRING, "Currency code"),
                "discount": FieldDefinition("discount", FieldType.NUMERIC, "Discount amount"),
                "discount_percentage": FieldDefinition("discount_percentage", FieldType.NUMERIC, "Discount percentage"),
                
                # Sales & Performance Metrics
                "units_sold": FieldDefinition("units_sold", FieldType.NUMERIC, "Number of units sold"),
                "stock_availability": FieldDefinition("stock_availability", FieldType.STRING, "Stock status"),
                "is_available": FieldDefinition("is_available", FieldType.BOOLEAN, "Boolean availability status"),
                "favorites_count": FieldDefinition("favorites_count", FieldType.NUMERIC, "Number of favorites/likes"),
                "views_count": FieldDefinition("views_count", FieldType.NUMERIC, "Number of product views"),
                
                # Customer Feedback
                "rating": FieldDefinition("rating", FieldType.NUMERIC, "Average rating (1-5)"),
                "reviews_count": FieldDefinition("reviews_count", FieldType.NUMERIC, "Number of reviews"),
                "rating_distribution": FieldDefinition("rating_distribution", FieldType.OBJECT, "Breakdown of ratings by star"),
                
                # Seller Information
                "seller_name": FieldDefinition("seller_name", FieldType.STRING, "Seller/shop name"),
                "shop_url": FieldDefinition("shop_url", FieldType.STRING, "Seller's shop URL"),
                "seller_rating": FieldDefinition("seller_rating", FieldType.NUMERIC, "Seller's overall rating"),
                "seller_reviews_count": FieldDefinition("seller_reviews_count", FieldType.NUMERIC, "Number of seller reviews"),
                "seller_followers": FieldDefinition("seller_followers", FieldType.NUMERIC, "Number of seller followers"),
                
                # Product Categories & Classification
                "category": FieldDefinition("category", FieldType.STRING, "Main product category"),
                "subcategory": FieldDefinition("subcategory", FieldType.STRING, "Product subcategory"),
                "brand": FieldDefinition("brand", FieldType.STRING, "Product brand"),
                "tags": FieldDefinition("tags", FieldType.ARRAY, "Product tags/keywords"),
                "attributes": FieldDefinition("attributes", FieldType.OBJECT, "Product specifications"),
                
                # Geographic & Platform Information
                "country": FieldDefinition("country", FieldType.STRING, "Shopee country/market"),
                "region": FieldDefinition("region", FieldType.STRING, "Geographic region"),
                "language": FieldDefinition("language", FieldType.STRING, "Product language"),
                "platform": FieldDefinition("platform", FieldType.STRING, "E-commerce platform"),
                
                # Timestamps & Metadata
                "created_at": FieldDefinition("created_at", FieldType.STRING, "Product listing date"),
                "updated_at": FieldDefinition("updated_at", FieldType.STRING, "Last update timestamp"),
                "scraped_at": FieldDefinition("scraped_at", FieldType.STRING, "Data collection timestamp")
            }
        )
        
        # Register the datasets
        self.register_dataset(amazon_schema)
        self.register_dataset(amazon_walmart_schema)
        self.register_dataset(shopee_schema)
    
    def get_field_reference(self, dataset_id: str) -> Dict[str, str]:
        """Get field reference for a specific dataset"""
        schema = self.get_dataset(dataset_id)
        if not schema:
            return {}
        
        return {
            field_name: field.description 
            for field_name, field in schema.fields.items()
        }
    
    def validate_field(self, dataset_id: str, field_name: str, operator: str) -> bool:
        """Validate if a field and operator combination is valid for a dataset"""
        schema = self.get_dataset(dataset_id)
        if not schema:
            return False
        
        field = schema.get_field(field_name)
        if not field:
            return False
        
        return operator in field.operators


# Global registry instance
dataset_registry = DatasetRegistry()

# Dataset name mapping for user-friendly access
DATASET_NAMES = {
    # Amazon Products
    "amazon_products": "gd_l7q7dkf244hwjntr0",
    "amazon_product": "gd_l7q7dkf244hwjntr0",
    "amazon": "gd_l7q7dkf244hwjntr0",
    
    # Amazon-Walmart Comparison
    "amazon_walmart": "gd_m4l6s4mn2g2rkx9lia",
    "amazon_walmart_comparison": "gd_m4l6s4mn2g2rkx9lia",
    "amazon_walmart_dataset": "gd_m4l6s4mn2g2rkx9lia",
    
    # Shopee Products
    "shopee_products": "gd_lk122xxgf86xf97py",
    "shopee": "gd_lk122xxgf86xf97py",
    "shopee_product": "gd_lk122xxgf86xf97py",
}


def get_dataset_schema(dataset_id: str) -> Optional[DatasetSchema]:
    """Get dataset schema by ID"""
    return dataset_registry.get_dataset(dataset_id)


def list_available_datasets(include_names: bool = False) -> Union[List[DatasetSchema], Dict[str, Any]]:
    """
    List all available datasets with optional name mapping
    
    Args:
        include_names: If True, returns a dictionary with both schemas and name mappings
        
    Returns:
        List of DatasetSchema objects, or dict with schemas and names if include_names=True
    """
    schemas = dataset_registry.list_datasets()
    
    if not include_names:
        return schemas
    
    # Return comprehensive dataset information
    return {
        "schemas": schemas,
        "names": DATASET_NAMES.copy(),
        "summary": {
            "total_datasets": len(schemas),
            "total_name_aliases": len(DATASET_NAMES),
            "available_names": list(DATASET_NAMES.keys())
        }
    }


def get_field_reference(dataset_id: str) -> Dict[str, str]:
    """Get field reference for a dataset"""
    return dataset_registry.get_field_reference(dataset_id)


def validate_field_operator(dataset_id: str, field_name: str, operator: str) -> bool:
    """Validate field and operator combination"""
    return dataset_registry.validate_field(dataset_id, field_name, operator)


def get_dataset_id(dataset_name: str) -> str:
    """
    Get dataset ID from user-friendly name
    
    Args:
        dataset_name: User-friendly dataset name (e.g., 'amazon_products', 'amazon', 'shopee')
        
    Returns:
        Dataset ID for use with BrightDataFilter
        
    Raises:
        ValueError: If dataset name is not recognized
    """
    dataset_name_lower = dataset_name.lower().replace(' ', '_')
    
    if dataset_name_lower in DATASET_NAMES:
        return DATASET_NAMES[dataset_name_lower]
    
    # If not found, check if it's already a dataset ID
    if dataset_name.startswith('gd_'):
        return dataset_name
    
    # List available names for better error message
    available_names = list(DATASET_NAMES.keys())
    raise ValueError(f"Unknown dataset name: '{dataset_name}'. Available names: {available_names}")


def list_dataset_names() -> Dict[str, str]:
    """
    List all available dataset names and their IDs
    
    Returns:
        Dictionary mapping user-friendly names to dataset IDs
    """
    return DATASET_NAMES.copy()


def list_datasets_comprehensive() -> Dict[str, Any]:
    """
    Get comprehensive dataset information including schemas, names, and summary
    
    Returns:
        Dictionary with schemas, names, and summary information
    """
    return list_available_datasets(include_names=True)
