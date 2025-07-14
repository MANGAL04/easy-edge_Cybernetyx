# Homebrew Tap for Easy Edge

This repository contains the Homebrew formula for [Easy Edge](https://github.com/yourusername/easy-edge), a simple Ollama-like tool for running LLMs locally.

## Installation

```bash
# Add the tap
brew tap yourusername/easy-edge

# Install Easy Edge
brew install easy-edge
```

## Usage

After installation, you can use Easy Edge like this:

```bash
# Download a model
easy-edge pull --url https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-qat-q4_0.gguf

# List installed models
easy-edge list

# Run a model
easy-edge run gemma-3-1b-it-qat-q4_0-gguf --interactive
```

## Updating

```bash
brew update
brew upgrade easy-edge
```

## Uninstalling

```bash
brew uninstall easy-edge
```

## Development

To install from source:

```bash
brew install --build-from-source yourusername/easy-edge/easy-edge
```

## License

MIT License - see the main Easy Edge repository for details. 