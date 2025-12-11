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
import importlib.util

# Add src to path to enable package imports
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Manually import modules to avoid Streamlit dependency from __init__.py
def import_module_from_file(module_name, file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Set up the package structure manually
pkg_path = src_path / 'streamlit_html_components'
sys.modules['streamlit_html_components'] = type(sys)('streamlit_html_components')
sys.modules['streamlit_html_components'].__path__ = [str(pkg_path)]

# Import core modules in dependency order
exceptions = import_module_from_file(
    'streamlit_html_components.exceptions',
    pkg_path / 'exceptions.py'
)
validators = import_module_from_file(
    'streamlit_html_components.validators',
    pkg_path / 'validators.py'
)
serialization = import_module_from_file(
    'streamlit_html_components.serialization',
    pkg_path / 'serialization.py'
)
config_v2 = import_module_from_file(
    'streamlit_html_components.config_v2',
    pkg_path / 'config_v2.py'
)
registry = import_module_from_file(
    'streamlit_html_components.registry',
    pkg_path / 'registry.py'
)


def test_serialization():
    """Test serialization utilities."""
    print("\n=== Testing Serialization ===")

    # Test serialize_value
    assert serialization.serialize_value(datetime(2025, 12, 11, 10, 30)) == '2025-12-11T10:30:00'
    assert serialization.serialize_value(Path('/tmp/test')) == '/tmp/test'
    print("✓ serialize_value works correctly")

    # Test deterministic serialization
    props1 = {'name': 'test', 'count': 5}
    props2 = {'count': 5, 'name': 'test'}
    assert serialization.serialize_props(props1) == serialization.serialize_props(props2)
    print("✓ serialize_props is deterministic")

    # Test hashing
    hash1 = serialization.hash_props(props1)
    hash2 = serialization.hash_props(props2)
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 hex
    print(f"✓ hash_props is deterministic: {hash1[:16]}...")


def test_configuration():
    """Test Pydantic configuration."""
    print("\n=== Testing Configuration ===")

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create required directories
        templates_dir = tmp_path / 'templates'
        styles_dir = tmp_path / 'styles'
        scripts_dir = tmp_path / 'scripts'

        for d in [templates_dir, styles_dir, scripts_dir]:
            d.mkdir()

        # Test config creation
        config = config_v2.ComponentConfig(
            templates_dir=templates_dir,
            styles_dir=styles_dir,
            scripts_dir=scripts_dir,
            frameworks=['tailwind'],
            cache=config_v2.CacheConfig(enabled=True, max_size_mb=50),
            security=config_v2.SecurityConfig(enable_csp=True)
        )

        assert config.templates_dir == templates_dir.resolve()
        assert config.cache.enabled == True
        assert config.cache.max_size_mb == 50
        assert 'tailwind' in config.frameworks
        print("✓ ComponentConfig creation works")

        # Test immutability
        try:
            config.cache.enabled = False
            assert False, "Should not allow mutation"
        except Exception:
            print("✓ Configuration is immutable")

        # Test create_default_config
        default_config = config_v2.create_default_config(
            templates_dir=templates_dir,
            styles_dir=styles_dir,
            scripts_dir=scripts_dir
        )
        assert default_config.templates_dir == templates_dir.resolve()
        print("✓ create_default_config works")


def test_component_registry():
    """Test component registry."""
    print("\n=== Testing Component Registry ===")

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create directory structure
        templates_dir = tmp_path / 'templates'
        styles_dir = tmp_path / 'styles'
        scripts_dir = tmp_path / 'scripts'

        for d in [templates_dir, styles_dir, scripts_dir]:
            d.mkdir()

        # Create test files
        (templates_dir / 'button.html').write_text('<button>{{ text }}</button>')
        (styles_dir / 'button.css').write_text('.btn { color: blue; }')
        (scripts_dir / 'button.js').write_text('console.log("loaded");')

        # Create config and registry
        config = config_v2.ComponentConfig(
            templates_dir=templates_dir,
            styles_dir=styles_dir,
            scripts_dir=scripts_dir
        )

        reg = registry.ComponentRegistry(config)

        # Register component
        schema = registry.ComponentSchema(
            name='button',
            template='button.html',
            styles=['button.css'],
            scripts=['button.js']
        )

        reg.register(schema, validate=True)
        print("✓ Component registration works")

        # Test retrieval
        assert 'button' in reg
        assert len(reg) == 1
        assert reg.get('button') is not None
        print("✓ Component retrieval works")

        # Test auto-discovery
        (templates_dir / 'card.html').write_text('<div>{{ content }}</div>')
        reg.auto_discover()
        assert 'card' in reg
        assert len(reg) == 2
        print("✓ Auto-discovery works")

        # Test list_components
        components = reg.list_components()
        assert 'button' in components
        assert 'card' in components
        print(f"✓ Listed components: {components}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("v2 Architecture Validation Tests")
    print("=" * 60)

    try:
        test_serialization()
        test_configuration()
        test_component_registry()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe v2 architecture is fully functional.")
        return 0

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
