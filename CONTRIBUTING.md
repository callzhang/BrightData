# Contributing to BrightData Manager

Thank you for your interest in contributing to BrightData Manager! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/brightdata-manager.git
   cd brightdata-manager
   ```

2. **Install dependencies**
   ```bash
   # Install core dependencies
   pip install -r requirements.txt
   
   # Install UI dependencies (for Streamlit app)
   pip install -r requirements_ui.txt
   ```

3. **Configure your environment**
   ```bash
   # Copy the example secrets file
   cp secrets.example.yaml secrets.yaml
   
   # Edit secrets.yaml with your BrightData API key
   # You can get an API key from https://brightdata.com/
   ```

4. **Run tests**
   ```bash
   # Run the test suite
   python -m pytest tests/
   
   # Or run specific tests
   python tests/run_tests.py
   ```

## 🛠️ Development Guidelines

### Code Style

- **Follow PEP 8** - Use `black` for automatic formatting
- **Type hints** - Add type hints to all functions and methods
- **Docstrings** - Use Google-style docstrings for all public functions
- **Error handling** - Include comprehensive error handling and validation

### Project Structure

```
brightdata-manager/
├── app.py                     # Main Streamlit app entry point
├── pages/                     # Multi-page Streamlit application
│   ├── 1_Query_Builder.py    # Query creation interface
│   ├── 2_Snapshot_Viewer.py  # Snapshot viewing and analysis
│   └── 3_Settings.py         # Configuration management
├── util/                      # Core utilities
│   ├── brightdata.py         # Main BrightData API interface
│   ├── config.py             # Configuration management
│   ├── dataset_config.py     # Dataset configuration loader
│   └── filter_criteria.py   # Filter system
├── config/                    # Configuration files
│   └── datasets.yaml         # Dataset definitions
├── docs/                      # Documentation
├── tests/                     # Test suite
└── examples/                  # Usage examples
```

### Adding New Features

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code patterns
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   python -m pytest tests/
   
   # Test the Streamlit app
   streamlit run app.py
   ```

4. **Submit a pull request**
   - Provide a clear description of your changes
   - Include screenshots for UI changes
   - Reference any related issues

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=util

# Run specific test file
python -m pytest tests/test_brightdata.py
```

### Writing Tests

- **Test files** should be in the `tests/` directory
- **Test functions** should start with `test_`
- **Use descriptive names** for test functions
- **Test both success and failure cases**

Example test structure:
```python
def test_brightdata_filter_initialization():
    """Test BrightDataFilter initialization with valid dataset."""
    filter_obj = BrightDataFilter("amazon_products")
    assert filter_obj.dataset_id == "gd_l7q7dkf244hwjntr0"
    assert filter_obj.api_key is not None

def test_invalid_dataset_raises_error():
    """Test that invalid dataset names raise ValueError."""
    with pytest.raises(ValueError):
        BrightDataFilter("invalid_dataset")
```

## 📝 Documentation

### Code Documentation

- **Docstrings** - All public functions need docstrings
- **Type hints** - Use type hints for better IDE support
- **Comments** - Explain complex logic with inline comments

### User Documentation

- **README.md** - Keep the main README up to date
- **Examples** - Add examples to the `examples/` directory
- **API docs** - Update API documentation for new features

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Description** - Clear description of the issue
2. **Steps to reproduce** - Detailed steps to reproduce the bug
3. **Expected behavior** - What should happen
4. **Actual behavior** - What actually happens
5. **Environment** - Python version, OS, etc.
6. **Screenshots** - If applicable

### Feature Requests

For feature requests, please include:

1. **Use case** - Why is this feature needed?
2. **Proposed solution** - How should it work?
3. **Alternatives** - Other ways to solve the problem
4. **Additional context** - Any other relevant information

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes** - Make sure all tests pass
2. **Update documentation** - Update relevant documentation
3. **Check code style** - Run `black` and `flake8`
4. **Commit messages** - Use clear, descriptive commit messages

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] Manual testing completed
- [ ] UI changes tested

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## 📋 Code Review Process

1. **Automated checks** - CI/CD pipeline runs tests and linting
2. **Manual review** - Maintainers review the code
3. **Feedback** - Address any feedback or requested changes
4. **Merge** - Once approved, the PR will be merged

## 🤝 Community Guidelines

- **Be respectful** - Treat everyone with respect
- **Be constructive** - Provide constructive feedback
- **Be patient** - Maintainers are volunteers
- **Be helpful** - Help others when you can

## 📞 Getting Help

- **GitHub Issues** - For bug reports and feature requests
- **GitHub Discussions** - For questions and general discussion
- **Email** - For security issues or private matters

## 🎉 Recognition

Contributors will be recognized in:
- **README.md** - Listed as contributors
- **Release notes** - Mentioned in release notes
- **GitHub** - Shown in the contributors section

Thank you for contributing to BrightData Manager! 🚀
