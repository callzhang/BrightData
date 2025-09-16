# 🚀 Batch Embedding Script for CSV Files

## Overview

The batch embedding script processes downloaded CSV files containing product data and generates embeddings for competitive intelligence analysis. It automatically detects CSV columns, processes products in batches, and stores embeddings in a vector database.

## Features

- **🔄 Automatic Column Detection**: Intelligently maps CSV columns to standard product fields
- **📦 Batch Processing**: Processes large datasets efficiently in configurable batches
- **🗄️ Vector Database Storage**: Stores embeddings in Chroma vector database for fast similarity search
- **📊 Progress Tracking**: Real-time progress updates and comprehensive logging
- **💾 Multiple Output Formats**: Saves results in JSON, CSV, and summary formats
- **🛡️ Error Handling**: Graceful handling of malformed data and processing errors
- **🔍 Flexible Platform Support**: Works with Amazon, Walmart, Shopee, and other platforms

## Quick Start

### 1. **Run Sample Data:**
```bash
python run_batch_embedding.py
```

### 2. **Process Your CSV File:**
```bash
python batch_embedding.py your_products.csv --platform amazon
```

### 3. **Command Line Options:**
```bash
python batch_embedding.py [CSV_FILE] [OPTIONS]

Options:
  --platform PLATFORM    Platform name (amazon, walmart, shopee, etc.)
  --output-dir DIR        Output directory (default: ./embedding_results)
  --verbose, -v           Enable verbose logging
  --help, -h              Show help message
```

## CSV Format Requirements

### **Supported Column Names:**

The script automatically detects these column patterns:

| Field | Supported Column Names |
|-------|----------------------|
| **Title** | `title`, `name`, `product_name`, `product_title`, `item_name` |
| **Brand** | `brand`, `manufacturer`, `company`, `maker` |
| **Category** | `category`, `cat`, `type`, `product_type`, `classification` |
| **Price** | `price`, `cost`, `amount`, `value`, `list_price` |
| **Rating** | `rating`, `score`, `stars`, `review_score`, `avg_rating` |
| **Description** | `description`, `desc`, `details`, `summary`, `overview` |
| **Platform** | `platform`, `source`, `marketplace`, `store` |

### **Sample CSV Format:**
```csv
title,brand,category,price,rating,description
iPhone 15 Pro 128GB,Apple,Electronics,999.0,4.5,Latest iPhone with titanium design
Samsung Galaxy S24 Ultra,Samsung,Electronics,899.0,4.3,Flagship Android phone
MacBook Pro 14-inch M3 Pro,Apple,Computers,1999.0,4.7,Professional laptop
```

## Output Files

The script generates several output files in the specified output directory:

### **1. Results JSON** (`{filename}_embedding_results_{timestamp}.json`)
Complete processing results including:
- Processing statistics
- Column mapping used
- All processed products with embedding IDs
- Failed products with error details

### **2. Processed Products CSV** (`{filename}_processed_products_{timestamp}.csv`)
Clean CSV with all successfully processed products:
- Product details
- Embedding IDs
- Platform information

### **3. Failed Products CSV** (`{filename}_failed_products_{timestamp}.csv`)
Products that failed processing:
- Row numbers
- Error messages
- Original data (if available)

### **4. Summary JSON** (`{filename}_summary_{timestamp}.json`)
High-level processing summary:
- Success rate
- Total products processed
- Platform information
- Processing timestamp

### **5. Vector Database** (`vector_db/`)
Chroma vector database containing:
- All product embeddings
- Metadata for filtering
- Indexes for fast similarity search

## Usage Examples

### **Example 1: Amazon Products**
```bash
python batch_embedding.py amazon_products.csv --platform amazon --output-dir ./amazon_embeddings
```

### **Example 2: Walmart Products**
```bash
python batch_embedding.py walmart_products.csv --platform walmart --verbose
```

### **Example 3: Shopee Products**
```bash
python batch_embedding.py shopee_products.csv --platform shopee --output-dir ./shopee_embeddings
```

### **Example 4: Mixed Platform Data**
```bash
python batch_embedding.py all_products.csv --output-dir ./mixed_embeddings
```

## Programmatic Usage

```python
from batch_embedding import CSVEmbeddingProcessor

# Initialize processor
processor = CSVEmbeddingProcessor(output_dir="./my_embeddings")

# Process CSV file
results = processor.process_csv_file("products.csv", platform="amazon")

# Get processing statistics
print(f"Processed: {results['processed_products']}/{results['total_rows']} products")

# Get database statistics
db_stats = processor.get_database_stats()
print(f"Total products in database: {db_stats['total_products']}")
```

## Performance

### **Processing Speed:**
- **Small files** (< 1K products): ~2-5 seconds
- **Medium files** (1K-10K products): ~30-120 seconds
- **Large files** (10K+ products): ~5-20 minutes

### **Memory Usage:**
- **Base memory**: ~200-300MB (model loading)
- **Per 1K products**: ~50-100MB additional
- **Recommended**: 4GB+ RAM for large datasets

### **Storage Requirements:**
- **Per 1K products**: ~2-5MB vector database storage
- **Model cache**: ~80MB (all-MiniLM-L6-v2)
- **Results files**: ~1-10MB depending on data size

## Error Handling

### **Common Issues and Solutions:**

1. **CSV Reading Errors:**
   - Ensure CSV is properly formatted
   - Check for encoding issues (UTF-8 recommended)
   - Verify file path is correct

2. **Column Detection Issues:**
   - Use standard column names (see supported names above)
   - Check for typos in column headers
   - Ensure required columns (title, brand, category) are present

3. **Memory Issues:**
   - Reduce batch size for large files
   - Process files in smaller chunks
   - Ensure sufficient RAM available

4. **Embedding Generation Errors:**
   - Check internet connection (for model download)
   - Verify sentence-transformers installation
   - Ensure product data is not empty

## Integration with Existing System

### **Using Generated Embeddings:**

```python
from embedding.vector_db import VectorDatabase

# Load the generated vector database
db = VectorDatabase(persist_directory="./embedding_results/vector_db")

# Find similar products
similar = db.find_similar_products(
    query_embedding=your_query_embedding,
    top_k=10,
    platform_filter="amazon"
)

# Get products by category
electronics = db.get_products_by_category("Electronics")
```

### **Competitive Analysis:**

```python
from embedding.product_analyzer import ProductAnalyzer

# Initialize analyzer with your data
analyzer = ProductAnalyzer(embedding_server)

# Analyze competitive landscape
results = analyzer.analyze_competitive_landscape(
    walmart_products, amazon_products, "amazon"
)
```

## Best Practices

### **1. Data Preparation:**
- Clean your CSV data before processing
- Ensure consistent column naming
- Remove duplicate products
- Validate price and rating formats

### **2. Processing:**
- Start with small test files
- Use verbose logging for debugging
- Monitor memory usage for large files
- Save results in organized directories

### **3. Analysis:**
- Use the vector database for similarity searches
- Combine with existing snapshot data
- Export results for further analysis
- Regular database maintenance

## Troubleshooting

### **Debug Mode:**
```bash
python batch_embedding.py your_file.csv --verbose
```

### **Check Dependencies:**
```bash
pip install -r requirements_embedding.txt
```

### **Verify Installation:**
```bash
python -c "from embedding.embedding_server import EmbeddingServer; print('✅ Embedding system ready')"
```

## Support

For issues or questions:
1. Check the error logs with `--verbose` flag
2. Verify CSV format matches requirements
3. Ensure all dependencies are installed
4. Check available disk space and memory

The batch embedding script is designed to handle real-world CSV data efficiently while providing comprehensive error handling and detailed output for analysis! 🚀
