#!/usr/bin/env python3
"""
Main Project Test Runner

This script runs all tests for the main Walmart Insights project.
Run this from the project root directory.

Author: Derek
Date: 2025-01-15
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_embedding_tests():
    """Run embedding system tests."""
    print("🧪 Running Embedding System Tests...")
    try:
        from embedding.tests.test_embedding_server import main as run_embedding_tests
        return run_embedding_tests()
    except Exception as e:
        print(f"❌ Error running embedding tests: {e}")
        return 1

def main():
    """Run all main project tests."""
    print("🚀 Walmart Insights Test Suite")
    print("=" * 50)
    
    # Run embedding system tests
    embedding_result = run_embedding_tests()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   Embedding System: {'✅ PASSED' if embedding_result == 0 else '❌ FAILED'}")
    
    if embedding_result == 0:
        print("\n🎉 All main project tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit(main())
