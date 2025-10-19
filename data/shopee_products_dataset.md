# Shopee Products Dataset

## Overview

The Shopee Products dataset provides comprehensive product data from Shopee, Southeast Asia's leading e-commerce platform, including pricing, reviews, seller information, and detailed product specifications. This dataset is ideal for Southeast Asian market analysis, competitive intelligence, and e-commerce strategy.

## Dataset Information

- **Dataset ID**: `gd_lk122xxgf86xf97py`
- **Source**: [BrightData Shopee Products](https://brightdata.com/cp/datasets/browse/gd_lk122xxgf86xf97py)
- **Update Frequency**: Daily
- **Data Volume**: Millions of products
- **Coverage**: Southeast Asian Shopee marketplaces
- **Data Quality**: High-quality, verified product data
- **Cost**: $0.002 per product

## Use Cases

### 🛒 **Southeast Asian E-commerce Analysis**
- **Market Research**: Analyze product trends and market dynamics in Southeast Asia
- **Competitive Intelligence**: Monitor competitor products and pricing strategies
- **Price Optimization**: Track price changes and identify pricing opportunities
- **Category Analysis**: Study product categories and market segments

### 📊 **Business Intelligence**
- **Market Entry**: Support market entry strategies for Southeast Asian markets
- **Product Strategy**: Develop product strategies for regional markets
- **Revenue Analysis**: Calculate potential revenue from Southeast Asian sales
- **Investment Decisions**: Support regional expansion and investment decisions

### 🔍 **Data Science & Analytics**
- **Sentiment Analysis**: Analyze customer reviews for product insights
- **Recommendation Systems**: Build product recommendation engines
- **Price Prediction**: Develop models to predict price changes
- **Market Segmentation**: Segment products and customers for targeted strategies

### 💰 **E-commerce Strategy**
- **Platform Optimization**: Optimize product listings and strategies
- **Inventory Management**: Monitor product availability and demand
- **Marketing Strategy**: Develop targeted marketing approaches
- **Customer Insights**: Understand customer preferences and behavior

## Complete Field Reference

### Product Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `url` | string | Product page URL | "https://shopee.sg/product/123" |
| `title` | string | Product name/title | "iPhone 15 Pro 128GB" |
| `description` | string | Product description | "Latest iPhone with advanced features" |
| `images` | array | URLs to product images | ["https://example.com/image1.jpg"] |
| `image_url` | string | Primary product image URL | "https://example.com/primary.jpg" |
| `images_count` | numeric | Number of product images | 5 |

### Pricing Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `initial_price` | numeric | Original/listed price | 999.99 |
| `final_price` | numeric | Current/sale price | 899.99 |
| `currency` | string | Currency code | "SGD" |
| `discount` | numeric | Discount amount | 100.00 |
| `discount_percentage` | numeric | Discount percentage | 10.0 |

### Sales & Performance Metrics
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `units_sold` | numeric | Number of units sold | 1500 |
| `stock_availability` | string | Stock status | "In Stock" |
| `is_available` | boolean | Boolean availability status | true |
| `favorites_count` | numeric | Number of favorites/likes | 250 |
| `views_count` | numeric | Number of product views | 5000 |

### Customer Feedback
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `rating` | numeric | Average rating (1-5) | 4.5 |
| `reviews_count` | numeric | Number of reviews | 1250 |
| `rating_distribution` | object | Breakdown of ratings by star | {"5": 800, "4": 300, "3": 100} |

### Seller Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `seller_name` | string | Seller/shop name | "TechStore SG" |
| `shop_url` | string | Seller's shop URL | "https://shopee.sg/shop/123" |
| `seller_rating` | numeric | Seller's overall rating | 4.8 |
| `seller_reviews_count` | numeric | Number of seller reviews | 5000 |
| `seller_followers` | numeric | Number of seller followers | 10000 |

### Product Categories & Classification
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `category` | string | Main product category | "Electronics" |
| `subcategory` | string | Product subcategory | "Cell Phones" |
| `brand` | string | Product brand | "Apple" |
| `tags` | array | Product tags/keywords | ["smartphone", "5G", "camera"] |
| `attributes` | object | Product specifications | {"color": "Blue", "storage": "128GB"} |

### Geographic & Platform Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `country` | string | Shopee country/market | "Singapore" |
| `region` | string | Geographic region | "Southeast Asia" |
| `language` | string | Product language | "English" |
| `platform` | string | E-commerce platform | "Shopee" |

### Timestamps & Metadata
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `created_at` | string | Product listing date | "2023-01-15T10:30:00Z" |
| `updated_at` | string | Last update timestamp | "2023-12-01T15:45:00Z" |
| `scraped_at` | string | Data collection timestamp | "2023-12-01T16:00:00Z" |

## Sample Queries

### 1. High-Rated Electronics
```yaml
filters:
  - field: "category"
    operator: "="
    value: "Electronics"
  - field: "rating"
    operator: ">="
    value: 4.5
  - field: "reviews_count"
    operator: ">="
    value: 100
  - field: "is_available"
    operator: "="
    value: true
```

### 2. Best-Selling Products in Singapore
```yaml
filters:
  - field: "country"
    operator: "="
    value: "Singapore"
  - field: "units_sold"
    operator: ">="
    value: 1000
  - field: "rating"
    operator: ">="
    value: 4.0
  - field: "stock_availability"
    operator: "="
    value: "In Stock"
```

### 3. Products with Discounts
```yaml
filters:
  - field: "discount_percentage"
    operator: ">="
    value: 20
  - field: "is_available"
    operator: "="
    value: true
  - field: "final_price"
    operator: "<="
    value: 100
```

### 4. Top-Rated Sellers
```yaml
filters:
  - field: "seller_rating"
    operator: ">="
    value: 4.8
  - field: "seller_reviews_count"
    operator: ">="
    value: 1000
  - field: "seller_followers"
    operator: ">="
    value: 5000
```

### 5. Trending Products
```yaml
filters:
  - field: "views_count"
    operator: ">="
    value: 10000
  - field: "favorites_count"
    operator: ">="
    value: 500
  - field: "rating"
    operator: ">="
    value: 4.0
  - field: "is_available"
    operator: "="
    value: true
```

## Data Quality & Privacy

### Data Quality
- **Verification**: Products are verified for authenticity
- **Completeness**: High data completeness scores
- **Freshness**: Daily updates ensure current information
- **Accuracy**: Multiple validation layers ensure data accuracy

### Privacy Compliance
- **Public Data Only**: Only publicly available product information
- **No Personal Data**: No customer personal information included
- **Terms Compliance**: Adheres to Shopee's terms of service
- **Data Retention**: Follows data retention policies

## Technical Specifications

### Data Format
- **Format**: JSON/CSV
- **Encoding**: UTF-8
- **Compression**: Optional GZIP compression
- **Batch Size**: Configurable (default: 1000 records)

### API Endpoints
- **Search**: `/datasets/filter`
- **Download**: `/datasets/snapshots/{id}/download`
- **Metadata**: `/datasets/snapshots/{id}`

### Rate Limits
- **Requests**: 1000 requests/hour
- **Data Volume**: 1M records/day
- **Concurrent**: 5 simultaneous requests

## Pricing

### Cost Structure
- **Per Record**: $0.002 per product
- **Bulk Discounts**: Available for large volumes
- **Enterprise**: Custom pricing for enterprise clients

### Example Costs
| Records | Cost | Use Case |
|---------|------|----------|
| 1,000 | $2.00 | Small product analysis |
| 10,000 | $20.00 | Category research |
| 100,000 | $200.00 | Market analysis |
| 1,000,000 | $2,000.00 | Comprehensive market study |

## Getting Started

### 1. Basic Setup
```python
from util import BrightDataFilter

# Initialize Shopee dataset
filter_obj = BrightDataFilter("gd_lk122xxgf86xf97py")
```

### 2. Simple Query
```python
# Find electronics in Singapore
filters = [
    {"field": "category", "operator": "=", "value": "Electronics"},
    {"field": "country", "operator": "=", "value": "Singapore"}
]

result = filter_obj.search_data(
    filter_obj=filters,
    records_limit=1000,
    title="Electronics in Singapore"
)
```

### 3. Download Results
```python
# Download when ready
response = filter_obj.download_snapshot_content(
    snapshot_id=result,
    format='json'
)
```

## Best Practices

### Query Optimization
- **Country Filtering**: Use specific country filters for targeted analysis
- **Category Focus**: Focus on specific product categories
- **Price Ranges**: Set realistic price ranges for the market
- **Availability**: Filter for available products only

### Data Analysis
- **Market Trends**: Track product trends and patterns
- **Seller Analysis**: Analyze seller performance and strategies
- **Price Analysis**: Monitor price trends and opportunities
- **Customer Insights**: Understand customer preferences through reviews

### Compliance
- **Data Usage**: Use data ethically and legally
- **Terms Respect**: Honor Shopee's terms of service
- **Purpose Limitation**: Use data for stated purposes only
- **Retention**: Follow data retention policies

## Support & Resources

### Documentation
- **API Reference**: Complete API documentation
- **Query Examples**: Sample queries and use cases
- **Integration Guides**: Step-by-step setup instructions

### Support Channels
- **Technical Support**: 24/7 technical assistance
- **Data Quality**: Data validation and quality assurance
- **Custom Solutions**: Tailored data solutions

### Community
- **Developer Forum**: Community support and discussions
- **Best Practices**: Shared knowledge and insights
- **Case Studies**: Real-world implementation examples

---

*This comprehensive dataset provides detailed Shopee product data for Southeast Asian market analysis, competitive intelligence, and e-commerce strategy. Use responsibly and in compliance with applicable terms of service.*
