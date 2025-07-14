#!/usr/bin/env python3
"""
Script to calculate SHA256 hashes for Homebrew formulas
"""

import hashlib
import requests
import sys
from pathlib import Path

def calculate_file_sha256(file_path):
    """Calculate SHA256 hash of a local file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def calculate_url_sha256(url):
    """Calculate SHA256 hash of a file from URL"""
    print(f"Downloading {url} to calculate SHA256...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    sha256_hash = hashlib.sha256()
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            sha256_hash.update(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                progress = (downloaded / total_size) * 100
                print(f"\rProgress: {progress:.1f}%", end="", flush=True)
    
    print()  # New line after progress
    return sha256_hash.hexdigest()

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python calculate_sha256.py <file_path_or_url>")
        print("Examples:")
        print("  python calculate_sha256.py dist/easy-edge-macos")
        print("  python calculate_sha256.py https://github.com/criminact/easy-edge/archive/v1.0.0.tar.gz")
        sys.exit(1)
    
    target = sys.argv[1]
    
    try:
        if target.startswith(('http://', 'https://')):
            # URL
            sha256 = calculate_url_sha256(target)
            print(f"SHA256 for {target}: {sha256}")
        else:
            # Local file
            file_path = Path(target)
            if not file_path.exists():
                print(f"Error: File {target} does not exist")
                sys.exit(1)
            
            sha256 = calculate_file_sha256(file_path)
            print(f"SHA256 for {target}: {sha256}")
        
        print("\nCopy this SHA256 to your Homebrew formula!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 