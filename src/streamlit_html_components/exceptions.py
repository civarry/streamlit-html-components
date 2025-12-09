"""Custom exceptions for streamlit-html-components package."""


class StreamlitHtmlComponentsError(Exception):
    """Base exception for all streamlit-html-components errors."""
    pass


class ComponentNotFoundError(StreamlitHtmlComponentsError):
    """Raised when a component template cannot be found."""
    pass


class AssetNotFoundError(StreamlitHtmlComponentsError):
    """Raised when a CSS or JavaScript asset file cannot be found."""
    pass


class TemplateSyntaxError(StreamlitHtmlComponentsError):
    """Raised when a template contains syntax errors."""
    pass


class InvalidPropsError(StreamlitHtmlComponentsError):
    """Raised when component props fail validation."""
    pass


class ConfigurationError(StreamlitHtmlComponentsError):
    """Raised when package configuration is invalid."""
    pass


class SecurityError(StreamlitHtmlComponentsError):
    """Raised when a security violation is detected (e.g., path traversal)."""
    pass
