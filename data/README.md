# BrightData Datasets Documentation

This directory contains comprehensive documentation for all available datasets in the BrightData platform. Each dataset is documented with detailed field references, use cases, sample queries, and technical specifications.

## Available Datasets

### 🛒 **E-commerce & Retail**

#### [Amazon Products Dataset](./amazon_products_dataset.md)
- **Dataset ID**: `gd_l7q7dkf244hwjntr0`
- **Description**: Comprehensive Amazon product data including pricing, reviews, availability, and specifications
- **Use Cases**: E-commerce analysis, competitive intelligence, price monitoring, market research
- **Fields**: 50+ fields covering product info, pricing, reviews, seller data, and performance metrics
- **Cost**: $0.002 per product

#### [Amazon-Walmart Comparison Dataset](./amazon_walmart_comparison_dataset.md)
- **Dataset ID**: `gd_m4l6s4mn2g2rkx9lia`
- **Description**: Cross-platform product comparison data between Amazon and Walmart
- **Use Cases**: Competitive analysis, price comparison, market intelligence, cross-platform strategy
- **Fields**: 60+ fields covering both platforms with comparison metrics
- **Cost**: $0.002 per comparison

#### [Target Products Dataset](./target_products_dataset.md)
- **Dataset ID**: `gd_lk122xxgf86xf97py`
- **Description**: Comprehensive Target product data for US retail market analysis
- **Use Cases**: Retail analysis, competitive intelligence, market research, pricing strategy
- **Fields**: 40+ fields covering product info, pricing, reviews, and store data
- **Cost**: $0.002 per product

### 🌏 **Global E-commerce**

#### [Shopee Products Dataset](./shopee_products_dataset.md)
- **Dataset ID**: `gd_lk122xxgf86xf97py`
- **Description**: Southeast Asian e-commerce product data from Shopee
- **Use Cases**: Southeast Asian market analysis, competitive intelligence, regional strategy
- **Fields**: 35+ fields covering product info, pricing, reviews, and seller data
- **Cost**: $0.002 per product

#### [TikTok Products Dataset](./tiktok_products_dataset.md)
- **Dataset ID**: `gd_lk122xxgf86xf97py`
- **Description**: Social commerce product data from TikTok Shop
- **Use Cases**: Social commerce analysis, influencer marketing, viral product identification
- **Fields**: 40+ fields including social media metrics and engagement data
- **Cost**: $0.002 per product

### 👥 **Professional Networks**

#### [LinkedIn Profiles Dataset](./linkedin_profiles_dataset.md)
- **Dataset ID**: `gd_l1viktl72bvl7bjuj0`
- **Description**: Comprehensive LinkedIn professional profile data
- **Use Cases**: Talent acquisition, market research, business intelligence, professional network analysis
- **Fields**: 42 fields covering career history, education, network metrics, and professional information
- **Cost**: $0.002 per profile

## Dataset Categories

### **E-commerce & Retail**
- Amazon Products
- Amazon-Walmart Comparison
- Target Products

### **Global E-commerce**
- Shopee Products
- TikTok Products

### **Professional Networks**
- LinkedIn Profiles

## Quick Start Guide

### 1. Choose Your Dataset
Select the dataset that best fits your use case:
- **E-commerce Analysis**: Amazon Products, Amazon-Walmart Comparison, Target Products
- **Global Markets**: Shopee Products, TikTok Products
- **Talent & Professional**: LinkedIn Profiles

### 2. Review Documentation
Each dataset has comprehensive documentation including:
- Complete field reference
- Sample queries
- Use cases and examples
- Technical specifications
- Pricing information

### 3. Build Your Query
Use the sample queries as starting points and customize them for your specific needs.

### 4. Execute and Analyze
Run your queries and analyze the results to gain insights.

## Common Use Cases

### **E-commerce & Retail**
- **Product Research**: Analyze product performance and market positioning
- **Competitive Intelligence**: Monitor competitor products and pricing strategies
- **Price Optimization**: Track price changes and identify opportunities
- **Market Analysis**: Study market trends and customer behavior

### **Global Markets**
- **Market Entry**: Support market entry strategies for new regions
- **Regional Analysis**: Understand regional market dynamics
- **Cross-Platform Strategy**: Develop multi-platform strategies
- **Cultural Insights**: Gain insights into regional preferences

### **Professional Networks**
- **Talent Acquisition**: Find and identify potential candidates
- **Skills Analysis**: Analyze skill trends and demand
- **Market Research**: Study professional demographics and trends
- **Business Development**: Identify potential partners and customers

## Technical Specifications

### **Data Format**
- **Format**: JSON/CSV
- **Encoding**: UTF-8
- **Compression**: Optional GZIP compression
- **Batch Size**: Configurable (default: 1000 records)

### **API Endpoints**
- **Search**: `/datasets/filter`
- **Download**: `/datasets/snapshots/{id}/download`
- **Metadata**: `/datasets/snapshots/{id}`

### **Rate Limits**
- **Requests**: 1000 requests/hour
- **Data Volume**: 1M records/day
- **Concurrent**: 5 simultaneous requests

## Pricing

### **Cost Structure**
- **Per Record**: $0.002 per record
- **Bulk Discounts**: Available for large volumes
- **Enterprise**: Custom pricing for enterprise clients

### **Example Costs**
| Records | Cost | Use Case |
|---------|------|----------|
| 1,000 | $2.00 | Small analysis |
| 10,000 | $20.00 | Category research |
| 100,000 | $200.00 | Market analysis |
| 1,000,000 | $2,000.00 | Comprehensive study |

## Best Practices

### **Query Optimization**
- Use specific filters to reduce data volume
- Set realistic price ranges and availability filters
- Use geographic filters for targeted analysis
- Leverage rating and review thresholds

### **Data Analysis**
- Start with small datasets to understand the data structure
- Use multiple filters to narrow down results
- Analyze trends and patterns over time
- Combine multiple datasets for comprehensive insights

### **Compliance**
- Use data ethically and legally
- Respect platform terms of service
- Follow data retention policies
- Protect sensitive information

## Support & Resources

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

*This comprehensive documentation provides everything you need to get started with BrightData datasets. Choose your dataset, review the documentation, and start building powerful data-driven insights.*
