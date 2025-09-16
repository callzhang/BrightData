#!/usr/bin/env python3
"""
Batch Embedding Script for CSV Files

This script processes downloaded CSV files and generates embeddings for all products.
It can handle various CSV formats and automatically detects the appropriate columns.

Author: Derek
Date: 2025-01-15
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from embedding.embedding_server import EmbeddingServer, ProductEmbedding
    # Note: vector_db.py was deleted, using basic embedding server for now
    VectorDatabase = None
except ImportError:
    # Fallback for direct execution
    from embedding_server import EmbeddingServer, ProductEmbedding
    VectorDatabase = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CSVEmbeddingProcessor:
    """
    Process CSV files and generate embeddings for products.
    
    Features:
    - Automatic column detection
    - Flexible CSV format support
    - Batch processing with progress tracking
    - Vector database storage
    - Export results to various formats
    """
    
    def __init__(self, output_dir: str = "./embedding_results"):
        """
        Initialize the CSV embedding processor.
        
        Args:
            output_dir: Directory to save results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize embedding server
        self.embedding_server = EmbeddingServer()
        
        # Initialize vector database (if available)
        if VectorDatabase:
            self.vector_db = VectorDatabase(
                persist_directory=str(self.output_dir / "vector_db")
            )
        else:
            self.vector_db = None
            logger.warning("Vector database not available. Embeddings will be saved to files only.")
        
        logger.info(f"CSV Embedding Processor initialized")
        logger.info(f"Output directory: {self.output_dir}")
    
    def detect_csv_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Automatically detect relevant columns in the CSV.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dict mapping standard field names to CSV column names
        """
        column_mapping = {}
        
        # Get all column names (case insensitive)
        columns_lower = {col.lower(): col for col in df.columns}
        
        # Common column name patterns
        patterns = {
            'title': ['title', 'name', 'product_name', 'product_title', 'item_name'],
            'brand': ['brand', 'manufacturer', 'company', 'maker'],
            'category': ['category', 'cat', 'type', 'product_type', 'classification'],
            'price': ['price', 'cost', 'amount', 'value', 'list_price'],
            'rating': ['rating', 'score', 'stars', 'review_score', 'avg_rating'],
            'description': ['description', 'desc', 'details', 'summary', 'overview'],
            'platform': ['platform', 'source', 'marketplace', 'store']
        }
        
        for field, patterns_list in patterns.items():
            for pattern in patterns_list:
                if pattern in columns_lower:
                    column_mapping[field] = columns_lower[pattern]
                    break
        
        # If no platform column found, try to infer from filename or add default
        if 'platform' not in column_mapping:
            column_mapping['platform'] = 'unknown'
        
        logger.info(f"Detected column mapping: {column_mapping}")
        return column_mapping
    
    def clean_product_data(self, row: pd.Series, column_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Clean and standardize product data from CSV row.
        
        Args:
            row: Pandas Series representing a CSV row
            column_mapping: Mapping of standard fields to CSV columns
            
        Returns:
            Cleaned product data dictionary
        """
        product_data = {}
        
        # Extract data using column mapping
        for field, csv_column in column_mapping.items():
            if csv_column in row.index and pd.notna(row[csv_column]):
                value = row[csv_column]
                
                # Clean and convert data types
                if field == 'price':
                    # Handle price formatting
                    if isinstance(value, str):
                        # Remove currency symbols and convert to float
                        value = ''.join(c for c in value if c.isdigit() or c == '.')
                    try:
                        product_data[field] = float(value)
                    except (ValueError, TypeError):
                        product_data[field] = None
                elif field == 'rating':
                    # Handle rating formatting
                    try:
                        product_data[field] = float(value)
                    except (ValueError, TypeError):
                        product_data[field] = None
                else:
                    # String fields
                    product_data[field] = str(value).strip()
            else:
                product_data[field] = None
        
        # Ensure required fields have default values
        if not product_data.get('title'):
            product_data['title'] = 'Unknown Product'
        if not product_data.get('brand'):
            product_data['brand'] = 'Unknown'
        if not product_data.get('category'):
            product_data['category'] = 'Unknown'
        
        return product_data
    
    def process_csv_file(self, csv_path: str, platform: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a CSV file and generate embeddings for all products.
        
        Args:
            csv_path: Path to the CSV file
            platform: Platform name (if not detected from CSV)
            
        Returns:
            Processing results dictionary
        """
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        logger.info(f"Processing CSV file: {csv_path}")
        
        # Read CSV file
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")
        
        logger.info(f"Loaded {len(df)} rows from CSV")
        
        # Detect columns
        column_mapping = self.detect_csv_columns(df)
        
        # Set platform if not detected
        if platform:
            column_mapping['platform'] = platform
        elif column_mapping.get('platform') == 'unknown':
            # Try to infer from filename
            filename = csv_path.stem.lower()
            if 'amazon' in filename:
                column_mapping['platform'] = 'amazon'
            elif 'walmart' in filename:
                column_mapping['platform'] = 'walmart'
            elif 'shopee' in filename:
                column_mapping['platform'] = 'shopee'
            else:
                column_mapping['platform'] = 'unknown'
        
        # Process products in batches
        batch_size = 100
        total_products = len(df)
        processed_products = []
        failed_products = []
        
        logger.info(f"Processing {total_products} products in batches of {batch_size}")
        
        for i in range(0, total_products, batch_size):
            batch_df = df.iloc[i:i + batch_size]
            batch_products = []
            
            # Clean product data for this batch
            for _, row in batch_df.iterrows():
                try:
                    product_data = self.clean_product_data(row, column_mapping)
                    batch_products.append(product_data)
                except Exception as e:
                    logger.warning(f"Error cleaning product data: {e}")
                    failed_products.append({'row': i, 'error': str(e)})
            
            if batch_products:
                try:
                    # Generate embeddings for batch
                    platform_name = column_mapping['platform']
                    embeddings = self.embedding_server.embed_products_batch(
                        batch_products, platform_name
                    )
                    
                    # Store in vector database (if available)
                    if self.vector_db:
                        embedding_ids = self.vector_db.add_embeddings_batch(embeddings)
                    else:
                        embedding_ids = [f"embedding_{i}_{j}" for j in range(len(embeddings))]
                    
                    # Add to processed products
                    for embedding, embedding_id in zip(embeddings, embedding_ids):
                        processed_products.append({
                            'id': embedding_id,
                            'title': embedding.title,
                            'brand': embedding.brand,
                            'category': embedding.category,
                            'platform': embedding.platform,
                            'price': embedding.metadata.get('price'),
                            'rating': embedding.metadata.get('rating'),
                            'description': embedding.description
                        })
                    
                    logger.info(f"Processed batch {i//batch_size + 1}: {len(embeddings)} products")
                    
                except Exception as e:
                    logger.error(f"Error processing batch {i//batch_size + 1}: {e}")
                    failed_products.extend([
                        {'row': i + j, 'error': str(e)} 
                        for j in range(len(batch_products))
                    ])
        
        # Generate results summary
        results = {
            'csv_file': str(csv_path),
            'total_rows': total_products,
            'processed_products': len(processed_products),
            'failed_products': len(failed_products),
            'platform': column_mapping['platform'],
            'column_mapping': column_mapping,
            'processing_timestamp': datetime.now().isoformat(),
            'processed_products_list': processed_products,
            'failed_products_list': failed_products
        }
        
        # Save results
        self.save_results(results, csv_path.stem)
        
        logger.info(f"Processing complete: {len(processed_products)}/{total_products} products processed")
        return results
    
    def save_results(self, results: Dict[str, Any], filename_prefix: str):
        """
        Save processing results to various formats.
        
        Args:
            results: Results dictionary
            filename_prefix: Prefix for output files
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_path = self.output_dir / f"{filename_prefix}_embedding_results_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Results saved to: {json_path}")
        
        # Save processed products as CSV
        if results['processed_products_list']:
            df_processed = pd.DataFrame(results['processed_products_list'])
            csv_path = self.output_dir / f"{filename_prefix}_processed_products_{timestamp}.csv"
            df_processed.to_csv(csv_path, index=False)
            logger.info(f"Processed products saved to: {csv_path}")
        
        # Save failed products if any
        if results['failed_products_list']:
            df_failed = pd.DataFrame(results['failed_products_list'])
            failed_path = self.output_dir / f"{filename_prefix}_failed_products_{timestamp}.csv"
            df_failed.to_csv(failed_path, index=False)
            logger.info(f"Failed products saved to: {failed_path}")
        
        # Save processing summary
        summary = {
            'total_rows': results['total_rows'],
            'processed_products': results['processed_products'],
            'failed_products': results['failed_products'],
            'success_rate': results['processed_products'] / results['total_rows'] * 100,
            'platform': results['platform'],
            'processing_timestamp': results['processing_timestamp']
        }
        
        summary_path = self.output_dir / f"{filename_prefix}_summary_{timestamp}.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Summary saved to: {summary_path}")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector database."""
        if self.vector_db:
            return self.vector_db.get_database_stats()
        else:
            return {
                "total_products": 0,
                "database_size_mb": 0,
                "platform_counts": {},
                "category_counts": {},
                "note": "Vector database not available"
            }


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Batch embedding processing for CSV files')
    parser.add_argument('csv_file', help='Path to the CSV file to process')
    parser.add_argument('--platform', help='Platform name (amazon, walmart, shopee, etc.)')
    parser.add_argument('--output-dir', default='./embedding_results', 
                       help='Output directory for results (default: ./embedding_results)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize processor
        processor = CSVEmbeddingProcessor(output_dir=args.output_dir)
        
        # Process CSV file
        results = processor.process_csv_file(args.csv_file, args.platform)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 BATCH EMBEDDING PROCESSING SUMMARY")
        print("="*60)
        print(f"📁 CSV File: {results['csv_file']}")
        print(f"🏪 Platform: {results['platform']}")
        print(f"📦 Total Rows: {results['total_rows']}")
        print(f"✅ Processed: {results['processed_products']}")
        print(f"❌ Failed: {results['failed_products']}")
        print(f"📈 Success Rate: {results['processed_products']/results['total_rows']*100:.1f}%")
        print(f"💾 Output Directory: {args.output_dir}")
        
        # Database stats
        db_stats = processor.get_database_stats()
        print(f"\n🗄️ Vector Database Stats:")
        print(f"   Total Products: {db_stats['total_products']}")
        print(f"   Database Size: {db_stats['database_size_mb']} MB")
        print(f"   Platforms: {list(db_stats['platform_counts'].keys())}")
        
        print("\n🎉 Batch embedding processing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
