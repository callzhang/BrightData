#!/usr/bin/env python3
"""
Embedding Server for E-commerce Product Analysis

This module provides a local embedding server using all-MiniLM-L6-v2 for:
- Product text embedding generation
- Cross-platform product similarity analysis
- Weak category identification for Walmart
- Competitive intelligence and market analysis

Author: Derek
Date: 2025-01-15
"""

import os
import json
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import pickle
from datetime import datetime

# Core ML libraries
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import pandas as pd

# Local imports
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from util.config import get_brightdata_api_key
    from util.brightdata import BrightDataFilter
except ImportError:
    # Fallback for direct execution from embedding directory
    def get_brightdata_api_key():
        return None
    BrightDataFilter = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProductEmbedding:
    """Data class for storing product embedding information"""
    product_id: str
    platform: str
    title: str
    description: str
    brand: str
    category: str
    embedding: np.ndarray
    metadata: Dict[str, Any]
    created_at: datetime

@dataclass
class SimilarityResult:
    """Data class for similarity analysis results"""
    product_a: ProductEmbedding
    product_b: ProductEmbedding
    similarity_score: float
    category_match: bool
    platform_match: bool
    price_difference: Optional[float] = None

class EmbeddingServer:
    """
    Local embedding server for e-commerce product analysis
    
    Features:
    - Product text embedding generation
    - Cross-platform similarity analysis
    - Category gap analysis
    - Competitive intelligence
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_dir: str = "embedding_cache"):
        """
        Initialize the embedding server
        
        Args:
            model_name: Name of the sentence transformer model
            cache_dir: Directory to cache embeddings and models
        """
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize model
        self.model = None
        self.embeddings_cache = {}
        self.products_cache = {}
        
        # Load or initialize model
        self._load_model()
        
        # Initialize BrightData filter for data access
        try:
            api_key = get_brightdata_api_key()
            self.brightdata_filter = BrightDataFilter(api_key)
        except Exception as e:
            logger.warning(f"Could not initialize BrightData filter: {e}")
            self.brightdata_filter = None
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            model_path = self.cache_dir / f"{self.model_name.replace('/', '_')}"
            
            if model_path.exists():
                logger.info(f"Loading cached model from {model_path}")
                self.model = SentenceTransformer(str(model_path))
            else:
                logger.info(f"Downloading and caching model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                self.model.save(str(model_path))
                
            logger.info(f"Model loaded successfully: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _create_product_text(self, product_data: Dict[str, Any]) -> str:
        """
        Create a comprehensive text representation of a product
        
        Args:
            product_data: Product data dictionary
            
        Returns:
            Combined text string for embedding
        """
        # Extract key text fields
        title = product_data.get('title', '')
        description = product_data.get('description', '')
        brand = product_data.get('brand', '')
        category = product_data.get('category', '') or product_data.get('department', '')
        
        # Handle categories array
        if isinstance(category, list):
            category = ' '.join(category)
        
        # Combine features if available
        features = product_data.get('features', [])
        if isinstance(features, list):
            features_text = ' '.join(features)
        else:
            features_text = str(features) if features else ''
        
        # Create comprehensive text
        text_parts = [
            title,
            description,
            f"Brand: {brand}" if brand else "",
            f"Category: {category}" if category else "",
            f"Features: {features_text}" if features_text else ""
        ]
        
        # Filter out empty parts and join
        combined_text = ' '.join([part.strip() for part in text_parts if part.strip()])
        
        return combined_text
    
    def embed_product(self, product_data: Dict[str, Any], platform: str = "unknown") -> ProductEmbedding:
        """
        Generate embedding for a single product
        
        Args:
            product_data: Product data dictionary
            platform: Platform name (amazon, walmart, shopee)
            
        Returns:
            ProductEmbedding object
        """
        # Create product text
        product_text = self._create_product_text(product_data)
        
        # Generate embedding
        embedding = self.model.encode(product_text, convert_to_numpy=True)
        
        # Create product ID
        product_id = product_data.get('asin') or product_data.get('product_id') or product_data.get('id', 'unknown')
        
        # Extract metadata
        metadata = {
            'price': product_data.get('final_price'),
            'rating': product_data.get('rating'),
            'reviews_count': product_data.get('reviews_count'),
            'availability': product_data.get('is_available'),
            'seller': product_data.get('seller_name'),
            'url': product_data.get('url')
        }
        
        # Create ProductEmbedding object
        product_embedding = ProductEmbedding(
            product_id=product_id,
            platform=platform,
            title=product_data.get('title', ''),
            description=product_data.get('description', ''),
            brand=product_data.get('brand', ''),
            category=product_data.get('category', '') or product_data.get('department', ''),
            embedding=embedding,
            metadata=metadata,
            created_at=datetime.now()
        )
        
        # Cache the embedding
        cache_key = f"{platform}_{product_id}"
        self.embeddings_cache[cache_key] = product_embedding
        self.products_cache[cache_key] = product_data
        
        return product_embedding
    
    def embed_products_batch(self, products_data: List[Dict[str, Any]], platform: str = "unknown") -> List[ProductEmbedding]:
        """
        Generate embeddings for multiple products in batch
        
        Args:
            products_data: List of product data dictionaries
            platform: Platform name
            
        Returns:
            List of ProductEmbedding objects
        """
        logger.info(f"Processing {len(products_data)} products from {platform}")
        
        # Create product texts
        product_texts = [self._create_product_text(product) for product in products_data]
        
        # Generate embeddings in batch (more efficient)
        embeddings = self.model.encode(product_texts, convert_to_numpy=True, show_progress_bar=True)
        
        # Create ProductEmbedding objects
        product_embeddings = []
        for i, (product_data, embedding) in enumerate(zip(products_data, embeddings)):
            product_id = product_data.get('asin') or product_data.get('product_id') or product_data.get('id', f'unknown_{i}')
            
            metadata = {
                'price': product_data.get('final_price'),
                'rating': product_data.get('rating'),
                'reviews_count': product_data.get('reviews_count'),
                'availability': product_data.get('is_available'),
                'seller': product_data.get('seller_name'),
                'url': product_data.get('url')
            }
            
            product_embedding = ProductEmbedding(
                product_id=product_id,
                platform=platform,
                title=product_data.get('title', ''),
                description=product_data.get('description', ''),
                brand=product_data.get('brand', ''),
                category=product_data.get('category', '') or product_data.get('department', ''),
                embedding=embedding,
                metadata=metadata,
                created_at=datetime.now()
            )
            
            # Cache
            cache_key = f"{platform}_{product_id}"
            self.embeddings_cache[cache_key] = product_embedding
            self.products_cache[cache_key] = product_data
            
            product_embeddings.append(product_embedding)
        
        logger.info(f"Generated {len(product_embeddings)} embeddings for {platform}")
        return product_embeddings
    
    def find_similar_products(self, 
                            query_product: ProductEmbedding, 
                            candidate_products: List[ProductEmbedding],
                            top_k: int = 10,
                            min_similarity: float = 0.7) -> List[SimilarityResult]:
        """
        Find similar products based on embedding similarity
        
        Args:
            query_product: Product to find similarities for
            candidate_products: List of candidate products
            top_k: Number of top similar products to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of SimilarityResult objects
        """
        if not candidate_products:
            return []
        
        # Extract embeddings
        query_embedding = query_product.embedding.reshape(1, -1)
        candidate_embeddings = np.array([p.embedding for p in candidate_products])
        
        # Calculate cosine similarities
        similarities = cosine_similarity(query_embedding, candidate_embeddings)[0]
        
        # Create similarity results
        results = []
        for i, (candidate, similarity) in enumerate(zip(candidate_products, similarities)):
            if similarity >= min_similarity:
                # Check if same category
                category_match = (query_product.category.lower() == candidate.category.lower() 
                                if query_product.category and candidate.category else False)
                
                # Check if same platform
                platform_match = (query_product.platform == candidate.platform)
                
                # Calculate price difference if available
                price_diff = None
                if (query_product.metadata.get('price') and 
                    candidate.metadata.get('price')):
                    price_diff = abs(query_product.metadata['price'] - candidate.metadata['price'])
                
                result = SimilarityResult(
                    product_a=query_product,
                    product_b=candidate,
                    similarity_score=similarity,
                    category_match=category_match,
                    platform_match=platform_match,
                    price_difference=price_diff
                )
                results.append(result)
        
        # Sort by similarity score and return top_k
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]
    
    def analyze_category_gaps(self, 
                            walmart_products: List[ProductEmbedding],
                            competitor_products: List[ProductEmbedding],
                            min_products_per_category: int = 5) -> Dict[str, Any]:
        """
        Analyze category gaps between Walmart and competitors
        
        Args:
            walmart_products: List of Walmart product embeddings
            competitor_products: List of competitor product embeddings
            min_products_per_category: Minimum products needed to consider a category
            
        Returns:
            Dictionary with gap analysis results
        """
        logger.info("Analyzing category gaps between Walmart and competitors")
        
        # Group products by category
        walmart_categories = {}
        competitor_categories = {}
        
        for product in walmart_products:
            category = product.category or "Unknown"
            if category not in walmart_categories:
                walmart_categories[category] = []
            walmart_categories[category].append(product)
        
        for product in competitor_products:
            category = product.category or "Unknown"
            if category not in competitor_categories:
                competitor_categories[category] = []
            competitor_categories[category].append(product)
        
        # Find categories where competitors have more products
        gap_analysis = {
            'weak_categories': [],
            'opportunity_categories': [],
            'strong_categories': [],
            'category_stats': {}
        }
        
        all_categories = set(walmart_categories.keys()) | set(competitor_categories.keys())
        
        for category in all_categories:
            walmart_count = len(walmart_categories.get(category, []))
            competitor_count = len(competitor_categories.get(category, []))
            
            category_stats = {
                'walmart_count': walmart_count,
                'competitor_count': competitor_count,
                'gap': competitor_count - walmart_count,
                'gap_percentage': ((competitor_count - walmart_count) / max(competitor_count, 1)) * 100
            }
            
            gap_analysis['category_stats'][category] = category_stats
            
            # Categorize based on gap
            if competitor_count >= min_products_per_category:
                if walmart_count < competitor_count * 0.5:  # Less than 50% of competitor
                    gap_analysis['weak_categories'].append({
                        'category': category,
                        'walmart_count': walmart_count,
                        'competitor_count': competitor_count,
                        'gap': competitor_count - walmart_count,
                        'opportunity_score': competitor_count - walmart_count
                    })
                elif walmart_count < competitor_count * 0.8:  # Less than 80% of competitor
                    gap_analysis['opportunity_categories'].append({
                        'category': category,
                        'walmart_count': walmart_count,
                        'competitor_count': competitor_count,
                        'gap': competitor_count - walmart_count,
                        'opportunity_score': competitor_count - walmart_count
                    })
                else:
                    gap_analysis['strong_categories'].append({
                        'category': category,
                        'walmart_count': walmart_count,
                        'competitor_count': competitor_count,
                        'gap': competitor_count - walmart_count
                    })
        
        # Sort by opportunity score
        gap_analysis['weak_categories'].sort(key=lambda x: x['opportunity_score'], reverse=True)
        gap_analysis['opportunity_categories'].sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        logger.info(f"Found {len(gap_analysis['weak_categories'])} weak categories")
        logger.info(f"Found {len(gap_analysis['opportunity_categories'])} opportunity categories")
        
        return gap_analysis
    
    def find_competitive_products(self, 
                                walmart_products: List[ProductEmbedding],
                                competitor_products: List[ProductEmbedding],
                                similarity_threshold: float = 0.8) -> List[SimilarityResult]:
        """
        Find competitive products between Walmart and competitors
        
        Args:
            walmart_products: List of Walmart product embeddings
            competitor_products: List of competitor product embeddings
            similarity_threshold: Minimum similarity for competitive products
            
        Returns:
            List of SimilarityResult objects
        """
        logger.info("Finding competitive products between Walmart and competitors")
        
        competitive_products = []
        
        for walmart_product in walmart_products:
            # Find similar products from competitors
            similar_products = self.find_similar_products(
                walmart_product, 
                competitor_products,
                top_k=5,
                min_similarity=similarity_threshold
            )
            
            # Filter for cross-platform matches (different platforms)
            cross_platform_matches = [
                result for result in similar_products 
                if not result.platform_match
            ]
            
            competitive_products.extend(cross_platform_matches)
        
        # Sort by similarity score
        competitive_products.sort(key=lambda x: x.similarity_score, reverse=True)
        
        logger.info(f"Found {len(competitive_products)} competitive product pairs")
        return competitive_products
    
    def save_embeddings(self, filepath: str):
        """Save embeddings cache to file"""
        cache_data = {
            'embeddings': {k: {
                'product_id': v.product_id,
                'platform': v.platform,
                'title': v.title,
                'description': v.description,
                'brand': v.brand,
                'category': v.category,
                'embedding': v.embedding.tolist(),
                'metadata': v.metadata,
                'created_at': v.created_at.isoformat()
            } for k, v in self.embeddings_cache.items()},
            'products': self.products_cache
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(cache_data, f)
        
        logger.info(f"Saved embeddings cache to {filepath}")
    
    def load_embeddings(self, filepath: str):
        """Load embeddings cache from file"""
        if not os.path.exists(filepath):
            logger.warning(f"Cache file not found: {filepath}")
            return
        
        with open(filepath, 'rb') as f:
            cache_data = pickle.load(f)
        
        # Reconstruct embeddings
        self.embeddings_cache = {}
        for k, v in cache_data['embeddings'].items():
            embedding = ProductEmbedding(
                product_id=v['product_id'],
                platform=v['platform'],
                title=v['title'],
                description=v['description'],
                brand=v['brand'],
                category=v['category'],
                embedding=np.array(v['embedding']),
                metadata=v['metadata'],
                created_at=datetime.fromisoformat(v['created_at'])
            )
            self.embeddings_cache[k] = embedding
        
        self.products_cache = cache_data['products']
        logger.info(f"Loaded embeddings cache from {filepath}")
    
    def get_embedding_stats(self) -> Dict[str, Any]:
        """Get statistics about cached embeddings"""
        if not self.embeddings_cache:
            return {'total_embeddings': 0}
        
        platforms = {}
        categories = {}
        
        for embedding in self.embeddings_cache.values():
            # Count by platform
            platform = embedding.platform
            platforms[platform] = platforms.get(platform, 0) + 1
            
            # Count by category
            category = embedding.category or "Unknown"
            categories[category] = categories.get(category, 0) + 1
        
        return {
            'total_embeddings': len(self.embeddings_cache),
            'platforms': platforms,
            'categories': categories,
            'cache_size_mb': sum(
                embedding.embedding.nbytes for embedding in self.embeddings_cache.values()
            ) / (1024 * 1024)
        }

def main():
    """Example usage of the EmbeddingServer"""
    # Initialize server
    server = EmbeddingServer()
    
    # Example product data
    sample_products = [
        {
            'title': 'Wireless Bluetooth Headphones',
            'description': 'High-quality wireless headphones with noise cancellation',
            'brand': 'Sony',
            'category': 'Electronics',
            'final_price': 99.99,
            'rating': 4.5,
            'reviews_count': 1250
        },
        {
            'title': 'Smartphone Case',
            'description': 'Protective case for iPhone with wireless charging support',
            'brand': 'Apple',
            'category': 'Accessories',
            'final_price': 29.99,
            'rating': 4.2,
            'reviews_count': 890
        }
    ]
    
    # Generate embeddings
    embeddings = server.embed_products_batch(sample_products, platform="test")
    
    # Find similar products
    if len(embeddings) >= 2:
        similar = server.find_similar_products(embeddings[0], embeddings[1:])
        print(f"Found {len(similar)} similar products")
    
    # Get stats
    stats = server.get_embedding_stats()
    print(f"Embedding stats: {stats}")

if __name__ == "__main__":
    main()
