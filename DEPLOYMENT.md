# Deployment Guide

## Deploy Showcase to Streamlit Cloud

### Step 1: Prepare Repository

1. **Create `.streamlit/config.toml` for the showcase:**

```bash
mkdir -p /Users/cjcarito/Documents/streamlit-html-components/.streamlit
```

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

2. **Create `requirements.txt` for deployment:**

```bash
cd /Users/cjcarito/Documents/streamlit-html-components
cat > requirements_deploy.txt << 'EOF'
streamlit>=1.29.0
jinja2>=3.1.0
EOF
```

3. **Create a root-level showcase app:**

Create `streamlit_app.py` in the root directory (Streamlit Cloud looks for this):
```python
"""
Redirect to showcase app
"""
import sys
from pathlib import Path

# Run the showcase app
sys.path.insert(0, str(Path(__file__).parent / 'src'))
exec(open('showcase/app.py').read())
```

### Step 2: Push to GitHub

1. **Initialize git repository (if not already):**

```bash
cd /Users/cjcarito/Documents/streamlit-html-components
git init
git add .
git commit -m "Add showcase landing page and examples"
```

2. **Create GitHub repository:**

Go to https://github.com/new and create a repository named `streamlit-html-components`

3. **Push to GitHub:**

```bash
git remote add origin https://github.com/YOUR_USERNAME/streamlit-html-components.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit https://share.streamlit.io/
   - Sign in with GitHub

2. **Create new app:**
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/streamlit-html-components`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - Advanced settings:
     - Python version: 3.11
     - Requirements file: `requirements_deploy.txt`

3. **Deploy:**
   - Click "Deploy!"
   - Wait for deployment (usually 2-5 minutes)

4. **Your app will be live at:**
   ```
   https://YOUR_USERNAME-streamlit-html-components-streamlit-app-xxxxx.streamlit.app
   ```

### Step 4: Custom Domain (Optional)

In Streamlit Cloud settings, you can add a custom domain:
- Settings → Custom subdomain
- Example: `streamlit-html-components.streamlit.app`

---

## Publish to PyPI

### Prerequisites

```bash
pip install build twine
```

### Step 1: Update Package Metadata

Edit `pyproject.toml` and ensure all fields are correct:
- Version number
- Description
- Author info
- URLs
- Classifiers

### Step 2: Build the Package

```bash
cd /Users/cjcarito/Documents/streamlit-html-components

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distribution files
python -m build
```

This creates:
- `dist/streamlit_html_components-0.1.0.tar.gz` (source distribution)
- `dist/streamlit_html_components-0.1.0-py3-none-any.whl` (wheel distribution)

### Step 3: Test on TestPyPI (Recommended)

1. **Create account on TestPyPI:**
   - Go to https://test.pypi.org/account/register/

2. **Upload to TestPyPI:**

```bash
python -m twine upload --repository testpypi dist/*
```

Enter your TestPyPI credentials when prompted.

3. **Test installation:**

```bash
pip install --index-url https://test.pypi.org/simple/ streamlit-html-components
```

4. **Verify it works:**

```bash
python -c "from streamlit_html_components import render_component; print('Success!')"
```

### Step 4: Publish to PyPI

1. **Create account on PyPI:**
   - Go to https://pypi.org/account/register/

2. **Create API token (recommended):**
   - Go to https://pypi.org/manage/account/token/
   - Create token with scope: "Entire account"
   - Save the token (starts with `pypi-`)

3. **Create `~/.pypirc` file:**

```bash
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
EOF

chmod 600 ~/.pypirc
```

4. **Upload to PyPI:**

```bash
python -m twine upload dist/*
```

5. **Verify on PyPI:**

Visit https://pypi.org/project/streamlit-html-components/

### Step 5: Test Installation from PyPI

```bash
# Create new virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install streamlit-html-components

# Test it
python -c "from streamlit_html_components import render_component; print('✅ Package works!')"
```

### Step 6: Update README with PyPI Badge

Add to your README.md:

```markdown
[![PyPI version](https://badge.fury.io/py/streamlit-html-components.svg)](https://badge.fury.io/py/streamlit-html-components)
[![Downloads](https://pepy.tech/badge/streamlit-html-components)](https://pepy.tech/project/streamlit-html-components)
```

---

## Publishing Updates

### Version Bumping

1. **Update version in `pyproject.toml`:**

```toml
[project]
version = "0.1.1"  # Increment version
```

2. **Update `__init__.py`:**

```python
__version__ = "0.1.1"
```

3. **Create git tag:**

```bash
git add .
git commit -m "Bump version to 0.1.1"
git tag v0.1.1
git push origin main --tags
```

4. **Rebuild and upload:**

```bash
rm -rf dist/
python -m build
python -m twine upload dist/*
```

### Semantic Versioning

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backwards compatible
- **PATCH** (0.0.1): Bug fixes

---

## Maintenance Checklist

### Before Each Release:

- [ ] Update version number
- [ ] Update CHANGELOG.md
- [ ] Run tests: `pytest`
- [ ] Update documentation
- [ ] Test examples still work
- [ ] Build package: `python -m build`
- [ ] Test on TestPyPI
- [ ] Upload to PyPI
- [ ] Create GitHub release
- [ ] Update Streamlit Cloud deployment

### Post-Release:

- [ ] Announce on social media
- [ ] Post on Streamlit forum
- [ ] Update showcase with new features
- [ ] Monitor PyPI downloads
- [ ] Respond to GitHub issues

---

## Troubleshooting

### Build Errors

**Error: "No module named 'setuptools'"**
```bash
pip install --upgrade setuptools wheel
```

**Error: "Invalid distribution file"**
```bash
rm -rf build/ dist/ *.egg-info
python -m build
```

### Upload Errors

**Error: "403 Forbidden"**
- Check your PyPI credentials
- Ensure package name is not taken
- Verify API token is correct

**Error: "File already exists"**
- Version already uploaded
- Increment version number
- Cannot re-upload same version

### Installation Errors

**Error: "Could not find a version"**
- Package not yet indexed (wait 5-10 minutes)
- Check package name spelling
- Verify on https://pypi.org/

---

## Resources

- **Streamlit Cloud Docs:** https://docs.streamlit.io/streamlit-community-cloud
- **PyPI Publishing Guide:** https://packaging.python.org/tutorials/packaging-projects/
- **Twine Docs:** https://twine.readthedocs.io/
- **Python Packaging:** https://packaging.python.org/

---

## Support

- **GitHub Issues:** https://github.com/cjcarito/streamlit-html-components/issues
- **Discussions:** https://github.com/cjcarito/streamlit-html-components/discussions
- **Email:** cjcarito@example.com
