# Bidirectional Communication Examples

This directory contains examples demonstrating the bidirectional communication features of streamlit-html-components.

## Examples

### 1. Counter Demo (`demo_counter.py`)

A complete interactive counter component showcasing:

- **JavaScript → Python Events**: Button clicks send events to Python
- **Python → JavaScript State**: Python updates are reflected in the UI
- **Real-time State Sync**: Changes are synchronized instantly
- **Event Recording**: All interactions are logged
- **State History**: Track all state changes over time

**Features Demonstrated:**
- Event callbacks (`on_increment`, `on_decrement`, `on_reset`)
- State management with `StateManager`
- Bridge script injection
- State subscribers
- Event history tracking

**Run it:**
```bash
python examples/bidirectional/demo_counter.py
```

**What to Expect:**
- Simulates user clicking increment/decrement buttons
- Shows event and state history
- Demonstrates state export to JSON
- Validates bidirectional communication flow

### 2. Advanced Demo (`demo_advanced.py`)

Advanced features including:

- **Conflict Resolution Strategies**
  - `CLIENT_WINS`: Client updates always accepted
  - `SERVER_WINS`: Server state maintained
  - `MERGE`: Intelligent merging
  - `CUSTOM`: User-defined resolution logic

- **State Diffing**
  - Compute differences between states
  - Track added/modified/removed fields
  - Apply diffs to reconstruct states

- **Event Replay**
  - Record all events automatically
  - Filter by component or event type
  - Replay events to reconstruct state
  - Export events as JSON

- **State History & Rollback**
  - Version tracking
  - Rollback to specific version
  - Access complete history

- **State Subscriptions**
  - Real-time change notifications
  - Multiple subscribers
  - Easy subscribe/unsubscribe

**Run it:**
```bash
python examples/bidirectional/demo_advanced.py
```

**What to Expect:**
- 6 comprehensive demos showing advanced features
- Detailed output explaining each feature
- Validation of conflict resolution strategies
- Examples of state diffing and replay

## Key Concepts

### BidirectionalBridge

Manages communication between JavaScript and Python:

```python
from streamlit_html_components.bidirectional import BidirectionalBridge

bridge = BidirectionalBridge()

# Register Python callback for JavaScript events
def on_click(data):
    print(f"Clicked: {data}")

bridge.register_callback('my_component', 'click', on_click)

# Inject bridge script into HTML
html_with_bridge = bridge.wrap_with_bridge(html_content, 'my_component')
```

### StateManager

Manages component state with versioning and conflict resolution:

```python
from streamlit_html_components.bidirectional import StateManager, ConflictResolution

manager = StateManager(
    conflict_resolution=ConflictResolution.LATEST_WINS,
    max_history=100
)

# Set state
manager.set_state('my_component', {'count': 0})

# Update state
manager.update_state('my_component', {'count': 1})

# Subscribe to changes
def on_change(snapshot):
    print(f"State changed: {snapshot.state}")

manager.subscribe('my_component', on_change)
```

### Event Recording

All events are automatically recorded for replay:

```python
# Events are recorded automatically when handle_event is called
bridge.handle_event('my_component', {
    'event': 'click',
    'data': {'button': 'submit'}
})

# Get event history
events = bridge.get_event_history('my_component')

# Replay events
bridge.replay_events('my_component')

# Export as JSON
json_data = bridge.export_events('my_component')
```

### State Diffing

Compare and apply state changes:

```python
from streamlit_html_components.bidirectional import StateDiff

old_state = {'name': 'John', 'age': 30}
new_state = {'name': 'Jane', 'age': 30}

# Compute diff
diff = StateDiff.diff(old_state, new_state)
# Result: {'added': {}, 'modified': {'name': {...}}, 'removed': {}}

# Apply diff
result = StateDiff.apply_diff(old_state, diff)
# Result: {'name': 'Jane', 'age': 30}
```

## Integration with Streamlit

In a real Streamlit app, you would use these components like this:

```python
import streamlit as st
from streamlit_html_components import render_component_v2
from streamlit_html_components.bidirectional import get_bridge, StateManager

# Initialize
bridge = get_bridge()
state_manager = StateManager()

# Set initial state
state_manager.set_state('my_component', {'value': 0})

# Register callbacks
def on_change(data):
    new_value = data.get('value')
    state_manager.update_state('my_component', {'value': new_value})
    st.rerun()  # Trigger Streamlit rerun

bridge.register_callback('my_component', 'change', on_change)

# Render component
result = render_component_v2(
    'my_component',
    props=state_manager.get_state('my_component')
)

# Handle events
if result:
    bridge.handle_event('my_component', result)
```

## Architecture

```
┌─────────────┐         Events          ┌─────────────┐
│             │ ───────────────────────> │             │
│  JavaScript │                          │   Python    │
│  (Browser)  │ <─────────────────────── │  (Backend)  │
│             │         State            │             │
└─────────────┘                          └─────────────┘
      │                                        │
      │                                        │
      v                                        v
┌─────────────┐                          ┌─────────────┐
│   Bridge    │                          │    State    │
│   Script    │                          │   Manager   │
└─────────────┘                          └─────────────┘
      │                                        │
      v                                        v
┌─────────────┐                          ┌─────────────┐
│    Event    │                          │   History   │
│  Recording  │                          │  Rollback   │
└─────────────┘                          └─────────────┘
```

## Tips

1. **Always use state management** for components with interactive state
2. **Choose the right conflict resolution** strategy for your use case
3. **Subscribe to state changes** to react to updates
4. **Use event replay** for debugging and testing
5. **Export state/events** for persistence and analytics

## Next Steps

- Try running the demos
- Modify the counter to add new features
- Experiment with different conflict resolution strategies
- Build your own bidirectional component
- Integrate with a real Streamlit application

## Troubleshooting

**Events not received in Python:**
- Check that bridge script is injected
- Verify callback is registered
- Check browser console for errors

**State not updating in JavaScript:**
- Ensure `window.onStreamlitData` is defined
- Check that state is being set in Python
- Verify component name matches

**Conflicts not resolving:**
- Check conflict resolution strategy
- Verify version numbers are tracked
- Consider using custom resolver for complex cases
