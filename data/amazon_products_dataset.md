# Amazon Products Dataset - Field Descriptions

This document describes the fields available in the Brightdata Amazon Products Dataset for programmatic filtering and analysis using the [Brightdata Marketplace Dataset API](https://docs.brightdata.com/api-reference/marketplace-dataset-api/filter-dataset).

## Dataset Overview
The Amazon Products Dataset provides comprehensive product data from Amazon, including product details, pricing, availability, seller information, reviews, and sales metrics. This dataset enables product research, market analysis, competitive intelligence, and e-commerce insights.

**Key Features:**
- **50+ fields** covering comprehensive Amazon product data
- **Real-time pricing** and availability information
- **Sales metrics** including recent purchase data
- **Review and rating** information
- **Seller and marketplace** data
- **Product categorization** and ranking information
- **Media content** including images and videos

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
  "dataset_id": "gd_m45m1u911dsa4274pi",
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
- **`bought_past_month`** (number): Number of units bought in the past month
  - *Example*: 150
  - *Use case*: Analyze recent sales trends and product popularity
- **`rating`** (number): Product rating (1-5)
- **`reviews_count`** (number): Number of product reviews
- **`is_available`** (boolean): Product availability status

### Product Information
- **`title`** (text): Product title
- **`brand`** (text): Product brand
- **`description`** (text): Brief description of the product
- **`asin`** (text): Unique identifier for each product (Amazon Standard Identification Number)
- **`categories`** (array): Product categories

### Pricing Information
- **`final_price`** (price): Final price of the product
- **`initial_price`** (price): Initial price before discounts
- **`currency`** (text): Currency of the product
- **`discount`** (text): Product discount information

### Seller Information
- **`seller_name`** (text): Seller name
- **`seller_id`** (text): Unique identifier for each seller
- **`buybox_seller`** (text): Seller in the buy box
- **`number_of_sellers`** (number): Number of sellers for the product

## Complete Field Descriptions

### Basic Product Information
- **`title`** (text): Product title on Amazon
- **`brand`** (text): Product brand on Amazon
- **`description`** (text): Brief description of the product
- **`asin`** (text): Unique identifier for each product (Amazon Standard Identification Number)
- **`parent_asin`** (text): Parent ASIN of the product
- **`input_asin`** (text): Input ASIN (currently inactive)

### Pricing Information
- **`initial_price`** (price): Initial price before discounts
- **`final_price`** (price): Final price of the product
- **`final_price_high`** (price): Highest value of the final price when it is a range
- **`currency`** (text): Currency of the product
- **`discount`** (text): Product discount information

### Seller Information
- **`seller_name`** (text): Seller name on Amazon
- **`seller_id`** (text): Unique identifier for each seller
- **`buybox_seller`** (text): Seller in the buy box
- **`number_of_sellers`** (number): Number of sellers for the product

### Product Details
- **`categories`** (array): Product categories
- **`department`** (text): Department to which the product belongs
- **`manufacturer`** (text): Manufacturer of the product
- **`model_number`** (text): Model number of the product
- **`upc`** (text): Universal Product Code
- **`item_weight`** (text): Weight of the product
- **`product_dimensions`** (text): Dimensions of the product
- **`country_of_origin`** (text): Country of origin of the product

### Reviews and Ratings
- **`rating`** (number): Product rating
- **`reviews_count`** (number): Number of reviews
- **`answered_questions`** (number): Number of answered questions
- **`top_review`** (text): Top review for the product

### Availability and Sales
- **`availability`** (text): Product availability
- **`is_available`** (boolean): Indication if the product is still available
- **`bought_past_month`** (number): Number of units bought in the past month

### Rankings and Categories
- **`root_bs_rank`** (number): Best sellers rank in the general category
- **`bs_rank`** (number): Best seller rank in the specific category
- **`root_bs_category`** (text): Best seller root category
- **`bs_category`** (text): Best seller category
- **`subcategory_rank`** (array): Subcategory ranking information

### Media and Content
- **`images_count`** (number): Number of images
- **`images`** (array): URLs of the product images
- **`image_url`** (url): URL that links directly to the product image
- **`video_count`** (number): Number of videos
- **`video`** (boolean): Boolean indicating the presence of videos
- **`videos`** (array): URLs of the product's videos
- **`downloadable_videos`** (array): Downloadable video information

### Product Features and Details
- **`features`** (array): Product features
- **`product_details`** (array): Full product details
- **`product_description`** (array): Detailed product description
- **`variations`** (array): Details about the same product in different variations
- **`delivery`** (array): Delivery-related information
- **`format`** (array): Format-related information

### Pricing and Buy Box
- **`buybox_prices`** (object): Product price details
- **`prices_breakdown`** (object): Detailed price breakdown
- **`other_sellers_prices`** (array): Other sellers details who sell the product

### Additional Information
- **`date_first_available`** (text): Date when the product first became available
- **`domain`** (url): URL of the product domain
- **`url`** (url): URL that links directly to the product
- **`origin_url`** (url): Original URL
- **`seller_url`** (url): Seller URL
- **`ingredients`** (text): Ingredients of the product, relevant mostly for food products
- **`plus_content`** (boolean): Boolean indicating the presence of additional content
- **`amazon_choice`** (boolean): Specifies if the product is Amazon's Choice
- **`badge`** (text): Product badge (e.g., #1 Best Seller or Amazon's Choice)
- **`climate_pledge_friendly`** (boolean): Climate pledge friendly status
- **`sustainability_features`** (array): Sustainability features
- **`from_the_brand`** (array): Brand-specific information
- **`customer_says`** (text): Customer feedback summary

## Complex Filtering Examples

### High-Rated Products with Recent Sales
```json
{
  "dataset_id": "gd_m45m1u911dsa4274pi",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "rating", "operator": ">=", "value": "4.5"},
      {"name": "reviews_count", "operator": ">", "value": "100"},
      {"name": "bought_past_month", "operator": ">", "value": "50"},
      {"name": "is_available", "operator": "=", "value": "true"}
    ]
  }
}
```

### Electronics Category Analysis
```json
{
  "dataset_id": "gd_m45m1u911dsa4274pi",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "department", "operator": "=", "value": "Electronics"},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "final_price", "operator": "<=", "value": "500"},
      {"name": "currency", "operator": "=", "value": "USD"}
    ]
  }
}
```

### Amazon's Choice Products
```json
{
  "dataset_id": "gd_m45m1u911dsa4274pi",
  "records_limit": 500,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "amazon_choice", "operator": "=", "value": "true"},
      {"name": "rating", "operator": ">=", "value": "4.0"},
      {"name": "is_available", "operator": "=", "value": "true"}
    ]
  }
}
```

### High-Volume Sales Products
```json
{
  "dataset_id": "gd_m45m1u911dsa4274pi",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "bought_past_month", "operator": ">", "value": "1000"},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "rating", "operator": ">=", "value": "4.0"},
      {"name": "categories", "operator": "array_includes", "value": "Electronics"}
    ]
  }
}
```

### Brand Analysis
```json
{
  "dataset_id": "gd_m45m1u911dsa4274pi",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "brand", "operator": "in", "value": ["Apple", "Samsung", "Sony"]},
      {"name": "department", "operator": "=", "value": "Electronics"},
      {"name": "is_available", "operator": "=", "value": "true"},
      {"name": "final_price", "operator": ">", "value": "100"}
    ]
  }
}
```

### Products with Delivery Constraints
```json
{
  "dataset_id": "gd_m45m1u911dsa4274pi",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "availability", "operator": "in", "value": ["only", "within", "limited", "unavailable"]},
      {"name": "bought_past_month", "operator": ">", "value": "500"},
      {"name": "rating", "operator": ">=", "value": "4.0"},
      {"name": "is_available", "operator": "=", "value": "true"}
    ]
  }
}
```

## Data Types Summary

### Field Data Types
- **Text fields**: title, brand, description, asin, parent_asin, input_asin, seller_name, seller_id, buybox_seller, department, manufacturer, model_number, upc, item_weight, product_dimensions, country_of_origin, top_review, date_first_available, domain, origin_url, ingredients, badge, root_bs_category, bs_category, customer_says, seller_url
- **Price fields**: initial_price, final_price, final_price_high
- **Number fields**: reviews_count, answered_questions, images_count, video_count, rating, root_bs_rank, bs_rank, number_of_sellers, bought_past_month
- **Boolean fields**: is_available, plus_content, video, amazon_choice, climate_pledge_friendly
- **Array fields**: categories, images, videos, downloadable_videos, features, product_details, product_description, variations, delivery, format, other_sellers_prices, subcategory_rank, sustainability_features, from_the_brand
- **Object fields**: buybox_prices, prices_breakdown
- **URL fields**: image_url, url

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

### Product Research
- Analyze product performance and market trends
- Study pricing strategies and promotional activities
- Research product categories and competition

### Market Analysis
- Track product availability and stock levels
- Monitor seller performance and marketplace dynamics
- Analyze consumer preferences and buying patterns

### Competitive Intelligence
- Compare product offerings and pricing
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
11. Sales data (bought_past_month) reflects recent purchasing activity
12. Price information is updated in real-time based on current marketplace conditions

## Dataset Source
This dataset is provided by [Brightdata](https://brightdata.com/products/datasets/amazon-products) and contains real-time product data from Amazon for analysis and research purposes. The dataset ID for this Amazon Products dataset is `gd_m45m1u911dsa4274pi`.