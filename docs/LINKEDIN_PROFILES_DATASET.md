# LinkedIn Profiles Dataset

## Overview

The LinkedIn Profiles dataset provides comprehensive professional profile data from LinkedIn, including career history, skills, education, network metrics, and engagement data. This dataset is ideal for talent acquisition, market research, competitive analysis, and professional networking insights.

## Dataset Information

- **Dataset ID**: `gd_l1viktl72bvl7bjuj0`
- **Source**: [BrightData LinkedIn Profiles](https://brightdata.com/cp/datasets/browse/gd_l1viktl72bvl7bjuj0?id=hl_d7861a3a)
- **Update Frequency**: Daily
- **Data Volume**: Millions of profiles
- **Coverage**: Global LinkedIn users
- **Data Quality**: High-quality, verified professional data

## Use Cases

### 🎯 **Talent Acquisition & Recruitment**
- **Candidate Sourcing**: Find qualified candidates by skills, experience, and location
- **Competitive Intelligence**: Analyze talent pools in specific industries
- **Salary Benchmarking**: Understand market rates for different roles
- **Skills Gap Analysis**: Identify trending skills and competencies

### 📊 **Market Research & Analysis**
- **Industry Trends**: Track career movements and industry shifts
- **Company Analysis**: Understand employee backgrounds and skills
- **Geographic Analysis**: Map talent distribution across regions
- **Professional Development**: Identify learning and development opportunities

### 🔍 **Business Development & Sales**
- **Lead Generation**: Find decision-makers and influencers
- **Account Research**: Understand client organizations and key personnel
- **Relationship Mapping**: Identify mutual connections and warm introductions
- **Competitive Analysis**: Monitor competitor talent and strategies

### 📈 **Data Science & Analytics**
- **Network Analysis**: Study professional relationship patterns
- **Career Path Modeling**: Predict career progression patterns
- **Skills Taxonomy**: Build comprehensive skills databases
- **Engagement Metrics**: Analyze professional content performance

## Data Schema

### Basic Profile Information
| Field | Type | Description |
|-------|------|-------------|
| `full_name` | string | Full name of the LinkedIn user |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `headline` | string | Professional headline/title |
| `summary` | string | Professional summary/about section |
| `location` | string | Current location |
| `industry` | string | Industry sector |
| `profile_url` | string | LinkedIn profile URL |
| `profile_image_url` | string | Profile picture URL |
| `background_image_url` | string | Background/banner image URL |

### Contact Information
| Field | Type | Description |
|-------|------|-------------|
| `email` | string | Email address (if public) |
| `phone` | string | Phone number (if public) |
| `website` | string | Personal website URL |
| `twitter_handle` | string | Twitter/X handle |
| `other_social_links` | array | Other social media links |

### Network Metrics
| Field | Type | Description |
|-------|------|-------------|
| `connections_count` | numeric | Number of connections |
| `followers_count` | numeric | Number of followers |
| `following_count` | numeric | Number of people following |
| `mutual_connections_count` | numeric | Number of mutual connections |

### Professional Information
| Field | Type | Description |
|-------|------|-------------|
| `current_position` | string | Current job title |
| `current_company` | string | Current company name |
| `current_company_url` | string | Current company LinkedIn URL |
| `employment_status` | string | Employment status |
| `open_to_work` | boolean | Open to work status |
| `open_to_remote` | boolean | Open to remote work |
| `open_to_relocation` | boolean | Open to relocation |

### Experience Data
| Field | Type | Description |
|-------|------|-------------|
| `experience_count` | numeric | Number of work experiences |
| `total_experience_years` | numeric | Total years of experience |
| `seniority_level` | string | Seniority level (entry, mid, senior, executive) |
| `management_experience` | boolean | Has management experience |

### Education Information
| Field | Type | Description |
|-------|------|-------------|
| `education_count` | numeric | Number of education entries |
| `highest_degree` | string | Highest degree obtained |
| `university` | string | University/college name |
| `graduation_year` | numeric | Graduation year |
| `field_of_study` | string | Field of study/major |

### Skills and Endorsements
| Field | Type | Description |
|-------|------|-------------|
| `skills_count` | numeric | Number of skills listed |
| `top_skills` | array | Top skills with endorsements |
| `endorsements_count` | numeric | Total number of skill endorsements |
| `certifications_count` | numeric | Number of certifications |

### Activity and Engagement
| Field | Type | Description |
|-------|------|-------------|
| `posts_count` | numeric | Number of posts published |
| `articles_count` | numeric | Number of articles published |
| `last_activity_date` | date | Last activity date |
| `profile_completeness` | numeric | Profile completeness percentage |

### Company Information
| Field | Type | Description |
|-------|------|-------------|
| `company_size` | string | Current company size |
| `company_type` | string | Company type (public, private, nonprofit) |
| `company_industry` | string | Company industry |
| `company_headquarters` | string | Company headquarters location |

### Geographic Information
| Field | Type | Description |
|-------|------|-------------|
| `country` | string | Country |
| `state_province` | string | State or province |
| `city` | string | City |
| `timezone` | string | Timezone |

### Premium Features
| Field | Type | Description |
|-------|------|-------------|
| `is_premium` | boolean | LinkedIn Premium member |
| `premium_type` | string | Type of LinkedIn Premium |
| `sales_navigator` | boolean | Sales Navigator access |
| `recruiter_lite` | boolean | Recruiter Lite access |

### Profile Quality Metrics
| Field | Type | Description |
|-------|------|-------------|
| `profile_views_count` | numeric | Number of profile views |
| `search_appearances_count` | numeric | Number of search appearances |
| `connection_requests_sent` | numeric | Connection requests sent |
| `connection_requests_received` | numeric | Connection requests received |

### Content and Media
| Field | Type | Description |
|-------|------|-------------|
| `media_count` | numeric | Number of media files shared |
| `video_count` | numeric | Number of videos shared |
| `document_count` | numeric | Number of documents shared |

### Recommendations
| Field | Type | Description |
|-------|------|-------------|
| `recommendations_given` | numeric | Number of recommendations given |
| `recommendations_received` | numeric | Number of recommendations received |
| `recommendation_score` | numeric | Average recommendation score |

### Groups and Organizations
| Field | Type | Description |
|-------|------|-------------|
| `groups_count` | numeric | Number of groups joined |
| `organizations_count` | numeric | Number of organizations |
| `volunteer_experience` | boolean | Has volunteer experience |

### Awards and Honors
| Field | Type | Description |
|-------|------|-------------|
| `awards_count` | numeric | Number of awards received |
| `honors_count` | numeric | Number of honors received |
| `publications_count` | numeric | Number of publications |

### Language and International
| Field | Type | Description |
|-------|------|-------------|
| `languages` | array | Languages spoken |
| `language_proficiency` | array | Language proficiency levels |
| `international_experience` | boolean | Has international work experience |

### Personal Information
| Field | Type | Description |
|-------|------|-------------|
| `birthday_month` | numeric | Birth month |
| `birthday_day` | numeric | Birth day |
| `age_range` | string | Age range category |
| `gender` | string | Gender (if specified) |

### Professional Interests
| Field | Type | Description |
|-------|------|-------------|
| `interests` | array | Professional interests |
| `causes` | array | Causes supported |
| `volunteer_causes` | array | Volunteer causes |

### Contact Preferences
| Field | Type | Description |
|-------|------|-------------|
| `contact_preferences` | array | Preferred contact methods |
| `availability_status` | string | Current availability status |
| `response_rate` | numeric | Response rate to messages |

### Data Quality and Metadata
| Field | Type | Description |
|-------|------|-------------|
| `profile_created_date` | date | Profile creation date |
| `last_updated_date` | date | Last profile update date |
| `data_quality_score` | numeric | Data quality score |
| `completeness_score` | numeric | Profile completeness score |
| `verification_status` | string | Profile verification status |

## Sample Queries

### 1. Find Software Engineers in San Francisco
```yaml
filters:
  - field: "current_position"
    operator: "includes"
    value: "Software Engineer"
  - field: "city"
    operator: "="
    value: "San Francisco"
  - field: "industry"
    operator: "="
    value: "Technology"
```

### 2. Identify Senior Marketing Professionals
```yaml
filters:
  - field: "seniority_level"
    operator: "in"
    value: ["senior", "executive"]
  - field: "industry"
    operator: "="
    value: "Marketing"
  - field: "total_experience_years"
    operator: ">="
    value: 5
```

### 3. Find Remote Work Opportunities
```yaml
filters:
  - field: "open_to_work"
    operator: "="
    value: true
  - field: "open_to_remote"
    operator: "="
    value: true
  - field: "current_position"
    operator: "includes"
    value: "Developer"
```

### 4. Analyze Skills Trends
```yaml
filters:
  - field: "top_skills"
    operator: "includes"
    value: "Machine Learning"
  - field: "industry"
    operator: "="
    value: "Technology"
  - field: "connections_count"
    operator: ">="
    value: 500
```

### 5. Find University Alumni
```yaml
filters:
  - field: "university"
    operator: "="
    value: "Stanford University"
  - field: "graduation_year"
    operator: ">="
    value: 2020
  - field: "industry"
    operator: "="
    value: "Technology"
```

## Data Quality & Privacy

### Data Quality
- **Verification**: Profiles are verified for authenticity
- **Completeness**: Data completeness scores provided
- **Freshness**: Regular updates ensure current information
- **Accuracy**: Multiple validation layers ensure data accuracy

### Privacy Compliance
- **GDPR Compliant**: European data protection standards
- **CCPA Compliant**: California privacy law compliance
- **Public Data Only**: Only publicly available information
- **Opt-out Respect**: Honors LinkedIn privacy settings

### Data Sources
- **Public Profiles**: Only publicly accessible information
- **Professional Networks**: Business-focused data
- **Verified Information**: Cross-referenced data points
- **Real-time Updates**: Current professional status

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
- **Per Record**: $0.002 per profile
- **Bulk Discounts**: Available for large volumes
- **Enterprise**: Custom pricing for enterprise clients

### Example Costs
- **1,000 profiles**: $2.00
- **10,000 profiles**: $20.00
- **100,000 profiles**: $200.00

## Getting Started

### 1. Configure API Access
```python
from util import BrightDataFilter

# Initialize with LinkedIn dataset
filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
```

### 2. Build Your Query
```python
# Example: Find data scientists in tech
filters = [
    {"field": "current_position", "operator": "includes", "value": "Data Scientist"},
    {"field": "industry", "operator": "=", "value": "Technology"},
    {"field": "location", "operator": "includes", "value": "San Francisco"}
]

# Submit query
result = filter_obj.search_data(
    filters=filters,
    records_limit=1000,
    title="Tech Data Scientists in SF"
)
```

### 3. Download Results
```python
# Download when ready
response = filter_obj.download_snapshot_content(
    snapshot_id=result['snapshot_id'],
    format='json'
)
```

## Best Practices

### Query Optimization
- **Specific Filters**: Use precise criteria to reduce costs
- **Geographic Targeting**: Focus on specific locations
- **Industry Filtering**: Target relevant industries
- **Skills Matching**: Use specific skill requirements

### Data Analysis
- **Skills Analysis**: Identify trending skills and competencies
- **Career Paths**: Track career progression patterns
- **Network Analysis**: Study professional relationship networks
- **Market Trends**: Monitor industry and role trends

### Compliance
- **Data Usage**: Use data ethically and legally
- **Privacy Respect**: Honor individual privacy preferences
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

*This dataset provides comprehensive LinkedIn professional data for talent acquisition, market research, and business intelligence. Use responsibly and in compliance with applicable privacy laws and LinkedIn's terms of service.*
