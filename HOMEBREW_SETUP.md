# Homebrew Distribution Setup Guide

This guide will help you set up Homebrew distribution for Easy Edge.

## Prerequisites

1. A GitHub account
2. Two GitHub repositories:
   - Main repository: `yourusername/easy-edge`
   - Homebrew tap repository: `yourusername/homebrew-tap`

## Step 1: Create the Homebrew Tap Repository

1. **Create a new GitHub repository** named `homebrew-tap`
2. **Clone it locally:**
   ```bash
   git clone https://github.com/yourusername/homebrew-tap.git
   cd homebrew-tap
   ```

3. **Copy the Homebrew files:**
   ```bash
   # Copy the formula and cask files
   cp ../easy-edge/homebrew-tap/Formula/easy-edge.rb Formula/
   cp ../easy-edge/homebrew-tap/Casks/easy-edge.rb Casks/
   cp ../easy-edge/homebrew-tap/README.md .
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Initial Easy Edge formula and cask"
   git push origin main
   ```

## Step 2: Set Up GitHub Secrets

In your main `easy-edge` repository, go to **Settings > Secrets and variables > Actions** and add:

1. **`HOMEBREW_TAP_TOKEN`**: A GitHub Personal Access Token with `repo` permissions
2. **`HOMEBREW_CORE_TOKEN`** (optional): A token for submitting to Homebrew core

## Step 3: Update Repository URLs

Replace `yourusername` with your actual GitHub username in these files:

- `homebrew-tap/Formula/easy-edge.rb`
- `homebrew-tap/Casks/easy-edge.rb`
- `homebrew-tap/README.md`
- `.github/workflows/update-homebrew.yml`

## Step 4: Calculate SHA256 Hashes

When you create a release, you'll need to calculate SHA256 hashes:

```bash
# For source tarball
python scripts/calculate_sha256.py https://github.com/yourusername/easy-edge/archive/v1.0.0.tar.gz

# For macOS binary
python scripts/calculate_sha256.py dist/easy-edge-macos
```

## Step 5: Test the Formula Locally

```bash
# Test the formula
brew install --build-from-source ./Formula/easy-edge.rb

# Test the cask
brew install --cask ./Casks/easy-edge.rb
```

## Step 6: Create Your First Release

1. **Tag a release:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Create a GitHub release** with the tag `v1.0.0`

3. **Upload the macOS binary** to the release

4. **The GitHub Action will automatically:**
   - Build executables for all platforms
   - Calculate SHA256 hashes
   - Update the Homebrew tap

## Step 7: Test Installation

Users can now install Easy Edge with:

```bash
# Add your tap
brew tap yourusername/easy-edge

# Install Easy Edge
brew install easy-edge

# Or install the binary version
brew install --cask easy-edge
```

## Step 8: Submit to Homebrew Core (Optional)

For wider distribution, you can submit to Homebrew core:

1. **Fork Homebrew/homebrew-core**
2. **Add your formula** to the fork
3. **Submit a pull request**

## Troubleshooting

### Common Issues

1. **SHA256 mismatch:**
   - Recalculate the hash using the script
   - Update the formula/cask file

2. **Formula not found:**
   - Make sure the tap is added: `brew tap yourusername/easy-edge`
   - Check that the repository exists and is public

3. **Installation fails:**
   - Check that all dependencies are available
   - Test locally first: `brew install --build-from-source ./Formula/easy-edge.rb`

### Testing Commands

```bash
# Test formula syntax
brew audit --strict Formula/easy-edge.rb

# Test cask syntax
brew audit --cask Casks/easy-edge.rb

# Install from local formula
brew install --build-from-source ./Formula/easy-edge.rb

# Uninstall
brew uninstall easy-edge
```

## Maintenance

### Updating Versions

1. **Create a new release** with a new tag
2. **The GitHub Action will automatically update** the Homebrew tap
3. **Users can update** with `brew upgrade easy-edge`

### Monitoring

- Check the GitHub Actions tab for build status
- Monitor the Homebrew tap repository for updates
- Respond to issues in both repositories

## Resources

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Homebrew Cask Cookbook](https://docs.brew.sh/Cask-Cookbook)
- [Homebrew Core Contributing Guide](https://github.com/Homebrew/homebrew-core/blob/HEAD/CONTRIBUTING.md) 