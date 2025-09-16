# 🧪 Main Project Test Suite

## Overview

This directory contains tests for the main Walmart Insights project. Tests are organized to ensure all components work correctly together.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── README.md               # This documentation
├── run_tests.py            # Main test runner
└── test_embedding.py       # Embedding system integration tests
```

## Running Tests

### From Project Root:
```bash
# Run all main project tests
python tests/run_tests.py

# Run specific embedding integration test
python tests/test_embedding.py
```

### Individual Test Files:
```bash
# Run embedding integration test
python -m tests.test_embedding
```

## Test Categories

### 🔍 **Embedding System Integration Tests**
- **File**: `test_embedding.py`
- **Purpose**: Tests embedding system integration with main project
- **Scope**: End-to-end functionality from main project perspective

## Test Dependencies

Tests require the following to be installed:
- All main project dependencies (`requirements.txt`)
- Embedding system dependencies (`embedding/requirements_embedding.txt`)

## Test Environment

Tests are designed to run in the main project environment and test integration between:
- Main project components
- Embedding system (as a submodule)
- External APIs (BrightData, etc.)

## Adding New Tests

When adding new tests to the main project:

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
python tests/run_tests.py --verbose
```
