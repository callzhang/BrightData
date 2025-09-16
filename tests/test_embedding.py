#!/usr/bin/env python3
"""
Embedding Test Launcher

This script runs the embedding tests from the main project directory.

Author: Derek
Date: 2025-01-15
"""

import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Run the embedding tests"""
    print("🧪 Running Embedding Tests...")
    print("=" * 50)
    
    try:
        # Import and run the embedding tests
        from embedding.tests.test_embedding_server import main as run_tests
        return run_tests()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the main project directory")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
