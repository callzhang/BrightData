# Amazon Walmart Dataset - Field Descriptions

This document describes the fields available in the Brightdata Amazon Walmart Dataset for programmatic filtering and analysis using the [Brightdata Marketplace Dataset API](https://docs.brightdata.com/api-reference/marketplace-dataset-api/filter-dataset).

## Dataset Overview
The Amazon Walmart Dataset provides comprehensive product comparison data between Amazon and Walmart, including product details, pricing, availability, and seller information from both platforms. This dataset enables competitive analysis, market research, and cross-platform product monitoring.

**Key Features:**
- **100+ total fields** covering both Amazon and Walmart data
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
- **`title_amazon`** (text): Product title on Amazon
- **`brand_amazon`** (text): Product brand on Amazon
- **`description_amazon`** (text): Brief description of the product
- **`seller_name_amazon`** (text): Seller name on Amazon
- **`asin_amazon`** (text): Unique identifier for each product
- **`categories_amazon`** (array): Product categories
- **`images_count_amazon`** (number): Number of images
- **`video_count_amazon`** (number): Number of videos
- **`amazon_choice_amazon`** (boolean): Specifies if the product is Amazon's Choice

### Walmart-Specific Fields (with `_walmart` suffix)
- **`rating_walmart`** (number): Walmart product rating (1-5)
- **`final_price_walmart`** (number): Walmart final price
- **`review_count_walmart`** (number): Number of Walmart reviews
- **`available_for_delivery_walmart`** (boolean): Walmart delivery availability
- **`available_for_pickup_walmart`** (boolean): Walmart pickup availability
- **`product_name_walmart`** (text): The name of the product
- **`brand_walmart`** (text): Product brand on Walmart
- **`description_walmart`** (text): Product description on Walmart
- **`product_id_walmart`** (text): The unique identifier of the product
- **`sku_walmart`** (text): Stock Keeping Unit (SKU) for product identification
- **`categories_walmart`** (array): Product categories on Walmart

## Complete Field Descriptions

### Amazon Fields (with `_amazon` suffix)

#### Basic Product Information
- **`title_amazon`** (text): Product title on Amazon
- **`brand_amazon`** (text): Product brand on Amazon
- **`description_amazon`** (text): Brief description of the product
- **`asin_amazon`** (text): Unique identifier for each product (Amazon Standard Identification Number)
- **`parent_asin_amazon`** (text): Parent ASIN of the product
- **`input_asin_amazon`** (text): Input ASIN (currently inactive)

#### Pricing Information
- **`initial_price_amazon`** (price): Initial price before discounts
- **`final_price_amazon`** (price): Final price of the product
- **`final_price_high_amazon`** (price): Highest value of the final price when it is a range
- **`currency_amazon`** (text): Currency of the product
- **`discount_amazon`** (text): Product discount information

#### Seller Information
- **`seller_name_amazon`** (text): Seller name on Amazon
- **`seller_id_amazon`** (text): Unique identifier for each seller
- **`buybox_seller_amazon`** (text): Seller in the buy box
- **`number_of_sellers_amazon`** (number): Number of sellers for the product

#### Product Details
- **`categories_amazon`** (array): Product categories
- **`department_amazon`** (text): Department to which the product belongs
- **`manufacturer_amazon`** (text): Manufacturer of the product
- **`model_number_amazon`** (text): Model number of the product
- **`upc_amazon`** (text): Universal Product Code
- **`item_weight_amazon`** (text): Weight of the product
- **`product_dimensions_amazon`** (text): Dimensions of the product
- **`country_of_origin_amazon`** (text): Country of origin of the product

#### Reviews and Ratings
- **`rating_amazon`** (number): Product rating
- **`reviews_count_amazon`** (number): Number of reviews
- **`answered_questions_amazon`** (number): Number of answered questions
- **`top_review_amazon`** (text): Top review for the product

#### Availability and Sales
- **`availability_amazon`** (text): Product availability
- **`is_available_amazon`** (boolean): Indication if the product is still available
- **`bought_past_month_amazon`** (number): Number of units bought in the past month

#### Rankings and Categories
- **`root_bs_rank_amazon`** (number): Best sellers rank in the general category
- **`bs_rank_amazon`** (number): Best seller rank in the specific category
- **`root_bs_category_amazon`** (text): Best seller root category
- **`bs_category_amazon`** (text): Best seller category
- **`subcategory_rank_amazon`** (array): Subcategory ranking information

#### Media and Content
- **`images_count_amazon`** (number): Number of images
- **`images_amazon`** (array): URLs of the product images
- **`image_url_amazon`** (url): URL that links directly to the product image
- **`video_count_amazon`** (number): Number of videos
- **`video_amazon`** (boolean): Boolean indicating the presence of videos
- **`videos_amazon`** (array): URLs of the product's videos
- **`downloadable_videos_amazon`** (array): Downloadable video information

#### Product Features and Details
- **`features_amazon`** (array): Product features
- **`product_details_amazon`** (array): Full product details
- **`product_description_amazon`** (array): Detailed product description
- **`variations_amazon`** (array): Details about the same product in different variations
- **`delivery_amazon`** (array): Delivery-related information
- **`format_amazon`** (array): Format-related information

#### Pricing and Buy Box
- **`buybox_prices_amazon`** (object): Product price details
- **`prices_breakdown_amazon`** (object): Detailed price breakdown
- **`other_sellers_prices_amazon`** (array): Other sellers details who sell the product

#### Additional Information
- **`date_first_available_amazon`** (text): Date when the product first became available
- **`domain_amazon`** (url): URL of the product domain
- **`url_amazon`** (url): URL that links directly to the product
- **`origin_url_amazon`** (url): Original URL
- **`seller_url_amazon`** (url): Seller URL
- **`ingredients_amazon`** (text): Ingredients of the product, relevant mostly for food products
- **`plus_content_amazon`** (boolean): Boolean indicating the presence of additional content
- **`amazon_choice_amazon`** (boolean): Specifies if the product is Amazon's Choice
- **`badge_amazon`** (text): Product badge (e.g., #1 Best Seller or Amazon's Choice)
- **`climate_pledge_friendly_amazon`** (boolean): Climate pledge friendly status
- **`sustainability_features_amazon`** (array): Sustainability features
- **`from_the_brand_amazon`** (array): Brand-specific information
- **`customer_says_amazon`** (text): Customer feedback summary

### Walmart Fields (with `_walmart` suffix)

#### Basic Product Information
- **`product_name_walmart`** (text): The name of the product
- **`brand_walmart`** (text): Product brand on Walmart
- **`description_walmart`** (text): Product description on Walmart
- **`product_id_walmart`** (text): The unique identifier of the product
- **`sku_walmart`** (text): Stock Keeping Unit (SKU) for product identification
- **`gtin_walmart`** (text): Global Trade Item Number (GTIN) for product identification
- **`upc_walmart`** (text): Universal Product Code (UPC) of the product

#### Pricing Information
- **`final_price_walmart`** (price): Price of the product
- **`initial_price_walmart`** (number): The price before the discount if exists
- **`currency_walmart`** (text): Currency used for the product price
- **`discount_walmart`** (text): The discount in value or percentage
- **`unit_price_walmart`** (number): The unit price of the product
- **`unit_walmart`** (text): The unit of measurement for the product

#### Product Details
- **`categories_walmart`** (array): Product categories on Walmart
- **`category_name_walmart`** (text): The name of the category associated with the product
- **`category_path_walmart`** (text): The path of the category associated with the product
- **`category_ids_walmart`** (text): The category IDs associated with the product
- **`category_url_walmart`** (url): URL representing the category link associated with the product
- **`root_category_name_walmart`** (text): The name of the root category associated with the product
- **`root_category_url_walmart`** (url): URL link associated with the product

#### Reviews and Ratings
- **`rating_walmart`** (number): The overall rating of the product
- **`review_count_walmart`** (number): Number indicating the count of reviews for the product
- **`rating_stars_walmart`** (object): Object representing the distribution of ratings in stars, from one star to five stars
- **`top_reviews_walmart`** (object): Object representing top reviews, including negative and positive reviews
- **`customer_reviews_walmart`** (array): Array of objects representing customer reviews
- **`review_tags_walmart`** (array): Tags associated with product reviews

#### Availability and Delivery
- **`available_for_delivery_walmart`** (boolean): Boolean indicating product availability for delivery
- **`available_for_pickup_walmart`** (boolean): Boolean indicating product availability for pickup
- **`free_returns_walmart`** (text): Information about free returns for the product

#### Seller Information
- **`seller_walmart`** (text): Seller of the product

#### Product Variations
- **`sizes_walmart`** (array): The sizes available for the product
- **`colors_walmart`** (array): The colors available for the product

#### Media and Images
- **`image_urls_walmart`** (array): Array of URLs representing product images
- **`main_image_walmart`** (image): The main product image

#### Product Specifications
- **`specifications_walmart`** (array): Array of objects representing product specifications
- **`other_attributes_walmart`** (array): Array of objects representing other attributes
- **`nutrition_information_walmart`** (array): Nutrition information
- **`ingredients_walmart`** (text): Ingredients of the product, relevant for food products mostly
- **`ingredients_full_walmart`** (array): Full ingredients information

#### Navigation and Links
- **`url_walmart`** (url): URL representing the product link
- **`breadcrumbs_walmart`** (array): Array of objects representing breadcrumb links
- **`related_pages_walmart`** (array): Array of related pages associated with the product

#### Additional Information
- **`aisle_walmart`** (text): The aisle where the product is located
- **`tags_walmart`** (array): Tags associated with the product

### Cross-Platform Comparison Fields
- **`price_difference`** (number): Amazon final price - Walmart final price
  - *Example*: 2.50, -1.25, 0.00
  - *Filtering examples*:
    ```json
    {"name": "price_difference", "operator": ">", "value": "0"}
    {"name": "price_difference", "operator": "<", "value": "0"}
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
      {"name": "is_available_amazon", "operator": "=", "value": "true"},
      {"name": "available_for_delivery_walmart", "operator": "=", "value": "true"},
      {"name": "currency_amazon", "operator": "=", "value": "USD"}
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
      {"name": "rating_amazon", "operator": ">=", "value": "4.5"},
      {"name": "rating_walmart", "operator": ">=", "value": "4.5"},
      {"name": "is_available_amazon", "operator": "=", "value": "true"},
      {"name": "available_for_delivery_walmart", "operator": "=", "value": "true"},
      {"name": "categories_amazon", "operator": "array_includes", "value": "Electronics"}
    ]
  }
}
```

### Amazon-Specific Analysis
```json
{
  "dataset_id": "gd_m4l6s4mn2g2rkx9lia",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "department_amazon", "operator": "=", "value": "Electronics"},
      {"name": "is_available_amazon", "operator": "=", "value": "true"},
      {"name": "bought_past_month_amazon", "operator": ">", "value": "100"}
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
      {"name": "price_difference", "operator": ">", "value": "10"},
      {"name": "is_available_amazon", "operator": "=", "value": "true"},
      {"name": "available_for_delivery_walmart", "operator": "=", "value": "true"},
      {"name": "brand_amazon", "operator": "=", "value": "brand_walmart"}
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
      {"name": "brand_amazon", "operator": "in", "value": ["Apple", "Samsung", "Sony"]},
      {"name": "department_amazon", "operator": "=", "value": "Electronics"},
      {"name": "is_available_amazon", "operator": "=", "value": "true"},
      {"name": "available_for_delivery_walmart", "operator": "=", "value": "true"}
    ]
  }
}
```

## Data Types Summary

### Amazon Fields Data Types
- **Text fields**: title_amazon, brand_amazon, description_amazon, asin_amazon, parent_asin_amazon, input_asin_amazon, seller_name_amazon, seller_id_amazon, buybox_seller_amazon, department_amazon, manufacturer_amazon, model_number_amazon, upc_amazon, item_weight_amazon, product_dimensions_amazon, country_of_origin_amazon, top_review_amazon, date_first_available_amazon, domain_amazon, origin_url_amazon, ingredients_amazon, badge_amazon, root_bs_category_amazon, bs_category_amazon, customer_says_amazon, seller_url_amazon
- **Price fields**: initial_price_amazon, final_price_amazon, final_price_high_amazon
- **Number fields**: reviews_count_amazon, answered_questions_amazon, images_count_amazon, video_count_amazon, rating_amazon, root_bs_rank_amazon, bs_rank_amazon, number_of_sellers_amazon, bought_past_month_amazon
- **Boolean fields**: is_available_amazon, plus_content_amazon, video_amazon, amazon_choice_amazon, climate_pledge_friendly_amazon
- **Array fields**: categories_amazon, images_amazon, videos_amazon, downloadable_videos_amazon, features_amazon, product_details_amazon, product_description_amazon, variations_amazon, delivery_amazon, format_amazon, other_sellers_prices_amazon, subcategory_rank_amazon, sustainability_features_amazon, from_the_brand_amazon
- **Object fields**: buybox_prices_amazon, prices_breakdown_amazon
- **URL fields**: image_url_amazon, url_amazon

### Walmart Fields Data Types
- **Text fields**: product_name_walmart, brand_walmart, description_walmart, product_id_walmart, sku_walmart, gtin_walmart, upc_walmart, currency_walmart, discount_walmart, unit_walmart, category_name_walmart, category_path_walmart, category_ids_walmart, root_category_name_walmart, seller_walmart, aisle_walmart, ingredients_walmart, free_returns_walmart
- **Price fields**: final_price_walmart, initial_price_walmart, unit_price_walmart
- **Number fields**: review_count_walmart, rating_walmart
- **Boolean fields**: available_for_delivery_walmart, available_for_pickup_walmart
- **Array fields**: categories_walmart, image_urls_walmart, customer_reviews_walmart, review_tags_walmart, sizes_walmart, colors_walmart, specifications_walmart, other_attributes_walmart, nutrition_information_walmart, ingredients_full_walmart, breadcrumbs_walmart, related_pages_walmart, tags_walmart
- **Object fields**: rating_stars_walmart, top_reviews_walmart
- **URL fields**: category_url_walmart, root_category_url_walmart, url_walmart
- **Image fields**: main_image_walmart

### Cross-Platform Fields Data Types
- **Number fields**: price_difference

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
