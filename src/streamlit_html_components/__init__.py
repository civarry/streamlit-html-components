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

Example (Legacy API):
    >>> from streamlit_html_components import render_component, configure
    >>>
    >>> configure(
    ...     templates_dir='components/templates',
    ...     styles_dir='components/styles',
    ...     scripts_dir='components/scripts'
    ... )
    >>>
    >>> render_component('button', props={'text': 'Click me!'})

Example (Modern v2 API):
    >>> from streamlit_html_components import configure_v2, render_component_v2
    >>>
    >>> configure_v2(
    ...     templates_dir='components/templates',
    ...     styles_dir='components/styles',
    ...     scripts_dir='components/scripts',
    ...     frameworks=['tailwind'],
    ...     auto_discover=True
    ... )
    >>>
    >>> render_component_v2('button', props={'text': 'Click me!'})
"""

# Legacy API (v1)
from .core import render_component, add_framework
from .config import configure, get_config, reset_config

# Modern API (v2)
from .core_v2 import (
    configure_v2,
    render_component_v2,
    register_component,
    list_components,
    get_component_info,
    get_config_v2,
    get_registry,
    get_renderer
)
from .renderer import ComponentRenderer

# Shared utilities
from .cache_manager import invalidate_cache, cache_stats
from .security import (
    CSPPolicy,
    create_default_csp,
    create_strict_csp,
    SecurityAuditor,
    inject_csp_meta
)
from .diagnostics import (
    FuzzyMatcher,
    PathSuggester,
    ErrorFormatter,
    DebugMode,
    Suggestion
)
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
    # Legacy Core API (v1)
    "render_component",
    "configure",
    "add_framework",

    # Modern Core API (v2)
    "configure_v2",
    "render_component_v2",
    "register_component",
    "list_components",
    "get_component_info",
    "get_config_v2",
    "get_registry",
    "get_renderer",
    "ComponentRenderer",

    # Cache management
    "invalidate_cache",
    "cache_stats",

    # Security
    "CSPPolicy",
    "create_default_csp",
    "create_strict_csp",
    "SecurityAuditor",
    "inject_csp_meta",

    # Diagnostics
    "FuzzyMatcher",
    "PathSuggester",
    "ErrorFormatter",
    "DebugMode",
    "Suggestion",

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
