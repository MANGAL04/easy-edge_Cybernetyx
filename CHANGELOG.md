# Changelog

All notable changes to Easy Edge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial development

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Easy Edge
- Support for downloading models from Hugging Face
- Interactive chat mode
- Model management (list, remove)
- Cross-platform support (Windows, macOS, Linux)
- Homebrew distribution
- Docker support
- GitHub Actions for automated builds and releases

### Features
- Automatic model name extraction from URLs
- Progress bars for downloads
- Rich terminal interface
- Configurable model parameters
- Support for GGUF model format

### Technical
- Built with llama.cpp for efficient inference
- Python-based CLI with Click
- Rich for beautiful terminal output
- Hugging Face Hub integration
- PyInstaller for standalone executables

---

## Release Process

This project uses automated releases via GitHub Actions:

1. **Create a tag**: `git tag v1.0.1`
2. **Push the tag**: `git push origin v1.0.1`
3. **GitHub Actions automatically**:
   - Builds executables for all platforms
   - Creates a GitHub release
   - Updates Homebrew tap
   - Publishes Docker images

## Version History

- **v1.0.0**: Initial release with core functionality 