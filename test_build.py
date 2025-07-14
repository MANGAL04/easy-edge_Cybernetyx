#!/usr/bin/env python3
"""
Test script to verify Easy Edge functionality
"""

import subprocess
import sys
import os

def test_help():
    """Test that the help command works"""
    print("Testing help command...")
    try:
        result = subprocess.run([sys.executable, "easy_edge.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Help command works")
            return True
        else:
            print(f"❌ Help command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Help command error: {e}")
        return False

def test_list():
    """Test that the list command works"""
    print("Testing list command...")
    try:
        result = subprocess.run([sys.executable, "easy_edge.py", "list"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ List command works")
            return True
        else:
            print(f"❌ List command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ List command error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Easy Edge...")
    
    tests = [
        test_help,
        test_list,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for build.")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before building.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 