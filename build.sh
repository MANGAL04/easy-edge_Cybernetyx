#!/usr/bin/env bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt
pip install pyinstaller

echo "Building easy-edge executable..."
pyinstaller --onefile --name easy-edge --add-data "models:models" easy_edge.py

echo "Build complete. Executable is in dist/easy-edge" 