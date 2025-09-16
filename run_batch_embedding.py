#!/usr/bin/env python3
"""
Simple Batch Embedding Runner

This script provides an easy way to run batch embedding on CSV files
with common configurations.

Author: Derek
Date: 2025-01-15
"""

import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from batch_embedding import CSVEmbeddingProcessor

def run_sample_embedding():
    """Run batch embedding on the sample CSV file."""
    print("🚀 Running Batch Embedding on Sample Data")
    print("=" * 50)
    
    # Initialize processor
    processor = CSVEmbeddingProcessor(output_dir="./embedding_results")
    
    # Process sample CSV
    csv_file = "sample_products.csv"
    if not Path(csv_file).exists():
        print(f"❌ Sample CSV file not found: {csv_file}")
        print("Please make sure sample_products.csv exists in the current directory")
        return 1
    
    try:
        results = processor.process_csv_file(csv_file, platform="sample")
        
        # Print results
        print(f"\n📊 Processing Results:")
        print(f"   📁 File: {results['csv_file']}")
        print(f"   🏪 Platform: {results['platform']}")
        print(f"   📦 Total Products: {results['total_rows']}")
        print(f"   ✅ Processed: {results['processed_products']}")
        print(f"   ❌ Failed: {results['failed_products']}")
        print(f"   📈 Success Rate: {results['processed_products']/results['total_rows']*100:.1f}%")
        
        # Show some processed products
        print(f"\n📋 Sample Processed Products:")
        for i, product in enumerate(results['processed_products_list'][:3]):
            print(f"   {i+1}. {product['title']} ({product['brand']}) - ${product['price']}")
        
        # Database stats
        db_stats = processor.get_database_stats()
        print(f"\n🗄️ Vector Database:")
        print(f"   Total Products: {db_stats['total_products']}")
        print(f"   Database Size: {db_stats['database_size_mb']} MB")
        
        print("\n🎉 Batch embedding completed successfully!")
        print("📁 Check the 'embedding_results' folder for detailed results")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

def main():
    """Main function."""
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        platform = sys.argv[2] if len(sys.argv) > 2 else None
        
        print(f"🚀 Processing CSV file: {csv_file}")
        if platform:
            print(f"🏪 Platform: {platform}")
        
        processor = CSVEmbeddingProcessor()
        try:
            results = processor.process_csv_file(csv_file, platform)
            print(f"✅ Processed {results['processed_products']}/{results['total_rows']} products")
            return 0
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    else:
        # Run sample embedding
        return run_sample_embedding()

if __name__ == "__main__":
    exit(main())
