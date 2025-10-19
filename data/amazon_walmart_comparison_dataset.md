# Amazon-Walmart Comparison Dataset

## Overview

The Amazon-Walmart Comparison dataset provides cross-platform product comparison data between Amazon and Walmart marketplaces, enabling comprehensive competitive analysis, price comparison, and market intelligence across two of the largest e-commerce platforms.

## Dataset Information

- **Dataset ID**: `gd_m4l6s4mn2g2rkx9lia`
- **Source**: [BrightData Amazon-Walmart Comparison](https://brightdata.com/cp/datasets/browse/gd_m4l6s4mn2g2rkx9lia)
- **Update Frequency**: Daily
- **Data Volume**: Millions of product comparisons
- **Coverage**: Global Amazon and Walmart marketplaces
- **Data Quality**: High-quality, verified cross-platform data
- **Cost**: $0.002 per comparison

## Use Cases

### 🏪 **Cross-Platform Analysis**
- **Price Comparison**: Compare prices between Amazon and Walmart for the same products
- **Market Share Analysis**: Understand market presence across platforms
- **Competitive Intelligence**: Monitor competitor strategies and positioning
- **Price Optimization**: Identify pricing opportunities and gaps

### 📊 **Business Intelligence**
- **Revenue Analysis**: Calculate potential revenue from cross-platform sales
- **Profit Optimization**: Identify high-margin opportunities across platforms
- **Market Sizing**: Estimate total addressable market across platforms
- **Investment Decisions**: Support multi-platform expansion strategies

### 🔍 **Data Science & Analytics**
- **Price Prediction**: Develop models to predict cross-platform price changes
- **Market Segmentation**: Segment products and customers across platforms
- **Trend Analysis**: Track cross-platform trends and patterns
- **Recommendation Systems**: Build multi-platform recommendation engines

### 💰 **E-commerce Strategy**
- **Platform Selection**: Choose optimal platforms for product launches
- **Pricing Strategy**: Develop competitive pricing strategies
- **Inventory Management**: Optimize inventory across platforms
- **Marketing Strategy**: Develop platform-specific marketing approaches

## Complete Field Reference

### Platform Identification
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `platform` | string | E-commerce platform | "Amazon" |
| `product_id` | string | Platform-specific product ID | "B0849MZ45Y" |

### Core Product Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `title` | string | Product name | "Vital Farms, Large Grade A Eggs, 12 Count" |
| `brand` | string | Product brand | "VITAL FARMS" |
| `description` | string | Product description | "Pasture raised eggs from happy hens" |
| `categories` | array | Product categories | ["Grocery & Gourmet Food", "Eggs"] |

### Pricing Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `initial_price` | numeric | Original price | 8.49 |
| `final_price` | numeric | Current price | 8.49 |
| `currency` | string | Currency code | "USD" |
| `discount` | numeric | Discount amount | 0.00 |

### Availability & Stock
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `availability` | string | Stock status | "In Stock" |
| `is_available` | boolean | Boolean availability | true |

### Seller Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `seller_name` | string | Seller name | "Amazon.com" |
| `seller_id` | string | Unique seller identifier | "ATVPDKIKX0DER" |
| `is_fulfilled_by_platform` | boolean | Platform fulfillment | true |

### Customer Reviews & Ratings
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `reviews_count` | numeric | Number of reviews | 9024 |
| `rating` | numeric | Average rating (1-5) | 4.9 |

### Product Details & Specifications
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `item_weight` | string | Product weight | "1.77 Pounds" |
| `product_dimensions` | string | Product dimensions | "0.39 x 0.39 x 0.5 inches" |
| `model_number` | string | Model number | "u-4c-7501" |
| `manufacturer` | string | Manufacturer | "VITAL FARMS" |
| `department` | string | Product department | "Grocery & Gourmet Food" |
| `upc` | string | Universal Product Code | "861745000010" |

### Media & Images
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `images` | array | Product image URLs | ["https://example.com/image1.jpg"] |
| `images_count` | numeric | Number of images | 11 |
| `image_url` | string | Primary image URL | "https://example.com/primary.jpg" |

### Best Sellers & Rankings
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `best_seller_rank` | numeric | Best seller rank | 18745 |
| `category_rank` | numeric | Category rank | 40 |
| `best_seller_category` | string | Best seller category | "Grocery & Gourmet Food" |

### Additional Product Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `date_first_available` | string | First available date | "December 12, 2023" |
| `url` | string | Product URL | "https://www.amazon.com/product" |
| `domain` | string | Platform domain | "https://www.amazon.com/" |

### Amazon-Specific Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `title_amazon` | string | Amazon product title | "iPhone 15 Pro" |
| `seller_name_amazon` | string | Amazon seller name | "Amazon.com" |
| `brand_amazon` | string | Amazon product brand | "Apple" |
| `description_amazon` | string | Amazon product description | "Latest iPhone with advanced features" |
| `initial_price_amazon` | numeric | Amazon initial price | 999.99 |
| `currency_amazon` | string | Amazon currency | "USD" |
| `availability_amazon` | string | Amazon availability | "In Stock" |
| `reviews_count_amazon` | numeric | Amazon reviews count | 1250 |
| `categories_amazon` | array | Amazon categories | ["Electronics", "Cell Phones"] |
| `asin_amazon` | string | Amazon ASIN | "B0CHX1W1XY" |
| `parent_asin_amazon` | string | Amazon parent ASIN | "B0CHX1W1XY" |
| `rating_amazon` | numeric | Amazon rating | 4.5 |
| `final_price_amazon` | numeric | Amazon final price | 899.99 |
| `bought_past_month_amazon` | numeric | Amazon bought past month | 150 |
| `is_available_amazon` | boolean | Amazon is available | true |
| `amazon_choice_amazon` | boolean | Amazon's Choice | true |

### Walmart-Specific Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `url_walmart` | string | Walmart product URL | "https://walmart.com/ip/product/123" |
| `final_price_walmart` | numeric | Walmart final price | 799.99 |
| `sku_walmart` | string | Walmart SKU | "123456789" |
| `currency_walmart` | string | Walmart currency | "USD" |
| `brand_walmart` | string | Walmart brand | "Apple" |
| `product_name_walmart` | string | Walmart product name | "iPhone 15 Pro" |
| `rating_walmart` | numeric | Walmart rating | 4.3 |
| `review_count_walmart` | numeric | Walmart review count | 850 |
| `available_for_delivery_walmart` | boolean | Walmart available for delivery | true |
| `available_for_pickup_walmart` | boolean | Walmart available for pickup | true |

### Cross-Platform Comparison Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `price_difference` | numeric | Amazon final price - Walmart final price | 99.99 |

### Complex Data Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `product_details` | array | Structured product details | [{"type": "Weight", "value": "1.77 lbs"}] |
| `variations` | array | Product variations | [{"color": "Red", "size": "Large"}] |
| `features` | array | Product features | ["Organic", "Free Range"] |
| `delivery` | array | Delivery options | ["Free shipping", "Prime delivery"] |

## Sample Queries

### 1. Price Comparison Analysis
```yaml
filters:
  - field: "price_difference"
    operator: ">"
    value: 0
  - field: "is_available_amazon"
    operator: "="
    value: true
  - field: "available_for_delivery_walmart"
    operator: "="
    value: true
```

### 2. High-Rated Products on Both Platforms
```yaml
filters:
  - field: "rating_amazon"
    operator: ">="
    value: 4.5
  - field: "rating_walmart"
    operator: ">="
    value: 4.5
  - field: "reviews_count_amazon"
    operator: ">="
    value: 100
  - field: "review_count_walmart"
    operator: ">="
    value: 100
```

### 3. Amazon's Choice vs Walmart Availability
```yaml
filters:
  - field: "amazon_choice_amazon"
    operator: "="
    value: true
  - field: "available_for_delivery_walmart"
    operator: "="
    value: true
  - field: "final_price_amazon"
    operator: "<="
    value: 500
```

### 4. Products with Significant Price Differences
```yaml
filters:
  - field: "price_difference"
    operator: ">="
    value: 50
  - field: "currency_amazon"
    operator: "="
    value: "USD"
  - field: "currency_walmart"
    operator: "="
    value: "USD"
```

### 5. Cross-Platform Best Sellers
```yaml
filters:
  - field: "best_seller_rank"
    operator: "<="
    value: 1000
  - field: "category_rank"
    operator: "<="
    value: 100
  - field: "is_available_amazon"
    operator: "="
    value: true
  - field: "available_for_delivery_walmart"
    operator: "="
    value: true
```

## Data Quality & Privacy

### Data Quality
- **Cross-Platform Verification**: Products verified across both platforms
- **Price Accuracy**: Real-time price comparison validation
- **Availability Sync**: Synchronized availability status
- **Data Completeness**: High completeness across all fields

### Privacy Compliance
- **Public Data Only**: Only publicly available product information
- **No Personal Data**: No customer personal information included
- **Terms Compliance**: Adheres to both Amazon and Walmart terms of service
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
- **Per Record**: $0.002 per comparison
- **Bulk Discounts**: Available for large volumes
- **Enterprise**: Custom pricing for enterprise clients

### Example Costs
| Records | Cost | Use Case |
|---------|------|----------|
| 1,000 | $2.00 | Small comparison analysis |
| 10,000 | $20.00 | Category comparison study |
| 100,000 | $200.00 | Market comparison analysis |
| 1,000,000 | $2,000.00 | Comprehensive market study |

## Getting Started

### 1. Basic Setup
```python
from util import BrightDataFilter

# Initialize Amazon-Walmart dataset
filter_obj = BrightDataFilter("gd_m4l6s4mn2g2rkx9lia")
```

### 2. Simple Query
```python
# Find products with price differences
filters = [
    {"field": "price_difference", "operator": ">", "value": 0},
    {"field": "is_available_amazon", "operator": "=", "value": True}
]

result = filter_obj.search_data(
    filter_obj=filters,
    records_limit=1000,
    title="Products with Price Differences"
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
- **Platform Filtering**: Use platform-specific filters
- **Price Ranges**: Set realistic price ranges for both platforms
- **Availability**: Filter for available products on both platforms
- **Rating Thresholds**: Use minimum rating requirements

### Data Analysis
- **Price Analysis**: Track cross-platform price trends
- **Market Share**: Analyze platform market presence
- **Competitive Analysis**: Monitor cross-platform strategies
- **Opportunity Identification**: Find pricing and availability gaps

### Compliance
- **Data Usage**: Use data ethically and legally
- **Terms Respect**: Honor both Amazon and Walmart terms of service
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

*This comprehensive dataset provides cross-platform product comparison data for competitive analysis, market intelligence, and business strategy. Use responsibly and in compliance with applicable terms of service.*
