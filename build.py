#!/usr/bin/env python3
"""
Build script for Easy Edge - creates standalone executables
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build the executable using PyInstaller"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    print(f"Building for {system} {arch}...")
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable
        "--name=easy-edge",  # Executable name
        "--add-data=models:models",  # Include models directory
        "--hidden-import=llama_cpp",  # Include llama-cpp-python
        "--hidden-import=huggingface_hub",
        "--hidden-import=rich",
        "--hidden-import=click",
        "--hidden-import=requests",
        "--hidden-import=tqdm",
        "--collect-all=llama_cpp",  # Collect all llama_cpp files
        "--collect-all=huggingface_hub",
        "easy_edge.py"
    ]
    
    # Platform-specific options
    if system == "darwin":  # macOS
        cmd.extend([
            "--target-arch=universal2",  # Universal binary for Intel + Apple Silicon
            "--codesign-identity=-",  # Skip code signing for now
        ])
    elif system == "windows":
        cmd.extend([
            "--console",  # Show console window
            "--icon=icon.ico" if Path("icon.ico").exists() else "",
        ])
    elif system == "linux":
        cmd.extend([
            "--strip",  # Strip debug symbols
        ])
    
    # Remove empty strings
    cmd = [arg for arg in cmd if arg]
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    print(f"✅ Build completed! Executable created in dist/easy-edge")

def create_installer():
    """Create installer packages"""
    system = platform.system().lower()
    
    if system == "darwin":
        create_macos_installer()
    elif system == "windows":
        create_windows_installer()
    elif system == "linux":
        create_linux_package()

def create_macos_installer():
    """Create macOS .app bundle and .dmg"""
    print("Creating macOS installer...")
    
    # Create .app bundle
    app_cmd = [
        "pyinstaller",
        "--windowed",  # No console window
        "--name=Easy Edge",
        "--add-data=models:models",
        "--hidden-import=llama_cpp",
        "--hidden-import=huggingface_hub",
        "--collect-all=llama_cpp",
        "--collect-all=huggingface_hub",
        "easy_edge.py"
    ]
    
    subprocess.check_call(app_cmd)
    
    print("✅ macOS .app bundle created in dist/Easy Edge.app")

def create_windows_installer():
    """Create Windows installer using NSIS or similar"""
    print("Creating Windows installer...")
    
    # For now, just create the executable
    # You can add NSIS or Inno Setup later
    print("✅ Windows executable created in dist/easy-edge.exe")

def create_linux_package():
    """Create Linux package (deb, rpm, etc.)"""
    print("Creating Linux package...")
    
    # For now, just create the executable
    # You can add deb/rpm packaging later
    print("✅ Linux executable created in dist/easy-edge")

def main():
    """Main build function"""
    print("Building Easy Edge...")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    build_executable()
    
    # Create platform-specific installers
    create_installer()
    
    print("\n🎉 Build completed successfully!")
    print("\nNext steps:")
    print("1. Test the executable: ./dist/easy-edge --help")
    print("2. Distribute the executable to users")
    print("3. Consider code signing for production releases")

if __name__ == "__main__":
    main() 