"""
Test hot reload functionality without Streamlit dependency.

Tests:
- FileWatcher detects file changes
- DevServer invalidates cache on changes
- File watching works in both watchdog and polling modes
"""

import sys
from pathlib import Path
import tempfile
import time
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
diagnostics = import_module_from_file(
    'streamlit_html_components.diagnostics',
    pkg_path / 'diagnostics.py'
)
file_watcher = import_module_from_file(
    'streamlit_html_components.file_watcher',
    pkg_path / 'file_watcher.py'
)
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
cache_manager = import_module_from_file(
    'streamlit_html_components.cache_manager',
    pkg_path / 'cache_manager.py'
)
dev_server = import_module_from_file(
    'streamlit_html_components.dev_server',
    pkg_path / 'dev_server.py'
)

print("=" * 60)
print("Hot Reload Functionality Tests")
print("=" * 60)

# Test 1: FileWatcher with polling
print("\n=== Test 1: FileWatcher (Polling Mode) ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)
    test_file = tmp_path / 'test.html'
    test_file.write_text('<div>Original</div>')

    changes_detected = []

    def on_change(event):
        changes_detected.append(event)

    # Create watcher in polling mode (don't use watchdog)
    watcher = file_watcher.FileWatcher(poll_interval=0.1, use_watchdog=False)
    watcher.watch(tmp_path, '*.html', on_change)
    watcher.start()

    # Modify file
    time.sleep(0.2)  # Let watcher start
    test_file.write_text('<div>Modified</div>')
    time.sleep(0.3)  # Wait for polling to detect change

    watcher.stop()

    assert len(changes_detected) > 0, "No changes detected"
    assert changes_detected[-1].event_type == 'modified'
    print(f"✅ FileWatcher detected {len(changes_detected)} change(s)")
    print(f"   Last event: {changes_detected[-1]}")

# Test 2: FileWatcher detects new files
print("\n=== Test 2: FileWatcher Detects New Files ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    changes_detected = []

    def on_change(event):
        changes_detected.append(event)

    watcher = file_watcher.FileWatcher(poll_interval=0.1, use_watchdog=False)
    watcher.watch(tmp_path, '*.css', on_change)
    watcher.start()

    time.sleep(0.2)

    # Create new file
    new_file = tmp_path / 'style.css'
    new_file.write_text('.btn { color: blue; }')
    time.sleep(0.3)

    watcher.stop()

    assert len(changes_detected) > 0, "No changes detected for new file"
    assert changes_detected[0].event_type == 'created'
    print(f"✅ FileWatcher detected new file creation")
    print(f"   Event: {changes_detected[0]}")

# Test 3: FileChangeEvent
print("\n=== Test 3: FileChangeEvent ===")
event = file_watcher.FileChangeEvent(
    path=Path('test.html'),
    event_type='modified'
)
assert event.event_type == 'modified'
assert event.path == Path('test.html')
assert event.timestamp is not None
print("✅ FileChangeEvent created successfully")
print(f"   {event}")

# Test 4: DevServer cache invalidation
print("\n=== Test 4: DevServer Cache Invalidation ===")
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

    # Create config
    config = config_v2.ComponentConfig(
        templates_dir=templates_dir,
        styles_dir=styles_dir,
        scripts_dir=scripts_dir
    )

    # Create cache manager
    cache = cache_manager.CacheManager()

    # Add something to cache
    cache.set_cached('test_key', '<div>cached</div>', component_name='button')
    assert cache.get_cached('test_key') is not None
    print("✅ Cache populated")

    # Create dev server
    dev = dev_server.DevServer(config, cache, poll_interval=0.1)
    dev.start()

    time.sleep(0.2)

    # Modify template - should invalidate cache
    (templates_dir / 'button.html').write_text('<button>Modified {{ text }}</button>')
    time.sleep(0.3)

    dev.stop()

    # Cache should be invalidated for 'button' component
    cached = cache.get_cached('test_key')
    assert cached is None, "Cache was not invalidated"
    print("✅ DevServer invalidated cache on file change")

# Test 5: DevServer with multiple file types
print("\n=== Test 5: DevServer Watches Multiple File Types ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    templates_dir = tmp_path / 'templates'
    styles_dir = tmp_path / 'styles'
    scripts_dir = tmp_path / 'scripts'

    for d in [templates_dir, styles_dir, scripts_dir]:
        d.mkdir()

    (templates_dir / 'card.html').write_text('<div>Card</div>')
    (styles_dir / 'card.css').write_text('.card {}')
    (scripts_dir / 'card.js').write_text('console.log("card");')

    config = config_v2.ComponentConfig(
        templates_dir=templates_dir,
        styles_dir=styles_dir,
        scripts_dir=scripts_dir
    )

    cache = cache_manager.CacheManager()
    dev = dev_server.DevServer(config, cache, poll_interval=0.1)

    # Check that watches are set up
    assert dev.watcher is not None
    assert len(dev.watcher._watches) == 3  # templates, styles, scripts
    print("✅ DevServer watching 3 directories")
    print(f"   Templates: {templates_dir}")
    print(f"   Styles: {styles_dir}")
    print(f"   Scripts: {scripts_dir}")

# Test 6: Context manager usage
print("\n=== Test 6: DevServer Context Manager ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    templates_dir = tmp_path / 'templates'
    styles_dir = tmp_path / 'styles'
    scripts_dir = tmp_path / 'scripts'

    for d in [templates_dir, styles_dir, scripts_dir]:
        d.mkdir()

    config = config_v2.ComponentConfig(
        templates_dir=templates_dir,
        styles_dir=styles_dir,
        scripts_dir=scripts_dir
    )

    cache = cache_manager.CacheManager()

    with dev_server.DevServer(config, cache) as dev:
        assert dev.is_running()
        print("✅ DevServer started via context manager")

    assert not dev.is_running()
    print("✅ DevServer stopped automatically")

# Test 7: FileWatcher context manager
print("\n=== Test 7: FileWatcher Context Manager ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    changes = []

    with file_watcher.FileWatcher(poll_interval=0.1, use_watchdog=False) as watcher:
        watcher.watch(tmp_path, '*.txt', lambda e: changes.append(e))
        assert watcher.is_running()
        print("✅ FileWatcher started via context manager")

    assert not watcher.is_running()
    print("✅ FileWatcher stopped automatically")

print("\n" + "=" * 60)
print("✅ ALL HOT RELOAD TESTS PASSED!")
print("=" * 60)
print("\nHot reload system is fully functional:")
print("- ✅ FileWatcher detects file changes (polling mode)")
print("- ✅ FileWatcher detects new files")
print("- ✅ DevServer invalidates cache on changes")
print("- ✅ DevServer watches multiple file types")
print("- ✅ Context manager support")
print("- ✅ Integration with cache manager")
print("\nNote: Watchdog library not tested (optional dependency)")
print("      Install with: pip install watchdog")
