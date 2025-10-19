# BrightData Datasets Overview

## Complete Dataset Catalog

This document provides a comprehensive overview of all available datasets in the BrightData platform, organized by category and use case.

## 📊 Dataset Summary

| Dataset | ID | Records | Fields | Cost/Record | Primary Use Case |
|---------|----|---------|---------|-------------|------------------|
| **Amazon Products** | `gd_l7q7dkf244hwjntr0` | Millions | 50+ | $0.002 | E-commerce Analysis |
| **Amazon-Walmart Comparison** | `gd_m4l6s4mn2g2rkx9lia` | Millions | 60+ | $0.002 | Cross-Platform Analysis |
| **Shopee Products** | `gd_lk122xxgf86xf97py` | Millions | 35+ | $0.002 | Southeast Asian Markets |
| **TikTok Products** | `gd_lk122xxgf86xf97py` | Millions | 40+ | $0.002 | Social Commerce |
| **Target Products** | `gd_lk122xxgf86xf97py` | Millions | 40+ | $0.002 | US Retail Analysis |
| **LinkedIn Profiles** | `gd_l1viktl72bvl7bjuj0` | Millions | 42 | $0.002 | Professional Networks |

## 🛒 E-commerce & Retail Datasets

### Amazon Products Dataset
- **Purpose**: Comprehensive Amazon marketplace analysis
- **Key Features**: Product data, pricing, reviews, seller information
- **Best For**: E-commerce analysis, competitive intelligence, price monitoring
- **Geographic Coverage**: Global Amazon marketplaces
- **Update Frequency**: Daily

### Amazon-Walmart Comparison Dataset
- **Purpose**: Cross-platform competitive analysis
- **Key Features**: Side-by-side product comparison, price differences
- **Best For**: Competitive intelligence, market positioning, pricing strategy
- **Geographic Coverage**: US marketplaces
- **Update Frequency**: Daily

### Target Products Dataset
- **Purpose**: US retail market analysis
- **Key Features**: Product data, pricing, store information
- **Best For**: Retail analysis, market research, competitive intelligence
- **Geographic Coverage**: US Target stores
- **Update Frequency**: Daily

## 🌏 Global E-commerce Datasets

### Shopee Products Dataset
- **Purpose**: Southeast Asian e-commerce analysis
- **Key Features**: Product data, pricing, seller information, regional metrics
- **Best For**: Southeast Asian market entry, regional analysis
- **Geographic Coverage**: Southeast Asian markets
- **Update Frequency**: Daily

### TikTok Products Dataset
- **Purpose**: Social commerce analysis
- **Key Features**: Product data, social engagement metrics, viral indicators
- **Best For**: Social commerce strategy, influencer marketing, viral analysis
- **Geographic Coverage**: Global TikTok Shop
- **Update Frequency**: Daily

## 👥 Professional Networks

### LinkedIn Profiles Dataset
- **Purpose**: Professional network analysis
- **Key Features**: Career history, skills, education, network metrics
- **Best For**: Talent acquisition, market research, business intelligence
- **Geographic Coverage**: Global LinkedIn network
- **Update Frequency**: Daily

## 🎯 Use Case Categories

### **E-commerce Analysis**
- Product performance tracking
- Competitive intelligence
- Price optimization
- Market trend analysis
- Customer behavior insights

### **Market Research**
- Industry analysis
- Market sizing
- Competitive landscape
- Regional market dynamics
- Consumer preferences

### **Business Intelligence**
- Revenue analysis
- Profit optimization
- Investment decisions
- Strategic planning
- Performance benchmarking

### **Data Science & Analytics**
- Predictive modeling
- Trend analysis
- Sentiment analysis
- Recommendation systems
- Market segmentation

### **Talent & Professional**
- Recruitment
- Skills analysis
- Career progression
- Professional networks
- Industry expertise

## 🔧 Technical Specifications

### **Data Formats**
- **Primary**: JSON (structured data)
- **Alternative**: CSV (tabular data)
- **Compression**: Optional GZIP compression
- **Encoding**: UTF-8

### **API Endpoints**
- **Search**: `/datasets/filter` - Query datasets with filters
- **Download**: `/datasets/snapshots/{id}/download` - Download results
- **Metadata**: `/datasets/snapshots/{id}` - Get snapshot information

### **Rate Limits**
- **Requests**: 1,000 requests per hour
- **Data Volume**: 1 million records per day
- **Concurrent**: 5 simultaneous requests

### **Data Quality**
- **Verification**: All data verified for accuracy
- **Completeness**: High data completeness scores
- **Freshness**: Daily updates ensure current information
- **Validation**: Multiple validation layers

## 💰 Pricing Structure

### **Per-Record Pricing**
- **Standard Rate**: $0.002 per record
- **Bulk Discounts**: Available for large volumes
- **Enterprise**: Custom pricing for enterprise clients

### **Cost Examples**
| Use Case | Records | Cost | Description |
|----------|---------|------|-------------|
| **Small Analysis** | 1,000 | $2.00 | Product category research |
| **Medium Study** | 10,000 | $20.00 | Market segment analysis |
| **Large Research** | 100,000 | $200.00 | Comprehensive market study |
| **Enterprise** | 1,000,000 | $2,000.00 | Full market intelligence |

## 🚀 Getting Started

### **1. Choose Your Dataset**
Select the dataset that best fits your use case:
- **E-commerce**: Amazon Products, Amazon-Walmart Comparison, Target Products
- **Global Markets**: Shopee Products, TikTok Products
- **Professional**: LinkedIn Profiles

### **2. Review Documentation**
Each dataset has comprehensive documentation:
- Complete field reference
- Sample queries
- Use cases and examples
- Technical specifications

### **3. Build Your Query**
Use the provided sample queries as starting points:
- Customize filters for your needs
- Set appropriate record limits
- Choose relevant fields

### **4. Execute and Analyze**
- Run your queries
- Download results
- Analyze data for insights

## 📈 Best Practices

### **Query Optimization**
- Use specific filters to reduce data volume
- Set realistic price ranges and availability filters
- Use geographic filters for targeted analysis
- Leverage rating and review thresholds

### **Data Analysis**
- Start with small datasets to understand structure
- Use multiple filters to narrow results
- Analyze trends and patterns over time
- Combine multiple datasets for comprehensive insights

### **Compliance**
- Use data ethically and legally
- Respect platform terms of service
- Follow data retention policies
- Protect sensitive information

## 🔍 Sample Queries

### **E-commerce Analysis**
```yaml
# High-rated electronics under $100
filters:
  - field: "category"
    operator: "="
    value: "Electronics"
  - field: "rating"
    operator: ">="
    value: 4.5
  - field: "final_price"
    operator: "<="
    value: 100
```

### **Professional Networks**
```yaml
# Software engineers in San Francisco
filters:
  - field: "current_position"
    operator: "includes"
    value: "Software Engineer"
  - field: "city"
    operator: "="
    value: "San Francisco"
  - field: "open_to_work"
    operator: "="
    value: true
```

### **Cross-Platform Analysis**
```yaml
# Products with price differences
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

## 📚 Documentation Structure

Each dataset includes:
- **Overview**: Purpose, use cases, and key features
- **Field Reference**: Complete list of available fields
- **Sample Queries**: Ready-to-use query examples
- **Technical Specs**: API endpoints, rate limits, data formats
- **Pricing**: Cost structure and examples
- **Best Practices**: Optimization and compliance guidelines

## 🆘 Support & Resources

### **Documentation**
- **API Reference**: Complete API documentation
- **Query Examples**: Sample queries and use cases
- **Integration Guides**: Step-by-step setup instructions

### **Support Channels**
- **Technical Support**: 24/7 technical assistance
- **Data Quality**: Data validation and quality assurance
- **Custom Solutions**: Tailored data solutions

### **Community**
- **Developer Forum**: Community support and discussions
- **Best Practices**: Shared knowledge and insights
- **Case Studies**: Real-world implementation examples

---

*This comprehensive overview provides everything you need to understand and utilize BrightData datasets effectively. Choose your dataset, review the documentation, and start building powerful data-driven insights.*
