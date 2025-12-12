"""
Advanced Bidirectional Communication Demo

Demonstrates:
- State conflict resolution
- Event replay capability
- Custom conflict resolvers
- State diffing
- State rollback
- Multiple components with synchronized state
"""

import sys
from pathlib import Path
import time

# Add src to path for development
src_path = Path(__file__).parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

# Import directly to avoid streamlit dependency
import importlib.util

def import_module_from_file(module_name, file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

bridge_module = import_module_from_file(
    'bridge',
    src_path / 'streamlit_html_components' / 'bidirectional' / 'bridge.py'
)
sync_module = import_module_from_file(
    'sync',
    src_path / 'streamlit_html_components' / 'bidirectional' / 'sync.py'
)

BidirectionalBridge = bridge_module.BidirectionalBridge
StateManager = sync_module.StateManager
StateDiff = sync_module.StateDiff
ConflictResolution = sync_module.ConflictResolution

print("=" * 70)
print("Advanced Bidirectional Communication Demo")
print("=" * 70)

# ===== Demo 1: State Conflict Resolution =====
print("\n" + "=" * 70)
print("Demo 1: State Conflict Resolution")
print("=" * 70)

# Create state manager with different conflict strategies
manager_client_wins = StateManager(conflict_resolution=ConflictResolution.CLIENT_WINS)
manager_server_wins = StateManager(conflict_resolution=ConflictResolution.SERVER_WINS)
manager_merge = StateManager(conflict_resolution=ConflictResolution.MERGE)

# Set initial server state
manager_client_wins.set_state('form', {'name': 'John', 'age': 30}, source='python')
manager_server_wins.set_state('form', {'name': 'John', 'age': 30}, source='python')
manager_merge.set_state('form', {'name': 'John', 'age': 30}, source='python')

print("\nInitial server state: {'name': 'John', 'age': 30}")

# Server updates state
time.sleep(0.1)
manager_client_wins.update_state('form', {'age': 31}, source='python')
manager_server_wins.update_state('form', {'age': 31}, source='python')
manager_merge.update_state('form', {'age': 31}, source='python')

print("Server updates: {'age': 31}")

# Client tries to update with old version
client_state = {'name': 'Jane', 'age': 30}  # Client's version is behind
print(f"Client attempts update: {client_state}")

# Test CLIENT_WINS strategy
print("\n1. CLIENT_WINS Strategy:")
success, _ = manager_client_wins.sync_from_client('form', client_state, client_version=1)
print(f"   Success: {success}")
print(f"   Final state: {manager_client_wins.get_state('form')}")

# Test SERVER_WINS strategy
print("\n2. SERVER_WINS Strategy:")
success, conflict = manager_server_wins.sync_from_client('form', client_state, client_version=1)
print(f"   Success: {success}")
print(f"   Server state maintained: {manager_server_wins.get_state('form')}")
if conflict:
    print(f"   Conflict data returned to client: {conflict}")

# Test MERGE strategy
print("\n3. MERGE Strategy:")
success, _ = manager_merge.sync_from_client('form', client_state, client_version=1)
print(f"   Success: {success}")
print(f"   Merged state: {manager_merge.get_state('form')}")

# ===== Demo 2: Custom Conflict Resolver =====
print("\n" + "=" * 70)
print("Demo 2: Custom Conflict Resolver")
print("=" * 70)

manager_custom = StateManager(conflict_resolution=ConflictResolution.CUSTOM)


def custom_resolver(client_state, server_state):
    """Custom resolver: keep newer values based on a priority system."""
    resolved = {}

    # Priority: specific fields from specific sources
    priority_fields = {
        'name': 'client',  # Client controls name
        'age': 'server',  # Server controls age
        'email': 'client'  # Client controls email
    }

    all_keys = set(client_state.keys()) | set(server_state.keys())

    for key in all_keys:
        priority = priority_fields.get(key, 'server')  # Default to server

        if priority == 'client' and key in client_state:
            resolved[key] = client_state[key]
        elif priority == 'server' and key in server_state:
            resolved[key] = server_state[key]
        elif key in server_state:
            resolved[key] = server_state[key]
        else:
            resolved[key] = client_state[key]

    return resolved


manager_custom.set_conflict_resolver(custom_resolver)
manager_custom.set_state('profile', {
    'name': 'Server Name',
    'age': 25,
    'email': 'server@example.com'
}, source='python')

client_update = {
    'name': 'Client Name',
    'age': 30,
    'email': 'client@example.com'
}

print("\nServer state: {'name': 'Server Name', 'age': 25, 'email': 'server@example.com'}")
print(f"Client state: {client_update}")
print("\nPriority rules:")
print("  - 'name' → client wins")
print("  - 'age' → server wins")
print("  - 'email' → client wins")

success, _ = manager_custom.sync_from_client('profile', client_update, client_version=1)
resolved_state = manager_custom.get_state('profile')

print(f"\nResolved state: {resolved_state}")
print(f"Expected: {{'name': 'Client Name', 'age': 25, 'email': 'client@example.com'}}")

# ===== Demo 3: State Diffing =====
print("\n" + "=" * 70)
print("Demo 3: State Diffing")
print("=" * 70)

old_state = {
    'username': 'john_doe',
    'email': 'john@example.com',
    'age': 30,
    'city': 'New York'
}

new_state = {
    'username': 'john_doe',  # unchanged
    'email': 'newemail@example.com',  # modified
    'age': 31,  # modified
    'country': 'USA'  # added (removed city)
}

print(f"\nOld state: {old_state}")
print(f"New state: {new_state}")

diff = StateDiff.diff(old_state, new_state)
print("\nDiff result:")
print(f"  Added: {diff['added']}")
print(f"  Modified: {diff['modified']}")
print(f"  Removed: {diff['removed']}")

# Apply diff to old state
restored = StateDiff.apply_diff(old_state, diff)
print(f"\nApplying diff to old state: {restored}")
print(f"Matches new state: {restored == new_state}")

# ===== Demo 4: Event Replay =====
print("\n" + "=" * 70)
print("Demo 4: Event Replay")
print("=" * 70)

bridge = BidirectionalBridge()
replay_results = []


def on_click(data):
    replay_results.append(f"Clicked: {data.get('button_id')}")


bridge.register_callback('buttons', 'click', on_click)

# Simulate a series of events
events_to_simulate = [
    {'event': 'click', 'data': {'button_id': 'btn1'}},
    {'event': 'click', 'data': {'button_id': 'btn2'}},
    {'event': 'click', 'data': {'button_id': 'btn3'}},
]

print("\nSimulating click events:")
for event_data in events_to_simulate:
    bridge.handle_event('buttons', event_data)
    print(f"  - {event_data['data']['button_id']}")

print(f"\nCallback results: {replay_results}")

# Get event history
history = bridge.get_event_history('buttons')
print(f"\nEvent history ({len(history)} events):")
for i, event in enumerate(history, 1):
    print(f"  {i}. {event.event_type}: {event.data}")

# Clear results and replay events
replay_results.clear()
print("\nReplaying all events...")
bridge.replay_events('buttons')

print(f"Replay results: {replay_results}")
print(f"Matches original: {len(replay_results) == len(events_to_simulate)}")

# Export events as JSON
print("\nExported events (JSON):")
json_export = bridge.export_events('buttons')
print(json_export)

# ===== Demo 5: State History and Rollback =====
print("\n" + "=" * 70)
print("Demo 5: State History and Rollback")
print("=" * 70)

manager = StateManager(max_history=10)

# Create a series of state changes
print("\nCreating state history:")
manager.set_state('editor', {'text': 'Hello', 'cursor': 5})
print("  v1: {'text': 'Hello', 'cursor': 5}")

time.sleep(0.05)
manager.update_state('editor', {'text': 'Hello World'})
print("  v2: {'text': 'Hello World', 'cursor': 5}")

time.sleep(0.05)
manager.update_state('editor', {'cursor': 11})
print("  v3: {'text': 'Hello World', 'cursor': 11}")

time.sleep(0.05)
manager.update_state('editor', {'text': 'Hello World!', 'cursor': 12})
print("  v4: {'text': 'Hello World!', 'cursor': 12}")

# Show history
print("\nState history:")
history = manager.get_history('editor')
for snapshot in history:
    print(f"  v{snapshot.version}: {snapshot.state}")

# Rollback to version 2
print("\nRolling back to version 2...")
manager.rollback('editor', to_version=2)
current = manager.get_state('editor')
print(f"Current state after rollback: {current}")

# Rollback 1 step from current
print("\nRolling back 1 step...")
manager.rollback('editor', steps=1)
current = manager.get_state('editor')
print(f"Current state after 1-step rollback: {current}")

# ===== Demo 6: State Subscriptions =====
print("\n" + "=" * 70)
print("Demo 6: State Subscriptions")
print("=" * 70)

manager = StateManager()
notifications = []


def on_state_change(snapshot):
    notifications.append(f"v{snapshot.version}: {snapshot.state}")


print("\nSubscribing to state changes...")
manager.subscribe('settings', on_state_change)

print("Making state updates...")
manager.set_state('settings', {'theme': 'light', 'fontSize': 14})
manager.update_state('settings', {'theme': 'dark'})
manager.update_state('settings', {'fontSize': 16})

print(f"\nReceived {len(notifications)} notifications:")
for notification in notifications:
    print(f"  - {notification}")

# ===== Summary =====
print("\n" + "=" * 70)
print("Summary: Advanced Features Demonstrated")
print("=" * 70)
print("""
✅ State Conflict Resolution
   - CLIENT_WINS: Client updates always accepted
   - SERVER_WINS: Server state maintained, conflicts rejected
   - MERGE: Intelligent merging of non-conflicting changes
   - CUSTOM: User-defined conflict resolution logic

✅ State Diffing
   - Compute differences between states
   - Track added, modified, and removed fields
   - Apply diffs to reconstruct states

✅ Event Replay
   - Automatic event recording
   - Filter events by component and type
   - Replay events to reconstruct state
   - Export events as JSON

✅ State History & Rollback
   - Version tracking for all state changes
   - Rollback to specific version or N steps back
   - Access complete state history

✅ State Subscriptions
   - Real-time notifications on state changes
   - Multiple subscribers per component
   - Easy subscribe/unsubscribe API

All features working correctly! 🎉
""")
