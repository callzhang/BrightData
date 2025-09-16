#!/usr/bin/env python3
"""
Embedding Server Use Cases and Integration Examples

This module demonstrates how to use the embedding server for various scenarios
and how to integrate it with existing applications like snapshot_viewer.

Author: Derek
Date: 2025-01-15
"""

import sys
import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
from datetime import datetime

# Local imports
from embedding_server import EmbeddingServer, ProductEmbedding
from product_analyzer import ProductAnalyzer
from util.brightdata import BrightDataFilter
from util.config import get_brightdata_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingUseCases:
    """
    Comprehensive use cases for the embedding server
    """
    
    def __init__(self):
        """Initialize the use cases with embedding server and analyzer"""
        self.embedding_server = EmbeddingServer()
        self.product_analyzer = ProductAnalyzer(self.embedding_server)
        
    def use_case_1_basic_product_similarity(self):
        """
        Use Case 1: Basic Product Similarity Analysis
        
        Scenario: Find similar products between two platforms
        """
        print("🔍 Use Case 1: Basic Product Similarity Analysis")
        print("=" * 60)
        
        # Sample products from different platforms
        walmart_products = [
            {
                'title': 'Apple iPhone 15 Pro 128GB Natural Titanium',
                'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system',
                'brand': 'Apple',
                'category': 'Electronics',
                'final_price': 999.99,
                'rating': 4.8,
                'reviews_count': 2500
            },
            {
                'title': 'Samsung Galaxy S24 Ultra 256GB Titanium Black',
                'description': 'Premium Android smartphone with S Pen, 200MP camera, and AI features',
                'brand': 'Samsung',
                'category': 'Electronics',
                'final_price': 1199.99,
                'rating': 4.6,
                'reviews_count': 1800
            }
        ]
        
        amazon_products = [
            {
                'title': 'iPhone 15 Pro 128GB Natural Titanium - Unlocked',
                'description': 'Apple iPhone 15 Pro with titanium build, A17 Pro processor, and Pro camera system',
                'brand': 'Apple',
                'category': 'Electronics',
                'final_price': 999.99,
                'rating': 4.7,
                'reviews_count': 3200
            },
            {
                'title': 'Samsung Galaxy S24 Ultra 256GB Titanium Black - Unlocked',
                'description': 'Samsung Galaxy S24 Ultra with S Pen stylus, 200MP camera, and advanced AI',
                'brand': 'Samsung',
                'category': 'Electronics',
                'final_price': 1199.99,
                'rating': 4.5,
                'reviews_count': 2100
            }
        ]
        
        # Generate embeddings
        walmart_embeddings = self.embedding_server.embed_products_batch(walmart_products, "walmart")
        amazon_embeddings = self.embedding_server.embed_products_batch(amazon_products, "amazon")
        
        # Find similar products
        print("\n📊 Similarity Analysis Results:")
        for walmart_product in walmart_embeddings:
            similar_products = self.embedding_server.find_similar_products(
                walmart_product, amazon_embeddings, top_k=2, min_similarity=0.7
            )
            
            print(f"\n🛒 Walmart: {walmart_product.title}")
            for result in similar_products:
                print(f"   📱 Amazon: {result.product_b.title}")
                print(f"   🎯 Similarity: {result.similarity_score:.3f}")
                print(f"   💰 Price Diff: ${result.price_difference:.2f}" if result.price_difference else "   💰 Price: N/A")
        
        return {
            'walmart_embeddings': walmart_embeddings,
            'amazon_embeddings': amazon_embeddings,
            'similarity_results': similar_products
        }
    
    def use_case_2_category_gap_analysis(self):
        """
        Use Case 2: Category Gap Analysis for Market Opportunities
        
        Scenario: Identify weak categories where Walmart is behind competitors
        """
        print("\n🎯 Use Case 2: Category Gap Analysis")
        print("=" * 60)
        
        # Simulate category data
        walmart_products = [
            {'title': 'Wireless Headphones', 'category': 'Electronics', 'brand': 'Sony', 'final_price': 99.99},
            {'title': 'Yoga Mat', 'category': 'Sports', 'brand': 'Lululemon', 'final_price': 68.00},
            {'title': 'Coffee Beans', 'category': 'Food', 'brand': 'Starbucks', 'final_price': 12.99},
            {'title': 'Phone Case', 'category': 'Electronics', 'brand': 'Apple', 'final_price': 29.99},
        ]
        
        amazon_products = [
            {'title': 'Bluetooth Headphones', 'category': 'Electronics', 'brand': 'Sony', 'final_price': 89.99},
            {'title': 'Premium Yoga Mat', 'category': 'Sports', 'brand': 'Manduka', 'final_price': 75.00},
            {'title': 'Gourmet Coffee', 'category': 'Food', 'brand': 'Blue Bottle', 'final_price': 15.99},
            {'title': 'iPhone Case', 'category': 'Electronics', 'brand': 'Apple', 'final_price': 34.99},
            {'title': 'Gaming Keyboard', 'category': 'Electronics', 'brand': 'Corsair', 'final_price': 129.99},
            {'title': 'Fitness Tracker', 'category': 'Electronics', 'brand': 'Fitbit', 'final_price': 199.99},
            {'title': 'Protein Powder', 'category': 'Health', 'brand': 'Optimum Nutrition', 'final_price': 49.99},
            {'title': 'Skincare Set', 'category': 'Beauty', 'brand': 'The Ordinary', 'final_price': 39.99},
        ]
        
        # Generate embeddings
        walmart_embeddings = self.embedding_server.embed_products_batch(walmart_products, "walmart")
        amazon_embeddings = self.embedding_server.embed_products_batch(amazon_products, "amazon")
        
        # Perform gap analysis
        gap_analysis = self.embedding_server.analyze_category_gaps(walmart_embeddings, amazon_embeddings)
        
        print("\n📈 Category Gap Analysis Results:")
        print(f"   🚨 Weak Categories: {len(gap_analysis['weak_categories'])}")
        print(f"   💡 Opportunity Categories: {len(gap_analysis['opportunity_categories'])}")
        print(f"   ✅ Strong Categories: {len(gap_analysis['strong_categories'])}")
        
        if gap_analysis['weak_categories']:
            print("\n🚨 Weak Categories (High Priority):")
            for category in gap_analysis['weak_categories']:
                print(f"   📦 {category['category']}: Walmart {category['walmart_count']} vs Amazon {category['competitor_count']} (Gap: {category['gap']})")
        
        if gap_analysis['opportunity_categories']:
            print("\n💡 Opportunity Categories (Medium Priority):")
            for category in gap_analysis['opportunity_categories']:
                print(f"   📦 {category['category']}: Walmart {category['walmart_count']} vs Amazon {category['competitor_count']} (Gap: {category['gap']})")
        
        return gap_analysis
    
    def use_case_3_competitive_intelligence(self):
        """
        Use Case 3: Competitive Intelligence Analysis
        
        Scenario: Comprehensive competitive analysis with strategic recommendations
        """
        print("\n🏆 Use Case 3: Competitive Intelligence Analysis")
        print("=" * 60)
        
        # Sample competitive data
        walmart_products = [
            {
                'title': 'Apple AirPods Pro 2nd Generation',
                'description': 'Active noise cancellation, spatial audio, and wireless charging case',
                'brand': 'Apple',
                'category': 'Electronics',
                'final_price': 249.99,
                'rating': 4.7,
                'reviews_count': 15000
            },
            {
                'title': 'Sony WH-1000XM5 Wireless Headphones',
                'description': 'Industry-leading noise canceling with 30-hour battery life',
                'brand': 'Sony',
                'category': 'Electronics',
                'final_price': 399.99,
                'rating': 4.8,
                'reviews_count': 8500
            }
        ]
        
        amazon_products = [
            {
                'title': 'Apple AirPods Pro (2nd Generation) with MagSafe Case',
                'description': 'Active noise cancellation, adaptive transparency, and spatial audio',
                'brand': 'Apple',
                'category': 'Electronics',
                'final_price': 229.99,
                'rating': 4.6,
                'reviews_count': 25000
            },
            {
                'title': 'Sony WH-1000XM5 Premium Noise Canceling Headphones',
                'description': 'Best-in-class noise canceling, 30-hour battery, quick charge',
                'brand': 'Sony',
                'category': 'Electronics',
                'final_price': 379.99,
                'rating': 4.7,
                'reviews_count': 12000
            }
        ]
        
        # Perform competitive analysis
        analysis_results = self.product_analyzer.analyze_competitive_landscape(
            walmart_products, amazon_products, "amazon"
        )
        
        print("\n📊 Competitive Analysis Results:")
        print(f"   🎯 Competitive Products Found: {analysis_results['summary']['total_competitive_products']}")
        print(f"   📈 Average Similarity Score: {analysis_results['summary']['avg_similarity_score']:.3f}")
        
        print("\n💡 Strategic Recommendations:")
        for i, rec in enumerate(analysis_results['strategic_recommendations'][:3], 1):
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            print(f"   {i}. {priority_emoji} {rec['recommendation']}")
            print(f"      Action: {rec['action']}")
        
        return analysis_results
    
    def use_case_4_batch_processing(self):
        """
        Use Case 4: Batch Processing for Large Datasets
        
        Scenario: Process large product catalogs efficiently
        """
        print("\n⚡ Use Case 4: Batch Processing for Large Datasets")
        print("=" * 60)
        
        # Generate large sample dataset
        categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty']
        brands = ['Apple', 'Samsung', 'Sony', 'Nike', 'Adidas', 'Amazon Basics', 'Generic']
        
        large_product_list = []
        for i in range(50):  # 50 products for demo
            category = categories[i % len(categories)]
            brand = brands[i % len(brands)]
            
            product = {
                'title': f'{brand} Product {i+1} - {category}',
                'description': f'High-quality {category.lower()} product from {brand} with advanced features',
                'brand': brand,
                'category': category,
                'final_price': round(10 + (i * 5.5), 2),
                'rating': round(3.5 + (i % 15) * 0.1, 1),
                'reviews_count': 100 + (i * 25)
            }
            large_product_list.append(product)
        
        print(f"📦 Processing {len(large_product_list)} products...")
        
        # Batch processing
        start_time = datetime.now()
        embeddings = self.embedding_server.embed_products_batch(large_product_list, "batch_test")
        end_time = datetime.now()
        
        processing_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Batch processing completed!")
        print(f"   📊 Products processed: {len(embeddings)}")
        print(f"   ⏱️  Processing time: {processing_time:.2f} seconds")
        print(f"   🚀 Speed: {len(embeddings)/processing_time:.1f} products/second")
        print(f"   💾 Memory usage: {self.embedding_server.get_embedding_stats()['cache_size_mb']:.2f} MB")
        
        return embeddings
    
    def use_case_5_integration_with_snapshots(self):
        """
        Use Case 5: Integration with Existing Snapshot Data
        
        Scenario: Use embedding server with existing BrightData snapshots
        """
        print("\n🔗 Use Case 5: Integration with Existing Snapshot Data")
        print("=" * 60)
        
        # Check for existing snapshots
        snapshot_dir = Path("snapshot_records")
        if not snapshot_dir.exists():
            print("❌ No snapshot records found. Please create some snapshots first.")
            return None
        
        snapshot_files = list(snapshot_dir.glob("*.json"))
        if not snapshot_files:
            print("❌ No snapshot files found in snapshot_records/")
            return None
        
        print(f"📁 Found {len(snapshot_files)} snapshot files")
        
        # Load and process first snapshot
        snapshot_file = snapshot_files[0]
        print(f"📄 Processing snapshot: {snapshot_file.name}")
        
        try:
            with open(snapshot_file, 'r') as f:
                snapshot_data = json.load(f)
            
            # Extract product data (this would need to be adapted based on your snapshot format)
            if 'products' in snapshot_data:
                products = snapshot_data['products']
            elif isinstance(snapshot_data, list):
                products = snapshot_data
            else:
                # Convert snapshot metadata to product format
                products = [{
                    'title': snapshot_data.get('title', 'Unknown Product'),
                    'description': snapshot_data.get('description', ''),
                    'brand': snapshot_data.get('brand', 'Unknown'),
                    'category': snapshot_data.get('category', 'General'),
                    'final_price': snapshot_data.get('price', 0),
                    'rating': snapshot_data.get('rating', 0),
                    'reviews_count': snapshot_data.get('reviews_count', 0)
                }]
            
            print(f"📦 Found {len(products)} products in snapshot")
            
            # Generate embeddings
            embeddings = self.embedding_server.embed_products_batch(products[:10], "snapshot")  # Limit to 10 for demo
            
            print(f"✅ Generated {len(embeddings)} embeddings from snapshot data")
            
            return embeddings
            
        except Exception as e:
            print(f"❌ Error processing snapshot: {e}")
            return None

def integration_with_snapshot_viewer():
    """
    Example of how to integrate embedding server with snapshot_viewer
    """
    print("\n🔗 Integration with Snapshot Viewer")
    print("=" * 60)
    
    # This shows how you would modify snapshot_viewer.py to include embedding analysis
    
    integration_code = '''
# Add this to your snapshot_viewer.py

import streamlit as st
from embedding_server import EmbeddingServer
from product_analyzer import ProductAnalyzer

# Initialize embedding components (add to your imports)
@st.cache_resource
def get_embedding_server():
    return EmbeddingServer()

@st.cache_resource  
def get_product_analyzer():
    return ProductAnalyzer(get_embedding_server())

# Add embedding analysis tab to your Streamlit app
def embedding_analysis_tab():
    st.header("🔍 Product Embedding Analysis")
    
    embedding_server = get_embedding_server()
    analyzer = get_product_analyzer()
    
    # Load snapshot data
    if st.button("Load Snapshot for Analysis"):
        # Your existing snapshot loading logic
        snapshot_data = load_snapshot_data()  # Your existing function
        
        if snapshot_data:
            # Generate embeddings
            with st.spinner("Generating embeddings..."):
                embeddings = embedding_server.embed_products_batch(
                    snapshot_data, platform="analysis"
                )
            
            st.success(f"Generated {len(embeddings)} embeddings!")
            
            # Show similarity analysis
            if len(embeddings) > 1:
                st.subheader("📊 Product Similarity Analysis")
                
                # Find most similar products
                query_product = st.selectbox(
                    "Select product to analyze:",
                    [f"{e.title} ({e.brand})" for e in embeddings]
                )
                
                if st.button("Find Similar Products"):
                    query_idx = [f"{e.title} ({e.brand})" for e in embeddings].index(query_product)
                    similar_products = embedding_server.find_similar_products(
                        embeddings[query_idx], 
                        [e for i, e in enumerate(embeddings) if i != query_idx],
                        top_k=5
                    )
                    
                    for result in similar_products:
                        st.write(f"**{result.product_b.title}** - Similarity: {result.similarity_score:.3f}")
    
    # Category gap analysis
    if st.button("Analyze Category Gaps"):
        st.subheader("🎯 Category Gap Analysis")
        # Your category gap analysis logic here
        st.info("Category gap analysis would show weak categories and opportunities")

# Add to your main Streamlit app
def main():
    # Your existing tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Snapshots", "📥 Downloads", "⚙️ Settings", "🔍 Embedding Analysis"])
    
    with tab4:
        embedding_analysis_tab()
'''
    
    print("📝 Integration Code Example:")
    print(integration_code)
    
    return integration_code

def main():
    """Run all use cases"""
    print("🚀 Embedding Server Use Cases Demo")
    print("=" * 80)
    
    use_cases = EmbeddingUseCases()
    
    # Run all use cases
    results = {}
    
    try:
        results['similarity'] = use_cases.use_case_1_basic_product_similarity()
        results['gap_analysis'] = use_cases.use_case_2_category_gap_analysis()
        results['competitive'] = use_cases.use_case_3_competitive_intelligence()
        results['batch_processing'] = use_cases.use_case_4_batch_processing()
        results['snapshot_integration'] = use_cases.use_case_5_integration_with_snapshots()
        
        # Show integration example
        integration_with_snapshot_viewer()
        
        print("\n🎉 All use cases completed successfully!")
        print(f"📊 Results summary: {len(results)} use cases executed")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"embedding_use_cases_results_{timestamp}.json"
        
        # Convert results to serializable format
        serializable_results = {}
        for key, value in results.items():
            if value is not None:
                if key == 'similarity' and 'walmart_embeddings' in value:
                    serializable_results[key] = {
                        'walmart_count': len(value['walmart_embeddings']),
                        'amazon_count': len(value['amazon_embeddings']),
                        'similarity_count': len(value['similarity_results'])
                    }
                elif key == 'gap_analysis':
                    serializable_results[key] = {
                        'weak_categories': len(value['weak_categories']),
                        'opportunity_categories': len(value['opportunity_categories']),
                        'strong_categories': len(value['strong_categories'])
                    }
                elif key == 'competitive':
                    serializable_results[key] = value['summary']
                elif key == 'batch_processing':
                    serializable_results[key] = {'processed_count': len(value)}
                else:
                    serializable_results[key] = str(value)
        
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")
        
    except Exception as e:
        print(f"❌ Error running use cases: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
