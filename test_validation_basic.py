"""
Basic validation test without pytest dependency.
"""

import sys
from pathlib import Path
import importlib.util

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Manually import modules to avoid relative import issues
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
validation = import_module_from_file(
    'streamlit_html_components.validation',
    pkg_path / 'validation.py'
)

print("=" * 60)
print("Validation System Basic Tests")
print("=" * 60)

# Test 1: ValidationRule
print("\n=== Test 1: ValidationRule ===")
rule = validation.ValidationRule('name', validation.ValidationType.REQUIRED)
is_valid, error = rule.validate('John')
assert is_valid and error is None
print("✅ Required validation (pass)")

is_valid, error = rule.validate(None)
assert not is_valid and error is not None
print("✅ Required validation (fail)")

# Test 2: Type validation
print("\n=== Test 2: Type Validation ===")
rule = validation.ValidationRule('age', validation.ValidationType.TYPE, int)
is_valid, error = rule.validate(25)
assert is_valid
print("✅ Type validation (int pass)")

is_valid, error = rule.validate("25")
assert not is_valid
print("✅ Type validation (int fail)")

# Test 3: Pattern validation
print("\n=== Test 3: Pattern Validation ===")
rule = validation.ValidationRule('email', validation.ValidationType.PATTERN, r'^[\w\.-]+@[\w\.-]+\.\w+$')
is_valid, error = rule.validate('test@example.com')
assert is_valid
print("✅ Pattern validation (pass)")

is_valid, error = rule.validate('invalid-email')
assert not is_valid
print("✅ Pattern validation (fail)")

# Test 4: Range validation
print("\n=== Test 4: Range Validation ===")
rule = validation.ValidationRule('score', validation.ValidationType.RANGE, (0, 100))
is_valid, error = rule.validate(50)
assert is_valid
print("✅ Range validation (pass)")

is_valid, error = rule.validate(150)
assert not is_valid
print("✅ Range validation (fail)")

# Test 5: Enum validation
print("\n=== Test 5: Enum Validation ===")
rule = validation.ValidationRule('status', validation.ValidationType.ENUM, ['active', 'inactive'])
is_valid, error = rule.validate('active')
assert is_valid
print("✅ Enum validation (pass)")

is_valid, error = rule.validate('archived')
assert not is_valid
print("✅ Enum validation (fail)")

# Test 6: PropsSchema
print("\n=== Test 6: PropsSchema ===")
schema = validation.PropsSchema()
schema.add_rule('name', validation.ValidationType.REQUIRED)
schema.add_rule('age', validation.ValidationType.TYPE, int)

is_valid, errors = schema.validate({'name': 'John', 'age': 30})
assert is_valid and len(errors) == 0
print("✅ PropsSchema validation (pass)")

is_valid, errors = schema.validate({})
assert not is_valid and 'name' in errors
print("✅ PropsSchema validation (fail - missing required)")

is_valid, errors = schema.validate({'name': 'John', 'age': 'thirty'})
assert not is_valid and 'age' in errors
print("✅ PropsSchema validation (fail - wrong type)")

# Test 7: JSON Schema parsing
print("\n=== Test 7: JSON Schema Parsing ===")
schema_dict = {
    'required': ['title'],
    'properties': {
        'title': {'type': 'string'},
        'count': {
            'type': 'integer',
            'minimum': 0,
            'maximum': 100
        }
    }
}

schema = validation.PropsSchema(schema_dict)
is_valid, errors = schema.validate({'title': 'Test', 'count': 50})
assert is_valid
print("✅ JSON Schema parsing and validation (pass)")

is_valid, errors = schema.validate({})
assert not is_valid and 'title' in errors
print("✅ JSON Schema validation (fail - missing required)")

# Test 8: PropsValidator
print("\n=== Test 8: PropsValidator ===")
validator = validation.PropsValidator()

card_schema = validation.PropsSchema()
card_schema.add_rule('title', validation.ValidationType.REQUIRED)
card_schema.add_rule('subtitle', validation.ValidationType.TYPE, str)

validator.register_schema('card', card_schema)

is_valid, errors = validator.validate('card', {'title': 'Hello', 'subtitle': 'World'}, raise_on_error=False)
assert is_valid
print("✅ PropsValidator registration and validation (pass)")

is_valid, errors = validator.validate('card', {}, raise_on_error=False)
assert not is_valid and 'title' in errors
print("✅ PropsValidator validation (fail)")

# Test with no schema registered
is_valid, errors = validator.validate('unknown', {'any': 'props'}, raise_on_error=False)
assert is_valid
print("✅ PropsValidator allows validation without schema")

# Test 9: Custom validation
print("\n=== Test 9: Custom Validation ===")
def is_even(x):
    return x % 2 == 0

rule = validation.ValidationRule('number', validation.ValidationType.CUSTOM, is_even)
is_valid, error = rule.validate(4)
assert is_valid
print("✅ Custom validation (pass)")

is_valid, error = rule.validate(3)
assert not is_valid
print("✅ Custom validation (fail)")

# Test 10: Error messages
print("\n=== Test 10: Custom Error Messages ===")
rule = validation.ValidationRule(
    'age',
    validation.ValidationType.RANGE,
    (18, 65),
    error_message="Age must be between 18 and 65"
)
is_valid, error = rule.validate(70)
assert not is_valid
assert error == "Age must be between 18 and 65"
print("✅ Custom error messages work")

print("\n" + "=" * 60)
print("✅ ALL VALIDATION TESTS PASSED!")
print("=" * 60)
print("\nValidation system is fully functional:")
print("- ✅ 5 validation types (required, type, pattern, range, enum, custom)")
print("- ✅ PropsSchema with JSON Schema support")
print("- ✅ PropsValidator for component registration")
print("- ✅ Custom error messages")
print("- ✅ Integration ready for renderer")
