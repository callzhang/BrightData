# Target Dataset - Field Descriptions

This document describes the fields available in the Brightdata Target Dataset for programmatic filtering and analysis using the [Brightdata Marketplace Dataset API](https://docs.brightdata.com/api-reference/marketplace-dataset-api/filter-dataset).

## Dataset Overview
The Target Dataset provides comprehensive product data from Target's e-commerce platform, including product details, pricing, availability, seller information, reviews, and specifications. This dataset enables retail analysis, competitive intelligence, and Target marketplace research.

**Key Features:**
- **35+ fields** covering comprehensive Target product data
- **Real-time pricing** and availability information
- **Review and rating** data with star distribution
- **Product specifications** and variations
- **Seller and retailer** information
- **High fill rates** for most critical fields
- **Navigation and categorization** data

## API Usage

### Authentication
Use your Bright Data API Key as a Bearer token in the Authorization header:
```
Authorization: Bearer <your_api_key>
```

### Filter Dataset Endpoint
```
POST https://api.brightdata.com/datasets/filter
```

### Request Format
```json
{
  "dataset_id": "gd_ltppk5mx2lp0v1k0vo",
  "records_limit": 1000,
  "filter": {
    "name": "field_name",
    "operator": "operator_type",
    "value": "filter_value"
  }
}
```

## Available Operators

Based on the [Brightdata API documentation](https://docs.brightdata.com/api-reference/marketplace-dataset-api/filter-dataset), the following operators are supported:

| Operator | Field Types | Description |
|----------|-------------|-------------|
| `=` | Any | Equal to |
| `!=` | Any | Not equal to |
| `<` | Number, Date | Lower than |
| `<=` | Number, Date | Lower than or equal |
| `>` | Number, Date | Greater than |
| `>=` | Number, Date | Greater than or equal |
| `in` | Any | Tests if field value is equal to any of the values provided |
| `not_in` | Any | Tests if field value is not equal to all of the values provided |
| `includes` | Array, Text | Tests if the field value contains the filter value |
| `not_includes` | Array, Text | Tests if the field value does not contain the filter value |
| `array_includes` | Array | Tests if filter value is in field value (exact match) |
| `not_array_includes` | Array | Tests if filter value is not in field value (exact match) |
| `is_null` | Any | Tests if the field value is equal to NULL |
| `is_not_null` | Any | Tests if the field value is not equal to NULL |

## Key Fields for Analysis

### Product Information
- **`title`** (text): Product title - *Fill rate: 100.00%*
- **`product_description`** (text): Product description - *Fill rate: 99.22%*
- **`product_id`** (text): Unique product identifier - *Fill rate: 100.00%*
- **`tcin_id`** (text): Target's internal product ID - *Fill rate: 99.94%*

### Pricing Information
- **`final_price`** (price): Final price after discount - *Fill rate: 99.98%*
- **`initial_price`** (price): Original price before discount - *Fill rate: 99.97%*
- **`discount`** (text): Discount information - *Fill rate: 99.93%*
- **`currency`** (text): Currency used - *Fill rate: 100.00%*

### Reviews and Ratings
- **`rating`** (number): Average product rating - *Fill rate: 100.00%*
- **`reviews_count`** (number): Number of reviews - *Fill rate: 100.00%*
- **`amount_of_stars`** (array): Star rating distribution - *Fill rate: 100.00%*

### Availability and Inventory
- **`is_available`** (boolean): Product availability - *Fill rate: 99.94%*
- **`availability_text`** (text): Availability description - *Fill rate: 99.94%*
- **`is_available_binary`** (number): Binary availability indicator - *Fill rate: 99.92%*

## Complete Field Descriptions

### Basic Product Information
- **`url`** (url): Product URL - *Fill rate: 100.00%*
- **`product_id`** (text): Unique identifier for the product - *Fill rate: 100.00%*
- **`title`** (text): Title or name of the product - *Fill rate: 100.00%*
- **`product_description`** (text): Description of the product - *Fill rate: 99.22%*
- **`product_brand`** (text): Product brand - *Fill rate: 93.37%*
- **`item_number`** (text): Item number - *Fill rate: 99.87%*
- **`retailer`** (text): Retailer information - *Fill rate: 99.94%*
- **`tcin_id`** (text): Target's internal product ID - *Fill rate: 99.94%*

### Pricing Information
- **`initial_price`** (price): Initial/original price of the product - *Fill rate: 99.97%*
- **`discount`** (text): Discount offered on the product - *Fill rate: 99.93%*
- **`final_price`** (price): Final price of the product after discount - *Fill rate: 99.98%*
- **`currency`** (text): Currency used for pricing - *Fill rate: 100.00%*
- **`price_range`** (text): Price range information - *Fill rate: 16.48%*

### Reviews and Ratings
- **`rating`** (number): Average rating of the product - *Fill rate: 100.00%*
- **`reviews_count`** (number): Number of ratings or reviews for the product - *Fill rate: 100.00%*
- **`amount_of_stars`** (array): Distribution of star ratings - *Fill rate: 100.00%*
- **`summary_of_reviews`** (text): Summary of reviews - *Fill rate: 2.50%*
- **`what_customers_said`** (array): Feedback from customers - *Fill rate: 15.58%*
- **`review_images`** (array): URLs of images related to reviews - *Fill rate: 7.86%*
- **`reviews_related`** (array): Related reviews - *Fill rate: 0.00%*

### Product Details and Specifications
- **`product_specifications`** (array): Specifications of the product - *Fill rate: 99.12%*
- **`variations`** (array): Variations of the product - *Fill rate: 36.92%*
- **`fit_and_sytle`** (array): Fit and style information - *Fill rate: 34.11%*
- **`upc`** (text): UPC of the product - *Fill rate: 99.89%*
- **`upc_normalization`** (text): Normalized UPC - *Fill rate: 99.86%*

### Navigation and Categories
- **`breadcrumbs`** (array): Navigation breadcrumbs for the product - *Fill rate: 99.03%*
- **`breadcrumb_text`** (text): Breadcrumb text - *Fill rate: 98.96%*
- **`related_categories`** (array): Related categories - *Fill rate: 99.01%*

### Seller Information
- **`seller_name`** (text): Name of the seller - *Fill rate: 100.00%*

### Availability and Inventory
- **`is_available`** (boolean): Product availability - *Fill rate: 99.94%*
- **`availability_text`** (text): Availability description - *Fill rate: 99.94%*
- **`is_available_binary`** (number): Binary availability indicator - *Fill rate: 99.92%*

### Media and Content
- **`images`** (array): URLs of images associated with the product - *Fill rate: 100.00%*

### Recommendations and Alternatives
- **`recommendations`** (array): Product recommendations - *Fill rate: 100.00%*
- **`find_alternative`** (array): Alternative products - *Fill rate: 0.08%*

### Policies and Offers
- **`shipping_returns_policy`** (array): Shipping and returns policy - *Fill rate: 0.05%*
- **`offers`** (array): Offers associated with the product - *Fill rate: 0.00%*
- **`promotion_fulltext`** (text): Full promotion text - *Fill rate: 1.98%*

### Q&A and Support
- **`q&a`** (array): Questions and answers - *Fill rate: 0.00%*

## Complex Filtering Examples

### High-Rated Products
```json
{
  "dataset_id": "gd_ltppk5mx2lp0v1k0vo",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "rating", "operator": ">=", "value": "4.5"},
      {"name": "reviews_count", "operator": ">", "value": "100"},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "final_price", "operator": "<=", "value": "100"}
    ]
  }
}
```

### Electronics Category Analysis
```json
{
  "dataset_id": "gd_ltppk5mx2lp0v1k0vo",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "breadcrumbs", "operator": "array_includes", "value": "Electronics"},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "currency", "operator": "=", "value": "USD"},
      {"name": "product_brand", "operator": "is_not_null", "value": null}
    ]
  }
}
```

### Products with Discounts
```json
{
  "dataset_id": "gd_ltppk5mx2lp0v1k0vo",
  "records_limit": 500,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "discount", "operator": "is_not_null", "value": null},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "rating", "operator": ">=", "value": "4.0"},
      {"name": "reviews_count", "operator": ">", "value": "50"}
    ]
  }
}
```

### Brand Analysis
```json
{
  "dataset_id": "gd_ltppk5mx2lp0v1k0vo",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "product_brand", "operator": "in", "value": ["Apple", "Samsung", "Sony"]},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "final_price", "operator": ">", "value": "50"},
      {"name": "rating", "operator": ">=", "value": "4.0"}
    ]
  }
}
```

### Products with Variations
```json
{
  "dataset_id": "gd_ltppk5mx2lp0v1k0vo",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "variations", "operator": "is_not_null", "value": null},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "reviews_count", "operator": ">", "value": "20"},
      {"name": "product_specifications", "operator": "is_not_null", "value": null}
    ]
  }
}
```

### Top-Rated Products by Category
```json
{
  "dataset_id": "gd_ltppk5mx2lp0v1k0vo",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "rating", "operator": ">=", "value": "4.8"},
      {"name": "reviews_count", "operator": ">", "value": "500"},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "amount_of_stars", "operator": "is_not_null", "value": null}
    ]
  }
}
```

## Data Types Summary

### Field Data Types and Fill Rates
- **Text fields**: title (100.00%), product_description (99.22%), product_brand (93.37%), item_number (99.87%), retailer (99.94%), tcin_id (99.94%), currency (100.00%), discount (99.93%), availability_text (99.94%), price_range (16.48%), breadcrumb_text (98.96%), upc (99.89%), upc_normalization (99.86%), seller_name (100.00%), summary_of_reviews (2.50%), promotion_fulltext (1.98%)
- **Price fields**: initial_price (99.97%), final_price (99.98%)
- **Number fields**: rating (100.00%), reviews_count (100.00%), is_available_binary (99.92%)
- **Boolean fields**: is_available (99.94%)
- **Array fields**: images (100.00%), breadcrumbs (99.03%), find_alternative (0.08%), fit_and_sytle (34.11%), offers (0.00%), product_specifications (99.12%), shipping_returns_policy (0.05%), q&a (0.00%), related_categories (99.01%), amount_of_stars (100.00%), recommendations (100.00%), variations (36.92%), what_customers_said (15.58%), review_images (7.86%), reviews_related (0.00%)
- **URL fields**: url (100.00%)

## API Response Format
The API returns a snapshot ID that you can use to download the filtered data:

```json
{
  "snapshot_id": "<string>"
}
```

Use the snapshot ID to download the data:
```
GET https://api.brightdata.com/datasets/snapshots/{snapshot_id}/download
```

## Use Cases

### Retail Analysis
- Analyze product performance on Target's platform
- Study pricing strategies and promotional activities
- Research product categories and consumer preferences

### Competitive Intelligence
- Compare product offerings and pricing with competitors
- Identify market opportunities and gaps
- Track competitor product launches and strategies

### Market Research
- Track product availability and inventory levels
- Monitor seller performance and marketplace dynamics
- Analyze consumer behavior and buying patterns

### E-commerce Optimization
- Optimize product listings and descriptions
- Improve pricing strategies based on market data
- Enhance inventory management and supply chain decisions

## Notes for Programmatic Filtering
1. All string comparisons are case-sensitive
2. Array fields should use `array_includes` or `array_not_includes` for exact matches
3. Use `includes` for partial string matching in text fields
4. Date fields should be formatted as strings (e.g., "2023-01-01")
5. Numeric fields support standard comparison operators (>, <, >=, <=, =, !=)
6. NULL checks can be performed using `is_null` or `is_not_null`
7. Multiple conditions can be combined using `and`/`or` operators with nested filter objects
8. Maximum nesting depth for filter groups is 3 levels
9. The API has a 5-minute timeout for job completion
10. Large result sets may be split into multiple parts for download
11. Price information is updated in real-time based on current marketplace conditions
12. Fill rates indicate data completeness - consider this when filtering on low-fill-rate fields
13. Fields with very low fill rates (0.00% - 5.00%) may not be useful for filtering
14. High-fill-rate fields (95%+) are most reliable for analysis and filtering

## Dataset Source
This dataset is provided by [Brightdata](https://brightdata.com/cp/datasets/browse/gd_ltppk5mx2lp0v1k0vo) and contains real-time product data from Target's e-commerce platform for analysis and research purposes. The dataset provides comprehensive coverage of Target's marketplace with high fill rates for critical fields like pricing, availability, and product information.




