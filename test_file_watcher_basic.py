"""
Basic file watcher test without external dependencies.

Tests core FileWatcher functionality in polling mode.
"""

import sys
from pathlib import Path
import tempfile
import time
import importlib.util

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Manually import modules
def import_module_from_file(module_name, file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Set up package structure
pkg_path = src_path / 'streamlit_html_components'
sys.modules['streamlit_html_components'] = type(sys)('streamlit_html_components')
sys.modules['streamlit_html_components'].__path__ = [str(pkg_path)]

# Import diagnostics first (file_watcher depends on it)
diagnostics = import_module_from_file(
    'streamlit_html_components.diagnostics',
    pkg_path / 'diagnostics.py'
)
file_watcher = import_module_from_file(
    'streamlit_html_components.file_watcher',
    pkg_path / 'file_watcher.py'
)

print("=" * 60)
print("FileWatcher Basic Tests")
print("=" * 60)

# Test 1: FileWatcher detects file modifications
print("\n=== Test 1: Detect File Modifications ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)
    test_file = tmp_path / 'test.html'
    test_file.write_text('<div>Original</div>')

    changes_detected = []

    def on_change(event):
        changes_detected.append(event)
        print(f"   Change detected: {event.event_type} - {event.path.name}")

    # Create watcher in polling mode
    watcher = file_watcher.FileWatcher(poll_interval=0.1, use_watchdog=False)
    watcher.watch(tmp_path, '*.html', on_change)
    watcher.start()

    # Wait for watcher to initialize
    time.sleep(0.2)

    # Modify file
    test_file.write_text('<div>Modified</div>')

    # Wait for change to be detected
    time.sleep(0.3)

    watcher.stop()

    assert len(changes_detected) > 0, "No changes detected"
    assert changes_detected[-1].event_type == 'modified'
    assert changes_detected[-1].path == test_file
    print(f"✅ Detected {len(changes_detected)} modification(s)")

# Test 2: FileWatcher detects new files
print("\n=== Test 2: Detect New Files ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    changes_detected = []

    def on_change(event):
        changes_detected.append(event)
        print(f"   Change detected: {event.event_type} - {event.path.name}")

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
    assert changes_detected[0].path == new_file
    print(f"✅ Detected new file creation")

# Test 3: FileWatcher with multiple files
print("\n=== Test 3: Watch Multiple Files ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    # Create initial files
    file1 = tmp_path / 'component1.js'
    file2 = tmp_path / 'component2.js'
    file1.write_text('console.log("1");')
    file2.write_text('console.log("2");')

    changes_detected = []

    def on_change(event):
        changes_detected.append(event)
        print(f"   Change detected: {event.path.name}")

    watcher = file_watcher.FileWatcher(poll_interval=0.1, use_watchdog=False)
    watcher.watch(tmp_path, '*.js', on_change)
    watcher.start()

    time.sleep(0.2)

    # Modify both files
    file1.write_text('console.log("1 modified");')
    time.sleep(0.15)
    file2.write_text('console.log("2 modified");')

    time.sleep(0.3)

    watcher.stop()

    assert len(changes_detected) >= 2, f"Expected 2+ changes, got {len(changes_detected)}"
    print(f"✅ Detected changes to {len(changes_detected)} file(s)")

# Test 4: FileChangeEvent
print("\n=== Test 4: FileChangeEvent ===")
event = file_watcher.FileChangeEvent(
    path=Path('test.html'),
    event_type='modified'
)
assert event.event_type == 'modified'
assert event.path == Path('test.html')
assert event.timestamp is not None

event_str = str(event)
assert 'MODIFIED' in event_str
assert 'test.html' in event_str
print("✅ FileChangeEvent works correctly")
print(f"   {event}")

# Test 5: FileWatcher start/stop
print("\n=== Test 5: FileWatcher Start/Stop ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    watcher = file_watcher.FileWatcher(poll_interval=0.1, use_watchdog=False)
    watcher.watch(tmp_path, '*.txt', lambda e: None)

    assert not watcher.is_running()
    print("✅ Watcher initially stopped")

    watcher.start()
    assert watcher.is_running()
    print("✅ Watcher started")

    watcher.stop()
    assert not watcher.is_running()
    print("✅ Watcher stopped")

# Test 6: Context manager
print("\n=== Test 6: Context Manager ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    changes = []

    with file_watcher.FileWatcher(poll_interval=0.1, use_watchdog=False) as watcher:
        watcher.watch(tmp_path, '*.md', lambda e: changes.append(e))
        assert watcher.is_running()
        print("✅ Watcher started via context manager")

        # Create file while watching
        test_file = tmp_path / 'README.md'
        time.sleep(0.2)
        test_file.write_text('# Test')
        time.sleep(0.3)

    assert not watcher.is_running()
    print("✅ Watcher stopped automatically")

    if len(changes) > 0:
        print(f"   Detected {len(changes)} change(s) during context")

# Test 7: Pattern matching
print("\n=== Test 7: Pattern Matching ===")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    html_changes = []
    css_changes = []

    watcher = file_watcher.FileWatcher(poll_interval=0.1, use_watchdog=False)
    watcher.watch(tmp_path, '*.html', lambda e: html_changes.append(e))
    watcher.watch(tmp_path, '*.css', lambda e: css_changes.append(e))
    watcher.start()

    time.sleep(0.2)

    # Create different file types
    (tmp_path / 'page.html').write_text('<div></div>')
    (tmp_path / 'style.css').write_text('.btn {}')
    (tmp_path / 'script.js').write_text('console.log("ignored");')

    time.sleep(0.3)

    watcher.stop()

    assert len(html_changes) > 0, "HTML changes not detected"
    assert len(css_changes) > 0, "CSS changes not detected"
    assert html_changes[0].path.name == 'page.html'
    assert css_changes[0].path.name == 'style.css'
    print("✅ Pattern matching works correctly")
    print(f"   HTML files: {len(html_changes)}")
    print(f"   CSS files: {len(css_changes)}")

print("\n" + "=" * 60)
print("✅ ALL FILEWATCHER TESTS PASSED!")
print("=" * 60)
print("\nFileWatcher is fully functional:")
print("- ✅ Detects file modifications")
print("- ✅ Detects new file creation")
print("- ✅ Watches multiple files")
print("- ✅ Pattern matching (*.html, *.css, *.js)")
print("- ✅ Start/stop control")
print("- ✅ Context manager support")
print("- ✅ FileChangeEvent with timestamps")
print("\nPolling mode tested successfully!")
print("Note: watchdog library support also available (install with: pip install watchdog)")
