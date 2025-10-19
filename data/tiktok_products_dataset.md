# TikTok Products Dataset

## Overview

The TikTok Products dataset provides comprehensive product data from TikTok Shop, the social commerce platform integrated with TikTok, including pricing, reviews, seller information, and detailed product specifications. This dataset is ideal for social commerce analysis, influencer marketing, and e-commerce strategy in the social media era.

## Dataset Information

- **Dataset ID**: `gd_lk122xxgf86xf97py`
- **Source**: [BrightData TikTok Products](https://brightdata.com/cp/datasets/browse/gd_lk122xxgf86xf97py)
- **Update Frequency**: Daily
- **Data Volume**: Millions of products
- **Coverage**: Global TikTok Shop marketplaces
- **Data Quality**: High-quality, verified product data
- **Cost**: $0.002 per product

## Use Cases

### 🛒 **Social Commerce Analysis**
- **Social Commerce Trends**: Analyze product trends in social commerce
- **Influencer Marketing**: Track products promoted by influencers
- **Viral Products**: Identify trending and viral products
- **Social Engagement**: Analyze product engagement metrics

### 📊 **Business Intelligence**
- **Social Commerce Strategy**: Develop social commerce strategies
- **Influencer Partnerships**: Identify potential influencer partnerships
- **Product Strategy**: Develop products for social commerce
- **Revenue Analysis**: Calculate potential revenue from social commerce

### 🔍 **Data Science & Analytics**
- **Viral Analysis**: Analyze what makes products go viral
- **Engagement Prediction**: Predict product engagement and success
- **Social Sentiment**: Analyze social sentiment around products
- **Trend Analysis**: Track social commerce trends and patterns

### 💰 **E-commerce Strategy**
- **Social Commerce Optimization**: Optimize product listings for social commerce
- **Influencer Strategy**: Develop influencer marketing strategies
- **Content Strategy**: Create content strategies for social commerce
- **Customer Insights**: Understand customer behavior in social commerce

## Complete Field Reference

### Product Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `url` | string | Product page URL | "https://www.tiktok.com/@shop/product/123" |
| `title` | string | Product name/title | "Viral Phone Case with LED Lights" |
| `description` | string | Product description | "Trendy phone case with LED lights" |
| `images` | array | URLs to product images | ["https://example.com/image1.jpg"] |
| `image_url` | string | Primary product image URL | "https://example.com/primary.jpg" |
| `images_count` | numeric | Number of product images | 5 |

### Pricing Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `initial_price` | numeric | Original/listed price | 29.99 |
| `final_price` | numeric | Current/sale price | 19.99 |
| `currency` | string | Currency code | "USD" |
| `discount` | numeric | Discount amount | 10.00 |
| `discount_percentage` | numeric | Discount percentage | 33.3 |

### Sales & Performance Metrics
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `units_sold` | numeric | Number of units sold | 5000 |
| `stock_availability` | string | Stock status | "In Stock" |
| `is_available` | boolean | Boolean availability status | true |
| `favorites_count` | numeric | Number of favorites/likes | 1000 |
| `views_count` | numeric | Number of product views | 50000 |

### Customer Feedback
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `rating` | numeric | Average rating (1-5) | 4.5 |
| `reviews_count` | numeric | Number of reviews | 2500 |
| `rating_distribution` | object | Breakdown of ratings by star | {"5": 1500, "4": 800, "3": 200} |

### Seller Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `seller_name` | string | Seller/shop name | "TrendyStore" |
| `shop_url` | string | Seller's shop URL | "https://www.tiktok.com/@shop/trendystore" |
| `seller_rating` | numeric | Seller's overall rating | 4.8 |
| `seller_reviews_count` | numeric | Number of seller reviews | 10000 |
| `seller_followers` | numeric | Number of seller followers | 50000 |

### Social Media Metrics
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `tiktok_views` | numeric | TikTok video views | 1000000 |
| `tiktok_likes` | numeric | TikTok video likes | 50000 |
| `tiktok_shares` | numeric | TikTok video shares | 10000 |
| `tiktok_comments` | numeric | TikTok video comments | 5000 |
| `hashtags` | array | Product hashtags | ["#viral", "#trending", "#phonecase"] |

### Product Categories & Classification
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `category` | string | Main product category | "Electronics" |
| `subcategory` | string | Product subcategory | "Phone Accessories" |
| `brand` | string | Product brand | "TrendyBrand" |
| `tags` | array | Product tags/keywords | ["phone case", "LED", "trendy"] |
| `attributes` | object | Product specifications | {"color": "Rainbow", "material": "Silicone"} |

### Geographic & Platform Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `country` | string | TikTok Shop country/market | "United States" |
| `region` | string | Geographic region | "North America" |
| `language` | string | Product language | "English" |
| `platform` | string | E-commerce platform | "TikTok Shop" |

### Timestamps & Metadata
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `created_at` | string | Product listing date | "2023-01-15T10:30:00Z" |
| `updated_at` | string | Last update timestamp | "2023-12-01T15:45:00Z" |
| `scraped_at` | string | Data collection timestamp | "2023-12-01T16:00:00Z" |

## Sample Queries

### 1. Viral Products with High Engagement
```yaml
filters:
  - field: "tiktok_views"
    operator: ">="
    value: 1000000
  - field: "tiktok_likes"
    operator: ">="
    value: 50000
  - field: "rating"
    operator: ">="
    value: 4.0
  - field: "is_available"
    operator: "="
    value: true
```

### 2. Trending Products in Electronics
```yaml
filters:
  - field: "category"
    operator: "="
    value: "Electronics"
  - field: "tiktok_views"
    operator: ">="
    value: 100000
  - field: "units_sold"
    operator: ">="
    value: 1000
  - field: "stock_availability"
    operator: "="
    value: "In Stock"
```

### 3. Products with High Social Engagement
```yaml
filters:
  - field: "tiktok_shares"
    operator: ">="
    value: 5000
  - field: "tiktok_comments"
    operator: ">="
    value: 1000
  - field: "favorites_count"
    operator: ">="
    value: 500
  - field: "is_available"
    operator: "="
    value: true
```

### 4. Top-Rated Sellers with Social Presence
```yaml
filters:
  - field: "seller_rating"
    operator: ">="
    value: 4.8
  - field: "seller_followers"
    operator: ">="
    value: 10000
  - field: "seller_reviews_count"
    operator: ">="
    value: 5000
```

### 5. Products with Specific Hashtags
```yaml
filters:
  - field: "hashtags"
    operator: "includes"
    value: "viral"
  - field: "tiktok_views"
    operator: ">="
    value: 500000
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
- **Terms Compliance**: Adheres to TikTok's terms of service
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

# Initialize TikTok dataset
filter_obj = BrightDataFilter("gd_lk122xxgf86xf97py")
```

### 2. Simple Query
```python
# Find viral products
filters = [
    {"field": "tiktok_views", "operator": ">=", "value": 1000000},
    {"field": "rating", "operator": ">=", "value": 4.0}
]

result = filter_obj.search_data(
    filter_obj=filters,
    records_limit=1000,
    title="Viral Products"
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
- **Social Metrics**: Use social engagement metrics for filtering
- **Category Focus**: Focus on specific product categories
- **Price Ranges**: Set realistic price ranges for the market
- **Availability**: Filter for available products only

### Data Analysis
- **Viral Analysis**: Analyze what makes products go viral
- **Engagement Trends**: Track engagement trends and patterns
- **Seller Analysis**: Analyze seller performance and strategies
- **Social Insights**: Understand social commerce dynamics

### Compliance
- **Data Usage**: Use data ethically and legally
- **Terms Respect**: Honor TikTok's terms of service
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

*This comprehensive dataset provides detailed TikTok Shop product data for social commerce analysis, influencer marketing, and e-commerce strategy. Use responsibly and in compliance with applicable terms of service.*
