# Technical Specifications

## System Overview

The BrightData Database System is a comprehensive Python library for accessing and filtering data using the BrightData API across multiple datasets. The system provides type-safe database queries with built-in support for various e-commerce datasets for competitive intelligence and market research.

## Core Components

### 1. BrightDataFilter (`util/brightdata_filter.py`)

**Purpose**: Main interface for interacting with the BrightData API

**Key Features**:
- Multi-dataset support with automatic dataset ID resolution
- Type-aware filtering with runtime validation
- Smart deduplication to prevent duplicate queries
- Local record storage for all submissions
- Real-time status monitoring
- Cost-aware download management

**Key Methods**:
- `search_data(filter_obj, records_limit, description, title)`: Submit filter queries
- `get_snapshot_metadata(snapshot_id)`: Retrieve snapshot information
- `download_snapshot_content(snapshot_id, format, compress)`: Download snapshot data
- `deliver_snapshot(snapshot_id, delivery_config)`: Trigger snapshot delivery

**Technical Details**:
- Automatic API key loading from `secrets.yaml`
- Order-independent filter comparison for deduplication
- Support for JSON and CSV download formats
- Compression support for large datasets
- Comprehensive error handling and validation

### 2. Filter Criteria System (`util/filter_criteria.py`)

**Purpose**: Type-aware filtering with automatic validation

**Key Classes**:
- `FilterField`: Base class for all filter fields
- `NumericalFilterField`: Handles numeric operations (>, <, >=, <=, =, !=)
- `StringFilterField`: Handles string operations (contains, includes, in, not_in)
- `BooleanFilterField`: Handles boolean operations (is_true, is_false)
- `ArrayFilterField`: Handles array operations (includes, not_includes, array_includes)
- `DatasetFilterFields`: Dynamic field generation based on dataset schema

**Technical Details**:
- Runtime field validation against dataset schemas
- Operator overloading for intuitive syntax (`field >= 4.5`)
- Support for complex logical operations (`&` for AND, `|` for OR)
- Automatic type coercion and validation
- Backward compatibility with legacy field names

### 3. Dataset Registry (`util/dataset_registry.py`)

**Purpose**: Centralized management of dataset schemas and metadata

**Key Features**:
- Dataset schema definitions with field types and operators
- Automatic dataset ID resolution from names
- Field validation and operator compatibility checking
- Support for multiple datasets (Amazon, Amazon-Walmart, Shopee)

**Technical Details**:
- JSON-based schema definitions
- Dynamic field generation based on schemas
- Comprehensive field metadata (type, operators, description)
- Extensible architecture for adding new datasets

### 4. Configuration Management (`util/config.py`)

**Purpose**: Secure configuration and secret management

**Key Features**:
- YAML-based configuration loading
- Secure API key management
- Environment variable support
- Validation of required secrets

**Technical Details**:
- Automatic `secrets.yaml` loading
- Fallback to environment variables
- Comprehensive validation and error reporting
- Support for multiple configuration sources



**Key Methods**:
- `fetch_platform_products(platform, category, limit, min_rating)`: Fetch products from platform
- `analyze_competitive_landscape(walmart_products, competitor_products, competitor_platform)`: Comprehensive analysis
- `generate_market_opportunity_report(analysis_results, output_file)`: Generate reports
- `save_analysis_results(results, filename)`: Save analysis results

## Data Flow Architecture

### 1. Query Submission Flow

```
User Input → Filter Validation → Deduplication Check → API Submission → Local Record Storage
```

1. **Filter Validation**: Runtime validation against dataset schema
2. **Deduplication Check**: Compare with existing snapshots to prevent duplicates
3. **API Submission**: Submit to BrightData API with proper authentication
4. **Local Record Storage**: Save submission details to JSON file

### 2. Status Monitoring Flow

```
Local Records → API Status Check → Record Update → UI Refresh
```

1. **Local Records**: Read from `snapshot_records/*.json`
2. **API Status Check**: Query BrightData API for current status
3. **Record Update**: Update local records with latest information
4. **UI Refresh**: Display updated status in user interface

### 3. Download Flow

```
Snapshot Ready → Download Request → Content Retrieval → Local Storage → UI Update
```

1. **Snapshot Ready**: Check if snapshot is ready for download
2. **Download Request**: Request content from BrightData API
3. **Content Retrieval**: Download data in specified format
4. **Local Storage**: Save to `data/downloads/` directory
5. **UI Update**: Update interface with download status

## File Structure

```
├── util/                          # Core utility modules
│   ├── __init__.py               # Package initialization and exports
│   ├── brightdata_filter.py      # Main API interface
│   ├── filter_criteria.py        # Type-aware filtering system
│   ├── dataset_registry.py       # Dataset schema management
│   └── config.py                 # Configuration management
├── docs/                         # Documentation
│   ├── architecture.mermaid      # System architecture diagram
│   └── technical.md              # This file
├── tasks/                        # Task management
│   └── tasks.md                  # Current development tasks
├── datasets/                     # Dataset schemas
│   ├── amazon_products_dataset.md
│   ├── amazon_walmart_dataset.md
│   └── shopee_dataset.md
├── snapshot_records/             # Local snapshot records
│   └── *.json                   # Individual snapshot records
├── data/downloads/               # Downloaded snapshot data
│   └── *.json                   # Downloaded snapshot files
├── snapshot_viewer.py            # Streamlit UI
├── snapshot_manager.py           # CLI management tool
└── secrets.yaml                  # Configuration and secrets
```

## API Integration

### BrightData API Endpoints

1. **Filter Dataset**: `POST /datasets/filter`
   - Submit filter queries
   - Returns snapshot ID for tracking

2. **Get Snapshot Metadata**: `GET /datasets/snapshots/{snapshot_id}`
   - Retrieve snapshot status and metadata
   - Used for status monitoring

3. **Download Snapshot Content**: `GET /datasets/snapshots/{snapshot_id}/content`
   - Download snapshot data
   - Supports multiple formats (JSON, CSV)
   - Supports compression

4. **Deliver Snapshot**: `POST /datasets/snapshots/{snapshot_id}/deliver`
   - Trigger snapshot delivery
   - Used when download URL is not available

### Authentication

- Bearer token authentication using API key from `secrets.yaml`
- Automatic token loading and header management
- Comprehensive error handling for authentication failures

## Error Handling

### API Error Handling

- HTTP status code validation
- Detailed error message extraction
- Graceful fallback for network issues
- Retry logic for transient failures

### Validation Error Handling

- Field existence validation
- Operator compatibility checking
- Type coercion with error reporting
- Comprehensive error messages with suggestions

### File System Error Handling

- Safe file operations with proper error handling
- Directory creation with error checking
- JSON serialization/deserialization error handling
- Backup and recovery mechanisms

## Performance Considerations

### Deduplication

- Order-independent filter comparison
- Efficient JSON comparison algorithms
- Caching of comparison results
- Minimal API calls for duplicate detection

### Memory Management

- Lazy loading of large datasets
- Streaming for large file operations
- Efficient data structures for filter operations
- Garbage collection optimization

### Network Optimization

- Connection pooling for API requests
- Request batching where possible
- Timeout management for long-running operations
- Retry logic with exponential backoff

## Security

### API Key Management

- Secure storage in `secrets.yaml`
- Environment variable fallback
- No hardcoded credentials
- Access control and validation

### Data Protection

- Local data encryption where applicable
- Secure file permissions
- Input validation and sanitization
- Protection against injection attacks

## Extensibility

### Adding New Datasets

1. Create dataset schema in `dataset_registry.py`
2. Add field definitions with types and operators
3. Update dataset documentation
4. Test with sample queries

### Adding New Filter Types

1. Extend `FilterField` base class
2. Implement required operators
3. Add validation logic
4. Update documentation and tests

### Adding New UI Components

1. Extend Streamlit interface
2. Add new functionality to `snapshot_viewer.py`
3. Update UI documentation
4. Test user interactions

## Testing Strategy

### Unit Testing

- Individual component testing
- Mock API responses
- Edge case validation
- Error condition testing

### Integration Testing

- End-to-end workflow testing
- API integration testing
- File system operations testing
- User interface testing

### Performance Testing

- Load testing with large datasets
- Memory usage profiling
- Network performance testing
- Concurrent operation testing

