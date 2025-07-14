# CI/CD Setup Guide for Easy Edge

This guide explains how to set up and use the automated CI/CD pipeline for Easy Edge.

## Overview

The CI/CD pipeline consists of two main workflows:

1. **CI/CD Pipeline** (`.github/workflows/ci-cd.yml`) - Runs on every push and PR
2. **Release Workflow** (`.github/workflows/release.yml`) - Creates releases when tags are pushed

## Workflow Details

### CI/CD Pipeline

**Triggers:**
- Push to `main` or `master` branch
- Pull requests to `main` or `master` branch
- Manual release creation

**Jobs:**
1. **Test** - Runs tests on Python version (3.9)
2. **Build Linux** - Creates Linux executable
3. **Build macOS** - Creates macOS executable  
4. **Build Windows** - Creates Windows executable
5. **Create Release** - Organizes release assets (only on releases)
6. **Homebrew Update** - Updates Homebrew formula (only on releases)

### Release Workflow

**Triggers:**
- Push of tags matching `v*` pattern (e.g., `v1.0.0`)

**Jobs:**
1. **Build and Release** - Builds executables on all platforms and creates GitHub release
2. **Create Release** - Attaches built executables to the GitHub release

## Setup Instructions

### 1. Enable GitHub Actions

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Click "Enable Actions" if not already enabled

### 2. Set up Repository Secrets (Optional)

For enhanced functionality, you can set up these secrets in your repository:

1. Go to Settings → Secrets and variables → Actions
2. Add the following secrets if needed:

```
CODECOV_TOKEN - For code coverage reporting
HOMEBREW_TAP_TOKEN - For automatic Homebrew formula updates
```

### 3. Configure Branch Protection (Recommended)

1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require status checks to pass before merging
   - Require branches to be up to date before merging
   - Select the "test" job as required status check

## Usage

### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

### Creating a Release

1. **Update version** in `package.json` and any other version files
2. **Create and push a tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. **Monitor the workflow** in the Actions tab
4. **Download release assets** from the created GitHub release

### Manual Workflow Trigger

You can manually trigger workflows:

1. Go to Actions tab
2. Select the workflow you want to run
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Artifacts

### Build Artifacts

The pipeline creates these artifacts:
- `easy-edge-linux-x64` - Linux executable
- `easy-edge-macos-x64` - macOS executable
- `easy-edge-windows-x64.exe` - Windows executable

### Release Assets

When a release is created, these files are attached:
- Platform-specific executables
- SHA256 checksums for verification
- Release notes (auto-generated)

## Troubleshooting

### Common Issues

1. **Build fails on macOS:**
   - Check if PyInstaller is compatible with your Python version
   - Ensure all dependencies are properly specified in `requirements.txt`

2. **Tests fail:**
   - Run tests locally first: `pytest`
   - Check if all required files exist (models directory, config files)

3. **Release creation fails:**
   - Ensure you have write permissions to the repository
   - Check that the tag format is correct (`v*`)

### Debugging

1. **View workflow logs:**
   - Go to Actions tab
   - Click on the failed workflow run
   - Click on the failed job
   - Expand the failed step to see detailed logs

2. **Re-run failed jobs:**
   - In the workflow run page, click "Re-run jobs"
   - Select specific jobs to re-run

## Customization

### Adding New Platforms

To add support for new platforms:

1. Add the platform to the matrix in the workflow files
2. Update the build script to handle the new platform
3. Add appropriate artifact paths

### Modifying Build Process

1. Edit `build.py` for build logic changes
2. Update workflow files for CI/CD process changes
3. Test changes locally before pushing

### Adding New Tests

1. Create test files in the `tests/` directory
2. Follow the naming convention: `test_*.py`
3. Use pytest for test framework
4. Add any new dependencies to `requirements.txt`

## Security Considerations

1. **Dependencies:** Regularly update dependencies in `requirements.txt`
2. **Secrets:** Never commit secrets to the repository
3. **Permissions:** Use minimal required permissions for workflows
4. **Code signing:** Consider adding code signing for production releases

## Performance Optimization

1. **Caching:** The pipeline uses pip caching to speed up builds
2. **Parallel builds:** Builds run in parallel across platforms
3. **Artifact retention:** Configure artifact retention policies in repository settings

## Support

For issues with the CI/CD pipeline:

1. Check the troubleshooting section above
2. Review GitHub Actions documentation
3. Check the workflow logs for specific error messages
4. Create an issue in the repository with detailed error information 