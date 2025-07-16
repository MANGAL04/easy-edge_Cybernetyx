# Easy Edge

[![CI/CD](https://github.com/criminact/easy-edge/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/criminact/easy-edge/actions/workflows/ci-cd.yml)
[![Release](https://github.com/criminact/easy-edge/workflows/Release/badge.svg)](https://github.com/criminact/easy-edge/actions/workflows/release.yml)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A simple Ollama-like tool for running Large Language Models (LLMs) locally using llama.cpp under the hood.

## Features

- 🚀 **Local LLM Inference**: Run models locally using llama.cpp
- 📥 **Automatic Downloads**: Download models from URLs or Hugging Face
- 💬 **Interactive Chat**: Chat with models in an interactive terminal
- 📋 **Model Management**: List, download, and remove models
- ⚙️ **Configurable**: Customize model parameters and settings

## Installation

### Option 1: Download Pre-built Executable (Recommended)

Download the latest release for your platform from the [Releases page](https://github.com/criminact/easy-edge/releases).

### Option 2: Install from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/criminact/easy-edge.git
   cd easy-edge
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make the tool executable:**
   ```bash
   chmod +x easy_edge.py
   ```

### Option 3: Using Package Managers

**macOS (Homebrew):**
```bash
# Add the tap
brew tap criminact/easy-edge

# Install Easy Edge
brew install easy-edge
```

**Docker:**
```bash
docker run -it --rm -v $(pwd)/models:/app/models easy-edge:latest
```

## Quick Start

### 1. Download a Model

Download a model from Hugging Face (model name is automatically extracted):
```bash
python easy_edge.py pull --repo-id TheBloke/Llama-2-7B-Chat-GGUF --filename llama-2-7b-chat.Q4_K_M.gguf
```

Or download from a Hugging Face URL:
```bash
python easy_edge.py pull --url https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-q4_0.gguf
```

### 2. Run the Model

**Single prompt:**
```bash
python easy_edge.py run gemma-3-1b-it-qat-q4_0-gguf --prompt "Hello, how are you?"
```

**Interactive chat:**
```bash
python easy_edge.py run gemma-3-1b-it-qat-q4_0-gguf --interactive
```

### 3. List Installed Models
```bash
python easy_edge.py list
```

### 4. Remove a Model
```bash
python easy_edge.py remove gemma-3-1b-it-qat-q4_0-gguf
```

## Available Models

Here are some popular models you can download:

### Llama 2 Models
```bash
# Llama 2 7B Chat (4-bit quantized)
python easy_edge.py pull llama2-7b-chat --repo-id TheBloke/Llama-2-7B-Chat-GGUF --filename llama-2-7b-chat.Q4_K_M.gguf

# Llama 2 13B Chat (4-bit quantized)
python easy_edge.py pull llama2-13b-chat --repo-id TheBloke/Llama-2-13B-Chat-GGUF --filename llama-2-13b-chat.Q4_K_M.gguf
```

### Mistral Models
```bash
# Mistral 7B Instruct (4-bit quantized)
python easy_edge.py pull mistral-7b-instruct --repo-id TheBloke/Mistral-7B-Instruct-v0.2-GGUF --filename mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

### Code Models
```bash
# Code Llama 7B Instruct (4-bit quantized)
python easy_edge.py pull codellama-7b-instruct --repo-id TheBloke/CodeLlama-7B-Instruct-GGUF --filename codellama-7b-instruct.Q4_K_M.gguf
```

## Configuration

The tool stores configuration in `models/config.json`. You can modify settings like:

- `max_tokens`: Maximum tokens to generate (default: 2048)
- `temperature`: Sampling temperature (default: 0.7)
- `top_p`: Top-p sampling parameter (default: 0.9)

## Requirements

- Python 3.11+
- 8GB+ RAM (for 7B models)
- 16GB+ RAM (for 13B models)
- 4GB+ free disk space per model

## Troubleshooting

### Common Issues

1. **"llama-cpp-python not installed"**
   ```bash
   pip install llama-cpp-python
   ```

2. **Out of memory errors**
   - Try smaller models (7B instead of 13B)
   - Use more quantized models (Q4_K_M instead of Q8_0)
   - Close other applications to free up RAM

3. **Slow inference**
   - The tool uses all CPU cores by default
   - For better performance, consider using GPU acceleration (requires CUDA)

### GPU Acceleration (Optional)

For faster inference with NVIDIA GPUs:

```bash
pip uninstall llama-cpp-python
pip install llama-cpp-python --force-reinstall --index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Building from Source

### Prerequisites
- Python 3.11+
- PyInstaller (for creating executables)

### Build Steps

1. **Install build dependencies:**
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script:**
   ```bash
   python build.py
   ```

3. **Find your executable:**
   - Windows: `dist/easy-edge.exe`
   - macOS: `dist/easy-edge` (universal binary)
   - Linux: `dist/easy-edge`

### Docker Build

```bash
docker build -t easy-edge .
docker run -it --rm -v $(pwd)/models:/app/models easy-edge:latest
```

## CI/CD Pipeline

This project uses comprehensive GitHub Actions for automated testing, building, and releasing:

### Workflows

- **`ci-cd.yml`**: Runs tests and builds on every push/PR
- **`release.yml`**: Creates releases with executables for all platforms
- **Homebrew Integration**: Ready for automatic Homebrew tap updates

### Automated Release Process

1. **Create a release tag:**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

2. **GitHub Actions automatically:**
   - ✅ Runs tests on multiple Python versions (3.8-3.12)
   - 🔨 Builds executables (Windows, macOS, Linux)
   - 📦 Creates GitHub release with downloads
   - 🔍 Generates SHA256 checksums for verification
   - 🍺 Ready for Homebrew tap updates

### Manual Release

You can also trigger a manual release from the GitHub Actions tab with a custom version.

## Distribution

### Automated Distribution

The CI/CD pipeline automatically distributes:

- **GitHub Releases**: Pre-built executables for all platforms
- **Docker Hub**: Container images for easy deployment
- **Homebrew**: macOS package manager integration
- **Direct Downloads**: Standalone executables

### Manual Distribution

For manual distribution, you can:

1. **Create executables:**
   ```bash
   python build.py
   ```

2. **Package for different platforms:**
   - **Windows**: Use NSIS or Inno Setup for installers
   - **macOS**: Create .dmg files with create-dmg
   - **Linux**: Create .deb or .rpm packages

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - The underlying inference engine
- [Ollama](https://ollama.ai/) - Inspiration for the tool design
- [Hugging Face](https://huggingface.co/) - Model hosting and distribution 