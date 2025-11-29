# Publishing to PyPI Guide

This document explains how to publish the `llm-content-extractor` package to the Python Package Index (PyPI), making it installable via `pip install`.

## Prerequisites

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Register for a PyPI Account**:
   - Visit [https://pypi.org/account/register/](https://pypi.org/account/register/)
   - Complete the registration process
   - Enable two-factor authentication (2FA) for enhanced security

3. **Create an API Token**:
   - After logging into PyPI, visit [https://pypi.org/manage/account/](https://pypi.org/manage/account/)
   - Scroll to the "API tokens" section
   - Click "Add API token"
   - Give the token a name (e.g., "llm-content-extractor")
   - Copy the generated token (starts with `pypi-`)

## Configure Poetry Authentication

Configure Poetry with your API token:

```bash
poetry config pypi-token.pypi pypi-AgEIcHlwaS5vcmcC...
```

Replace the token above with your actual API token.

## Publishing Workflow

### 1. Update Version Number

Before publishing a new version, update the version number in `pyproject.toml`:

```bash
# Automatically update patch version (0.1.0 -> 0.1.1)
poetry version patch

# Or update minor version (0.1.0 -> 0.2.0)
poetry version minor

# Or update major version (0.1.0 -> 1.0.0)
poetry version major

# Or manually specify a version
poetry version 1.2.3
```

### 2. Update CHANGELOG

Record changes for this version in `CHANGELOG.md`:

```markdown
## [0.1.1] - 2025-01-29

### Added
- New feature XXX

### Fixed
- Fixed issue XXX

### Changed
- Improved XXX performance
```

### 3. Run Tests

Ensure all tests pass:

```bash
poetry install
poetry run pytest
```

### 4. Build the Distribution Package

```bash
poetry build
```

This will create two files in the `dist/` directory:
- `llm_content_extractor-0.1.0-py3-none-any.whl` (wheel format)
- `llm_content_extractor-0.1.0.tar.gz` (source distribution)

### 5. Publish to TestPyPI (Optional but Recommended)

Before publishing to the official PyPI, it's recommended to test on TestPyPI:

```bash
# Configure TestPyPI token
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-AgEIcHlwaS5vcmcC...

# Publish to TestPyPI
poetry publish -r testpypi
```

Test the installation:

```bash
pip install --index-url https://test.pypi.org/simple/ llm-content-extractor
```

### 6. Publish to PyPI

After confirming everything works, publish to the official PyPI:

```bash
poetry publish
```

### 7. Verify the Publication

Visit the package's PyPI page to verify successful publication:
```
https://pypi.org/project/llm-content-extractor/
```

Test the installation:

```bash
pip install llm-content-extractor
```

### 8. Create a Git Tag

Create a git tag for the new version:

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

## Automated Publishing (GitHub Actions)

You can create a GitHub Actions workflow to automate the publishing process:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -

      - name: Build and publish
        env:
          POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          poetry build
          poetry publish
```

Add the `PYPI_API_TOKEN` secret in your GitHub repository settings.

## Common Issues

### Issue: Publication failed with "File already exists" error

**Solution**: PyPI doesn't allow re-uploading the same version. You need to update the version number, rebuild, and publish again.

### Issue: Package name is already taken

**Solution**: Search PyPI to confirm if the package name is available. If it's already taken, you'll need to change the package name in `pyproject.toml`.

### Issue: Dependency version conflicts

**Solution**: Check that the dependency version ranges in `pyproject.toml` are reasonable and compatible with common Python environments.

## Version Management Best Practices

Follow [Semantic Versioning](https://semver.org/):

- **Major version (X.0.0)**: Incompatible API changes
- **Minor version (0.X.0)**: Backward-compatible feature additions
- **Patch version (0.0.X)**: Backward-compatible bug fixes

## Security Notes

1. **NEVER** commit API tokens to the code repository
2. Use environment variables or GitHub Secrets to store sensitive information
3. Rotate API tokens regularly
4. Use different tokens for different projects
5. Enable two-factor authentication on PyPI

## Revoking a Published Version

If you discover a critical issue, you can remove a version from PyPI:

1. Log into PyPI
2. Go to the project management page
3. Select the version to delete
4. Click "Delete" and confirm

**Note**: Once deleted, that version number cannot be reused.

## Reference Resources

- [Poetry Documentation - Publishing](https://python-poetry.org/docs/cli/#publish)
- [PyPI Official Documentation](https://pypi.org/help/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
