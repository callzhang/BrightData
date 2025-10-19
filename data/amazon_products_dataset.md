# Amazon Products Dataset

## Overview

The Amazon Products dataset provides comprehensive product data from Amazon's marketplace, including pricing, reviews, availability, seller information, and detailed product specifications. This dataset is ideal for e-commerce analysis, competitive intelligence, price monitoring, and market research.

## Dataset Information

- **Dataset ID**: `gd_l7q7dkf244hwjntr0`
- **Source**: [BrightData Amazon Products](https://brightdata.com/cp/datasets/browse/gd_l7q7dkf244hwjntr0)
- **Update Frequency**: Daily
- **Data Volume**: Millions of products
- **Coverage**: Global Amazon marketplaces
- **Data Quality**: High-quality, verified product data
- **Cost**: $0.002 per product

## Use Cases

### 🛒 **E-commerce Analysis**
- **Product Research**: Analyze product performance, pricing trends, and market positioning
- **Competitive Intelligence**: Monitor competitor products, pricing strategies, and market share
- **Price Optimization**: Track price changes, identify pricing opportunities, and optimize profit margins
- **Inventory Management**: Monitor product availability, stock levels, and demand patterns

### 📊 **Market Research**
- **Category Analysis**: Study product categories, trends, and market dynamics
- **Brand Performance**: Analyze brand presence, pricing strategies, and market positioning
- **Customer Insights**: Understand customer preferences through reviews and ratings
- **Market Trends**: Track emerging products, seasonal patterns, and market shifts

### 💰 **Business Intelligence**
- **Revenue Analysis**: Calculate potential revenue from product sales
- **Profit Optimization**: Identify high-margin products and pricing opportunities
- **Market Sizing**: Estimate market size and growth potential
- **Investment Decisions**: Support product development and market entry strategies

### 🔍 **Data Science & Analytics**
- **Sentiment Analysis**: Analyze customer reviews for product insights
- **Recommendation Systems**: Build product recommendation engines
- **Price Prediction**: Develop models to predict price changes
- **Market Segmentation**: Segment products and customers for targeted strategies

## Complete Field Reference

### Core Product Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `title` | string | Product title/name | "iPhone 15 Pro 128GB" |
| `asin` | string | Unique Amazon identifier | "B0CHX1W1XY" |
| `parent_asin` | string | Parent ASIN for variations | "B0CHX1W1XY" |
| `brand` | string | Product brand | "Apple" |
| `description` | string | Product description | "Latest iPhone with advanced features" |
| `categories` | array | Product categories | ["Electronics", "Cell Phones"] |

### Pricing Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `initial_price` | numeric | Original/listed price | 999.99 |
| `final_price` | numeric | Current/sale price | 899.99 |
| `final_price_high` | numeric | Highest price in range | 999.99 |
| `currency` | string | Currency code | "USD" |
| `discount` | string | Discount information | "20% off" |

### Reviews & Ratings
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `rating` | numeric | Average rating (1-5) | 4.5 |
| `reviews_count` | numeric | Number of reviews | 1250 |
| `answered_questions` | numeric | Answered questions count | 45 |
| `top_review` | string | Top review text | "Great product, highly recommend!" |

### Sales & Performance
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `bought_past_month` | numeric | Units bought last month | 150 |
| `availability` | string | Stock status | "In Stock" |
| `is_available` | boolean | Boolean availability | true |

### Seller Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `seller_name` | string | Seller name | "Amazon.com" |
| `seller_id` | string | Unique seller identifier | "ATVPDKIKX0DER" |
| `seller_url` | string | Seller profile URL | "https://amazon.com/seller/ATVPDKIKX0DER" |
| `buybox_seller` | string | Buy box seller | "Amazon.com" |
| `number_of_sellers` | numeric | Total sellers for product | 5 |

### Rankings & Performance
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `bs_rank` | numeric | Best seller rank in category | 150 |
| `root_bs_rank` | numeric | Best seller rank overall | 25 |
| `bs_category` | string | Best seller category | "Electronics" |
| `root_bs_category` | string | Root best seller category | "Electronics" |

### Media & Content
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `url` | string | Product page URL | "https://amazon.com/dp/B0CHX1W1XY" |
| `domain` | string | Product domain | "amazon.com" |
| `image_url` | string | Primary product image | "https://images.amazon.com/image.jpg" |
| `images` | array | All product images | ["https://images.amazon.com/image1.jpg"] |
| `images_count` | numeric | Number of images | 5 |
| `video` | boolean | Has videos | true |
| `video_count` | numeric | Number of videos | 2 |

### Product Details
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `department` | string | Product department | "Electronics" |
| `item_weight` | string | Product weight | "1.2 lbs" |
| `product_dimensions` | string | Product dimensions | "6.1 x 2.8 x 0.3 inches" |
| `model_number` | string | Model number | "A3108" |
| `manufacturer` | string | Manufacturer | "Apple" |
| `upc` | string | Universal Product Code | "194253000000" |
| `country_of_origin` | string | Country of origin | "USA" |
| `date_first_available` | string | First available date | "2023-01-15" |

### Features & Content
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `features` | array | Product features | ["5G", "Face ID", "Wireless Charging"] |
| `product_details` | array | Detailed specifications | [{"type": "Weight", "value": "1.2 lbs"}] |
| `plus_content` | boolean | Has additional content | true |

### Amazon-Specific Features
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `amazon_choice` | boolean | Amazon's Choice badge | true |
| `amazon_prime` | boolean | Prime eligible | true |
| `badge` | string | Product badge | "#1 Best Seller" |
| `sponsered` | boolean | Sponsored product | false |
| `climate_pledge_friendly` | boolean | Climate pledge friendly | true |

### Delivery & Shipping
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `delivery` | array | Delivery options | ["Free shipping", "Prime delivery"] |
| `ships_from` | string | Shipping location | "Amazon Fulfillment Center" |

## Sample Queries

### 1. Find Electronics Under $100
```yaml
filters:
  - field: "department"
    operator: "="
    value: "Electronics"
  - field: "final_price"
    operator: "<="
    value: 100
  - field: "is_available"
    operator: "="
    value: true
```

### 2. High-Rated Products with Many Reviews
```yaml
filters:
  - field: "rating"
    operator: ">="
    value: 4.5
  - field: "reviews_count"
    operator: ">="
    value: 1000
  - field: "availability"
    operator: "="
    value: "In Stock"
```

### 3. Amazon's Choice Products
```yaml
filters:
  - field: "amazon_choice"
    operator: "="
    value: true
  - field: "amazon_prime"
    operator: "="
    value: true
  - field: "final_price"
    operator: "<="
    value: 500
```

### 4. Best Sellers in Specific Category
```yaml
filters:
  - field: "bs_category"
    operator: "="
    value: "Electronics"
  - field: "bs_rank"
    operator: "<="
    value: 100
  - field: "rating"
    operator: ">="
    value: 4.0
```

### 5. Products with Discounts
```yaml
filters:
  - field: "discount"
    operator: "!="
    value: null
  - field: "final_price"
    operator: "<"
    value: "initial_price"
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
- **Terms Compliance**: Adheres to Amazon's terms of service
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

# Initialize Amazon dataset
filter_obj = BrightDataFilter("gd_l7q7dkf244hwjntr0")
```

### 2. Simple Query
```python
# Find electronics under $100
filters = [
    {"field": "department", "operator": "=", "value": "Electronics"},
    {"field": "final_price", "operator": "<=", "value": 100}
]

result = filter_obj.search_data(
    filter_obj=filters,
    records_limit=1000,
    title="Electronics Under $100"
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
- **Specific Categories**: Use precise category filters
- **Price Ranges**: Set realistic price ranges
- **Availability**: Filter for available products only
- **Rating Thresholds**: Use minimum rating requirements

### Data Analysis
- **Price Analysis**: Track price trends and patterns
- **Review Analysis**: Analyze customer sentiment
- **Category Trends**: Monitor category performance
- **Brand Analysis**: Track brand performance and positioning

### Compliance
- **Data Usage**: Use data ethically and legally
- **Terms Respect**: Honor Amazon's terms of service
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

*This comprehensive dataset provides detailed Amazon product data for e-commerce analysis, competitive intelligence, and market research. Use responsibly and in compliance with applicable terms of service.*