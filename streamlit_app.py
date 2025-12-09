"""
Streamlit HTML Components - Official Showcase

Entry point for Streamlit Cloud deployment.
This file redirects to the showcase app.
"""

import sys
from pathlib import Path

# Add src to path for package imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Import and run the showcase app
import streamlit as st

# Set path for showcase
showcase_path = Path(__file__).parent / 'showcase'
sys.path.insert(0, str(showcase_path))

# Run showcase app
exec(open(showcase_path / 'app.py').read())
