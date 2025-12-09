# Quick Start Guide

## Installation

### Development Installation (Local)

```bash
cd /Users/cjcarito/Documents/streamlit-html-components
pip install -e .
```

### Install Dependencies

```bash
pip install streamlit>=1.29.0 jinja2>=3.1.0
```

## Test the Package

### Run the Basic Button Example

```bash
cd examples/basic_button
streamlit run app.py
```

### Run the Tailwind Card Example

```bash
cd examples/tailwind_card
streamlit run app.py
```

## Create Your First Component

1. **Create directories:**
   ```bash
   mkdir -p my_app/components/{templates,styles,scripts}
   ```

2. **Create template (components/templates/greeting.html):**
   ```html
   <div class="greeting">
       <h1>Hello, {{ name }}!</h1>
       <p>{{ message }}</p>
   </div>
   ```

3. **Create style (components/styles/greeting.css):**
   ```css
   .greeting {
       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
       color: white;
       padding: 20px;
       border-radius: 10px;
       text-align: center;
   }
   ```

4. **Create app (my_app/app.py):**
   ```python
   import streamlit as st
   from streamlit_html_components import render_component, configure

   configure(
       templates_dir='components/templates',
       styles_dir='components/styles',
       scripts_dir='components/scripts'
   )

   st.title("My First Component")

   name = st.text_input("Your name", "World")

   render_component('greeting', props={
       'name': name,
       'message': 'Welcome to streamlit-html-components!'
   }, height=200)
   ```

5. **Run your app:**
   ```bash
   cd my_app
   streamlit run app.py
   ```

## Publish to PyPI (Future)

1. Build the package:
   ```bash
   python -m build
   ```

2. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

Then users can install with:
```bash
pip install streamlit-html-components
```
