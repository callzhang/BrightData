# Amazon Walmart Dataset - Field Descriptions

This document describes the fields available in the Brightdata Amazon Walmart Dataset for programmatic filtering and analysis using the [Brightdata Marketplace Dataset API](https://docs.brightdata.com/api-reference/marketplace-dataset-api/filter-dataset).

## Dataset Overview
The Amazon Walmart Dataset provides comprehensive product comparison data between Amazon and Walmart, including product details, pricing, availability, and seller information from both platforms. This dataset enables competitive analysis, market research, and cross-platform product monitoring.

**Key Features:**
- **63 total fields** covering both Amazon and Walmart data
- **Platform-specific fields** with `_amazon` and `_walmart` suffixes
- **Cross-platform comparison** with `price_difference` field
- **Recent sales data** with `bought_past_month_amazon` field
- **Comprehensive coverage** of product information, pricing, reviews, and availability

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
  "dataset_id": "gd_m4l6s4mn2g2rkx9lia",
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

### Cross-Platform Comparison
- **`price_difference`** (number): Amazon final price - Walmart final price
  - *Example*: 99.99 (Amazon is $99.99 more expensive)
  - *Use case*: Identify pricing opportunities and competitive advantages

### Amazon-Specific Fields (with `_amazon` suffix)
- **`bought_past_month_amazon`** (number): Number of units bought on Amazon in the past month
  - *Example*: 150
  - *Use case*: Analyze recent sales trends and product popularity
- **`rating_amazon`** (number): Amazon product rating (1-5)
- **`final_price_amazon`** (number): Amazon final price
- **`reviews_count_amazon`** (number): Number of Amazon reviews
- **`is_available_amazon`** (boolean): Amazon availability status

### Walmart-Specific Fields (with `_walmart` suffix)
- **`rating_walmart`** (number): Walmart product rating (1-5)
- **`final_price_walmart`** (number): Walmart final price
- **`review_count_walmart`** (number): Number of Walmart reviews
- **`available_for_delivery_walmart`** (boolean): Walmart delivery availability
- **`available_for_pickup_walmart`** (boolean): Walmart pickup availability

## Field Descriptions

### Platform Identification
- **`platform`** (string): The e-commerce platform where the product is listed
  - *Example*: "Amazon", "Walmart"
  - *Filtering examples*:
    ```json
    {"name": "platform", "operator": "=", "value": "Amazon"}
    {"name": "platform", "operator": "in", "value": ["Amazon", "Walmart"]}
    ```

### Core Product Information
- **`title`** (string): The name of the product as listed on the platform
  - *Example*: "Vital Farms, Large Grade A Eggs, 12 Count"
  - *Filtering examples*:
    ```json
    {"name": "title", "operator": "includes", "value": "iPhone"}
    {"name": "title", "operator": "=", "value": "Vital Farms, Large Grade A Eggs, 12 Count"}
    ```

- **`product_id`** (string): Platform-specific product identifier
  - *Amazon*: ASIN (Amazon Standard Identification Number)
  - *Walmart*: Product ID
  - *Example*: "B0849MZ45Y", "12345678"
  - *Filtering examples*:
    ```json
    {"name": "product_id", "operator": "=", "value": "B0849MZ45Y"}
    {"name": "product_id", "operator": "in", "value": ["B0849MZ45Y", "12345678"]}
    ```

- **`brand`** (string): The brand associated with the product
  - *Example*: "VITAL FARMS", "KCULE", "Stonyfield Organic"
  - *Filtering examples*:
    ```json
    {"name": "brand", "operator": "=", "value": "VITAL FARMS"}
    {"name": "brand", "operator": "in", "value": ["KCULE", "Stonyfield Organic"]}
    ```

- **`description`** (string): Detailed description of the product
  - *Example*: "Vital Farms alfresco pasture raised large grade a eggs are produced by happy, healthy hens..."
  - *Filtering examples*:
    ```json
    {"name": "description", "operator": "includes", "value": "organic"}
    {"name": "description", "operator": "includes", "value": "stainless steel"}
    ```

- **`categories`** (array): The category or categories under which the product is listed (JSON array format)
  - *Example*: ["Grocery & Gourmet Food", "Dairy, Eggs & Plant-Based Alternatives", "Eggs & Egg Substitutes", "Whole Eggs"]
  - *Filtering examples*:
    ```json
    {"name": "categories", "operator": "array_includes", "value": "Electronics"}
    {"name": "categories", "operator": "array_includes", "value": "Grocery & Gourmet Food"}
    ```

### Pricing Information
- **`initial_price`** (decimal): The original price of the product before any discounts
  - *Example*: 8.49, 9.98, 7.99
  - *Filtering examples*:
    ```json
    {"name": "initial_price", "operator": ">", "value": "100"}
    {"name": "initial_price", "operator": ">=", "value": "50"}
    ```

- **`final_price`** (decimal): The current/final price of the product
  - *Example*: 8.49, 9.98, 7.99
  - *Filtering examples*:
    ```json
    {"name": "final_price", "operator": "<=", "value": "200"}
    {"name": "final_price", "operator": "=", "value": "8.49"}
    ```

- **`currency`** (string): The currency in which the product is priced
  - *Example*: "USD"
  - *Filtering examples*:
    ```json
    {"name": "currency", "operator": "=", "value": "USD"}
    {"name": "currency", "operator": "in", "value": ["USD", "EUR", "GBP"]}
    ```

- **`discount`** (decimal): Any discount applied to the product's initial price
  - *Example*: null (no discount), 5.00 (discount amount)
  - *Filtering examples*:
    ```json
    {"name": "discount", "operator": ">", "value": "0"}
    {"name": "discount", "operator": "is_not_null", "value": null}
    ```

### Availability & Stock
- **`availability`** (string): The stock status of the product
  - *Example*: "In Stock", "Out of Stock", "Limited Stock"
  - *Filtering examples*:
    ```json
    {"name": "availability", "operator": "=", "value": "In Stock"}
    {"name": "availability", "operator": "!=", "value": "Out of Stock"}
    ```

- **`is_available`** (boolean): Boolean flag indicating if the product is available
  - *Example*: true, false
  - *Filtering examples*:
    ```json
    {"name": "is_available", "operator": "=", "value": "true"}
    ```

### Seller Information
- **`seller_name`** (string): The name of the seller offering the product
  - *Amazon*: "Amazon.com", "Kcule®", "Ama***.co***"
  - *Walmart*: "Walmart", "Third Party Seller"
  - *Filtering examples*:
    ```json
    {"name": "seller_name", "operator": "=", "value": "Amazon.com"}
    {"name": "seller_name", "operator": "includes", "value": "Amazon"}
    ```

- **`seller_id`** (string): A unique identifier for the seller
  - *Example*: "ATVPDKIKX0DER", "A2VDSVO2R3Q720"
  - *Filtering examples*:
    ```json
    {"name": "seller_id", "operator": "=", "value": "ATVPDKIKX0DER"}
    ```

- **`is_fulfilled_by_platform`** (boolean): Whether the product is fulfilled by the platform (Amazon/Walmart)
  - *Example*: true, false
  - *Filtering examples*:
    ```json
    {"name": "is_fulfilled_by_platform", "operator": "=", "value": "true"}
    ```

### Customer Reviews & Ratings
- **`reviews_count`** (integer): The total number of reviews the product has received
  - *Example*: 9024, 1039, 1214
  - *Filtering examples*:
    ```json
    {"name": "reviews_count", "operator": ">", "value": "100"}
    {"name": "reviews_count", "operator": ">=", "value": "1000"}
    ```

- **`rating`** (decimal): The average rating given to the product by customers (typically 1-5 scale)
  - *Example*: 4.9, 4.8, 4.5
  - *Filtering examples*:
    ```json
    {"name": "rating", "operator": ">=", "value": "4.0"}
    {"name": "rating", "operator": ">", "value": "4.5"}
    ```

### Product Details & Specifications
- **`item_weight`** (string): Weight of the product
  - *Example*: "1.77 Pounds", "1.2 ounces", "37.2 Ounces"
  - *Filtering examples*:
    ```json
    {"name": "item_weight", "operator": "is_not_null", "value": null}
    ```

- **`product_dimensions`** (string): Physical dimensions of the product
  - *Example*: "0.39 x 0.39 x 0.5 inches; 1.77 Pounds"
  - *Filtering examples*:
    ```json
    {"name": "product_dimensions", "operator": "is_not_null", "value": null}
    ```

- **`model_number`** (string): Model number of the product
  - *Example*: "u-4c-7501", "STEELTAG-SILVER-A"
  - *Filtering examples*:
    ```json
    {"name": "model_number", "operator": "is_not_null", "value": null}
    ```

- **`manufacturer`** (string): Manufacturer of the product
  - *Example*: "VITAL FARMS", "KCULE", "Stonyfield Organic"
  - *Filtering examples*:
    ```json
    {"name": "manufacturer", "operator": "=", "value": "VITAL FARMS"}
    ```

- **`department`** (string): Department/category of the product
  - *Example*: "Grocery & Gourmet Food", "Clothing, Shoes & Jewelry", "Baby Products"
  - *Filtering examples*:
    ```json
    {"name": "department", "operator": "=", "value": "Electronics"}
    ```

### Media & Images
- **`images`** (array): URLs or links to images of the product (JSON array)
  - *Example*: ["https://m.media-amazon.com/images/I/71zyUBNd3GL._SL1500_.jpg", ...]
  - *Filtering examples*:
    ```json
    {"name": "images", "operator": "is_not_null", "value": null}
    {"name": "images", "operator": "array_includes", "value": "https://"}
    ```

- **`images_count`** (integer): Number of product images available
  - *Example*: 11, 7, 10
  - *Filtering examples*:
    ```json
    {"name": "images_count", "operator": ">", "value": "5"}
    ```

- **`image_url`** (string): Primary image URL for the product
  - *Example*: "https://m.media-amazon.com/images/I/71zyUBNd3GL._SL1500_.jpg"
  - *Filtering examples*:
    ```json
    {"name": "image_url", "operator": "is_not_null", "value": null}
    ```

### Best Sellers & Rankings
- **`best_seller_rank`** (integer): Best seller rank in the category
  - *Example*: null, 18745, 5557
  - *Filtering examples*:
    ```json
    {"name": "best_seller_rank", "operator": "is_not_null", "value": null}
    {"name": "best_seller_rank", "operator": "<=", "value": "10000"}
    ```

- **`category_rank`** (integer): Rank within the specific category
  - *Example*: 40, 6
  - *Filtering examples*:
    ```json
    {"name": "category_rank", "operator": "<=", "value": "100"}
    ```

- **`best_seller_category`** (string): Best seller category
  - *Example*: "Clothing, Shoes & Jewelry", "Baby"
  - *Filtering examples*:
    ```json
    {"name": "best_seller_category", "operator": "=", "value": "Electronics"}
    ```

### Additional Product Information
- **`date_first_available`** (string): Date when the product was first available on the platform
  - *Example*: "December 12, 2023"
  - *Filtering examples*:
    ```json
    {"name": "date_first_available", "operator": "is_not_null", "value": null}
    ```

- **`url`** (string): Product URL on the platform
  - *Example*: "https://www.amazon.com/VITAL-FARMS-Large-Grade-Eggs/dp/B0849MZ45Y"
  - *Filtering examples*:
    ```json
    {"name": "url", "operator": "is_not_null", "value": null}
    ```

- **`domain`** (string): Platform domain
  - *Example*: "https://www.amazon.com/", "https://www.walmart.com/"
  - *Filtering examples*:
    ```json
    {"name": "domain", "operator": "=", "value": "https://www.amazon.com/"}
    {"name": "domain", "operator": "in", "value": ["https://www.amazon.com/", "https://www.walmart.com/"]}
    ```

- **`upc`** (string): Universal Product Code
  - *Example*: "861745000010", "052159703288"
  - *Filtering examples*:
    ```json
    {"name": "upc", "operator": "is_not_null", "value": null}
    ```

### Cross-Platform Comparison Fields
- **`price_difference`** (decimal): Price difference between Amazon and Walmart for the same product
  - *Example*: 2.50, -1.25, 0.00
  - *Filtering examples*:
    ```json
    {"name": "price_difference", "operator": ">", "value": "0"}
    {"name": "price_difference", "operator": "<", "value": "0"}
    ```

- **`price_difference_percentage`** (decimal): Percentage difference in price between platforms
  - *Example*: 15.5, -8.2, 0.0
  - *Filtering examples*:
    ```json
    {"name": "price_difference_percentage", "operator": ">", "value": "10"}
    ```

- **`availability_match`** (boolean): Whether the product is available on both platforms
  - *Example*: true, false
  - *Filtering examples*:
    ```json
    {"name": "availability_match", "operator": "=", "value": "true"}
    ```

- **`brand_match`** (boolean): Whether the same brand is available on both platforms
  - *Example*: true, false
  - *Filtering examples*:
    ```json
    {"name": "brand_match", "operator": "=", "value": "true"}
    ```

### Complex Data Fields
- **`product_details`** (array): Structured product details (JSON array of objects)
  - *Example*: [{"type": "Product Dimensions", "value": "0.39 x 0.39 x 0.5 inches; 1.77 Pounds"}, ...]
  - *Filtering examples*:
    ```json
    {"name": "product_details", "operator": "is_not_null", "value": null}
    ```

- **`variations`** (array): Product variations (colors, sizes, etc.) (JSON array of objects)
  - *Example*: [{"product_id": "B0CP65BYKJ", "color": "Classic Square-black", ...}, ...]
  - *Filtering examples*:
    ```json
    {"name": "variations", "operator": "is_not_null", "value": null}
    ```

- **`features`** (array): Product features (JSON array)
  - *Example*: ["MADE WITH FRESH AIR AND SUNSHINE Our hens are tended by hand on small family farms in the USA.", ...]
  - *Filtering examples*:
    ```json
    {"name": "features", "operator": "array_includes", "value": "organic"}
    ```

- **`delivery`** (array): Delivery options (JSON array)
  - *Example*: ["$9.95 for 2-hour delivery with Prime", "$4.99 delivery August 22 - 27."]
  - *Filtering examples*:
    ```json
    {"name": "delivery", "operator": "array_includes", "value": "Prime"}
    ```

## Complex Filtering Examples

### Cross-Platform Price Comparison
```json
{
  "dataset_id": "gd_m4l6s4mn2g2rkx9lia",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "price_difference", "operator": ">", "value": "0"},
      {"name": "availability_match", "operator": "=", "value": "true"},
      {"name": "currency", "operator": "=", "value": "USD"}
    ]
  }
}
```

### High-Rated Products Available on Both Platforms
```json
{
  "dataset_id": "gd_m4l6s4mn2g2rkx9lia",
  "records_limit": 500,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "rating", "operator": ">=", "value": "4.5"},
      {"name": "availability_match", "operator": "=", "value": "true"},
      {"name": "categories", "operator": "array_includes", "value": "Electronics"}
    ]
  }
}
```

### Platform-Specific Analysis
```json
{
  "dataset_id": "gd_m4l6s4mn2g2rkx9lia",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "platform", "operator": "=", "value": "Amazon"},
      {"name": "department", "operator": "=", "value": "Electronics"},
      {"name": "is_available", "operator": "=", "value": "true"}
    ]
  }
}
```

### Products with Significant Price Differences
```json
{
  "dataset_id": "gd_m4l6s4mn2g2rkx9lia",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "price_difference_percentage", "operator": ">", "value": "20"},
      {"name": "availability_match", "operator": "=", "value": "true"},
      {"name": "brand_match", "operator": "=", "value": "true"}
    ]
  }
}
```

### Brand Analysis Across Platforms
```json
{
  "dataset_id": "gd_m4l6s4mn2g2rkx9lia",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "brand", "operator": "in", "value": ["Apple", "Samsung", "Sony"]},
      {"name": "department", "operator": "=", "value": "Electronics"},
      {"name": "is_available", "operator": "=", "value": "true"}
    ]
  }
}
```

## Data Types Summary
- **String fields**: platform, title, product_id, brand, description, currency, availability, seller_name, seller_id, item_weight, product_dimensions, model_number, manufacturer, department, best_seller_category, date_first_available, url, domain, upc
- **Numeric fields**: initial_price, final_price, discount, reviews_count, rating, images_count, best_seller_rank, category_rank, price_difference, price_difference_percentage
- **Boolean fields**: is_available, is_fulfilled_by_platform, availability_match, brand_match
- **Array fields**: categories, images, product_details, variations, features, delivery
- **Object fields**: Complex nested structures for detailed product information

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

### Competitive Analysis
- Compare product offerings and pricing between Amazon and Walmart
- Identify market trends and competitive advantages
- Analyze product availability across platforms

### Market Research
- Study product descriptions and branding strategies
- Understand consumer preferences and market positioning
- Track pricing strategies and promotional activities

### Inventory Management
- Monitor product availability across platforms
- Optimize stock levels and supply chain decisions
- Identify products with high demand on both platforms

### Price Optimization
- Find products with significant price differences
- Identify opportunities for competitive pricing
- Track price changes over time across platforms

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
11. Cross-platform comparison fields are only available when both platforms have data for the same product
12. Price difference calculations are based on current prices at the time of data collection

## Dataset Source
This dataset is provided by [Brightdata](https://brightdata.com/products/datasets/amazon-walmart) and contains real-time product comparison data between Amazon and Walmart for analysis and research purposes. The dataset ID for this Amazon Walmart dataset is `gd_m4l6s4mn2g2rkx9lia`.
