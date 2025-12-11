# Migration Guide: v1 to v2 API

This guide will help you migrate from the legacy v1 API to the modern v2 API.

## What's New in v2?

### 1. Pydantic-Based Configuration

**v1 (Legacy):**
```python
from streamlit_html_components import configure

configure(
    templates_dir='components/templates',
    styles_dir='components/styles',
    scripts_dir='components/scripts',
    default_cache=True
)
```

**v2 (Modern):**
```python
from streamlit_html_components import configure_v2

config = configure_v2(
    templates_dir='components/templates',
    styles_dir='components/styles',
    scripts_dir='components/scripts',
    enable_cache=True,
    cache_max_size_mb=100,
    cache_ttl_seconds=300,
    auto_discover=True  # NEW: Auto-register components
)

# Configuration is immutable and type-safe
print(config.cache.enabled)  # True
print(config.security.enable_csp)  # True
```

### 2. Component Registry

**v1 (Legacy):**
```python
# Components validated at render time
render_component('button', props={'text': 'Click'})
# ❌ Error only happens when rendering
```

**v2 (Modern):**
```python
# Components validated at startup
configure_v2(auto_discover=True)
# ✅ Errors detected immediately with helpful messages

# List available components
from streamlit_html_components import list_components
print(list_components())  # ['button', 'card', 'hero']

# Get component info
from streamlit_html_components import get_component_info
info = get_component_info('button')
print(info.template)  # 'button.html'
print(info.styles)    # ['button.css']
```

### 3. Deterministic Caching

**v1 (Legacy):**
```python
# Cache key based on component name and props only
# Doesn't detect file changes
render_component('button', props={'text': 'Click'}, cache=True)
```

**v2 (Modern):**
```python
# Cache key includes file content hashes
# Automatically invalidates when files change
render_component_v2('button', props={'text': 'Click'}, cache=True)
# ✅ Cache automatically invalidated when button.html/css/js changes
```

### 4. Better Error Messages

**v1 (Legacy):**
```python
# Generic error message
ComponentNotFoundError: Template not found: button.html
```

**v2 (Modern):**
```python
# Detailed error with suggestions
ComponentNotFoundError: Component 'button' not registered.
Available components: card, hero, navbar
Use register_component() or enable auto_discover in configure_v2()

Template not found: /path/to/templates/button.html
Component: button
Template file: button.html
Templates directory: /path/to/templates
Available templates: card.html, hero.html, navbar.html
```

## Step-by-Step Migration

### Step 1: Install Dependencies

The v2 API requires Pydantic:

```bash
pip install pydantic>=2.0.0
```

Or update your requirements:

```txt
streamlit>=1.52.0
jinja2>=3.1.0
pydantic>=2.0.0
```

### Step 2: Update Configuration

Replace `configure()` with `configure_v2()`:

**Before (v1):**
```python
from streamlit_html_components import configure

configure(
    templates_dir='components/templates',
    styles_dir='components/styles',
    scripts_dir='components/scripts',
    default_cache=True,
    external_frameworks=['tailwind']
)
```

**After (v2):**
```python
from streamlit_html_components import configure_v2

configure_v2(
    templates_dir='components/templates',
    styles_dir='components/styles',
    scripts_dir='components/scripts',
    frameworks=['tailwind'],
    enable_cache=True,
    auto_discover=True  # Automatically register all components
)
```

### Step 3: Update Render Calls

Replace `render_component()` with `render_component_v2()`:

**Before (v1):**
```python
from streamlit_html_components import render_component

render_component(
    'button',
    props={'text': 'Click me'},
    height=100,
    cache=True
)
```

**After (v2):**
```python
from streamlit_html_components import render_component_v2

render_component_v2(
    'button',
    props={'text': 'Click me'},
    height=100,
    cache=True
)
```

### Step 4: Leverage New Features

#### Auto-discovery

**v1:** Manual component specification
```python
render_component('button', ...)
render_component('card', ...)
render_component('hero', ...)
```

**v2:** Auto-discover at startup
```python
configure_v2(auto_discover=True)

# All components in templates/ automatically registered
render_component_v2('button', ...)
render_component_v2('card', ...)
render_component_v2('hero', ...)
```

#### Manual Registration

**v2:** Register components with validation
```python
from streamlit_html_components import register_component

register_component(
    name='custom_button',
    template='button.html',
    styles=['button.css', 'animations.css'],
    scripts=['button.js'],
    validate=True  # Validates files exist at registration
)
```

#### List Components

**v2:** See what's registered
```python
from streamlit_html_components import list_components

components = list_components()
st.sidebar.write("Available components:", components)
```

## Gradual Migration

You can use both v1 and v2 APIs in the same application:

```python
import streamlit as st
from streamlit_html_components import (
    # v1 API
    configure,
    render_component,

    # v2 API
    configure_v2,
    render_component_v2
)

# Configure both
configure(templates_dir='legacy_components/templates')
configure_v2(templates_dir='new_components/templates', auto_discover=True)

# Use v1 for legacy components
render_component('old_button', props={'text': 'Legacy'})

# Use v2 for new components
render_component_v2('new_button', props={'text': 'Modern'})
```

## Configuration Comparison

| Feature | v1 | v2 |
|---------|-----|-----|
| Type validation | ❌ No | ✅ Pydantic |
| Immutable config | ❌ No | ✅ Yes |
| Auto-discovery | ❌ No | ✅ Yes |
| File validation | ⚠️ At render | ✅ At startup |
| Content-based cache | ❌ No | ✅ Yes |
| Component registry | ❌ No | ✅ Yes |
| Error messages | ⚠️ Generic | ✅ Detailed |
| Path validation | ⚠️ Basic | ✅ Comprehensive |

## API Mapping

### Configuration

| v1 | v2 |
|-----|-----|
| `configure()` | `configure_v2()` |
| `get_config()` | `get_config_v2()` |
| `reset_config()` | Create new config |

### Rendering

| v1 | v2 |
|-----|-----|
| `render_component()` | `render_component_v2()` |
| N/A | `register_component()` |
| N/A | `list_components()` |
| N/A | `get_component_info()` |

### Cache Management

| Function | v1 | v2 |
|----------|-----|-----|
| `invalidate_cache()` | ✅ | ✅ |
| `cache_stats()` | ✅ | ✅ |

## Common Migration Issues

### Issue 1: Pydantic Not Installed

**Error:**
```
ModuleNotFoundError: No module named 'pydantic'
```

**Solution:**
```bash
pip install pydantic>=2.0.0
```

### Issue 2: Invalid Directory Paths

**v1:** Silently uses default if invalid

**v2:** Raises validation error

**Solution:**
```python
# Ensure directories exist before configuration
from pathlib import Path

templates_dir = Path('components/templates')
templates_dir.mkdir(parents=True, exist_ok=True)

configure_v2(templates_dir=str(templates_dir))
```

### Issue 3: Component Not Found

**Error:**
```
ComponentNotFoundError: Component 'button' not registered
```

**Solution 1:** Enable auto-discovery
```python
configure_v2(auto_discover=True)
```

**Solution 2:** Manually register
```python
register_component(
    name='button',
    template='button.html'
)
```

### Issue 4: Framework Names

**v1:** Accepts any string

**v2:** Validates framework names

**Solution:**
```python
# Valid frameworks: 'tailwind', 'bootstrap', 'bulma', 'material'
configure_v2(frameworks=['tailwind'])

# Or use custom URL
configure_v2(frameworks=['https://cdn.example.com/framework.css'])
```

## Benefits of Migrating

### 1. Earlier Error Detection

```python
# v1: Error at render time (maybe in production!)
configure(templates_dir='wrong/path')
render_component('button')  # ❌ Fails here

# v2: Error at startup (during development)
configure_v2(templates_dir='wrong/path')  # ✅ Fails immediately
```

### 2. Better Performance

```python
# v1: Cache doesn't detect file changes
render_component('button', cache=True)
# Edit button.html → Still serves old cached version

# v2: Cache invalidates on file changes
render_component_v2('button', cache=True)
# Edit button.html → Automatically re-renders
```

### 3. Type Safety

```python
# v1: No type checking
config = get_config()
config.templates_dir = 123  # ❌ Silently breaks

# v2: Type-safe with Pydantic
config = get_config_v2()
# config.templates_dir = 123  # ✅ Would raise ValidationError
# Config is immutable anyway
```

### 4. Better Developer Experience

```python
# v1: Trial and error to find components
render_component('buton')  # Typo - generic error

# v2: Helpful suggestions
render_component_v2('buton')
# ✅ Error: Component 'buton' not registered
#    Did you mean 'button'?
#    Available: button, card, hero
```

## Recommended Approach

1. **New projects:** Use v2 from the start
2. **Existing projects:** Gradual migration
   - Start with new components using v2
   - Migrate existing components one by one
   - Use both APIs during transition
3. **Large projects:** Create a migration plan
   - Identify all component usage
   - Test in development environment
   - Deploy incrementally

## Need Help?

- **Documentation:** [README.md](README.md)
- **Examples:** Check `examples/` directory
- **Issues:** [GitHub Issues](https://github.com/cjcarito/streamlit-html-components/issues)

---

**Ready to migrate?** Start with `configure_v2(auto_discover=True)` and you're 90% there!
