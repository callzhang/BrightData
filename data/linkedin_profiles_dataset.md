# LinkedIn Profiles Dataset

## Overview

The LinkedIn Profiles dataset provides comprehensive professional profile data from LinkedIn, including career history, education, network metrics, and professional information. This dataset is ideal for talent acquisition, market research, business intelligence, and professional network analysis.

## Dataset Information

- **Dataset ID**: `gd_l1viktl72bvl7bjuj0`
- **Source**: [BrightData LinkedIn Profiles](https://brightdata.com/cp/datasets/browse/gd_l1viktl72bvl7bjuj0)
- **Update Frequency**: Daily
- **Data Volume**: Millions of professional profiles
- **Coverage**: Global LinkedIn professional network
- **Data Quality**: High-quality, verified professional data
- **Cost**: $0.002 per profile

## Use Cases

### 👥 **Talent Acquisition**
- **Recruitment**: Find and identify potential candidates for job openings
- **Skills Matching**: Match candidates with required skills and experience
- **Location-Based Search**: Find candidates in specific geographic areas
- **Industry Expertise**: Identify professionals with specific industry experience

### 📊 **Market Research**
- **Industry Analysis**: Study industry trends and professional demographics
- **Competitive Intelligence**: Analyze competitor talent and organizational structure
- **Market Sizing**: Estimate market size and growth potential
- **Professional Trends**: Track professional development and career trends

### 🔍 **Data Science & Analytics**
- **Professional Networks**: Analyze professional network structures
- **Career Progression**: Study career progression patterns
- **Skills Analysis**: Analyze skill trends and demand
- **Geographic Analysis**: Study professional distribution and migration patterns

### 💼 **Business Intelligence**
- **Sales Prospecting**: Identify potential customers and decision makers
- **Partnership Development**: Find potential business partners
- **Market Entry**: Support market entry and expansion strategies
- **Investment Analysis**: Analyze talent and market opportunities

## Complete Field Reference (42 Fields)

### Core Profile Information
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `id` | string | A unique identifier for the person's LinkedIn profile | 100.00% |
| `name` | string | Profile name | 97.40% |
| `first_name` | string | First name of the user | 94.56% |
| `last_name` | string | Last name of the user | 94.25% |
| `position` | string | The current job title or position of the profile | 91.72% |
| `about` | string | A concise profile summary | 19.05% |
| `url` | string | URL that link directly to the LinkedIn profile | 100.00% |
| `linkedin_id` | string | LinkedIn profile identifier | 100.00% |
| `linkedin_num_id` | string | Numeric LinkedIn profile ID | 100.00% |
| `input_url` | string | The URL that was entered when starting the scraping process | 100.00% |

### Location Information
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `city` | string | Geographical location of the user | 96.09% |
| `country_code` | string | Geographical location of the user | 96.95% |
| `location` | string | Geographical location of the user | 60.80% |

### Profile Media
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `avatar` | string | URL that link to the profile picture of the LinkedIn user | 96.06% |
| `banner_image` | string | Banner image | 96.06% |
| `default_avatar` | boolean | Is the avatar picture the default avatar empty picture | 95.47% |
| `memorialized_account` | boolean | Boolean indicating if the account is memorialized | 99.41% |

### Network Metrics
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `followers` | numeric | How many users/companies following the profile | 72.82% |
| `connections` | numeric | How many connections the profile has | 71.87% |
| `recommendations_count` | numeric | A numeric count of the total number of recommendations that the user has received | 3.71% |

### Current Company Information
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `current_company` | object | Provides information about the user's current professional position | 100.00% |
| `current_company_company_id` | string | The id of the latest/current company of the profile | 36.37% |
| `current_company_name` | string | The name of the latest/current company of the profile | 68.17% |

### Professional Experience
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `experience` | array | Contains information about user's professional history | 66.94% |

### Education Information
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `educations_details` | string | Provides information about the user's educational background | 42.90% |
| `education` | array | Provides information about the user's educational background | 42.75% |
| `courses` | array | Contains information about courses or educational programs that the user has undertaken | 2.63% |

### Skills and Certifications
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `languages` | array | Contains information about the user's proficiency in different languages | 9.49% |
| `certifications` | array | Licenses & Certifications | 8.41% |

### Content and Activity
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `posts` | array | Contains information related to the user's last LinkedIn posts | 2.34% |
| `activity` | array | Any activity the user has regarding posts | 32.60% |
| `recommendations` | array | Recommendations that the user has received from their connections or colleagues on LinkedIn | 3.64% |

### Professional Development
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `volunteer_experience` | array | Contains information related to the user's volunteer work | 4.25% |
| `publications` | array | Published works or presentations | 1.27% |
| `patents` | array | Patents filed or granted | 0.13% |
| `projects` | array | Professional or academic projects | 2.12% |
| `organizations` | array | Memberships in professional organizations | 1.84% |
| `honors_and_awards` | array | Awards and recognitions received | 2.18% |

### Network and Discovery
| Field | Type | Description | Fill Rate |
|-------|------|-------------|-----------|
| `people_also_viewed` | array | Provides a list of LinkedIn profiles that users who have viewed the user's profile, have viewed these as well | 37.66% |
| `similar_profiles` | array | Profiles similar to the current one | 18.32% |
| `bio_links` | array | External links added to the bio | 2.98% |

## Sample Queries

### 1. Software Engineers in San Francisco
```yaml
filters:
  - field: "position"
    operator: "includes"
    value: "Software Engineer"
  - field: "city"
    operator: "="
    value: "San Francisco"
  - field: "connections"
    operator: ">="
    value: 100
```

### 2. Professionals with High Network Activity
```yaml
filters:
  - field: "followers"
    operator: ">="
    value: 1000
  - field: "connections"
    operator: ">="
    value: 500
  - field: "recommendations_count"
    operator: ">="
    value: 10
```

### 3. Education-Focused Professionals
```yaml
filters:
  - field: "education"
    operator: "!="
    value: null
  - field: "courses"
    operator: "!="
    value: null
  - field: "certifications"
    operator: "!="
    value: null
```

### 4. Content Creators and Influencers
```yaml
filters:
  - field: "posts"
    operator: "!="
    value: null
  - field: "activity"
    operator: "!="
    value: null
  - field: "followers"
    operator: ">="
    value: 5000
```

### 5. Research and Academic Professionals
```yaml
filters:
  - field: "publications"
    operator: "!="
    value: null
  - field: "patents"
    operator: "!="
    value: null
  - field: "organizations"
    operator: "!="
    value: null
```

## Data Quality & Privacy

### Data Quality
- **Verification**: Profiles are verified for authenticity
- **Completeness**: Variable fill rates across fields (see field reference)
- **Freshness**: Daily updates ensure current information
- **Accuracy**: Multiple validation layers ensure data accuracy

### Privacy Compliance
- **Public Data Only**: Only publicly available profile information
- **No Personal Data**: No private or sensitive personal information included
- **Terms Compliance**: Adheres to LinkedIn's terms of service
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
- **Per Record**: $0.002 per profile
- **Bulk Discounts**: Available for large volumes
- **Enterprise**: Custom pricing for enterprise clients

### Example Costs
| Records | Cost | Use Case |
|---------|------|----------|
| 1,000 | $2.00 | Small talent search |
| 10,000 | $20.00 | Department recruitment |
| 100,000 | $200.00 | Company-wide analysis |
| 1,000,000 | $2,000.00 | Market research study |

## Getting Started

### 1. Basic Setup
```python
from util import BrightDataFilter

# Initialize LinkedIn dataset
filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
```

### 2. Simple Query
```python
# Find software engineers
filters = [
    {"field": "position", "operator": "includes", "value": "Software Engineer"},
    {"field": "city", "operator": "=", "value": "San Francisco"}
]

result = filter_obj.search_data(
    filter_obj=filters,
    records_limit=1000,
    title="Software Engineers in SF"
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
- **Specific Roles**: Use precise job title filters
- **Location Focus**: Filter by specific geographic areas
- **Network Size**: Use connection/follower thresholds
- **Content Activity**: Filter for active content creators

### Data Analysis
- **Talent Analysis**: Analyze talent pools and trends
- **Network Analysis**: Study professional network structures
- **Geographic Analysis**: Study professional distribution
- **Career Progression**: Analyze career development patterns

### Compliance
- **Data Usage**: Use data ethically and legally
- **Terms Respect**: Honor LinkedIn's terms of service
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

*This comprehensive dataset provides detailed LinkedIn professional profile data for talent acquisition, market research, and business intelligence. Use responsibly and in compliance with applicable terms of service.*