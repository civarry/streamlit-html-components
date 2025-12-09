"""
Basic Button Example - streamlit-html-components

This example demonstrates:
- Basic component rendering
- Template variables (props)
- CSS styling
- JavaScript interactivity
- Callback handling (optional)
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import the package
# In production, you would install via: pip install streamlit-html-components
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from streamlit_html_components import render_component, configure

# Configure the package
configure(
    templates_dir='templates',
    styles_dir='styles',
    scripts_dir='scripts',
    default_cache=True
)

# Streamlit app
st.set_page_config(page_title="Basic Button Example", page_icon="🔘", layout="centered")

st.title("🔘 Basic Button Example")
st.markdown("### streamlit-html-components Demo")

st.markdown("""
This example shows how to create a custom button component with:
- **HTML template** with Jinja2 variables
- **CSS styling** with modern gradients and transitions
- **JavaScript** for interactivity and click counting
- **Optional callback** to send events from JS to Python
""")

st.divider()

# Example 1: Basic button
st.subheader("Example 1: Simple Button")
st.code("""
render_component(
    'button',
    props={'text': 'Click me!', 'show_counter': True},
    height=150
)
""", language='python')

render_component(
    'button',
    props={
        'text': 'Click me!',
        'show_counter': True
    },
    height=150
)

st.divider()

# Example 2: Customizable button
st.subheader("Example 2: Customizable Button")

col1, col2 = st.columns(2)
with col1:
    button_text = st.text_input("Button Text", "Hello World!")
with col2:
    show_counter = st.checkbox("Show Click Counter", value=True)

render_component(
    'button',
    props={
        'text': button_text,
        'show_counter': show_counter
    },
    height=150,
    key='custom_button'
)

st.divider()

# Example 3: With callback (demonstration)
st.subheader("Example 3: With Python Callback")
st.markdown("_(Note: Full bidirectional communication requires running in a proper Streamlit environment)_")

if 'click_count' not in st.session_state:
    st.session_state.click_count = 0

def on_button_click(data):
    """Callback function when button is clicked"""
    st.session_state.click_count += 1
    st.info(f"Button clicked {st.session_state.click_count} times! Data: {data}")

st.code("""
def on_button_click(data):
    st.session_state.click_count += 1
    st.write(f"Clicked {st.session_state.click_count} times!")

render_component(
    'button',
    props={'text': 'Click for Callback', 'show_counter': False},
    on_event=on_button_click,
    height=120
)
""", language='python')

render_component(
    'button',
    props={
        'text': 'Click for Callback',
        'show_counter': False
    },
    on_event=on_button_click,
    height=120,
    key='callback_button'
)

if st.session_state.click_count > 0:
    st.success(f"Total clicks received by Python: {st.session_state.click_count}")

st.divider()

# File structure
with st.expander("📁 Component File Structure"):
    st.code("""
basic_button/
├── templates/
│   └── button.html       # HTML template with Jinja2 variables
├── styles/
│   └── button.css        # CSS styling
├── scripts/
│   └── button.js         # JavaScript for interactivity
└── app.py                # This Streamlit app
    """, language='text')

    st.markdown("**button.html**")
    st.code("""<div class="button-container">
    <button class="custom-btn" id="myBtn" type="button">
        {{ text }}
    </button>
    {% if show_counter %}
    <p class="counter" id="counter">Clicks: 0</p>
    {% endif %}
</div>""", language='html')

# Tips
with st.expander("💡 Tips & Best Practices"):
    st.markdown("""
    1. **Auto-discovery**: By default, `render_component('button')` automatically loads:
       - `templates/button.html`
       - `styles/button.css`
       - `scripts/button.js`

    2. **Props validation**: All props are automatically validated and sanitized for XSS prevention

    3. **Caching**: Components are cached by default for better performance

    4. **Framework integration**: Add `frameworks=['tailwind']` to use external CSS frameworks

    5. **Multiple files**: Load multiple CSS/JS files with `styles=['common', 'button']`
    """)
