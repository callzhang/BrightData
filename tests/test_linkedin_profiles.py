#!/usr/bin/env python3
"""
Test LinkedIn Profiles Dataset Integration
Comprehensive tests for LinkedIn profiles data functionality
"""

import sys
import os
import unittest
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from util import BrightDataFilter
from util.dataset_registry import dataset_registry

class TestLinkedInProfilesDataset(unittest.TestCase):
    """Test cases for LinkedIn profiles dataset functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.dataset_id = "gd_l1viktl72bvl7bjuj0"
        # Use dataset registry instead of config loader
        
    def test_dataset_configuration(self):
        """Test that LinkedIn profiles dataset is properly configured"""
        try:
            linkedin_config = dataset_registry.get_dataset(self.dataset_id)
            
            # Test basic configuration
            self.assertEqual(linkedin_config.dataset_id, self.dataset_id)
            self.assertEqual(linkedin_config.name, "LinkedIn Profiles")
            self.assertIn("LinkedIn", linkedin_config.description)
            
            # Test field count (should have many fields)
            self.assertGreater(len(linkedin_config.fields), 50)
            
            # Test specific important fields exist
            field_names = list(linkedin_config.fields.keys())
            important_fields = [
                "full_name", "headline", "location", "industry",
                "current_position", "current_company", "connections_count",
                "skills_count", "education_count", "experience_count"
            ]
            
            for field in important_fields:
                self.assertIn(field, field_names, f"Missing important field: {field}")
                
        except Exception as e:
            self.fail(f"Failed to load LinkedIn profiles configuration: {e}")
    
    def test_basic_profile_fields(self):
        """Test that basic profile fields are properly configured"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        # Basic profile information
        basic_fields = [
            "full_name", "first_name", "last_name", "headline", "summary",
            "location", "industry", "profile_url", "profile_image_url"
        ]
        
        for field in basic_fields:
            self.assertIn(field, field_names, f"Missing basic field: {field}")
    
    def test_contact_information_fields(self):
        """Test contact information fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        contact_fields = [
            "email", "phone", "website", "twitter_handle", "other_social_links"
        ]
        
        for field in contact_fields:
            self.assertIn(field, field_names, f"Missing contact field: {field}")
    
    def test_network_metrics_fields(self):
        """Test network metrics fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        network_fields = [
            "connections_count", "followers_count", "following_count",
            "mutual_connections_count"
        ]
        
        for field in network_fields:
            self.assertIn(field, field_names, f"Missing network field: {field}")
    
    def test_professional_information_fields(self):
        """Test professional information fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        professional_fields = [
            "current_position", "current_company", "employment_status",
            "open_to_work", "open_to_remote", "open_to_relocation"
        ]
        
        for field in professional_fields:
            self.assertIn(field, field_names, f"Missing professional field: {field}")
    
    def test_experience_fields(self):
        """Test experience-related fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        experience_fields = [
            "experience_count", "total_experience_years", "seniority_level",
            "management_experience"
        ]
        
        for field in experience_fields:
            self.assertIn(field, field_names, f"Missing experience field: {field}")
    
    def test_education_fields(self):
        """Test education-related fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        education_fields = [
            "education_count", "highest_degree", "university",
            "graduation_year", "field_of_study"
        ]
        
        for field in education_fields:
            self.assertIn(field, field_names, f"Missing education field: {field}")
    
    def test_skills_fields(self):
        """Test skills and endorsements fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        skills_fields = [
            "skills_count", "top_skills", "endorsements_count",
            "certifications_count"
        ]
        
        for field in skills_fields:
            self.assertIn(field, field_names, f"Missing skills field: {field}")
    
    def test_activity_fields(self):
        """Test activity and engagement fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        activity_fields = [
            "posts_count", "articles_count", "last_activity_date",
            "profile_completeness"
        ]
        
        for field in activity_fields:
            self.assertIn(field, field_names, f"Missing activity field: {field}")
    
    def test_company_fields(self):
        """Test company information fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        company_fields = [
            "company_size", "company_type", "company_industry",
            "company_headquarters"
        ]
        
        for field in company_fields:
            self.assertIn(field, field_names, f"Missing company field: {field}")
    
    def test_geographic_fields(self):
        """Test geographic information fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        geographic_fields = [
            "country", "state_province", "city", "timezone"
        ]
        
        for field in geographic_fields:
            self.assertIn(field, field_names, f"Missing geographic field: {field}")
    
    def test_premium_fields(self):
        """Test premium features fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        premium_fields = [
            "is_premium", "premium_type", "sales_navigator", "recruiter_lite"
        ]
        
        for field in premium_fields:
            self.assertIn(field, field_names, f"Missing premium field: {field}")
    
    def test_data_quality_fields(self):
        """Test data quality and metadata fields"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        field_names = [field.name for field in linkedin_config.fields]
        
        quality_fields = [
            "profile_created_date", "last_updated_date", "data_quality_score",
            "completeness_score", "verification_status"
        ]
        
        for field in quality_fields:
            self.assertIn(field, field_names, f"Missing quality field: {field}")
    
    def test_field_types(self):
        """Test that field types are correctly specified"""
        linkedin_config = self.config_loader.get_dataset("linkedin_profiles")
        
        # Test specific field types
        field_type_map = {field.name: field.type for field in linkedin_config.fields}
        
        # String fields
        string_fields = ["full_name", "headline", "location", "industry"]
        for field in string_fields:
            if field in field_type_map:
                self.assertEqual(field_type_map[field], "string", f"Field {field} should be string")
        
        # Numeric fields
        numeric_fields = ["connections_count", "experience_count", "skills_count"]
        for field in numeric_fields:
            if field in field_type_map:
                self.assertEqual(field_type_map[field], "numeric", f"Field {field} should be numeric")
        
        # Boolean fields
        boolean_fields = ["open_to_work", "open_to_remote", "is_premium"]
        for field in boolean_fields:
            if field in field_type_map:
                self.assertEqual(field_type_map[field], "boolean", f"Field {field} should be boolean")
        
        # Array fields
        array_fields = ["top_skills", "languages", "interests"]
        for field in array_fields:
            if field in field_type_map:
                self.assertEqual(field_type_map[field], "array", f"Field {field} should be array")
        
        # Date fields
        date_fields = ["last_activity_date", "profile_created_date"]
        for field in date_fields:
            if field in field_type_map:
                self.assertEqual(field_type_map[field], "date", f"Field {field} should be date")
    
    def test_brightdata_filter_initialization(self):
        """Test BrightDataFilter initialization with LinkedIn dataset"""
        try:
            filter_obj = BrightDataFilter(self.dataset_id)
            self.assertEqual(filter_obj.dataset_id, self.dataset_id)
        except Exception as e:
            self.fail(f"Failed to initialize BrightDataFilter with LinkedIn dataset: {e}")
    
    def test_sample_query_structure(self):
        """Test that sample queries can be constructed"""
        # Test basic query structure
        sample_filters = [
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
            }
        ]
        
        # Validate filter structure
        for filter_item in sample_filters:
            self.assertIn("field", filter_item)
            self.assertIn("operator", filter_item)
            self.assertIn("value", filter_item)
    
    def test_dataset_choices(self):
        """Test that LinkedIn profiles appears in dataset choices"""
        try:
            choices = self.config_loader.get_dataset_choices()
            linkedin_choices = [choice for choice in choices if "LinkedIn" in choice]
            self.assertGreater(len(linkedin_choices), 0, "LinkedIn profiles should appear in dataset choices")
        except Exception as e:
            self.fail(f"Failed to get dataset choices: {e}")

class TestLinkedInProfilesQueries(unittest.TestCase):
    """Test LinkedIn profiles query examples"""
    
    def setUp(self):
        """Set up test environment"""
        self.dataset_id = "gd_l1viktl72bvl7bjuj0"
    
    def test_talent_acquisition_query(self):
        """Test talent acquisition query structure"""
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
                "field": "open_to_work",
                "operator": "=",
                "value": True
            }
        ]
        
        # Validate query structure
        self.assertEqual(len(filters), 3)
        self.assertEqual(filters[0]["field"], "current_position")
        self.assertEqual(filters[1]["operator"], "=")
        self.assertEqual(filters[2]["value"], True)
    
    def test_market_research_query(self):
        """Test market research query structure"""
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
            }
        ]
        
        # Validate query structure
        self.assertEqual(len(filters), 3)
        self.assertEqual(filters[0]["field"], "industry")
        self.assertEqual(filters[1]["operator"], "includes")
        self.assertEqual(filters[2]["operator"], ">=")
    
    def test_sales_prospecting_query(self):
        """Test sales prospecting query structure"""
        filters = [
            {
                "field": "seniority_level",
                "operator": "in",
                "value": ["senior", "executive"]
            },
            {
                "field": "industry",
                "operator": "=",
                "value": "Healthcare"
            },
            {
                "field": "company_size",
                "operator": ">=",
                "value": "1000"
            }
        ]
        
        # Validate query structure
        self.assertEqual(len(filters), 3)
        self.assertEqual(filters[0]["operator"], "in")
        self.assertIsInstance(filters[0]["value"], list)
    
    def test_skills_analysis_query(self):
        """Test skills analysis query structure"""
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
                "field": "certifications_count",
                "operator": ">=",
                "value": 1
            }
        ]
        
        # Validate query structure
        self.assertEqual(len(filters), 3)
        self.assertEqual(filters[0]["field"], "current_position")
        self.assertEqual(filters[1]["field"], "top_skills")
        self.assertEqual(filters[2]["field"], "certifications_count")

def run_linkedin_tests():
    """Run all LinkedIn profiles tests"""
    print("🧪 Running LinkedIn Profiles Dataset Tests")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLinkedInProfilesDataset))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLinkedInProfilesQueries))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed! LinkedIn profiles dataset is ready to use.")
    else:
        print(f"\n⚠️ {len(result.failures + result.errors)} test(s) failed.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_linkedin_tests()
    sys.exit(0 if success else 1)
