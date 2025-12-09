"""
Streamlit HTML Components - Official Showcase & Landing Page
Professional, polished UI/UX design
"""

import streamlit as st
import sys
from pathlib import Path
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from streamlit_html_components import render_component, configure

# Page configuration
st.set_page_config(
    page_title="streamlit-html-components - Build Beautiful UIs with HTML/CSS/JS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configure the framework
configure(
    templates_dir='templates',
    styles_dir='styles',
    scripts_dir='scripts',
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
        'title': 'Test Title',
        'subtitle': 'Test Subtitle',
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
# EXAMPLES SECTION
# ============================================

# Create a simple demo using the framework itself
# This demo should also be a component, not inline HTML

# First, let's create a demo button component
render_component(
    'demo_button',
    props={
        'button_text': 'Try Demo Button',
        'initial_count': 0
    },
    styles=['global', 'demo_button'],
    scripts=['demo_button'],
    height=450,
    key='demo_button_section'
)

# Now the examples section
tabs_data = [
    {
        'id': 'button-tab',
        'title': '🔘 Interactive Button',
        'content': {
            'title': 'Interactive Button',
            'features': [
                'Custom CSS animations',
                'Click counter',
                'JavaScript events',
                'Smooth transitions'
            ],
            'code': '''render_component('button',
    props={
        'text': 'Click me!',
        'show_counter': True
    },
    height=150
)''',
            'info': '👆 See the demo button above!'
        },
        'has_demo': True,
        'demo_target': 'demo_button_section'
    },
    {
        'id': 'card-tab',
        'title': '🎨 Tailwind Card',
        'content': {
            'title': 'Tailwind CSS Card',
            'features': [
                'No custom CSS needed',
                'Responsive design',
                'Template loops',
                'Custom filters'
            ],
            'code': '''configure(external_frameworks=['tailwind'])

render_component('card',
    props={
        'title': 'Premium Headphones',
        'price': 299.99,
        'tags': ['new', 'sale']
    }
)''',
            'info': 'See examples/tailwind_card/ for full implementation'
        },
        'has_demo': False
    },
    {
        'id': 'crud-tab',
        'title': '📝 Full CRUD App',
        'content': {
            'title': 'Full CRUD Todo Application',
            'features': [
                'Create, Read, Update, Delete',
                'LocalStorage persistence',
                'Real-time filtering',
                'Beautiful UI/UX'
            ],
            'code': '''# Run the full example
cd examples/crud_todo
streamlit run app.py''',
            'info': 'Complete app with all CRUD operations'
        },
        'has_demo': False
    }
]

crud_features = [
    {'icon': '✅', 'title': 'Create Tasks', 'description': 'Add new todos'},
    {'icon': '📖', 'title': 'Read & Filter', 'description': 'View all tasks'},
    {'icon': '✏️', 'title': 'Update', 'description': 'Edit details'},
    {'icon': '🗑️', 'title': 'Delete', 'description': 'Remove tasks'}
]

render_component(
    'examples',
    props={
        'tabs': tabs_data,
        'crud_section': {
            'title': '📝 Full CRUD Todo Application',
            'description': 'A complete todo list app with Create, Read, Update, Delete operations, localStorage persistence, filtering, and beautiful UI.',
            'features': crud_features,
            'instructions': 'To run the full CRUD example:',
            'code': '''cd examples/crud_todo
streamlit run app.py''',
            'note': 'The CRUD app is a full-featured application best viewed in its own window'
        }
    },
    styles=['global', 'examples'],
    scripts=['examples'],
    height=2000,
    key='examples_section'
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