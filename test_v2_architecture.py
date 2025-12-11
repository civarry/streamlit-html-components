"""
Test script to validate the v2 architecture without requiring Streamlit.

This script tests:
1. Configuration system with Pydantic validation
2. Component registry and validation
3. Serialization utilities
"""

from pathlib import Path
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'streamlit_html_components'))

# Import modules directly to avoid Streamlit dependency
import config_v2
import registry
import serialization

from config_v2 import ComponentConfig, create_default_config, CacheConfig, SecurityConfig
from registry import ComponentRegistry, ComponentSchema
from serialization import (
    serialize_value,
    serialize_props,
    hash_props,
    hash_file_content,
    generate_cache_key
)


def test_serialization():
    """Test serialization utilities."""
    print("\n=== Testing Serialization ===")

    # Test serialize_value
    assert serialize_value(datetime(2025, 12, 11, 10, 30)) == '2025-12-11T10:30:00'
    assert serialize_value(Path('/tmp/test')) == '/tmp/test'
    print("✓ serialize_value works correctly")

    # Test serialize_props
    props = {'name': 'test', 'count': 5, 'active': True}
    json_str = serialize_props(props)
    assert 'name' in json_str and 'count' in json_str
    print("✓ serialize_props works correctly")

    # Test hash_props
    hash_str = hash_props(props)
    assert len(hash_str) == 64  # SHA256 produces 64 hex characters
    print("✓ hash_props works correctly")

    # Test that same props produce same hash (deterministic)
    hash_str2 = hash_props({'count': 5, 'active': True, 'name': 'test'})  # Different order
    assert hash_str == hash_str2
    print("✓ hash_props is deterministic")

    print("✓ All serialization tests passed!")


def test_config_validation():
    """Test Pydantic configuration validation."""
    print("\n=== Testing Configuration ===")

    # Test that non-existent directories raise errors
    try:
        config = ComponentConfig(
            templates_dir='/nonexistent/path',
            styles_dir='styles',
            scripts_dir='scripts'
        )
        assert False, "Should have raised ValueError for non-existent directory"
    except ValueError as e:
        assert "does not exist" in str(e)
        print("✓ Configuration validates directory existence")

    # Test framework validation
    try:
        config = create_default_config(
            templates_dir='.',
            styles_dir='.',
            scripts_dir='.',
            frameworks=['invalid_framework']
        )
        assert False, "Should have raised ValueError for invalid framework"
    except ValueError as e:
        assert "Unknown framework" in str(e)
        print("✓ Configuration validates framework names")

    # Test cache config
    cache_config = CacheConfig(enabled=True, max_size_mb=50, ttl_seconds=300)
    assert cache_config.enabled == True
    assert cache_config.max_size_mb == 50
    print("✓ CacheConfig works correctly")

    # Test security config
    security_config = SecurityConfig(
        enable_csp=True,
        allowed_origins=['https://example.com'],
        validate_paths=True
    )
    assert security_config.enable_csp == True
    assert 'https://example.com' in security_config.allowed_origins
    print("✓ SecurityConfig works correctly")

    # Test immutability
    try:
        cache_config.enabled = False
        assert False, "Should not allow mutation"
    except Exception:
        print("✓ Configuration is immutable")

    print("✓ All configuration tests passed!")


def test_component_schema():
    """Test component schema validation."""
    print("\n=== Testing Component Schema ===")

    # Test valid component schema
    schema = ComponentSchema(
        name='button',
        template='button.html',
        styles=['button.css'],
        scripts=['button.js']
    )
    assert schema.name == 'button'
    assert schema.template == 'button.html'
    print("✓ ComponentSchema creation works")

    # Test invalid component name
    try:
        schema = ComponentSchema(
            name='invalid name!',  # Spaces and special chars not allowed
            template='template.html'
        )
        assert False, "Should have raised ValueError for invalid name"
    except ValueError as e:
        assert "invalid" in str(e).lower()
        print("✓ ComponentSchema validates component names")

    print("✓ All component schema tests passed!")


def test_cache_key_generation():
    """Test cache key generation."""
    print("\n=== Testing Cache Key Generation ===")

    # Create a temporary file for testing
    test_file = Path('/tmp/test_cache_key.txt')
    test_file.write_text('test content')

    try:
        # Generate cache key
        key = generate_cache_key(
            component_name='button',
            props={'text': 'Click me'},
            template_path=test_file,
            css_paths=[test_file],
            js_paths=[test_file]
        )

        assert isinstance(key, str)
        assert 'button' in key
        print("✓ Cache key generation works")

        # Test that same inputs produce same key
        key2 = generate_cache_key(
            component_name='button',
            props={'text': 'Click me'},
            template_path=test_file,
            css_paths=[test_file],
            js_paths=[test_file]
        )
        assert key == key2
        print("✓ Cache key generation is deterministic")

        # Test that different props produce different keys
        key3 = generate_cache_key(
            component_name='button',
            props={'text': 'Different text'},
            template_path=test_file,
            css_paths=[test_file],
            js_paths=[test_file]
        )
        assert key != key3
        print("✓ Cache key changes with different props")

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()

    print("✓ All cache key tests passed!")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing streamlit-html-components v2 Architecture")
    print("=" * 60)

    try:
        test_serialization()
        test_config_validation()
        test_component_schema()
        test_cache_key_generation()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return 0

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
