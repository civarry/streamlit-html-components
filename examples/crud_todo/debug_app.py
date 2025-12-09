"""
Debug version of CRUD Todo App - Tests if CSS/JS are loading
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from streamlit_html_components import render_component, configure

# Configure the package
configure(
    templates_dir='templates',
    styles_dir='styles',
    scripts_dir='scripts',
    default_cache=False
)

st.title("🐛 Debug - CRUD Todo App")

st.info("""
This debug version will help verify that CSS and JavaScript are loading correctly.
Check your browser's console (F12) for any errors.
""")

# Display file paths for verification
st.write("**File paths:**")
st.code(f"""
Templates: {Path('templates').absolute()}
Styles: {Path('styles').absolute()}
Scripts: {Path('scripts').absolute()}
""")

# Check if files exist
from pathlib import Path

files_check = {
    "index.html": Path("templates/index.html").exists(),
    "styles.css": Path("styles/styles.css").exists(),
    "main.js": Path("scripts/main.js").exists()
}

st.write("**Files exist:**")
for file, exists in files_check.items():
    if exists:
        st.success(f"✅ {file}")
    else:
        st.error(f"❌ {file} - NOT FOUND!")

st.markdown("---")

st.write("**Rendering component...**")

# Render the component with explicit file names
result = render_component(
    'index',
    props={
        'app_title': 'Debug Todo List',
        'subtitle': 'Testing CSS and JS loading'
    },
    styles=['styles'],  # Load styles.css
    scripts=['main'],   # Load main.js
    height=800,
    key='debug_todo'
)

st.markdown("---")

st.write("**Browser Console Instructions:**")
st.info("""
1. Press F12 to open browser developer tools
2. Go to Console tab
3. Look for:
   - "Todo CRUD App initialized!" (means JS loaded)
   - "Todo CRUD App ready!" (means JS executed)
   - Any error messages

4. Go to Elements/Inspector tab
5. Look for <style> tags with CSS
6. Look for <script> tags with JavaScript
""")

# Show what should be rendered
with st.expander("🔍 Expected HTML structure"):
    st.code("""
<!DOCTYPE html>
<html>
<head>
    <style>
        /* styles.css content should be here */
    </style>
</head>
<body>
    <div class="container">
        <header class="app-header">
            <!-- Should have gradient background -->
        </header>
        ...
    </div>
    <script>
        /* main.js content should be here */
    </script>
</body>
</html>
    """, language='html')
