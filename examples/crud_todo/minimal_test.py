"""
Minimal test - Just to verify the framework works
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from streamlit_html_components import render_component, configure

configure(
    templates_dir='templates',
    styles_dir='styles',
    scripts_dir='scripts'
)

st.title("🧪 Minimal Test")

# Test with inline HTML first
st.subheader("Test 1: Direct HTML (should work)")

from streamlit_html_components.core import _get_template_engine
engine = _get_template_engine('templates')

# Render directly
html = """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 30px; border-radius: 10px; text-align: center;">
    <h1>✅ If you see this styled, the framework works!</h1>
    <p>Beautiful gradient background</p>
</div>
"""

import streamlit.components.v1 as components
components.html(html, height=150)

st.markdown("---")

# Test with component
st.subheader("Test 2: With Component Files")

st.write("Checking files...")
st.write(f"✅ index.html exists: {Path('templates/index.html').exists()}")
st.write(f"✅ styles.css exists: {Path('styles/styles.css').exists()}")
st.write(f"✅ main.js exists: {Path('scripts/main.js').exists()}")

st.write("Rendering component...")

try:
    result = render_component(
        'index',
        props={'app_title': 'Test', 'subtitle': 'Testing'},
        styles=['styles'],
        scripts=['main'],
        height=600
    )
    st.success("✅ Component rendered!")
except Exception as e:
    st.error(f"❌ Error: {e}")
    import traceback
    st.code(traceback.format_exc())
