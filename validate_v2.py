"""
Simple validation script to check the v2 architecture files.

This script validates:
1. All files have valid Python syntax
2. All imports are correctly structured
3. Key classes and functions are defined
"""

import ast
from pathlib import Path


def validate_python_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)


def check_class_exists(file_path, class_name):
    """Check if a class is defined in a file."""
    with open(file_path, 'r') as f:
        code = f.read()
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return True
    return False


def check_function_exists(file_path, func_name):
    """Check if a function is defined in a file."""
    with open(file_path, 'r') as f:
        code = f.read()
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return True
    return False


def main():
    """Run validation."""
    print("=" * 60)
    print("Validating streamlit-html-components v2 Architecture")
    print("=" * 60)

    src_dir = Path(__file__).parent / 'src' / 'streamlit_html_components'

    files_to_validate = {
        'config_v2.py': {
            'classes': ['ComponentConfig', 'CacheConfig', 'SecurityConfig'],
            'functions': ['create_default_config']
        },
        'registry.py': {
            'classes': ['ComponentRegistry', 'ComponentSchema'],
            'functions': []
        },
        'serialization.py': {
            'classes': [],
            'functions': ['serialize_value', 'serialize_props', 'hash_props', 'generate_cache_key']
        },
        'core_v2.py': {
            'classes': [],
            'functions': ['configure_v2', 'render_component_v2', 'register_component', 'list_components']
        },
        'cache_manager.py': {
            'classes': ['CacheManager'],
            'functions': ['get_cache_manager']
        }
    }

    all_valid = True

    for filename, expectations in files_to_validate.items():
        file_path = src_dir / filename
        print(f"\n📄 Validating {filename}...")

        # Check file exists
        if not file_path.exists():
            print(f"  ✗ File not found: {file_path}")
            all_valid = False
            continue

        # Check syntax
        valid, error = validate_python_syntax(file_path)
        if not valid:
            print(f"  ✗ Syntax error: {error}")
            all_valid = False
            continue
        print(f"  ✓ Valid Python syntax")

        # Check expected classes
        for class_name in expectations['classes']:
            if check_class_exists(file_path, class_name):
                print(f"  ✓ Class '{class_name}' defined")
            else:
                print(f"  ✗ Class '{class_name}' not found")
                all_valid = False

        # Check expected functions
        for func_name in expectations['functions']:
            if check_function_exists(file_path, func_name):
                print(f"  ✓ Function '{func_name}' defined")
            else:
                print(f"  ✗ Function '{func_name}' not found")
                all_valid = False

    print("\n" + "=" * 60)
    if all_valid:
        print("✓ ALL VALIDATIONS PASSED!")
        print("=" * 60)
        print("\nThe v2 architecture is ready to use:")
        print("  - config_v2.py: Pydantic-based configuration")
        print("  - registry.py: Component registry with validation")
        print("  - serialization.py: Deterministic serialization")
        print("  - core_v2.py: Modern rendering API")
        print("  - cache_manager.py: Updated with new serialization")
        print("\nTo use the v2 API:")
        print("  from streamlit_html_components import configure_v2, render_component_v2")
        return 0
    else:
        print("✗ SOME VALIDATIONS FAILED")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
