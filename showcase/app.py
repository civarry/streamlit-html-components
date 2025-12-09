"""
Streamlit HTML Components - Official Showcase & Landing Page
Professional, polished UI/UX design
"""

import streamlit as st
import sys
from pathlib import Path

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

# Custom CSS for polished UI
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Remove default padding */
    .main > div {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }

    .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    /* Responsive margins */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .stMarkdown {
            padding: 0 20px;
        }
    }

    /* Beautiful section backgrounds */
    .stMarkdown {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 40px;
    }

    /* Add margins to columns */
    [data-testid="column"] {
        padding: 0 10px;
    }

    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 2px solid #667eea30;
        border-radius: 16px;
        padding: 30px;
        height: 100%;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }

    /* Code blocks */
    .stCodeBlock {
        border-radius: 12px;
        border: 2px solid #667eea30;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        background-color: #f0f2f6;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 12px;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background: #f0f2f6;
    }

    /* Section dividers */
    hr {
        margin: 60px 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea50, transparent);
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
        'subtitle': 'Build Beautiful Streamlit Apps with Traditional Web Development',
        'stats': {
            'components': '10+',
            'lines': '2000+',
            'examples': '3'
        }
    },
    styles=['hero'],
    scripts=['hero'],
    height=600,
    key='hero_section'
)

# ============================================
# WHY SECTION - Beautiful Cards
# ============================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; max-width: 800px; margin: 0 auto 60px auto; padding: 0 20px;'>
    <h1 style='font-size: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               margin-bottom: 20px;'>
        ✨ Why Choose This Framework?
    </h1>
    <p style='font-size: 1.3rem; color: #666; line-height: 1.6;'>
        Stop fighting with Streamlit's limited components. Use the full power of HTML, CSS, and JavaScript
        while keeping all the benefits of Streamlit's free deployment.
    </p>
</div>
""", unsafe_allow_html=True)

# Feature cards in columns
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class='feature-card'>
        <div style='font-size: 3rem; margin-bottom: 20px;'>📁</div>
        <h3 style='color: #667eea; margin-bottom: 15px;'>Organized Structure</h3>
        <p style='color: #666; line-height: 1.6; margin-bottom: 20px;'>
            Write HTML, CSS, and JavaScript in <strong>separate files</strong> - just like real web development.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("💻 See Code Example"):
        st.code("""
components/
├── templates/button.html
├── styles/button.css
└── scripts/button.js
        """, language="text")

with col2:
    st.markdown("""
    <div class='feature-card'>
        <div style='font-size: 3rem; margin-bottom: 20px;'>🎨</div>
        <h3 style='color: #667eea; margin-bottom: 15px;'>Any CSS Framework</h3>
        <p style='color: #666; line-height: 1.6; margin-bottom: 20px;'>
            Use <strong>Tailwind, Bootstrap, Bulma</strong>, or any framework via CDN. Your choice!
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("💻 See Code Example"):
        st.code("""
configure(
    external_frameworks=['tailwind']
)

render_component('card')
        """, language="python")

with col3:
    st.markdown("""
    <div class='feature-card'>
        <div style='font-size: 3rem; margin-bottom: 20px;'>⚡</div>
        <h3 style='color: #667eea; margin-bottom: 15px;'>Lightning Fast</h3>
        <p style='color: #666; line-height: 1.6; margin-bottom: 20px;'>
            <strong>Multi-level caching</strong> makes your components render instantly after first load.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("💻 See Code Example"):
        st.code("""
render_component('button',
    cache=True,
    cache_ttl=300  # 5 minutes
)
        """, language="python")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class='feature-card'>
        <div style='font-size: 3rem; margin-bottom: 20px;'>🔄</div>
        <h3 style='color: #667eea; margin-bottom: 15px;'>Jinja2 Templates</h3>
        <p style='color: #666; line-height: 1.6; margin-bottom: 20px;'>
            Powerful templating with <strong>variables, loops, filters</strong>, and inheritance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("💻 See Code Example"):
        st.code("""
<h1>{{ title }}</h1>
{% for item in items %}
    <p>{{ item.price | currency }}</p>
{% endfor %}
        """, language="html")

with col2:
    st.markdown("""
    <div class='feature-card'>
        <div style='font-size: 3rem; margin-bottom: 20px;'>🔌</div>
        <h3 style='color: #667eea; margin-bottom: 15px;'>Bidirectional</h3>
        <p style='color: #666; line-height: 1.6; margin-bottom: 20px;'>
            <strong>JavaScript can talk to Python</strong> and vice versa. Build truly interactive apps!
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("💻 See Code Example"):
        st.code("""
// In JavaScript
window.sendToStreamlit('click', data);

# In Python
def on_click(data):
    st.write(data)
        """, language="python")

with col3:
    st.markdown("""
    <div class='feature-card'>
        <div style='font-size: 3rem; margin-bottom: 20px;'>🚀</div>
        <h3 style='color: #667eea; margin-bottom: 15px;'>Cloud Ready</h3>
        <p style='color: #666; line-height: 1.6; margin-bottom: 20px;'>
            Works perfectly with <strong>Streamlit Cloud</strong> free tier. Deploy in minutes!
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("💻 See Code Example"):
        st.code("""
# No build step needed!
# Just push to GitHub and deploy
git push origin main
        """, language="bash")

# ============================================
# LIVE EXAMPLES SECTION
# ============================================

st.markdown("---")

st.markdown("""
<div style='text-align: center; max-width: 900px; margin: 0 auto 60px auto; padding: 0 20px;'>
    <h1 style='font-size: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               margin-bottom: 20px;'>
        💡 See It In Action
    </h1>
    <p style='font-size: 1.3rem; color: #666; line-height: 1.6;'>
        Explore real, working examples that demonstrate the power and flexibility of the framework.
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔘 Interactive Button", "🎨 Tailwind Card", "📝 Full CRUD App"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### Interactive Button")
        st.markdown("""
        A beautiful gradient button with:
        - Custom CSS animations
        - Click counter
        - JavaScript events
        - Smooth transitions
        """)

        st.code("""
render_component('button',
    props={
        'text': 'Click me!',
        'show_counter': True
    },
    height=150
)
        """, language="python")

        st.info("👉 Full code in `examples/basic_button/`")

    with col2:
        st.markdown("### Live Demo")
        configure(
            templates_dir='../examples/basic_button/templates',
            styles_dir='../examples/basic_button/styles',
            scripts_dir='../examples/basic_button/scripts'
        )
        render_component(
            'button',
            props={'text': 'Try Me! 🎉', 'show_counter': True},
            height=180,
            key='demo_button'
        )

with tab2:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### Tailwind CSS Card")
        st.markdown("""
        Product card using Tailwind utility classes:
        - No custom CSS needed
        - Responsive design
        - Template loops
        - Custom filters
        """)

        st.code("""
configure(external_frameworks=['tailwind'])

render_component('card',
    props={
        'title': 'Product',
        'price': 99.99,
        'tags': ['new', 'sale']
    }
)
        """, language="python")

        st.info("👉 Full code in `examples/tailwind_card/`")

    with col2:
        st.markdown("### Live Demo")
        configure(
            templates_dir='../examples/tailwind_card/templates',
            styles_dir='../examples/tailwind_card/styles',
            scripts_dir='../examples/tailwind_card/scripts',
            external_frameworks=['tailwind']
        )
        render_component(
            'card',
            props={
                'title': 'Premium Headphones',
                'description': 'Wireless noise-cancelling headphones with 30hr battery',
                'price': 299.99,
                'original_price': 399.99,
                'tags': ['wireless', 'premium', 'sale'],
                'show_button': True,
                'button_text': 'Add to Cart'
            },
            height=450,
            key='demo_card'
        )

with tab3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
                border: 2px solid #667eea30; border-radius: 16px; padding: 40px; text-align: center;'>
        <h2 style='color: #667eea; margin-bottom: 20px;'>📝 Full CRUD Todo Application</h2>
        <p style='font-size: 1.1rem; color: #666; margin-bottom: 30px;'>
            A complete todo list app with Create, Read, Update, Delete operations,
            localStorage persistence, filtering, and beautiful UI.
        </p>

        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px; margin: 30px 0;'>
            <div style='background: white; padding: 20px; border-radius: 12px; border: 2px solid #10b98130;'>
                <div style='font-size: 2rem; margin-bottom: 10px;'>✅</div>
                <strong style='color: #10b981;'>Create Tasks</strong>
                <p style='font-size: 0.9rem; color: #666; margin-top: 5px;'>Add new todos</p>
            </div>
            <div style='background: white; padding: 20px; border-radius: 12px; border: 2px solid #3b82f630;'>
                <div style='font-size: 2rem; margin-bottom: 10px;'>📖</div>
                <strong style='color: #3b82f6;'>Read & Filter</strong>
                <p style='font-size: 0.9rem; color: #666; margin-top: 5px;'>View all tasks</p>
            </div>
            <div style='background: white; padding: 20px; border-radius: 12px; border: 2px solid #f59e0b30;'>
                <div style='font-size: 2rem; margin-bottom: 10px;'>✏️</div>
                <strong style='color: #f59e0b;'>Update</strong>
                <p style='font-size: 0.9rem; color: #666; margin-top: 5px;'>Edit details</p>
            </div>
            <div style='background: white; padding: 20px; border-radius: 12px; border: 2px solid #ef444430;'>
                <div style='font-size: 2rem; margin-bottom: 10px;'>🗑️</div>
                <strong style='color: #ef4444;'>Delete</strong>
                <p style='font-size: 0.9rem; color: #666; margin-top: 5px;'>Remove tasks</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <p style='font-size: 1.1rem; color: #666; margin-bottom: 20px;'>
                To run the full CRUD example:
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.code("""
cd examples/crud_todo
streamlit run app.py
        """, language="bash")

        st.info("💡 The CRUD app is a full-featured application best viewed in its own window")

# ============================================
# INSTALLATION SECTION
# ============================================

st.markdown("---")

st.markdown("""
<div style='text-align: center; max-width: 800px; margin: 0 auto 60px auto; padding: 0 20px;'>
    <h1 style='font-size: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               margin-bottom: 20px;'>
        📦 Get Started in 60 Seconds
    </h1>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 1️⃣ Install")
    st.code("pip install streamlit-html-components", language="bash")

    st.markdown("### 2️⃣ Create Your Component")
    st.code("""
# app.py
from streamlit_html_components import render_component, configure

configure(
    templates_dir='components/templates',
    styles_dir='components/styles',
    scripts_dir='components/scripts'
)

render_component('button', props={'text': 'Hello!'})
    """, language="python")

    st.markdown("### 3️⃣ Run")
    st.code("streamlit run app.py", language="bash")

    st.success("🎉 That's it! Your first component is live!")

# ============================================
# FOOTER/CTA
# ============================================

st.markdown("---")

st.markdown("""
<div style='text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px; margin: 0 20px;'>
    <h2 style='color: white; font-size: 2.5rem; margin-bottom: 20px;'>
        Ready to Build Something Amazing?
    </h2>
    <p style='color: rgba(255,255,255,0.9); font-size: 1.3rem; margin-bottom: 40px;'>
        Join developers who are already building beautiful Streamlit apps with traditional web tools
    </p>
    <div style='display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;'>
        <a href='https://github.com/cjcarito/streamlit-html-components' target='_blank' style='text-decoration: none;'>
            <div style='background: white; color: #667eea; padding: 16px 40px; border-radius: 12px;
                       font-weight: 600; font-size: 1.1rem; cursor: pointer; transition: transform 0.3s;'>
                ⭐ Star on GitHub
            </div>
        </a>
        <a href='https://pypi.org/project/streamlit-html-components' target='_blank' style='text-decoration: none;'>
            <div style='background: rgba(255,255,255,0.2); color: white; padding: 16px 40px;
                       border-radius: 12px; border: 2px solid white; font-weight: 600;
                       font-size: 1.1rem; cursor: pointer; transition: transform 0.3s;'>
                📦 View on PyPI
            </div>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: #999; padding: 40px 20px;'>
    <p style='margin-bottom: 10px;'><strong>streamlit-html-components</strong> v0.1.0</p>
    <p style='margin-bottom: 20px;'>Built with ❤️ by CJ Carito</p>
    <p style='font-size: 0.9rem;'>
        <a href='https://github.com/cjcarito/streamlit-html-components' style='color: #667eea; text-decoration: none;'>GitHub</a> •
        <a href='https://pypi.org/project/streamlit-html-components' style='color: #667eea; text-decoration: none;'>PyPI</a> •
        <a href='https://github.com/cjcarito/streamlit-html-components/blob/main/LICENSE' style='color: #667eea; text-decoration: none;'>MIT License</a>
    </p>
</div>
""", unsafe_allow_html=True)
