#!/usr/bin/env python3
"""
Test script to verify Instagram Follower Analyzer setup
"""
import os
import sys
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    required_modules = {
        'click': '8.1.7+',
        'requests': '2.31.0+',
        'tabulate': '0.9.0+',
        'instagrapi': '2.0.0+',
        'python-dotenv': '1.0.0+',
    }
    
    for module, version in required_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {module} installed")
        except ImportError:
            print(f"  ✗ {module} NOT installed (required: {version})")
            print(f"    Run: pip install {module}")
            return False
    
    return True


def test_file_structure():
    """Test if all required files exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'cli.py',
        'config.py',
        'instagram_api.py',
        'follower_analyzer.py',
        'utils.py',
        '__init__.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md',
    ]
    
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} NOT FOUND")
            return False
    
    return True


def test_cache_directory():
    """Test if cache directory exists"""
    print("\n🔍 Testing cache directory...")
    
    cache_dir = Path('cache')
    if not cache_dir.exists():
        try:
            cache_dir.mkdir()
            print(f"  ✓ Created cache directory")
        except Exception as e:
            print(f"  ✗ Could not create cache directory: {e}")
            return False
    else:
        print(f"  ✓ Cache directory exists")
    
    return True


def test_env_file():
    """Test if .env file exists"""
    print("\n🔍 Testing .env file...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print(f"  ✓ .env file exists")
        
        # Check if credentials are set
        with open(env_file, 'r') as f:
            content = f.read()
            if 'INSTAGRAM_USERNAME' in content and 'INSTAGRAM_PASSWORD' in content:
                print(f"  ℹ️  Make sure to set Instagram credentials in .env")
            else:
                print(f"  ✗ Instagram credentials not found in .env")
    else:
        if env_example.exists():
            print(f"  ⚠️  .env not found, but .env.example exists")
            print(f"    Run: cp .env.example .env")
        else:
            print(f"  ✗ Neither .env nor .env.example found")
        return False
    
    return True


def test_python_version():
    """Test Python version"""
    print("\n🔍 Testing Python version...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (required 3.8+)")
        return False


def test_imports_modules():
    """Test if our modules can be imported"""
    print("\n🔍 Testing local modules...")
    
    try:
        import config
        print(f"  ✓ config module loads")
    except Exception as e:
        print(f"  ✗ config module error: {e}")
        return False
    
    try:
        import follower_analyzer
        print(f"  ✓ follower_analyzer module loads")
    except Exception as e:
        print(f"  ✗ follower_analyzer module error: {e}")
        return False
    
    try:
        import utils
        print(f"  ✓ utils module loads")
    except Exception as e:
        print(f"  ✗ utils module error: {e}")
        return False
    
    try:
        import cli
        print(f"  ✓ cli module loads")
    except Exception as e:
        print(f"  ✗ cli module error: {e}")
        return False
    
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Instagram Follower Analyzer - Setup Test")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("File Structure", test_file_structure),
        ("Cache Directory", test_cache_directory),
        ("Environment File", test_env_file),
        ("Required Modules", test_imports),
        ("Local Modules", test_imports_modules),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n✓ All tests passed! You're ready to use the analyzer.")
        print("\nNext steps:")
        print("1. Edit .env with your Instagram credentials")
        print("2. Run: python cli.py login")
        print("3. Run: python cli.py fetch")
        print("4. Run: python cli.py stats")
        return True
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please fix the issues above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
