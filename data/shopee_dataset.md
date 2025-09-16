# Shopee Products Dataset Documentation

## Overview

The Shopee Products Dataset provides comprehensive product information from the Shopee e-commerce platform, enabling detailed market analysis, competitive intelligence, and business strategy development. This dataset is particularly valuable for understanding Southeast Asian e-commerce trends and consumer behavior.

**Dataset ID:** `gd_lk122xxgf86xf97py`  
**Platform:** Shopee  
**Data Source:** [BrightData Shopee Dataset](https://brightdata.com/cp/datasets/browse/gd_lk122xxgf86xf97py?id=hl_a6e6d183)  
**Update Frequency:** Daily, Weekly, Monthly, or Custom  
**Data Formats:** JSON, NDJSON, JSON Lines, CSV, Parquet (with optional .gz compression)

## Dataset Fields

### Product Information
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `url` | String | Product page URL | `https://shopee.sg/product/123456` |
| `title` | String | Product name/title | `"Wireless Bluetooth Headphones"` |
| `description` | String | Product description | `"High-quality wireless headphones with noise cancellation"` |
| `images` | Array | URLs to product images | `["https://img1.jpg", "https://img2.jpg"]` |
| `image_url` | String | Primary product image URL | `"https://img1.jpg"` |
| `images_count` | Numeric | Number of product images | `5` |

### Pricing Information
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `initial_price` | Numeric | Original/listed price | `99.99` |
| `final_price` | Numeric | Current/sale price | `79.99` |
| `currency` | String | Currency code | `"SGD"` |
| `discount` | Numeric | Discount amount | `20.00` |
| `discount_percentage` | Numeric | Discount percentage | `20.0` |

### Sales & Performance Metrics
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `units_sold` | Numeric | Number of units sold | `1250` |
| `stock_availability` | String | Stock status | `"In Stock"` |
| `is_available` | Boolean | Boolean availability status | `true` |
| `favorites_count` | Numeric | Number of favorites/likes | `342` |
| `views_count` | Numeric | Number of product views | `5678` |

### Customer Feedback
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `rating` | Numeric | Average rating (1-5) | `4.5` |
| `reviews_count` | Numeric | Number of reviews | `89` |
| `rating_distribution` | Object | Breakdown of ratings by star | `{"5": 45, "4": 30, "3": 10, "2": 3, "1": 1}` |

### Seller Information
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `seller_name` | String | Seller/shop name | `"TechStore SG"` |
| `shop_url` | String | Seller's shop URL | `"https://shopee.sg/techstore-sg"` |
| `seller_rating` | Numeric | Seller's overall rating | `4.8` |
| `seller_reviews_count` | Numeric | Number of seller reviews | `1250` |
| `seller_followers` | Numeric | Number of seller followers | `5000` |

### Product Categories & Classification
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `category` | String | Main product category | `"Electronics"` |
| `subcategory` | String | Product subcategory | `"Audio & Headphones"` |
| `brand` | String | Product brand | `"Sony"` |
| `tags` | Array | Product tags/keywords | `["wireless", "bluetooth", "noise-cancelling"]` |
| `attributes` | Object | Product specifications | `{"color": "black", "weight": "250g"}` |

### Geographic & Platform Information
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `country` | String | Shopee country/market | `"Singapore"` |
| `region` | String | Geographic region | `"Southeast Asia"` |
| `language` | String | Product language | `"English"` |
| `platform` | String | E-commerce platform | `"Shopee"` |

### Timestamps & Metadata
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `created_at` | String | Product listing date | `"2024-01-15T10:30:00Z"` |
| `updated_at` | String | Last update timestamp | `"2024-01-20T14:45:00Z"` |
| `scraped_at` | String | Data collection timestamp | `"2024-01-21T09:15:00Z"` |

## API Usage

### Basic Filtering Examples

```python
from util import BrightDataFilter, SHOPEE_FIELDS as SF, get_brightdata_api_key

# Initialize the filter for Shopee dataset
api_key = get_brightdata_api_key()
shopee_filter = BrightDataFilter(api_key, "gd_lk122xxgf86xf97py")

# Find high-rated electronics
high_rated_electronics = (
    SF.rating >= 4.5 &
    SF.category == "Electronics" &
    SF.final_price < 100 &
    SF.is_available.is_true()
)

# Find best-selling products
best_sellers = (
    SF.units_sold > 1000 &
    SF.rating >= 4.0 &
    SF.favorites_count > 100
)

# Find products with discounts
discounted_products = (
    SF.discount_percentage > 20 &
    SF.final_price > 10 &
    SF.is_available.is_true()
)
```

### Advanced Filtering Examples

```python
# Find trending products (high views, good ratings)
trending_products = (
    SF.views_count > 5000 &
    SF.rating >= 4.0 &
    SF.units_sold > 500 &
    SF.favorites_count > 200
)

# Find products from top-rated sellers
top_seller_products = (
    SF.seller_rating >= 4.8 &
    SF.seller_reviews_count > 1000 &
    SF.rating >= 4.0 &
    SF.is_available.is_true()
)

# Find products in specific price ranges
mid_range_products = (
    SF.final_price.in_range(50, 200) &
    SF.rating >= 4.0 &
    SF.category.in_list(["Electronics", "Fashion", "Home & Living"])
)
```

## Use Cases

### 1. Market Analysis
- **Product Performance:** Analyze which products are performing well based on sales, ratings, and customer engagement
- **Price Trends:** Monitor pricing strategies and discount patterns across different categories
- **Category Insights:** Understand market dynamics within specific product categories

### 2. Competitive Intelligence
- **Competitor Monitoring:** Track competitors' product offerings, pricing, and customer feedback
- **Market Positioning:** Identify gaps in the market and opportunities for new products
- **Pricing Strategy:** Compare pricing across similar products to optimize your own pricing

### 3. Customer Behavior Analysis
- **Review Analysis:** Understand customer preferences and pain points through review data
- **Purchase Patterns:** Analyze what drives customer purchases (ratings, price, seller reputation)
- **Seasonal Trends:** Identify seasonal patterns in product performance and pricing

### 4. Seller Performance Analysis
- **Seller Rankings:** Identify top-performing sellers based on ratings, sales, and customer satisfaction
- **Seller Strategies:** Analyze successful sellers' product selection and pricing strategies
- **Partnership Opportunities:** Find potential partners or suppliers with strong performance metrics

### 5. Product Development
- **Market Research:** Identify popular product features and specifications
- **Gap Analysis:** Find underserved market segments or product categories
- **Feature Prioritization:** Understand which product attributes drive customer satisfaction

## Data Quality & Considerations

### Data Completeness
- **High Coverage:** The dataset provides comprehensive coverage of Shopee's product catalog
- **Regular Updates:** Data is updated frequently to ensure accuracy and currency
- **Quality Assurance:** BrightData implements quality checks to ensure data reliability

### Geographic Coverage
- **Multi-Market:** Covers multiple Southeast Asian markets where Shopee operates
- **Localized Data:** Includes country-specific information and local market dynamics
- **Currency Support:** Handles multiple currencies used across different markets

### Limitations
- **Platform Specific:** Data is limited to Shopee platform only
- **Historical Data:** Limited historical data availability depending on subscription
- **Data Volume:** Large datasets may require significant storage and processing resources

## Integration Examples

### E-commerce Analytics Dashboard
```python
# Create comprehensive product analytics
def analyze_shopee_market():
    # High-performing products
    top_products = (
        SF.rating >= 4.5 &
        SF.units_sold > 1000 &
        SF.favorites_count > 500
    )
    
    # Emerging trends
    trending = (
        SF.views_count > 10000 &
        SF.rating >= 4.0 &
        SF.created_at >= "2024-01-01"
    )
    
    # Price analysis
    price_analysis = (
        SF.final_price.in_range(10, 500) &
        SF.discount_percentage > 0 &
        SF.is_available.is_true()
    )
    
    return {
        'top_products': shopee_filter.search_data(top_products, 100),
        'trending': shopee_filter.search_data(trending, 100),
        'price_analysis': shopee_filter.search_data(price_analysis, 1000)
    }
```

### Competitive Monitoring System
```python
# Monitor competitor products
def monitor_competitors(brand_name):
    competitor_products = (
        SF.brand == brand_name &
        SF.rating >= 4.0 &
        SF.is_available.is_true()
    )
    
    # Analyze pricing strategy
    pricing_strategy = (
        SF.brand == brand_name &
        SF.discount_percentage > 0 &
        SF.final_price > 0
    )
    
    return {
        'products': shopee_filter.search_data(competitor_products, 500),
        'pricing': shopee_filter.search_data(pricing_strategy, 500)
    }
```

## Best Practices

### 1. Data Filtering
- **Use Specific Criteria:** Apply multiple filters to narrow down results to relevant products
- **Consider Data Freshness:** Use timestamp filters to ensure you're working with recent data
- **Validate Results:** Always validate filter results against expected outcomes

### 2. Performance Optimization
- **Limit Results:** Use appropriate record limits to avoid overwhelming your system
- **Batch Processing:** Process large datasets in batches for better performance
- **Cache Results:** Cache frequently accessed data to reduce API calls

### 3. Data Analysis
- **Cross-Reference:** Combine Shopee data with other datasets for comprehensive analysis
- **Trend Analysis:** Look for patterns over time rather than single data points
- **Statistical Validation:** Use statistical methods to validate your findings

## Support & Resources

- **Documentation:** [BrightData Shopee Dataset Documentation](https://brightdata.com/products/datasets/shopee)
- **API Reference:** [BrightData API Documentation](https://docs.brightdata.com/)
- **Sample Data:** Request sample data to evaluate dataset quality before purchase
- **Support:** Contact BrightData support for technical assistance and custom requirements

## Conclusion

The Shopee Products Dataset provides a comprehensive foundation for e-commerce analysis, competitive intelligence, and market research in the Southeast Asian market. With its rich set of product, seller, and customer data, it enables businesses to make data-driven decisions and stay competitive in the dynamic e-commerce landscape.

The dataset's flexibility in terms of data formats, update frequencies, and customizable subsets makes it suitable for various use cases, from academic research to enterprise-level business intelligence applications.
