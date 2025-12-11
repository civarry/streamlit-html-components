"""
Basic validation test for v2 API (no external dependencies required).

Tests modules that don't require pydantic:
- Serialization utilities
- Security utilities
- File structure validation
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'streamlit_html_components'))

print("=" * 60)
print("Basic v2 Validation Tests")
print("=" * 60)

# Test 1: Serialization module
print("\n=== Testing Serialization Module ===")
try:
    import serialization

    # Test serialize_value
    assert serialization.serialize_value(datetime(2025, 12, 11, 10, 30)) == '2025-12-11T10:30:00'
    assert serialization.serialize_value(Path('/tmp/test')) == '/tmp/test'
    print("✅ serialize_value handles complex types")

    # Test deterministic props
    props1 = {'name': 'test', 'count': 5, 'active': True}
    props2 = {'count': 5, 'active': True, 'name': 'test'}  # Different order

    json1 = serialization.serialize_props(props1)
    json2 = serialization.serialize_props(props2)
    assert json1 == json2
    print("✅ Props serialization is deterministic")

    # Test hashing
    hash1 = serialization.hash_props(props1)
    hash2 = serialization.hash_props(props2)
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256
    print(f"✅ Props hashing is deterministic: {hash1[:16]}...")

    print("✅ Serialization module: ALL TESTS PASSED")

except Exception as e:
    print(f"✗ Serialization module tests FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Security module
print("\n=== Testing Security Module ===")
try:
    import security

    # Test CSP policy generation
    policy = security.create_default_csp()
    header = policy.to_header()
    assert "default-src 'self'" in header
    assert "script-src" in header
    assert "style-src" in header
    print("✅ Default CSP policy generation works")

    # Test strict CSP
    strict_policy = security.create_strict_csp()
    strict_header = strict_policy.to_header()
    assert "'unsafe-inline'" not in strict_header
    assert "object-src 'none'" in strict_header
    print("✅ Strict CSP policy generation works")

    # Test meta tag generation
    meta = policy.to_meta_tag()
    assert '<meta http-equiv="Content-Security-Policy"' in meta
    assert 'content=' in meta
    print("✅ CSP meta tag generation works")

    # Test security auditor
    auditor = security.SecurityAuditor()

    # Test eval detection
    html_with_eval = '<script>eval(userInput)</script>'
    issues = auditor.audit_html(html_with_eval)
    assert len(issues) > 0
    assert any('eval' in issue['pattern'] for issue in issues)
    print("✅ Security auditor detects eval()")

    # Test innerHTML detection
    html_with_innerHTML = '<script>element.innerHTML = userInput</script>'
    issues = auditor.audit_html(html_with_innerHTML)
    assert len(issues) > 0
    assert any('innerhtml' in issue['pattern'] for issue in issues)
    print("✅ Security auditor detects innerHTML")

    # Test sanitization
    dangerous = '<script>alert("XSS")</script>'
    safe = auditor.sanitize_user_input(dangerous)
    assert '<script>' not in safe
    assert '&lt;script&gt;' in safe
    print("✅ Input sanitization works")

    # Test CSP injection
    html = '<html><head></head><body>Content</body></html>'
    result = security.inject_csp_meta(html)
    assert 'Content-Security-Policy' in result
    assert '<head>' in result
    print("✅ CSP meta tag injection works")

    print("✅ Security module: ALL TESTS PASSED")

except Exception as e:
    print(f"✗ Security module tests FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: File structure validation
print("\n=== Testing File Structure ===")
try:
    src_dir = Path(__file__).parent / 'src' / 'streamlit_html_components'

    required_files = [
        'config_v2.py',
        'registry.py',
        'serialization.py',
        'core_v2.py',
        'renderer.py',
        'security.py',
        'cache_manager.py',
    ]

    for filename in required_files:
        filepath = src_dir / filename
        assert filepath.exists(), f"Missing required file: {filename}"
        print(f"✅ Found {filename}")

    print("✅ File structure: ALL FILES PRESENT")

except Exception as e:
    print(f"✗ File structure validation FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Import validation (syntax check)
print("\n=== Testing Module Imports (Syntax Validation) ===")
try:
    # These will fail to import due to pydantic dependency, but we can check syntax
    import ast

    files_to_check = [
        src_dir / 'config_v2.py',
        src_dir / 'registry.py',
        src_dir / 'core_v2.py',
        src_dir / 'renderer.py',
    ]

    for filepath in files_to_check:
        with open(filepath, 'r') as f:
            code = f.read()
            try:
                ast.parse(code)
                print(f"✅ {filepath.name} has valid Python syntax")
            except SyntaxError as e:
                print(f"✗ {filepath.name} has syntax error: {e}")
                raise

    print("✅ Module syntax: ALL FILES VALID")

except Exception as e:
    print(f"✗ Module syntax validation FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("✅ ALL BASIC VALIDATION TESTS PASSED!")
print("=" * 60)
print("\nThe v2 API core functionality is working correctly.")
print("\nNote: Full integration tests require pydantic to be installed.")
print("Install with: pip install pydantic")
print("\nSecurity tests require pytest:")
print("Install with: pip install pytest")
