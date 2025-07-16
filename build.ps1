Write-Host "Installing dependencies..."
pip install -r requirements.txt
pip install pyinstaller

Write-Host "Building easy-edge executable..."
pyinstaller --onefile --name easy-edge --add-data "models;models" easy_edge.py

Write-Host "Build complete. Executable is in dist\easy-edge.exe" 