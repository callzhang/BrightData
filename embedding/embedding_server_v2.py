#!/usr/bin/env python3
"""
Enhanced Embedding Server with Vector Database Integration

This module provides an enhanced embedding server that integrates with Chroma vector database
for persistent storage and fast similarity search of product embeddings.

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
    from embedding.vector_db import VectorDatabase
except ImportError:
    # Fallback for direct execution
    from util.config import get_brightdata_api_key
    from util.brightdata import BrightDataFilter
    from vector_db import VectorDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProductEmbedding:
    """Data class for storing product embedding information"""
    platform: str
    title: str
    brand: str
    category: str
    price: Optional[float] = None
    rating: Optional[float] = None
    embedding: np.ndarray = None
    metadata: Dict[str, Any] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class SimilarityResult:
    """Data class for similarity search results"""
    product_a: ProductEmbedding
    product_b: ProductEmbedding
    similarity_score: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class EmbeddingServerV2:
    """
    Enhanced embedding server with vector database integration.
    
    Features:
    - all-MiniLM-L6-v2 model for 384-dimensional embeddings
    - Chroma vector database for persistent storage
    - Fast similarity search and retrieval
    - Batch processing capabilities
    - Metadata filtering and querying
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_dir: str = "./embedding_cache"):
        """
        Initialize the enhanced embedding server.
        
        Args:
            model_name: Name of the sentence transformer model
            cache_dir: Directory for model and vector database storage
        """
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize model
        self.model = None
        self._load_model()
        
        # Initialize vector database
        self.vector_db = VectorDatabase(
            persist_directory=str(self.cache_dir / "vector_db")
        )
        
        # Initialize BrightData filter (optional)
        self.brightdata_filter = None
        self._initialize_brightdata_filter()
        
        logger.info("Enhanced embedding server initialized successfully")
    
    def _load_model(self):
        """Load the sentence transformer model."""
        try:
            model_path = self.cache_dir / self.model_name
            
            if model_path.exists():
                logger.info(f"Loading cached model from {model_path}")
                self.model = SentenceTransformer(str(model_path))
            else:
                logger.info(f"Downloading and caching model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                self.model.save(str(model_path))
            
            logger.info(f"Model loaded successfully: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _initialize_brightdata_filter(self):
        """Initialize BrightData filter if available."""
        try:
            api_key = get_brightdata_api_key()
            if api_key:
                self.brightdata_filter = BrightDataFilter(api_key)
                logger.info("BrightData filter initialized successfully")
            else:
                logger.warning("Could not initialize BrightData filter: No API key found")
        except Exception as e:
            logger.warning(f"Could not initialize BrightData filter: {e}")
    
    def embed_product(self, product_data: Dict[str, Any], platform: str) -> ProductEmbedding:
        """
        Generate embedding for a single product.
        
        Args:
            product_data: Dictionary containing product information
            platform: Platform name (e.g., 'amazon', 'walmart')
            
        Returns:
            ProductEmbedding: Product embedding object
        """
        # Extract product information
        title = product_data.get('title', '')
        brand = product_data.get('brand', '')
        category = product_data.get('category', '')
        price = product_data.get('price')
        rating = product_data.get('rating')
        
        # Create text for embedding
        text_parts = [title]
        if brand:
            text_parts.append(brand)
        if category:
            text_parts.append(category)
        
        text = " ".join(text_parts)
        
        # Generate embedding
        embedding = self.model.encode([text])[0]
        
        # Create ProductEmbedding object
        product_embedding = ProductEmbedding(
            platform=platform,
            title=title,
            brand=brand,
            category=category,
            price=price,
            rating=rating,
            embedding=embedding,
            metadata=product_data
        )
        
        return product_embedding
    
    def embed_products_batch(self, products_data: List[Dict[str, Any]], platform: str) -> List[ProductEmbedding]:
        """
        Generate embeddings for multiple products in batch.
        
        Args:
            products_data: List of product dictionaries
            platform: Platform name
            
        Returns:
            List[ProductEmbedding]: List of product embeddings
        """
        if not products_data:
            return []
        
        logger.info(f"Processing {len(products_data)} products from {platform}")
        
        # Prepare texts for batch processing
        texts = []
        product_info = []
        
        for product_data in products_data:
            title = product_data.get('title', '')
            brand = product_data.get('brand', '')
            category = product_data.get('category', '')
            
            text_parts = [title]
            if brand:
                text_parts.append(brand)
            if category:
                text_parts.append(category)
            
            text = " ".join(text_parts)
            texts.append(text)
            product_info.append(product_data)
        
        # Generate embeddings in batch
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Create ProductEmbedding objects
        product_embeddings = []
        for i, (product_data, embedding) in enumerate(zip(product_info, embeddings)):
            product_embedding = ProductEmbedding(
                platform=platform,
                title=product_data.get('title', ''),
                brand=product_data.get('brand', ''),
                category=product_data.get('category', ''),
                price=product_data.get('price'),
                rating=product_data.get('rating'),
                embedding=embedding,
                metadata=product_data
            )
            product_embeddings.append(product_embedding)
        
        logger.info(f"Generated {len(product_embeddings)} embeddings for {platform}")
        return product_embeddings
    
    def store_embeddings(self, embeddings: List[ProductEmbedding]) -> List[str]:
        """
        Store embeddings in the vector database.
        
        Args:
            embeddings: List of ProductEmbedding objects to store
            
        Returns:
            List[str]: List of stored embedding IDs
        """
        return self.vector_db.add_embeddings_batch(embeddings)
    
    def find_similar_products(
        self, 
        query_embedding: ProductEmbedding, 
        candidates: List[ProductEmbedding] = None,
        top_k: int = 10,
        platform_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
        min_similarity: float = 0.0
    ) -> List[SimilarityResult]:
        """
        Find similar products using vector similarity search.
        
        Args:
            query_embedding: Query product embedding
            candidates: Optional list of candidate embeddings (if None, searches database)
            top_k: Number of similar products to return
            platform_filter: Filter by platform
            category_filter: Filter by category
            min_similarity: Minimum similarity threshold
            
        Returns:
            List[SimilarityResult]: List of similar products with similarity scores
        """
        if candidates is not None:
            # Calculate similarity with provided candidates
            return self._calculate_similarity_with_candidates(
                query_embedding, candidates, top_k, min_similarity
            )
        else:
            # Use vector database for similarity search
            return self.vector_db.find_similar_products(
                query_embedding.embedding,
                top_k=top_k,
                platform_filter=platform_filter,
                category_filter=category_filter,
                min_similarity=min_similarity
            )
    
    def _calculate_similarity_with_candidates(
        self, 
        query_embedding: ProductEmbedding, 
        candidates: List[ProductEmbedding],
        top_k: int,
        min_similarity: float
    ) -> List[SimilarityResult]:
        """Calculate similarity with provided candidate embeddings."""
        if not candidates:
            return []
        
        # Calculate cosine similarity
        query_vector = query_embedding.embedding.reshape(1, -1)
        candidate_vectors = np.array([c.embedding for c in candidates])
        
        similarities = cosine_similarity(query_vector, candidate_vectors)[0]
        
        # Create similarity results
        results = []
        for i, (candidate, similarity) in enumerate(zip(candidates, similarities)):
            if similarity >= min_similarity:
                result = SimilarityResult(
                    product_a=query_embedding,
                    product_b=candidate,
                    similarity_score=float(similarity)
                )
                results.append(result)
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]
    
    def analyze_category_gaps(
        self, 
        walmart_products: List[ProductEmbedding], 
        competitor_products: List[ProductEmbedding],
        competitor_name: str = "competitor"
    ) -> Dict[str, Any]:
        """
        Analyze category gaps between Walmart and competitors.
        
        Args:
            walmart_products: List of Walmart product embeddings
            competitor_products: List of competitor product embeddings
            competitor_name: Name of the competitor
            
        Returns:
            Dict: Analysis results with weak and opportunity categories
        """
        logger.info(f"Analyzing category gaps between Walmart and {competitor_name}")
        
        # Get unique categories
        walmart_categories = set(p.category for p in walmart_products if p.category)
        competitor_categories = set(p.category for p in competitor_products if p.category)
        
        # Find weak categories (Walmart has fewer products)
        weak_categories = []
        opportunity_categories = []
        
        for category in competitor_categories:
            walmart_count = sum(1 for p in walmart_products if p.category == category)
            competitor_count = sum(1 for p in competitor_products if p.category == category)
            
            if walmart_count < competitor_count * 0.5:  # Walmart has less than 50% of competitor's products
                weak_categories.append({
                    'category': category,
                    'walmart_count': walmart_count,
                    'competitor_count': competitor_count,
                    'gap_ratio': competitor_count / max(walmart_count, 1)
                })
        
        # Find opportunity categories (Walmart doesn't have but competitor does)
        for category in competitor_categories:
            if category not in walmart_categories:
                competitor_count = sum(1 for p in competitor_products if p.category == category)
                opportunity_categories.append({
                    'category': category,
                    'competitor_count': competitor_count,
                    'opportunity_score': competitor_count
                })
        
        # Sort by gap ratio and opportunity score
        weak_categories.sort(key=lambda x: x['gap_ratio'], reverse=True)
        opportunity_categories.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        logger.info(f"Found {len(weak_categories)} weak categories")
        logger.info(f"Found {len(opportunity_categories)} opportunity categories")
        
        return {
            'weak_categories': weak_categories,
            'opportunity_categories': opportunity_categories,
            'total_walmart_categories': len(walmart_categories),
            'total_competitor_categories': len(competitor_categories),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the embedding database."""
        return self.vector_db.get_database_stats()
    
    def get_products_by_platform(self, platform: str) -> List[Dict[str, Any]]:
        """Get all products from a specific platform."""
        return self.vector_db.get_products_by_platform(platform)
    
    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all products from a specific category."""
        return self.vector_db.get_products_by_category(category)
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """Export all products to a pandas DataFrame."""
        return self.vector_db.export_to_dataframe()
    
    def clear_database(self):
        """Clear all data from the vector database."""
        self.vector_db.clear_database()
        logger.info("Vector database cleared")


def main():
    """Test the enhanced embedding server."""
    print("🚀 Testing Enhanced Embedding Server with Vector Database...")
    
    try:
        # Initialize server
        server = EmbeddingServerV2()
        
        # Test data
        test_products = [
            {
                'title': 'iPhone 15 Pro 128GB',
                'brand': 'Apple',
                'category': 'Electronics',
                'price': 999.0,
                'rating': 4.5
            },
            {
                'title': 'Samsung Galaxy S24 Ultra',
                'brand': 'Samsung',
                'category': 'Electronics',
                'price': 899.0,
                'rating': 4.3
            }
        ]
        
        # Generate embeddings
        embeddings = server.embed_products_batch(test_products, 'test')
        print(f"✅ Generated {len(embeddings)} embeddings")
        
        # Store in vector database
        ids = server.store_embeddings(embeddings)
        print(f"✅ Stored {len(ids)} embeddings in vector database")
        
        # Test similarity search
        similar = server.find_similar_products(embeddings[0], top_k=5)
        print(f"✅ Found {len(similar)} similar products")
        
        # Get database stats
        stats = server.get_database_stats()
        print(f"✅ Database stats: {stats['total_products']} products")
        
        print("🎉 Enhanced embedding server test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing enhanced embedding server: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
