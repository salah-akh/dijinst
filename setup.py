#!/usr/bin/env python3
"""
Setup script for Instagram Follower Analyzer
"""
import os
import shutil
import sys
from pathlib import Path


def setup():
    """Initialize the project"""
    
    print("=" * 60)
    print("Instagram Follower Analyzer - Setup")
    print("=" * 60)
    
    # Create cache directory
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    print(f"✓ Cache directory created: {cache_dir}")
    
    # Check if .env exists
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print(f"✓ Created .env file from template")
            print("  ⚠️  Please edit .env and add your Instagram credentials")
        else:
            print("✗ .env.example not found")
            sys.exit(1)
    else:
        print("✓ .env file already exists")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"✗ Python 3.8+ required, but you have {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check if pip can be used
    try:
        import pip
        print("✓ pip is available")
    except ImportError:
        print("✗ pip is not available")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit .env file with your Instagram credentials:")
    print("   INSTAGRAM_USERNAME=your_username")
    print("   INSTAGRAM_PASSWORD=your_password")
    print("\n2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n3. Test your setup:")
    print("   python cli.py login")
    print("\n4. Fetch your followers:")
    print("   python cli.py fetch")
    print("\n5. View analysis:")
    print("   python cli.py stats")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        print(f"\n✗ Setup failed: {str(e)}")
        sys.exit(1)
