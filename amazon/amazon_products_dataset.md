# Amazon Products Dataset - Field Descriptions

This document describes the fields available in the Brightdata Amazon Products Dataset for programmatic filtering and analysis using the [Brightdata Marketplace Dataset API](https://docs.brightdata.com/api-reference/marketplace-dataset-api/filter-dataset).

## Dataset Overview
The Amazon Products Dataset provides comprehensive product information from Amazon, including product details, pricing, reviews, seller information, and marketplace data. This dataset contains real-time Amazon product data for analysis and research purposes.

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
  "dataset_id": "gd_l7q7dkf244hwjntr0",
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

## Field Descriptions

Based on the actual CSV data structure, here are the available fields:

### Core Product Information
- **`title`** (string): The name of the product as listed on Amazon
  - *Example*: "Vital Farms, Large Grade A Eggs, 12 Count"
  - *Filtering examples*: 
    ```json
    {"name": "title", "operator": "includes", "value": "iPhone"}
    {"name": "title", "operator": "=", "value": "Vital Farms, Large Grade A Eggs, 12 Count"}
    ```

- **`asin`** (string): Amazon Standard Identification Number - unique identifier for each product
  - *Example*: "B0849MZ45Y"
  - *Filtering examples*:
    ```json
    {"name": "asin", "operator": "=", "value": "B0849MZ45Y"}
    {"name": "asin", "operator": "in", "value": ["B0849MZ45Y", "B0CQ2XTP5F"]}
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
  - *Example*: "In Stock", "Out of Stock"
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
  - *Example*: "Amazon.com", "Kcule®", "Ama***.co***"
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

- **`buybox_seller`** (string): The seller who currently holds the buy box
  - *Example*: "Kcule®", "Amazon.com"
  - *Filtering examples*:
    ```json
    {"name": "buybox_seller", "operator": "=", "value": "Amazon.com"}
    ```

- **`number_of_sellers`** (integer): Number of sellers offering this product
  - *Example*: 1, 5, 10
  - *Filtering examples*:
    ```json
    {"name": "number_of_sellers", "operator": ">", "value": "1"}
    ```

### Customer Reviews & Ratings
- **`reviews_count`** (integer): The total number of reviews the product has received
  - *Example*: 9024, 1039, 1214
  - *Filtering examples*:
    ```json
    {"name": "reviews_count", "operator": ">", "value": "100"}
    {"name": "reviews_count", "operator": ">=", "value": "1000"}
    ```

- **`bought_past_month`** (number): Number of units bought in the past month - key metric for analyzing recent sales trends
  - *Example*: 150, 500, 1200
  - *Fill Rate*: 1.39%
  - *Filtering examples*:
    ```json
    {"name": "bought_past_month", "operator": ">=", "value": "100"}
    {"name": "bought_past_month", "operator": ">", "value": "500"}
    {"name": "bought_past_month", "operator": "is_not_null", "value": null}
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
- **`root_bs_rank`** (integer): Best seller rank in the root category
  - *Example*: null, 18745, 5557
  - *Filtering examples*:
    ```json
    {"name": "root_bs_rank", "operator": "is_not_null", "value": null}
    {"name": "root_bs_rank", "operator": "<=", "value": "10000"}
    ```

- **`bs_rank`** (integer): Best seller rank in the specific category
  - *Example*: 40, 6
  - *Filtering examples*:
    ```json
    {"name": "bs_rank", "operator": "<=", "value": "100"}
    ```

- **`root_bs_category`** (string): Root best seller category
  - *Example*: "Clothing, Shoes & Jewelry", "Baby"
  - *Filtering examples*:
    ```json
    {"name": "root_bs_category", "operator": "=", "value": "Electronics"}
    ```

- **`bs_category`** (string): Best seller category
  - *Example*: "Luggage Tags", "Baby & Toddler Smoothies"
  - *Filtering examples*:
    ```json
    {"name": "bs_category", "operator": "includes", "value": "Electronics"}
    ```

### Additional Product Information
- **`date_first_available`** (string): Date when the product was first available on Amazon
  - *Example*: "December 12, 2023"
  - *Filtering examples*:
    ```json
    {"name": "date_first_available", "operator": "is_not_null", "value": null}
    ```

- **`url`** (string): Amazon product URL
  - *Example*: "https://www.amazon.com/VITAL-FARMS-Large-Grade-Eggs/dp/B0849MZ45Y"
  - *Filtering examples*:
    ```json
    {"name": "url", "operator": "is_not_null", "value": null}
    ```

- **`domain`** (string): Amazon domain
  - *Example*: "https://www.amazon.com/"
  - *Filtering examples*:
    ```json
    {"name": "domain", "operator": "=", "value": "https://www.amazon.com/"}
    ```

- **`upc`** (string): Universal Product Code
  - *Example*: "861745000010", "052159703288"
  - *Filtering examples*:
    ```json
    {"name": "upc", "operator": "is_not_null", "value": null}
    ```

### Complex Data Fields
- **`product_details`** (array): Structured product details (JSON array of objects)
  - *Example*: [{"type": "Product Dimensions", "value": "0.39 x 0.39 x 0.5 inches; 1.77 Pounds"}, ...]
  - *Filtering examples*:
    ```json
    {"name": "product_details", "operator": "is_not_null", "value": null}
    ```

- **`variations`** (array): Product variations (colors, sizes, etc.) (JSON array of objects)
  - *Example*: [{"asin": "B0CP65BYKJ", "color": "Classic Square-black", ...}, ...]
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

### Combining Multiple Conditions
```json
{
  "dataset_id": "gd_l7q7dkf244hwjntr0",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "rating", "operator": ">=", "value": "4.0"},
      {"name": "reviews_count", "operator": ">", "value": "100"},
      {"name": "availability", "operator": "=", "value": "In Stock"},
      {"name": "currency", "operator": "=", "value": "USD"}
    ]
  }
}
```

### High-Rated Products with Discounts
```json
{
  "dataset_id": "gd_l7q7dkf244hwjntr0",
  "records_limit": 500,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "rating", "operator": ">=", "value": "4.5"},
      {"name": "discount", "operator": "is_not_null", "value": null},
      {"name": "categories", "operator": "array_includes", "value": "Electronics"}
    ]
  }
}
```

### Brand-Specific Products
```json
{
  "dataset_id": "gd_l7q7dkf244hwjntr0",
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

### Products with Multiple Sellers
```json
{
  "dataset_id": "gd_l7q7dkf244hwjntr0",
  "records_limit": 1000,
  "filter": {
    "operator": "and",
    "filters": [
      {"name": "number_of_sellers", "operator": ">", "value": "1"},
      {"name": "buybox_seller", "operator": "!=", "value": "Amazon.com"}
    ]
  }
}
```

## Data Types Summary
- **String fields**: title, asin, brand, description, currency, availability, seller_name, seller_id, buybox_seller, item_weight, product_dimensions, model_number, manufacturer, department, root_bs_category, bs_category, date_first_available, url, domain, upc
- **Numeric fields**: initial_price, final_price, discount, reviews_count, rating, images_count, number_of_sellers, root_bs_rank, bs_rank, bought_past_month, answered_questions, video_count, max_quantity_available
- **Boolean fields**: is_available, plus_content, video, amazon_choice, climate_pledge_friendly, premium_brand, amazon_prime
- **Array fields**: categories, images, product_details, variations, features, delivery, videos, other_sellers_prices, editorial_reviews, sustainability_features
- **Object fields**: buybox_prices, prices_breakdown, customers_say, variations_values, return_policy

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

## Using the bought_past_month Field

The `bought_past_month` field is particularly valuable for analyzing recent sales trends and identifying trending products. Here are some practical use cases:

### Finding Trending Products (High Recent Sales)
```json
{
  "dataset_id": "gd_l7q7dkf244hwjntr0",
  "records_limit": 1000,
  "filter": {
    "operator": "AND",
    "filters": [
      {"name": "bought_past_month", "operator": ">=", "value": "100"},
      {"name": "rating", "operator": ">=", "value": "4.0"},
      {"name": "final_price", "operator": "<=", "value": "200"},
      {"name": "is_available", "operator": "=", "value": "true"}
    ]
  }
}
```

### Finding Products with Recent Sales Data Available
```json
{
  "dataset_id": "gd_l7q7dkf244hwjntr0",
  "records_limit": 1000,
  "filter": {
    "operator": "AND",
    "filters": [
      {"name": "bought_past_month", "operator": "is_not_null", "value": null},
      {"name": "bought_past_month", "operator": ">", "value": "0"},
      {"name": "rating", "operator": ">=", "value": "4.5"}
    ]
  }
}
```

### Finding High-Volume Recent Sales
```json
{
  "dataset_id": "gd_l7q7dkf244hwjntr0",
  "records_limit": 1000,
  "filter": {
    "operator": "AND",
    "filters": [
      {"name": "bought_past_month", "operator": ">", "value": "500"},
      {"name": "reviews_count", "operator": ">=", "value": "1000"},
      {"name": "rating", "operator": ">=", "value": "4.0"}
    ]
  }
}
```

**Note**: `bought_past_month` has a 1.39% fill rate, so use `is_not_null` to filter for products with this data.

## Dataset Source
This dataset is provided by [Brightdata](https://brightdata.com/products/datasets/amazon/product) and contains real-time Amazon product data for analysis and research purposes. The dataset ID for this Amazon products dataset is `gd_l7q7dkf244hwjntr0`.