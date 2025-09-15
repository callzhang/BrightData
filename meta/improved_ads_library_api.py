#!/usr/bin/env python3
"""
Improved Facebook Ads Library API implementation based on Facebook Research repository
Adapted for Walmart Customer Insights project
"""

import json
import re
import requests
from datetime import datetime
from collections import Counter
import csv

class ImprovedFbAdsLibraryAPI:
    """
    Improved Facebook Ads Library API client based on Facebook Research implementation
    """
    
    # Supported countries from Facebook Research repo
    SUPPORTED_COUNTRIES = [
        "AT", "BE", "BG", "CA", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", 
        "GB", "GR", "HR", "HU", "IE", "IL", "IN", "IT", "LT", "LU", "LV", "MT", 
        "NL", "PL", "PT", "RO", "SE", "SI", "SK", "UA", "US"
    ]
    
    # Valid fields from Facebook Research repo
    VALID_FIELDS = [
        "ad_creation_time", "ad_creative_body", "ad_creative_bodies", 
        "ad_creative_link_caption", "ad_creative_link_captions",
        "ad_creative_link_description", "ad_creative_link_descriptions",
        "ad_creative_link_title", "ad_creative_link_titles",
        "ad_delivery_start_time", "ad_delivery_stop_time", "ad_snapshot_url",
        "currency", "delivery_by_region", "demographic_distribution",
        "bylines", "id", "impressions", "languages", "page_id", "page_name",
        "potential_reach", "publisher_platforms", "region_distribution", "spend"
    ]
    
    def __init__(self, access_token, api_version="v19.0"):
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = f"https://graph.facebook.com/{api_version}/ads_archive"
        
    def search_ads(self, 
                   search_terms="sustainability",
                   countries=["US"],
                   fields=None,
                   search_page_ids="",
                   ad_active_status="ALL",
                   after_date="2023-01-01",
                   limit=500,
                   retry_limit=3):
        """
        Search for ads in the Facebook Ads Library
        
        Args:
            search_terms (str): Search terms for ads
            countries (list): List of country codes
            fields (list): Fields to retrieve
            search_page_ids (str): Specific page IDs to search
            ad_active_status (str): Active status filter
            after_date (str): Only ads after this date
            limit (int): Number of results per page
            retry_limit (int): Number of retries on error
        """
        
        # Set default fields if none provided
        if fields is None:
            fields = [
                "id", "ad_creative_body", "ad_snapshot_url", "publisher_platforms",
                "page_name", "ad_delivery_start_time", "ad_delivery_stop_time",
                "demographic_distribution", "region_distribution"
            ]
        
        # Validate countries
        for country in countries:
            if country not in self.SUPPORTED_COUNTRIES:
                raise ValueError(f"Unsupported country: {country}")
        
        # Validate fields
        for field in fields:
            if field not in self.VALID_FIELDS:
                raise ValueError(f"Unsupported field: {field}")
        
        # Build request parameters
        params = {
            "access_token": self.access_token,
            "fields": ",".join(fields),
            "search_terms": search_terms,
            "ad_reached_countries": countries,
            "search_page_ids": search_page_ids,
            "ad_active_status": ad_active_status,
            "limit": limit
        }
        
        print(f"🔍 Searching for: '{search_terms}' in {countries}")
        print(f"📊 Fields: {', '.join(fields)}")
        print(f"📅 After date: {after_date}")
        
        return self._fetch_ads_with_pagination(params, after_date, retry_limit)
    
    def _fetch_ads_with_pagination(self, params, after_date, retry_limit):
        """
        Fetch ads with pagination support and error handling
        """
        next_url = self.base_url
        last_error_url = None
        last_retry_count = 0
        start_time_cutoff = datetime.strptime(after_date, "%Y-%m-%d").timestamp()
        total_ads = 0
        
        while next_url:
            try:
                # Make request
                if next_url == self.base_url:
                    response = requests.get(next_url, params=params)
                else:
                    response = requests.get(next_url)
                
                response_data = response.json()
                
                # Handle errors
                if "error" in response_data:
                    if next_url == last_error_url:
                        if last_retry_count >= retry_limit:
                            raise Exception(f"API Error: {response_data['error']}")
                    else:
                        last_error_url = next_url
                        last_retry_count = 0
                    last_retry_count += 1
                    continue
                
                # Filter ads by date
                if "data" in response_data:
                    filtered_ads = [
                        ad for ad in response_data["data"]
                        if "ad_delivery_start_time" in ad and
                        datetime.strptime(ad["ad_delivery_start_time"], "%Y-%m-%d").timestamp() >= start_time_cutoff
                    ]
                    
                    if not filtered_ads:
                        print("📅 No more ads after the specified date")
                        break
                    
                    total_ads += len(filtered_ads)
                    print(f"📈 Found {len(filtered_ads)} ads (Total: {total_ads})")
                    
                    yield filtered_ads
                
                # Get next page URL
                if "paging" in response_data and "next" in response_data["paging"]:
                    next_url = response_data["paging"]["next"]
                else:
                    next_url = None
                    
            except Exception as e:
                print(f"❌ Error fetching ads: {e}")
                break
        
        print(f"✅ Search completed. Total ads found: {total_ads}")
    
    def count_ads(self, ads_generator):
        """Count total number of ads"""
        count = 0
        for ads_batch in ads_generator:
            count += len(ads_batch)
        return count
    
    def save_to_csv(self, ads_generator, filename, fields):
        """Save ads to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            
            total_count = 0
            for ads_batch in ads_generator:
                for ad in ads_batch:
                    # Flatten complex fields
                    row = {}
                    for field in fields:
                        if field in ad:
                            value = ad[field]
                            if isinstance(value, (dict, list)):
                                row[field] = json.dumps(value)
                            else:
                                row[field] = str(value)
                        else:
                            row[field] = ""
                    writer.writerow(row)
                    total_count += 1
            
        print(f"💾 Saved {total_count} ads to {filename}")
        return total_count
    
    def analyze_sustainability_trends(self, ads_generator, output_file="sustainability_trends.csv"):
        """Analyze sustainability ad trends over time"""
        date_counts = Counter()
        total_ads = 0
        
        for ads_batch in ads_generator:
            for ad in ads_batch:
                if "ad_delivery_start_time" in ad:
                    date = ad["ad_delivery_start_time"]
                    date_counts[date] += 1
                    total_ads += 1
        
        # Save trends to CSV
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date', 'count'])
            for date in sorted(date_counts.keys()):
                writer.writerow([date, date_counts[date]])
        
        print(f"📊 Analyzed {total_ads} ads. Trends saved to {output_file}")
        return date_counts

# Example usage function
def main():
    """Example usage of the improved API"""
    
    # Your app credentials
    app_id = '1085953080371790'
    app_secret = 'c30129eb139d373f3427d48fa6f39c74'
    
    # Get app access token (from your previous code)
    def get_app_access_token(app_id, app_secret):
        url = "https://graph.facebook.com/oauth/access_token"
        params = {
            "client_id": app_id,
            "client_secret": app_secret,
            "grant_type": "client_credentials"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Error getting token: {response.json()}")
    
    try:
        # Get access token
        access_token = get_app_access_token(app_id, app_secret)
        print(f"✅ Got access token: {access_token[:20]}...")
        
        # Initialize API
        api = ImprovedFbAdsLibraryAPI(access_token)
        
        # Search for sustainability ads
        print("\n🔍 Searching for sustainability ads...")
        ads_generator = api.search_ads(
            search_terms="sustainability",
            countries=["US"],
            after_date="2024-01-01"
        )
        
        # Count ads
        total_count = api.count_ads(ads_generator)
        print(f"📊 Total sustainability ads found: {total_count}")
        
        # Save to CSV
        fields = ["id", "ad_creative_body", "page_name", "ad_delivery_start_time", "publisher_platforms"]
        ads_generator = api.search_ads(
            search_terms="sustainability",
            countries=["US"],
            after_date="2024-01-01"
        )
        api.save_to_csv(ads_generator, "sustainability_ads.csv", fields)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
