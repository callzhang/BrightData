# LinkedIn Profiles Dataset - Complete Guide

## 🎯 Overview

The LinkedIn Profiles dataset provides comprehensive professional profile data from LinkedIn, enabling talent acquisition, market research, competitive intelligence, and business development. This dataset includes detailed information about professionals' careers, skills, education, network metrics, and engagement data.

## 📊 Dataset Information

- **Dataset ID**: `gd_l1viktl72bvl7bjuj0`
- **Source**: [BrightData LinkedIn Profiles](https://brightdata.com/cp/datasets/browse/gd_l1viktl72bvl7bjuj0?id=hl_d7861a3a)
- **Update Frequency**: Daily
- **Data Volume**: Millions of profiles
- **Coverage**: Global LinkedIn users
- **Data Quality**: High-quality, verified professional data
- **Cost**: $0.002 per profile

## 🚀 Quick Start

### 1. Basic Setup
```python
from util import BrightDataFilter

# Initialize LinkedIn dataset
filter_obj = BrightDataFilter("gd_l1viktl72bvl7bjuj0")
```

### 2. Simple Query
```python
# Find software engineers in San Francisco
filters = [
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Software Engineer"
    },
    {
        "field": "location",
        "operator": "includes",
        "value": "San Francisco"
    }
]

result = filter_obj.search_data(
    filters=filters,
    records_limit=1000,
    title="SF Software Engineers"
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

## 🎯 Use Cases

### Talent Acquisition & Recruitment
- **Candidate Sourcing**: Find qualified candidates by skills, experience, and location
- **Skills Matching**: Match job requirements with candidate skills
- **Salary Benchmarking**: Understand market rates for different roles
- **Diversity Analysis**: Analyze talent diversity across demographics

### Market Research & Analysis
- **Industry Trends**: Track career movements and industry shifts
- **Skills Trends**: Identify trending skills and competencies
- **Geographic Analysis**: Map talent distribution across regions
- **Company Analysis**: Understand employee backgrounds and skills

### Business Development & Sales
- **Lead Generation**: Find decision-makers and influencers
- **Account Research**: Understand client organizations and key personnel
- **Relationship Mapping**: Identify mutual connections
- **Competitive Analysis**: Monitor competitor talent and strategies

### Data Science & Analytics
- **Network Analysis**: Study professional relationship patterns
- **Career Path Modeling**: Predict career progression patterns
- **Skills Taxonomy**: Build comprehensive skills databases
- **Engagement Metrics**: Analyze professional content performance

## 📋 Complete Field Reference

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

## 🔍 Query Examples

### 1. Talent Acquisition - Software Engineers
```python
filters = [
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Software Engineer"
    },
    {
        "field": "industry",
        "operator": "=",
        "value": "Technology"
    },
    {
        "field": "location",
        "operator": "includes",
        "value": "San Francisco"
    },
    {
        "field": "total_experience_years",
        "operator": ">=",
        "value": 3
    },
    {
        "field": "open_to_work",
        "operator": "=",
        "value": True
    }
]
```

### 2. Market Research - Skills Analysis
```python
filters = [
    {
        "field": "industry",
        "operator": "=",
        "value": "Technology"
    },
    {
        "field": "top_skills",
        "operator": "includes",
        "value": "Machine Learning"
    },
    {
        "field": "connections_count",
        "operator": ">=",
        "value": 500
    },
    {
        "field": "profile_completeness",
        "operator": ">=",
        "value": 80
    }
]
```

### 3. Sales Prospecting - Decision Makers
```python
filters = [
    {
        "field": "industry",
        "operator": "=",
        "value": "Healthcare"
    },
    {
        "field": "seniority_level",
        "operator": "in",
        "value": ["senior", "executive"]
    },
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Director"
    },
    {
        "field": "company_size",
        "operator": ">=",
        "value": "1000"
    }
]
```

### 4. University Alumni Network
```python
filters = [
    {
        "field": "university",
        "operator": "=",
        "value": "Stanford University"
    },
    {
        "field": "graduation_year",
        "operator": ">=",
        "value": 2015
    },
    {
        "field": "industry",
        "operator": "=",
        "value": "Technology"
    },
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Engineer"
    }
]
```

### 5. Remote Work Analysis
```python
filters = [
    {
        "field": "open_to_remote",
        "operator": "=",
        "value": True
    },
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Developer"
    },
    {
        "field": "industry",
        "operator": "=",
        "value": "Technology"
    },
    {
        "field": "total_experience_years",
        "operator": ">=",
        "value": 2
    }
]
```

### 6. Skills Gap Analysis
```python
filters = [
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Data Scientist"
    },
    {
        "field": "top_skills",
        "operator": "includes",
        "value": "Python"
    },
    {
        "field": "top_skills",
        "operator": "includes",
        "value": "Machine Learning"
    },
    {
        "field": "certifications_count",
        "operator": ">=",
        "value": 1
    }
]
```

### 7. Competitive Intelligence
```python
filters = [
    {
        "field": "current_company",
        "operator": "in",
        "value": ["Google", "Microsoft", "Amazon", "Apple", "Meta"]
    },
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Engineer"
    },
    {
        "field": "seniority_level",
        "operator": "in",
        "value": ["senior", "executive"]
    },
    {
        "field": "total_experience_years",
        "operator": ">=",
        "value": 5
    }
]
```

### 8. Geographic Analysis
```python
filters = [
    {
        "field": "industry",
        "operator": "=",
        "value": "Technology"
    },
    {
        "field": "country",
        "operator": "in",
        "value": ["United States", "Canada", "United Kingdom", "Germany"]
    },
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Manager"
    },
    {
        "field": "connections_count",
        "operator": ">=",
        "value": 1000
    }
]
```

## 💰 Pricing & Costs

### Cost Structure
- **Per Record**: $0.002 per profile
- **Bulk Discounts**: Available for large volumes
- **Enterprise**: Custom pricing for enterprise clients

### Example Costs
| Records | Cost | Use Case |
|---------|------|----------|
| 1,000 | $2.00 | Small recruitment campaign |
| 5,000 | $10.00 | Market research study |
| 10,000 | $20.00 | Large talent acquisition |
| 50,000 | $100.00 | Enterprise analysis |
| 100,000 | $200.00 | Comprehensive market study |

## 🛠️ Technical Implementation

### 1. Configuration Setup
```python
# Load dataset configuration
from util.dataset_config import DatasetConfigLoader

config_loader = DatasetConfigLoader()
linkedin_config = config_loader.get_dataset("linkedin_profiles")
```

### 2. Query Building
```python
# Build complex queries
filters = [
    {
        "field": "current_position",
        "operator": "includes",
        "value": "Software Engineer"
    },
    {
        "field": "industry",
        "operator": "=",
        "value": "Technology"
    }
]

# Submit query
result = filter_obj.search_data(
    filters=filters,
    records_limit=1000,
    title="Tech Software Engineers"
)
```

### 3. Data Processing
```python
# Download and process data
response = filter_obj.download_snapshot_content(
    snapshot_id=result,
    format='json'
)

# Convert to DataFrame
import pandas as pd
data = response.json()
df = pd.DataFrame(data)
```

## 📊 Data Analysis Examples

### 1. Skills Analysis
```python
# Analyze top skills
top_skills = df['top_skills'].explode().value_counts().head(10)
print("Top 10 Skills:")
print(top_skills)
```

### 2. Geographic Distribution
```python
# Analyze geographic distribution
location_analysis = df['location'].value_counts().head(10)
print("Top 10 Locations:")
print(location_analysis)
```

### 3. Industry Analysis
```python
# Analyze industry distribution
industry_analysis = df['industry'].value_counts()
print("Industry Distribution:")
print(industry_analysis)
```

### 4. Experience Analysis
```python
# Analyze experience levels
experience_analysis = df['total_experience_years'].describe()
print("Experience Statistics:")
print(experience_analysis)
```

## 🔒 Privacy & Compliance

### Data Privacy
- **Public Data Only**: Only publicly available information
- **GDPR Compliant**: European data protection standards
- **CCPA Compliant**: California privacy law compliance
- **Opt-out Respect**: Honors LinkedIn privacy settings

### Ethical Usage
- **Professional Use**: Use data for legitimate business purposes
- **Respect Privacy**: Honor individual privacy preferences
- **Purpose Limitation**: Use data for stated purposes only
- **Data Retention**: Follow data retention policies

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Access
```yaml
# secrets.yaml
brightdata:
  api_key: "your_api_key_here"
  base_url: "https://api.brightdata.com"
  dataset_id: "gd_l1viktl72bvl7bjuj0"
```

### 3. Run Examples
```bash
python examples/linkedin_profiles_example.py
```

### 4. Run Tests
```bash
python tests/test_linkedin_profiles.py
```

## 📚 Additional Resources

### Documentation
- [Complete Dataset Documentation](LINKEDIN_PROFILES_DATASET.md)
- [API Reference](docs/API_REFERENCE.md)
- [Query Examples](examples/linkedin_profiles_example.py)

### Support
- **Technical Support**: 24/7 technical assistance
- **Data Quality**: Data validation and quality assurance
- **Custom Solutions**: Tailored data solutions

### Community
- **Developer Forum**: Community support and discussions
- **Best Practices**: Shared knowledge and insights
- **Case Studies**: Real-world implementation examples

---

*This comprehensive guide provides everything you need to get started with LinkedIn profiles data. Use responsibly and in compliance with applicable privacy laws and LinkedIn's terms of service.*
