"""
Tailwind CSS Card Example - streamlit-html-components

This example demonstrates:
- External CSS framework integration (Tailwind CSS)
- Using utility classes instead of custom CSS
- Template variables with custom Jinja2 filters
- Conditional rendering in templates
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from streamlit_html_components import render_component, configure

# Configure with Tailwind CSS
configure(
    templates_dir='templates',
    styles_dir='styles',
    scripts_dir='scripts',
    external_frameworks=['tailwind']  # Load Tailwind CSS via CDN
)

# Streamlit app
st.set_page_config(page_title="Tailwind Card Example", page_icon="🎨", layout="wide")

st.title("🎨 Tailwind CSS Card Example")
st.markdown("### Using External CSS Frameworks with streamlit-html-components")

st.markdown("""
This example demonstrates how to use **Tailwind CSS** with your components.
No custom CSS file needed - just use Tailwind's utility classes in your HTML template!
""")

st.divider()

# Example 1: Product Card
st.subheader("Example 1: Product Card")

col1, col2 = st.columns([2, 1])

with col1:
    render_component(
        'card',
        props={
            'title': 'Premium Headphones',
            'description': 'Experience crystal-clear audio with our state-of-the-art wireless headphones. '
                         'Featuring active noise cancellation and 30-hour battery life.',
            'price': 299.99,
            'original_price': 399.99,
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
            'tags': ['wireless', 'noise-cancelling', 'premium'],
            'show_button': True,
            'button_text': 'Add to Cart'
        },
        height=600,
        key='product_card'
    )

with col2:
    st.code("""
render_component(
    'card',
    props={
        'title': 'Premium Headphones',
        'description': '...',
        'price': 299.99,
        'original_price': 399.99,
        'image_url': '...',
        'tags': ['wireless', 'noise-cancelling'],
        'show_button': True
    },
    height=600
)
    """, language='python')

st.divider()

# Example 2: Service Card
st.subheader("Example 2: Service Card (No Image)")

col1, col2 = st.columns([2, 1])

with col1:
    render_component(
        'card',
        props={
            'title': 'Web Development',
            'description': 'Professional web development services using modern frameworks like React, Vue, '
                         'and Streamlit. Build fast, responsive, and beautiful web applications.',
            'price': 150.00,
            'tags': ['development', 'consulting', 'react', 'streamlit'],
            'show_button': True,
            'button_text': 'Get Started'
        },
        height=450,
        key='service_card'
    )

with col2:
    st.code("""
render_component(
    'card',
    props={
        'title': 'Web Development',
        'description': '...',
        'price': 150.00,
        'tags': ['development'],
        'show_button': True
    }
)
    """, language='python')

st.divider()

# Example 3: Interactive Builder
st.subheader("Example 3: Build Your Own Card")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Customize Your Card:**")

    card_title = st.text_input("Card Title", "Your Amazing Product")
    card_description = st.text_area(
        "Description",
        "Describe your product or service here. Make it compelling and informative!"
    )

    show_image = st.checkbox("Show Image", value=True)
    image_url = ""
    if show_image:
        image_url = st.text_input(
            "Image URL",
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop"
        )

    show_pricing = st.checkbox("Show Pricing", value=True)
    price = 0
    original_price = 0
    if show_pricing:
        col_a, col_b = st.columns(2)
        with col_a:
            price = st.number_input("Price ($)", value=99.99, min_value=0.0, step=0.01)
        with col_b:
            has_original = st.checkbox("Show original price", value=False)
            if has_original:
                original_price = st.number_input("Original Price ($)", value=149.99, min_value=0.0, step=0.01)

    tags_input = st.text_input("Tags (comma-separated)", "tag1, tag2, tag3")
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    show_button = st.checkbox("Show Button", value=True)
    button_text = ""
    if show_button:
        button_text = st.text_input("Button Text", "Learn More")

with col2:
    st.markdown("**Preview:**")

    render_component(
        'card',
        props={
            'title': card_title,
            'description': card_description,
            'image_url': image_url if show_image else None,
            'price': price if show_pricing else None,
            'original_price': original_price if original_price > 0 else None,
            'tags': tags if tags else None,
            'show_button': show_button,
            'button_text': button_text
        },
        height=700,
        key='custom_card'
    )

st.divider()

# Template showcase
with st.expander("📝 Template Code (card.html)"):
    st.markdown("Notice how we use **Tailwind utility classes** directly in the HTML:")
    st.code("""<div class="max-w-sm mx-auto rounded-lg overflow-hidden shadow-lg bg-white hover:shadow-2xl transition-shadow duration-300">
    {% if image_url %}
    <img class="w-full h-48 object-cover" src="{{ image_url }}" alt="{{ title }}">
    {% endif %}

    <div class="px-6 py-4">
        <div class="font-bold text-2xl mb-2 text-gray-800">{{ title }}</div>
        <p class="text-gray-700 text-base leading-relaxed">
            {{ description }}
        </p>
    </div>

    {% if price %}
    <div class="px-6 py-2">
        <span class="text-3xl font-bold text-indigo-600">{{ price | currency }}</span>
    </div>
    {% endif %}

    {% if tags %}
    <div class="px-6 pt-4 pb-2">
        {% for tag in tags %}
        <span class="inline-block bg-indigo-100 rounded-full px-3 py-1 text-sm font-semibold text-indigo-700 mr-2 mb-2">
            #{{ tag }}
        </span>
        {% endfor %}
    </div>
    {% endif %}
</div>""", language='html')

# Configuration
with st.expander("⚙️ Configuration"):
    st.markdown("""
    To use Tailwind CSS (or any external framework), simply configure it:

    ```python
    from streamlit_html_components import configure

    configure(
        templates_dir='templates',
        styles_dir='styles',
        scripts_dir='scripts',
        external_frameworks=['tailwind']  # Automatically loads Tailwind CDN
    )
    ```

    **Supported frameworks:**
    - `'tailwind'` - Tailwind CSS
    - `'bootstrap'` - Bootstrap 5
    - `'bulma'` - Bulma CSS
    - `'material'` - Material Design

    You can also use custom CDN URLs for any framework!
    """)

# Features
with st.expander("✨ Features Demonstrated"):
    st.markdown("""
    1. **External Framework Integration**: Tailwind CSS loaded via CDN
    2. **Jinja2 Template Features**:
       - Conditional rendering (`{% if ... %}`)
       - Loops (`{% for tag in tags %}`)
       - Custom filters (`{{ price | currency }}`)
    3. **Responsive Design**: Tailwind's utility classes
    4. **No Custom CSS**: All styling via Tailwind utilities
    5. **Component Reusability**: Same template, different props
    """)
