#!/usr/bin/env python3
"""
Embedding Demo Launcher

This script launches the embedding demo from the main project directory.
It handles the import paths correctly for the embedding subfolder.

Author: Derek
Date: 2025-01-15
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Launch the embedding demo"""
    print("🚀 Launching Embedding Demo...")
    print("=" * 50)
    
    try:
        # Import and run the embedding examples
        from embedding.embedding_examples import main as run_examples
        run_examples()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the main project directory")
        return 1
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
