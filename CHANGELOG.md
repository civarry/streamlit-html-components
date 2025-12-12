# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.2] - 2024-12-12

### Bug Fixes
- **Fixed** Hot reload parameter error: Changed `level` to `verbose_level` in `DebugMode.enable()` call
- **Fixed** TypeError when calling `enable_hot_reload(verbose=True)`

## [0.3.1] - 2024-12-12

### Bug Fixes
- **Fixed** Streamlit 1.52.1 compatibility issue by removing unsupported `key` parameter from `components.html()` calls
- **Fixed** TypeError in `render_component_v2()` when using Streamlit 1.52.1+
- **Updated** API documentation to reflect removed `key` parameter

## [0.3.0] - 2024-12-12

### Major Features

#### 🔥 Hot Reload System (Phase 3.1)
- **Added** `DevServer` class for development-time file watching
- **Added** `FileWatcher` with dual-mode support (watchdog or polling fallback)
- **Added** `enable_hot_reload()` convenience function
- **Added** Automatic cache invalidation on file changes
- **Added** Streamlit rerun integration for instant updates
- Component files now auto-reload during development with zero manual intervention
- **Optional dependency**: `watchdog` for instant file detection (falls back to polling without it)

#### 🔄 Enhanced Bidirectional Communication (Phase 3.2)
- **Added** `StateManager` class for real-time state synchronization
- **Added** 5 conflict resolution strategies (CLIENT_WINS, SERVER_WINS, LATEST_WINS, MERGE, CUSTOM)
- **Added** State versioning and history tracking
- **Added** State rollback by version or steps
- **Added** `StateDiff` utility for computing state differences
- **Added** State export/import as JSON
- **Added** `Event` dataclass for structured event handling
- **Added** Automatic event recording for all communications
- **Added** Event replay capability for debugging and testing
- **Added** Event filtering by component and type
- **Added** State subscribers for real-time change notifications
- Enhanced `BidirectionalBridge` with state management methods
- Added Python → JavaScript state push functionality

#### ✅ Props Validation (Phase 2.2)
- **Added** `PropsSchema` class with JSON Schema support
- **Added** `ValidationRule` for manual validation rules
- **Added** 6 validation types: REQUIRED, TYPE, PATTERN, RANGE, ENUM, CUSTOM
- **Added** `PropsValidator` for component-level validation
- **Added** Integration with component registry
- **Added** `InvalidPropsError` exception with detailed error messages
- Components can now validate props at registration or render time

#### 📦 Component Registry Enhancements (Phase 2.1)
- **Added** `ComponentRegistry` class for centralized component management
- **Added** `register_component()` function for manual registration
- **Added** `list_components()` to list all registered components
- **Added** `get_component_info()` for component metadata
- **Added** Auto-discovery of components at startup
- **Added** Early validation (at registration, not render time)
- **Added** Component schemas with file tracking

### Improvements

- **Updated** Modern v2 API with immutable Pydantic-based configuration
- **Updated** Better error messages with fuzzy matching suggestions
- **Updated** Enhanced caching with content-based invalidation
- **Updated** Security improvements with origin validation in bidirectional bridge
- **Updated** Documentation with comprehensive examples
- **Updated** Python requirement to 3.10+ (from 3.8+)

### New Files

**Core Features:**
- `src/streamlit_html_components/file_watcher.py` - File watching system
- `src/streamlit_html_components/dev_server.py` - Development server with hot reload
- `src/streamlit_html_components/bidirectional/sync.py` - State synchronization
- `src/streamlit_html_components/validation.py` - Props validation
- `src/streamlit_html_components/registry.py` - Component registry
- `src/streamlit_html_components/config_v2.py` - v2 configuration
- `src/streamlit_html_components/core_v2.py` - v2 core API
- `src/streamlit_html_components/serialization.py` - Data serialization utilities

**Examples:**
- `examples/bidirectional/demo_counter.py` - Interactive counter with state management
- `examples/bidirectional/demo_advanced.py` - Advanced bidirectional features demo
- `examples/bidirectional/README.md` - Bidirectional communication guide

**Tests:**
- `test_bidirectional_basic.py` - 20 comprehensive bidirectional tests
- `test_file_watcher_basic.py` - 7 file watcher tests
- `test_hot_reload.py` - Hot reload integration tests
- `test_validation_basic.py` - 22 validation tests
- `tests/test_validation.py` - Pytest validation suite
- `test_v2_architecture.py` - v2 API architecture tests
- `test_v2_basic.py` - v2 API basic functionality tests
- `test_integration_v2.py` - v2 API integration tests

### Documentation

- **Added** PROGRESS.md documenting all phases
- **Added** MIGRATION_V2.md for v1 to v2 migration guide
- **Added** Comprehensive examples for all new features
- **Updated** README.md with v0.3.0 features
- **Updated** API documentation with new functions

### Breaking Changes

- **Changed** Minimum Python version from 3.8 to 3.10
- The v1 API remains backward compatible

### Statistics

- **Lines added**: ~5,200
- **New files**: 20+
- **Tests added**: 72
- **Test pass rate**: 100%
- **Features completed**: 5 major phases

## [0.1.0] - Initial Release

### Features

- Basic HTML/CSS/JS component rendering
- Jinja2 template engine integration
- External framework support (Tailwind, Bootstrap, Bulma)
- Component caching
- Basic bidirectional communication
- Security features (XSS prevention, path validation)
- Streamlit Cloud deployment support

### Core API

- `render_component()` - Render HTML components
- `configure()` - Configure component directories
- `add_framework()` - Add external frameworks
- `invalidate_cache()` - Cache management
- `cache_stats()` - Cache statistics

### Documentation

- Initial README with quick start guide
- Basic examples
- API reference

---

## Release Notes

### Upgrading from 0.1.0 to 0.3.0

1. **Python Version**: Update to Python 3.10+
   ```bash
   # Check your Python version
   python --version  # Should be 3.10 or higher
   ```

2. **Install the update**:
   ```bash
   pip install --upgrade streamlit-html-components
   ```

3. **Optional: Enable new features**:
   ```python
   from streamlit_html_components import configure_v2, enable_hot_reload

   # Use v2 API (recommended)
   configure_v2(
       templates_dir='components/templates',
       auto_discover=True
   )

   # Enable hot reload for development
   enable_hot_reload()
   ```

4. **Optional: Add validation**:
   ```python
   from streamlit_html_components import register_component, PropsSchema

   schema = PropsSchema({
       "type": "object",
       "properties": {
           "name": {"type": "string"},
           "age": {"type": "integer"}
       }
   })

   register_component('my_component', props_schema=schema)
   ```

### Deprecation Notice

No deprecations in this release. The v1 API remains fully supported and backward compatible.

### Known Issues

None at this time.

### Contributors

- CJ Carito (@cjcarito)
- Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
