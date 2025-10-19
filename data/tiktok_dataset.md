# TikTok Dataset - Field Descriptions

This document describes the fields available in the Brightdata TikTok Dataset for programmatic filtering and analysis using the [Brightdata Marketplace Dataset API](https://docs.brightdata.com/api-reference/marketplace-dataset-api/filter-dataset).

## Dataset Overview
The TikTok Dataset provides comprehensive product data from TikTok Shop, including product details, pricing, availability, seller information, reviews, and sales metrics. This dataset enables e-commerce analysis, social commerce insights, and TikTok Shop market research.

**Key Features:**
- **31 fields** covering comprehensive TikTok Shop product data
- **Real-time pricing** and availability information
- **Sales metrics** including sold quantities
- **Review and rating** information with detailed review data
- **Seller and store** data with store details
- **Product variations** and specifications
- **Media content** including images and videos
- **High fill rates** for most critical fields
- **Timestamp tracking** for data freshness

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
  "dataset_id": "gd_tiktok_dataset_id",
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

### Sales and Performance Metrics
- **`sold`** (number): Number of units sold - *Fill rate: 100.00%*
  - *Example*: 150
  - *Use case*: Analyze product popularity and sales performance
- **`prodct_rating`** (number): Product rating - *Fill rate: 46.45%*
- **`reviews_count`** (number): Number of product reviews - *Fill rate: 99.65%*
- **`available`** (boolean): Product availability status - *Fill rate: 100.00%*

### Product Information
- **`title`** (text): Product title - *Fill rate: 100.00%*
- **`description`** (text): Product description - *Fill rate: 97.50%*
- **`id`** (text): Product ID - *Fill rate: 100.00%*
- **`category`** (text): Product category - *Fill rate: 49.50%*

### Pricing Information
- **`final_price`** (number): Final price of the product - *Fill rate: 94.95%*
- **`initial_price`** (number): Initial price before discounts - *Fill rate: 94.96%*
- **`discount_percent`** (number): Discount percentage - *Fill rate: 100.00%*
- **`currency`** (text): Currency of the product - *Fill rate: 99.88%*
- **`shipping_fee`** (number): Shipping fee - *Fill rate: 69.80%*

### Seller Information
- **`seller_id`** (text): Seller identifier - *Fill rate: 89.35%*
- **`store_details`** (object): Store information - *Fill rate: 100.00%*

## Complete Field Descriptions

### Basic Product Information
- **`url`** (url): Product URL - *Fill rate: 100.00%*
- **`title`** (text): Product title - *Fill rate: 100.00%*
- **`description`** (text): Product description - *Fill rate: 97.50%*
- **`id`** (text): Product ID - *Fill rate: 100.00%*
- **`domain`** (text): Product domain (e.g., "www.tiktok.com") - *Fill rate: 100.00%*
- **`category`** (text): Product category - *Fill rate: 49.50%*
- **`category_url`** (url): Category URL - *Fill rate: 56.65%*
- **`seller_id`** (text): Seller identifier - *Fill rate: 89.35%*
- **`position`** (number): Product's position on the page - *Fill rate: 0.00%*
- **`timestamp`** (text): Data collection timestamp - *Fill rate: 100.00%*

### Pricing Information
- **`initial_price`** (number): Initial price before discounts - *Fill rate: 94.96%*
- **`final_price`** (number): Final price of the product - *Fill rate: 94.95%*
- **`discount_percent`** (number): Discount percentage - *Fill rate: 100.00%*
- **`currency`** (text): Currency of the product - *Fill rate: 99.88%*
- **`initial_price_low`** (number): Low end of initial price range - *Fill rate: 16.12%*
- **`initial_price_high`** (number): High end of initial price range - *Fill rate: 3.01%*
- **`final_price_low`** (number): Low end of final price range - *Fill rate: 94.93%*
- **`final_price_high`** (number): High end of final price range - *Fill rate: 16.13%*
- **`shipping_fee`** (number): Shipping fee - *Fill rate: 69.80%*

### Product Details
- **`category`** (text): Product category - *Fill rate: 49.50%*
- **`category_url`** (url): Category URL - *Fill rate: 56.65%*
- **`specifications`** (array): Product specifications - *Fill rate: 70.96%*
- **`variations`** (array): Product variations - *Fill rate: 86.26%*

### Reviews and Ratings
- **`prodct_rating`** (number): Product rating - *Fill rate: 46.45%*
- **`reviews_count`** (number): Number of product reviews - *Fill rate: 99.65%*
- **`reviews`** (array): Detailed review data including date, name, rating, and review text - *Fill rate: 53.44%*

### Availability and Sales
- **`available`** (boolean): Product availability status - *Fill rate: 100.00%*
- **`sold`** (number): Number of units sold - *Fill rate: 100.00%*
- **`position`** (number): Product's position on the page - *Fill rate: 0.00%*

### Product Variations
- **`colors`** (array): Available colors - *Fill rate: 33.11%*
- **`sizes`** (array): Available sizes - *Fill rate: 18.76%*
- **`variations`** (array): Product variations - *Fill rate: 86.26%*

### Media and Content
- **`images`** (array): Product images - *Fill rate: 100.00%*
- **`videos`** (array): Product videos - *Fill rate: 15.40%*

### Seller Information
- **`seller_id`** (text): Seller identifier - *Fill rate: 89.35%*
- **`store_details`** (object): Store information - *Fill rate: 100.00%*

## Complex Filtering Examples

### High-Selling Products
```json
{
  "dataset_id": "gd_tiktok_dataset_id",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "sold", "operator": ">", "value": "100"},
      {"name": "available", "operator": "=", "value": "true"},
      {"name": "prodct_rating", "operator": ">=", "value": "4.0"},
      {"name": "reviews_count", "operator": ">", "value": "50"}
    ]
  }
}
```

### Electronics Category Analysis
```json
{
  "dataset_id": "gd_tiktok_dataset_id",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "category", "operator": "includes", "value": "Electronics"},
      {"name": "available", "operator": "=", "value": "true"},
      {"name": "final_price", "operator": "<=", "value": "500"},
      {"name": "currency", "operator": "=", "value": "USD"}
    ]
  }
}
```

### Products with High Discounts
```json
{
  "dataset_id": "gd_tiktok_dataset_id",
  "records_limit": 500,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "discount_percent", "operator": ">", "value": "20"},
      {"name": "available", "operator": "=", "value": "true"},
      {"name": "sold", "operator": ">", "value": "10"}
    ]
  }
}
```

### Products with Videos
```json
{
  "dataset_id": "gd_tiktok_dataset_id",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "videos", "operator": "is_not_null", "value": null},
      {"name": "available", "operator": "=", "value": "true"},
      {"name": "reviews_count", "operator": ">", "value": "20"}
    ]
  }
}
```

### Color and Size Variations
```json
{
  "dataset_id": "gd_tiktok_dataset_id",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "colors", "operator": "array_includes", "value": "Red"},
      {"name": "sizes", "operator": "array_includes", "value": "Large"},
      {"name": "available", "operator": "=", "value": "true"},
      {"name": "final_price", "operator": ">", "value": "10"}
    ]
  }
}
```

### Top-Rated Products
```json
{
  "dataset_id": "gd_tiktok_dataset_id",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "prodct_rating", "operator": ">=", "value": "4.5"},
      {"name": "reviews_count", "operator": ">", "value": "100"},
      {"name": "available", "operator": "=", "value": "true"},
      {"name": "sold", "operator": ">", "value": "50"}
    ]
  }
}
```

### Products with Rich Review Data
```json
{
  "dataset_id": "gd_tiktok_dataset_id",
  "records_limit": 500,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "reviews", "operator": "is_not_null", "value": null},
      {"name": "reviews_count", "operator": ">", "value": "50"},
      {"name": "available", "operator": "=", "value": "true"},
      {"name": "prodct_rating", "operator": ">=", "value": "4.0"}
    ]
  }
}
```

## Data Types Summary

### Field Data Types and Fill Rates
- **Text fields**: title (100.00%), description (97.50%), currency (99.88%), category (49.50%), domain (100.00%), id (100.00%), seller_id (89.35%), timestamp (100.00%)
- **Number fields**: initial_price (94.96%), final_price (94.95%), discount_percent (100.00%), initial_price_low (16.12%), initial_price_high (3.01%), final_price_low (94.93%), final_price_high (16.13%), sold (100.00%), shipping_fee (69.80%), reviews_count (99.65%), prodct_rating (46.45%), position (0.00%)
- **Boolean fields**: available (100.00%)
- **Array fields**: colors (33.11%), sizes (18.76%), specifications (70.96%), reviews (53.44%), images (100.00%), videos (15.40%), variations (86.26%)
- **Object fields**: store_details (100.00%)
- **URL fields**: url (100.00%), category_url (56.65%)

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

### Social Commerce Analysis
- Analyze product performance on TikTok Shop
- Study viral product trends and social commerce patterns
- Research product categories and consumer preferences

### Market Research
- Track product availability and pricing trends
- Monitor seller performance and marketplace dynamics
- Analyze consumer behavior and buying patterns

### Competitive Intelligence
- Compare product offerings and pricing strategies
- Identify market opportunities and gaps
- Track competitor product launches and strategies

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
11. Sales data (sold) reflects current purchasing activity
12. Price information is updated in real-time based on current marketplace conditions
13. Fill rates indicate data completeness - consider this when filtering on low-fill-rate fields
14. Position field has 0.00% fill rate and may not be useful for filtering
15. **Rich Review Data**: The `reviews` array contains detailed review objects with date, name, rating, and review text
16. **Variations Data**: The `variations` array contains detailed product variation information including SKU, stock, and pricing
17. **Timestamp Tracking**: The `timestamp` field provides data collection timestamps for freshness analysis

## Dataset Source
This dataset is provided by [Brightdata](https://brightdata.com/products/datasets/tiktok) and contains real-time product data from TikTok Shop for analysis and research purposes. The dataset provides comprehensive coverage of TikTok's social commerce platform with high fill rates for critical fields like pricing, availability, and sales data.
