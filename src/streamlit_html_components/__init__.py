"""
streamlit-html-components

A framework for using traditional HTML/CSS/JS file structure with Streamlit applications.

Features:
- Write HTML/CSS/JS in separate files (traditional web development workflow)
- Template variables and props support via Jinja2
- External CSS framework integration (Tailwind, Bootstrap, Bulma, etc.)
- Component caching for performance optimization
- Bidirectional JavaScript-Python communication
- Works with Streamlit Cloud free deployment

Example:
    >>> from streamlit_html_components import render_component, configure
    >>>
    >>> configure(
    ...     templates_dir='components/templates',
    ...     styles_dir='components/styles',
    ...     scripts_dir='components/scripts'
    ... )
    >>>
    >>> render_component('button', props={'text': 'Click me!'})
"""

from .core import render_component, add_framework
from .config import configure, get_config, reset_config
from .cache_manager import invalidate_cache, cache_stats
from .exceptions import (
    StreamlitHtmlComponentsError,
    ComponentNotFoundError,
    AssetNotFoundError,
    TemplateSyntaxError,
    InvalidPropsError,
    ConfigurationError,
    SecurityError,
)

__version__ = "0.1.0"
__author__ = "CJ Carito"
__license__ = "MIT"

__all__ = [
    # Core API
    "render_component",
    "configure",
    "add_framework",

    # Cache management
    "invalidate_cache",
    "cache_stats",

    # Configuration
    "get_config",
    "reset_config",

    # Exceptions
    "StreamlitHtmlComponentsError",
    "ComponentNotFoundError",
    "AssetNotFoundError",
    "TemplateSyntaxError",
    "InvalidPropsError",
    "ConfigurationError",
    "SecurityError",
]
