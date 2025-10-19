# 🧪 BrightData Manager Test Suite

## Overview

This directory contains tests for the BrightData Manager project. Tests are organized to ensure all components work correctly together.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── README.md                     # This documentation
├── run_tests.py                  # Main test runner
├── test_brightdata_filter.py     # Core API functionality tests
└── test_streamlit_app.py         # Streamlit application tests
```

## Running Tests

### From Project Root:
```bash
# Run all tests
python tests/run_tests.py

# Run specific test files
python tests/test_brightdata_filter.py
python tests/test_streamlit_app.py
```

### Individual Test Files:
```bash
# Run core functionality tests
python -m tests.test_brightdata_filter

# Run Streamlit app tests
python -m tests.test_streamlit_app
```

## Test Categories

### 🔧 **Core Functionality Tests**
- **File**: `test_brightdata_filter.py`
- **Purpose**: Tests BrightDataFilter API interface and core functionality
- **Scope**: API initialization, filter creation, dataset configuration

### 🖥️ **Streamlit Application Tests**
- **File**: `test_streamlit_app.py`
- **Purpose**: Tests multi-page Streamlit application structure
- **Scope**: App imports, configuration files, requirements

## Test Dependencies

Tests require the following to be installed:
- Core dependencies (`requirements.txt`)
- UI dependencies (`requirements_ui.txt`)

## Test Environment

Tests are designed to run in the main project environment and test:
- Core API functionality
- Streamlit application structure
- Configuration management
- File structure validation

## Adding New Tests

When adding new tests to the project:

1. **Create test file** in this directory
2. **Follow naming convention**: `test_*.py`
3. **Update run_tests.py** to include new test
4. **Update this README** with test description

## Test Best Practices

- **Isolation**: Tests should not depend on external services
- **Mocking**: Use mocks for external API calls
- **Cleanup**: Clean up test data after each test
- **Documentation**: Document what each test validates

## Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure you're running from project root
2. **Missing Dependencies**: Install all requirements
3. **API Errors**: Check if external services are available

### Debug Mode:
```bash
# Run with verbose output
python tests/run_tests.py
```
