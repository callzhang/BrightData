#!/usr/bin/env python3
"""
Product Analyzer for E-commerce Competitive Intelligence

This module provides comprehensive product analysis capabilities using embeddings
to identify market opportunities, competitive gaps, and strategic insights for Walmart.

Features:
- Cross-platform product comparison
- Category gap analysis
- Competitive intelligence
- Market opportunity identification
- Strategic recommendations

Author: Derek
Date: 2025-01-15
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np

# Local imports
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from embedding.embedding_server import EmbeddingServer, ProductEmbedding, SimilarityResult
    from util.brightdata import BrightDataFilter
    from util.dataset_registry import get_dataset_schema
    from util.config import get_brightdata_api_key
except ImportError:
    # Fallback for direct execution
    from embedding_server import EmbeddingServer, ProductEmbedding, SimilarityResult
    from util.brightdata import BrightDataFilter
    from util.dataset_registry import get_dataset_schema
    from util.config import get_brightdata_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductAnalyzer:
    """
    Comprehensive product analysis system for competitive intelligence
    
    This class integrates with the BrightData system to:
    1. Fetch product data from multiple platforms
    2. Generate embeddings for semantic analysis
    3. Identify market gaps and opportunities
    4. Provide strategic recommendations
    """
    
    def __init__(self, embedding_server: Optional[EmbeddingServer] = None):
        """
        Initialize the ProductAnalyzer
        
        Args:
            embedding_server: Optional pre-initialized embedding server
        """
        # Initialize embedding server
        if embedding_server:
            self.embedding_server = embedding_server
        else:
            self.embedding_server = EmbeddingServer()
        
        # Initialize BrightData filter
        try:
            api_key = get_brightdata_api_key()
            self.brightdata_filter = BrightDataFilter(api_key)
        except Exception as e:
            logger.error(f"Failed to initialize BrightData filter: {e}")
            self.brightdata_filter = None
        
        # Dataset configurations
        self.datasets = {
            'amazon': 'gd_l7q7dkf244hwjntr0',
            'amazon_walmart': 'gd_m4l6s4mn2g2rkx9lia',
            'shopee': 'gd_lk122xxgf86xf97py'
        }
        
        # Analysis results cache
        self.analysis_cache = {}
    
    def fetch_platform_products(self, 
                               platform: str, 
                               category: Optional[str] = None,
                               limit: int = 1000,
                               min_rating: float = 4.0) -> List[Dict[str, Any]]:
        """
        Fetch products from a specific platform using BrightData
        
        Args:
            platform: Platform name (amazon, amazon_walmart, shopee)
            category: Optional category filter
            limit: Maximum number of products to fetch
            min_rating: Minimum rating filter
            
        Returns:
            List of product data dictionaries
        """
        if not self.brightdata_filter:
            logger.error("BrightData filter not initialized")
            return []
        
        if platform not in self.datasets:
            logger.error(f"Unknown platform: {platform}")
            return []
        
        logger.info(f"Fetching {limit} products from {platform}")
        
        try:
            # Get dataset schema for the platform
            dataset_schema = get_dataset_schema(self.datasets[platform])
            if not dataset_schema:
                logger.error(f"Unknown dataset: {self.datasets[platform]}")
                return []
            
            dataset_fields = dataset_schema.get_field_names()
            
            # Build filter criteria
            filters = []
            
            # Add rating filter
            if 'rating' in dataset_fields:
                filters.append({
                    'name': 'rating',
                    'operator': '>=',
                    'value': str(min_rating)
                })
            
            # Add category filter if specified
            if category and 'categories' in dataset_fields:
                filters.append({
                    'name': 'categories',
                    'operator': 'array_includes',
                    'value': category
                })
            elif category and 'category' in dataset_fields:
                filters.append({
                    'name': 'category',
                    'operator': '=',
                    'value': category
                })
            
            # Add availability filter
            if 'is_available' in dataset_fields:
                filters.append({
                    'name': 'is_available',
                    'operator': '=',
                    'value': 'true'
                })
            
            # Create filter object
            if len(filters) == 1:
                filter_obj = filters[0]
            else:
                filter_obj = {
                    'operator': 'and',
                    'filters': filters
                }
            
            # Submit query
            snapshot_id = self.brightdata_filter.search_data(
                filter_obj=filter_obj,
                records_limit=limit,
                description=f"Products from {platform} for embedding analysis",
                title=f"{platform.title()} Products Analysis"
            )
            
            logger.info(f"Submitted query for {platform}, snapshot ID: {snapshot_id}")
            
            # Wait for completion and download
            # Note: In a real implementation, you'd want to poll for completion
            # For now, we'll return the snapshot ID for manual download
            
            return {
                'snapshot_id': snapshot_id,
                'platform': platform,
                'status': 'submitted',
                'message': 'Query submitted successfully. Use snapshot_id to download results.'
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch products from {platform}: {e}")
            return []
    
    def load_products_from_snapshot(self, snapshot_id: str, platform: str) -> List[Dict[str, Any]]:
        """
        Load products from a downloaded snapshot
        
        Args:
            snapshot_id: BrightData snapshot ID
            platform: Platform name for context
            
        Returns:
            List of product data dictionaries
        """
        if not self.brightdata_filter:
            logger.error("BrightData filter not initialized")
            return []
        
        try:
            # Download snapshot content
            content = self.brightdata_filter.download_snapshot_content(
                snapshot_id=snapshot_id,
                format='json'
            )
            
            if not content:
                logger.error(f"No content found for snapshot {snapshot_id}")
                return []
            
            # Parse JSON content
            if isinstance(content, str):
                products = json.loads(content)
            else:
                products = content
            
            # Ensure it's a list
            if isinstance(products, dict):
                products = [products]
            
            logger.info(f"Loaded {len(products)} products from {platform}")
            return products
            
        except Exception as e:
            logger.error(f"Failed to load products from snapshot {snapshot_id}: {e}")
            return []
    
    def analyze_competitive_landscape(self, 
                                    walmart_products: List[Dict[str, Any]],
                                    competitor_products: List[Dict[str, Any]],
                                    competitor_platform: str = "amazon") -> Dict[str, Any]:
        """
        Analyze competitive landscape between Walmart and competitors
        
        Args:
            walmart_products: List of Walmart product data
            competitor_products: List of competitor product data
            competitor_platform: Name of competitor platform
            
        Returns:
            Comprehensive competitive analysis results
        """
        logger.info(f"Analyzing competitive landscape: Walmart vs {competitor_platform}")
        
        # Generate embeddings for both platforms
        walmart_embeddings = self.embedding_server.embed_products_batch(
            walmart_products, platform="walmart"
        )
        
        competitor_embeddings = self.embedding_server.embed_products_batch(
            competitor_products, platform=competitor_platform
        )
        
        # Perform gap analysis
        gap_analysis = self.embedding_server.analyze_category_gaps(
            walmart_embeddings, competitor_embeddings
        )
        
        # Find competitive products
        competitive_products = self.embedding_server.find_competitive_products(
            walmart_embeddings, competitor_embeddings
        )
        
        # Analyze pricing strategies
        pricing_analysis = self._analyze_pricing_strategies(
            walmart_products, competitor_products
        )
        
        # Generate strategic recommendations
        recommendations = self._generate_strategic_recommendations(
            gap_analysis, competitive_products, pricing_analysis
        )
        
        # Compile results
        analysis_results = {
            'analysis_date': datetime.now().isoformat(),
            'platforms_analyzed': {
                'walmart': len(walmart_products),
                competitor_platform: len(competitor_products)
            },
            'gap_analysis': gap_analysis,
            'competitive_products': [
                {
                    'walmart_product': {
                        'title': result.product_a.title,
                        'brand': result.product_a.brand,
                        'category': result.product_a.category,
                        'price': result.product_a.metadata.get('price')
                    },
                    'competitor_product': {
                        'title': result.product_b.title,
                        'brand': result.product_b.brand,
                        'category': result.product_b.category,
                        'price': result.product_b.metadata.get('price')
                    },
                    'similarity_score': result.similarity_score,
                    'price_difference': result.price_difference
                }
                for result in competitive_products[:20]  # Top 20
            ],
            'pricing_analysis': pricing_analysis,
            'strategic_recommendations': recommendations,
            'summary': {
                'total_weak_categories': len(gap_analysis['weak_categories']),
                'total_opportunity_categories': len(gap_analysis['opportunity_categories']),
                'total_competitive_products': len(competitive_products),
                'avg_similarity_score': np.mean([r.similarity_score for r in competitive_products]) if competitive_products else 0
            }
        }
        
        # Cache results
        cache_key = f"competitive_analysis_{competitor_platform}_{datetime.now().strftime('%Y%m%d')}"
        self.analysis_cache[cache_key] = analysis_results
        
        logger.info("Competitive landscape analysis completed")
        return analysis_results
    
    def _analyze_pricing_strategies(self, 
                                  walmart_products: List[Dict[str, Any]],
                                  competitor_products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze pricing strategies between platforms"""
        
        # Extract prices
        walmart_prices = [p.get('final_price', 0) for p in walmart_products if p.get('final_price')]
        competitor_prices = [p.get('final_price', 0) for p in competitor_products if p.get('final_price')]
        
        if not walmart_prices or not competitor_prices:
            return {'error': 'Insufficient pricing data'}
        
        # Calculate statistics
        walmart_stats = {
            'mean': np.mean(walmart_prices),
            'median': np.median(walmart_prices),
            'std': np.std(walmart_prices),
            'min': np.min(walmart_prices),
            'max': np.max(walmart_prices)
        }
        
        competitor_stats = {
            'mean': np.mean(competitor_prices),
            'median': np.median(competitor_prices),
            'std': np.std(competitor_prices),
            'min': np.min(competitor_prices),
            'max': np.max(competitor_prices)
        }
        
        # Price comparison
        price_advantage = {
            'walmart_cheaper_percentage': len([p for p in walmart_prices if p < np.mean(competitor_prices)]) / len(walmart_prices) * 100,
            'competitor_cheaper_percentage': len([p for p in competitor_prices if p < np.mean(walmart_prices)]) / len(competitor_prices) * 100,
            'avg_price_difference': np.mean(walmart_prices) - np.mean(competitor_prices)
        }
        
        return {
            'walmart_pricing': walmart_stats,
            'competitor_pricing': competitor_stats,
            'price_comparison': price_advantage
        }
    
    def _generate_strategic_recommendations(self, 
                                          gap_analysis: Dict[str, Any],
                                          competitive_products: List[SimilarityResult],
                                          pricing_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategic recommendations based on analysis"""
        
        recommendations = []
        
        # Category gap recommendations
        for weak_category in gap_analysis['weak_categories'][:5]:  # Top 5
            recommendations.append({
                'type': 'category_expansion',
                'priority': 'high',
                'category': weak_category['category'],
                'recommendation': f"Expand {weak_category['category']} category - competitors have {weak_category['competitor_count']} products vs Walmart's {weak_category['walmart_count']}",
                'opportunity_score': weak_category['opportunity_score'],
                'action': f"Add {weak_category['gap']} products to {weak_category['category']} category"
            })
        
        # Pricing recommendations
        if 'price_comparison' in pricing_analysis:
            price_comp = pricing_analysis['price_comparison']
            if price_comp['avg_price_difference'] > 0:
                recommendations.append({
                    'type': 'pricing_strategy',
                    'priority': 'medium',
                    'recommendation': f"Walmart prices are ${price_comp['avg_price_difference']:.2f} higher on average",
                    'action': "Review pricing strategy to improve competitiveness"
                })
        
        # Competitive product recommendations
        high_similarity_products = [p for p in competitive_products if p.similarity_score > 0.9]
        if high_similarity_products:
            recommendations.append({
                'type': 'product_optimization',
                'priority': 'high',
                'recommendation': f"Found {len(high_similarity_products)} highly similar products with competitors",
                'action': "Review product positioning and differentiation strategies"
            })
        
        return recommendations
    
    def generate_market_opportunity_report(self, 
                                         analysis_results: Dict[str, Any],
                                         output_file: Optional[str] = None) -> str:
        """
        Generate a comprehensive market opportunity report
        
        Args:
            analysis_results: Results from competitive analysis
            output_file: Optional output file path
            
        Returns:
            Report content as string
        """
        
        report = f"""
# Walmart Competitive Intelligence Report
Generated: {analysis_results['analysis_date']}

## Executive Summary

This report analyzes Walmart's competitive position against {list(analysis_results['platforms_analyzed'].keys())[1]} 
based on product catalog analysis using semantic embeddings.

### Key Findings:
- **Weak Categories**: {analysis_results['summary']['total_weak_categories']} categories where competitors significantly outperform Walmart
- **Opportunity Categories**: {analysis_results['summary']['total_opportunity_categories']} categories with growth potential
- **Competitive Products**: {analysis_results['summary']['total_competitive_products']} direct product competitors identified
- **Average Similarity**: {analysis_results['summary']['avg_similarity_score']:.2f} similarity score with competitor products

## Category Gap Analysis

### Weak Categories (High Priority)
"""
        
        for category in analysis_results['gap_analysis']['weak_categories'][:10]:
            report += f"""
**{category['category']}**
- Walmart Products: {category['walmart_count']}
- Competitor Products: {category['competitor_count']}
- Gap: {category['gap']} products
- Opportunity Score: {category['opportunity_score']}
"""
        
        report += """
### Opportunity Categories (Medium Priority)
"""
        
        for category in analysis_results['gap_analysis']['opportunity_categories'][:10]:
            report += f"""
**{category['category']}**
- Walmart Products: {category['walmart_count']}
- Competitor Products: {category['competitor_count']}
- Gap: {category['gap']} products
- Opportunity Score: {category['opportunity_score']}
"""
        
        report += """
## Strategic Recommendations

### High Priority Actions
"""
        
        high_priority = [r for r in analysis_results['strategic_recommendations'] if r['priority'] == 'high']
        for rec in high_priority:
            report += f"""
**{rec['type'].replace('_', ' ').title()}**
- {rec['recommendation']}
- Action: {rec['action']}
"""
        
        report += """
### Medium Priority Actions
"""
        
        medium_priority = [r for r in analysis_results['strategic_recommendations'] if r['priority'] == 'medium']
        for rec in medium_priority:
            report += f"""
**{rec['type'].replace('_', ' ').title()}**
- {rec['recommendation']}
- Action: {rec['action']}
"""
        
        report += """
## Competitive Product Analysis

### Top Competitive Products
"""
        
        for i, product in enumerate(analysis_results['competitive_products'][:10], 1):
            report += f"""
**{i}. {product['walmart_product']['title']} vs {product['competitor_product']['title']}**
- Similarity Score: {product['similarity_score']:.3f}
- Walmart Price: ${product['walmart_product']['price'] or 'N/A'}
- Competitor Price: ${product['competitor_product']['price'] or 'N/A'}
- Price Difference: ${product['price_difference'] or 'N/A'}
"""
        
        report += """
## Next Steps

1. **Immediate Actions (1-2 weeks)**:
   - Review top weak categories for quick wins
   - Analyze pricing strategies for competitive products
   - Identify suppliers for gap categories

2. **Short-term Actions (1-3 months)**:
   - Develop category expansion plans
   - Implement pricing optimization strategies
   - Launch competitive product analysis

3. **Long-term Actions (3-12 months)**:
   - Build comprehensive category coverage
   - Develop competitive intelligence monitoring
   - Implement dynamic pricing strategies

---
*Report generated by Walmart Competitive Intelligence System*
"""
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Report saved to {output_file}")
        
        return report
    
    def save_analysis_results(self, results: Dict[str, Any], filename: str):
        """Save analysis results to JSON file"""
        output_path = Path("analysis_results") / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Analysis results saved to {output_path}")
    
    def load_analysis_results(self, filename: str) -> Dict[str, Any]:
        """Load analysis results from JSON file"""
        input_path = Path("analysis_results") / filename
        
        if not input_path.exists():
            logger.error(f"Analysis file not found: {input_path}")
            return {}
        
        with open(input_path, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        logger.info(f"Analysis results loaded from {input_path}")
        return results

def main():
    """Example usage of the ProductAnalyzer"""
    
    # Initialize analyzer
    analyzer = ProductAnalyzer()
    
    # Example: Load sample data and perform analysis
    sample_walmart_products = [
        {
            'title': 'Wireless Bluetooth Headphones',
            'description': 'High-quality wireless headphones with noise cancellation',
            'brand': 'Sony',
            'category': 'Electronics',
            'final_price': 99.99,
            'rating': 4.5,
            'reviews_count': 1250
        }
    ]
    
    sample_amazon_products = [
        {
            'title': 'Bluetooth Wireless Headphones',
            'description': 'Premium wireless headphones with active noise cancellation',
            'brand': 'Sony',
            'category': 'Electronics',
            'final_price': 89.99,
            'rating': 4.6,
            'reviews_count': 2100
        }
    ]
    
    # Perform competitive analysis
    results = analyzer.analyze_competitive_landscape(
        sample_walmart_products, 
        sample_amazon_products, 
        "amazon"
    )
    
    # Generate report
    report = analyzer.generate_market_opportunity_report(results)
    print(report)

if __name__ == "__main__":
    main()
