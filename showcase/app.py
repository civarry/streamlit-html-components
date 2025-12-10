"""
Streamlit HTML Components - Official Showcase & Landing Page
Professional, polished UI/UX design
"""

import streamlit as st
import sys
from pathlib import Path

# Get the absolute path to the showcase directory
BASE_DIR = Path(__file__).parent

# Add parent directory to path for imports
sys.path.insert(0, str(BASE_DIR.parent / 'src'))

from streamlit_html_components import render_component, configure

# Page configuration
st.set_page_config(
    page_title="streamlit-html-components - Build Beautiful UIs with HTML/CSS/JS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configure the framework with absolute paths
configure(
    templates_dir=str(BASE_DIR / 'templates'),
    styles_dir=str(BASE_DIR / 'styles'),
    scripts_dir=str(BASE_DIR / 'scripts'),
    default_cache=True
)

# Remove ALL HTML/CSS from here - use global.css instead
# We'll add a simple streamlit spacing fix ONLY
st.markdown("""
<style>
    .main > div {
        padding-left: 0rem;
        padding-right: 0rem;
    }
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HERO SECTION
# ============================================

render_component(
    'hero',
    props={
        'title': 'streamlit-html-components',
        'subtitle': 'Build Beautiful UIs with HTML, CSS, and JavaScript',
        'stats': {'components': '1', 'lines': '100', 'examples': '1'}
    },
    styles=['global', 'hero'],
    scripts=['hero'],
    height=700,
    key='test_hero'
)

# ============================================
# WHY SECTION
# ============================================

features_data = [
    {
        'icon': '📁',
        'title': 'Organized Structure',
        'description': 'Write HTML, CSS, and JavaScript in separate files - just like real web development.',
        'code_example': '''components/
├── templates/button.html
├── styles/button.css
└── scripts/button.js'''
    },
    {
        'icon': '🎨',
        'title': 'Any CSS Framework',
        'description': 'Use Tailwind, Bootstrap, Bulma, or any framework via CDN. Your choice!',
        'code_example': '''configure(
    external_frameworks=['tailwind']
)

render_component('card')'''
    },
    {
        'icon': '⚡',
        'title': 'Lightning Fast',
        'description': 'Multi-level caching makes your components render instantly after first load.',
        'code_example': '''render_component('button',
    cache=True,
    cache_ttl=300  # 5 minutes
)'''
    },
    {
        'icon': '🔄',
        'title': 'Jinja2 Templates',
        'description': 'Powerful templating with variables, loops, filters, and inheritance.',
        'code_example': '''<h1>{{ title }}</h1>
{% for item in items %}
    <p>{{ item.price | currency }}</p>
{% endfor %}'''
    },
    {
        'icon': '🔌',
        'title': 'Bidirectional',
        'description': 'JavaScript can talk to Python and vice versa. Build truly interactive apps!',
        'code_example': '''// In JavaScript
window.sendToStreamlit('click', data)

# In Python
def on_click(data):
    st.write(data)'''
    },
    {
        'icon': '🚀',
        'title': 'Cloud Ready',
        'description': 'Works perfectly with Streamlit Cloud free tier. Deploy in minutes!',
        'code_example': '''# No build step needed!
# Just push to GitHub and deploy
git push origin main'''
    }
]

render_component(
    'why',
    props={'features': features_data},
    styles=['global', 'why'],
    scripts=['why'],
    height=1250,
    key='why_section'
)

# ============================================
# INSTALLATION SECTION
# ============================================

render_component(
    'installation',
    props={},
    styles=['global', 'installation'],
    scripts=['installation'],
    height=1500,
    key='installation_section'
)

# ============================================
# FOOTER SECTION
# ============================================

render_component(
    'footer',
    props={
        'version': 'v0.1.0',
        'author': 'CJ Carito',
        'links': [
            {'name': 'GitHub', 'url': 'https://github.com/civarry/streamlit-html-components'},
            {'name': 'PyPI', 'url': 'https://pypi.org/project/streamlit-html-components'},
            {'name': 'MIT License', 'url': 'https://github.com/civarry/streamlit-html-components/blob/main/LICENSE'}
        ]
    },
    styles=['global', 'footer'],
    scripts=['footer'],
    height=450,
    key='footer_section'
)