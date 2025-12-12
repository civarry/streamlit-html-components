"""
Bidirectional Counter Demo

Demonstrates:
- State synchronization between Python and JavaScript
- Event handling (button clicks)
- Python → JavaScript state updates
- JavaScript → Python event communication
- Real-time state management
"""

import sys
from pathlib import Path

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
ConflictResolution = sync_module.ConflictResolution

# Initialize bridge and state manager
bridge = BidirectionalBridge()
state_manager = StateManager(conflict_resolution=ConflictResolution.LATEST_WINS)

# Set initial state
state_manager.set_state('counter', {'count': 0, 'step': 1})


def on_increment(data):
    """Handle increment button click."""
    print(f"[Python] Increment clicked with data: {data}")

    # Get current state
    current_state = state_manager.get_state('counter')
    count = current_state.get('count', 0)
    step = current_state.get('step', 1)

    # Update state
    new_count = count + step
    state_manager.update_state('counter', {'count': new_count})

    print(f"[Python] Counter updated: {count} -> {new_count}")


def on_decrement(data):
    """Handle decrement button click."""
    print(f"[Python] Decrement clicked with data: {data}")

    # Get current state
    current_state = state_manager.get_state('counter')
    count = current_state.get('count', 0)
    step = current_state.get('step', 1)

    # Update state
    new_count = count - step
    state_manager.update_state('counter', {'count': new_count})

    print(f"[Python] Counter updated: {count} -> {new_count}")


def on_reset(data):
    """Handle reset button click."""
    print(f"[Python] Reset clicked")

    # Reset counter to 0
    state_manager.update_state('counter', {'count': 0})

    print(f"[Python] Counter reset to 0")


def on_step_change(data):
    """Handle step value change."""
    new_step = data.get('step', 1)
    print(f"[Python] Step changed to: {new_step}")

    # Update step in state
    state_manager.update_state('counter', {'step': new_step})


# Register event callbacks
bridge.register_callback('counter', 'increment', on_increment)
bridge.register_callback('counter', 'decrement', on_decrement)
bridge.register_callback('counter', 'reset', on_reset)
bridge.register_callback('counter', 'step_change', on_step_change)


# Subscribe to state changes
def on_state_change(snapshot):
    """Called whenever counter state changes."""
    print(f"[Python] State changed (v{snapshot.version}): {snapshot.state}")


state_manager.subscribe('counter', on_state_change)


# Create HTML component
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Counter Demo</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 500px;
            margin: 40px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .counter-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        h1 {
            text-align: center;
            color: #333;
            margin: 0 0 30px 0;
        }

        .count-display {
            text-align: center;
            font-size: 72px;
            font-weight: bold;
            color: #667eea;
            margin: 30px 0;
            padding: 20px;
            background: #f7fafc;
            border-radius: 10px;
        }

        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin: 20px 0;
        }

        button {
            padding: 15px 20px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            color: white;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        button:active {
            transform: translateY(0);
        }

        .btn-increment {
            background: #48bb78;
        }

        .btn-decrement {
            background: #f56565;
        }

        .btn-reset {
            background: #4299e1;
            grid-column: span 3;
        }

        .step-control {
            margin: 20px 0;
            padding: 20px;
            background: #f7fafc;
            border-radius: 10px;
        }

        .step-control label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #4a5568;
        }

        .step-control input {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            box-sizing: border-box;
        }

        .step-control input:focus {
            outline: none;
            border-color: #667eea;
        }

        .info {
            margin-top: 20px;
            padding: 15px;
            background: #edf2f7;
            border-radius: 8px;
            font-size: 14px;
            color: #4a5568;
        }
    </style>
</head>
<body>
    <div class="counter-card">
        <h1>🔄 Bidirectional Counter</h1>

        <div class="count-display" id="count">0</div>

        <div class="controls">
            <button class="btn-decrement" id="decrementBtn">− Decrease</button>
            <button class="btn-increment" id="incrementBtn">+ Increase</button>
            <button class="btn-reset" id="resetBtn">↺ Reset</button>
        </div>

        <div class="step-control">
            <label for="stepInput">Step Value:</label>
            <input type="number" id="stepInput" value="1" min="1" max="100">
        </div>

        <div class="info">
            <strong>How it works:</strong><br>
            • Click buttons to send events to Python<br>
            • Python updates state and sends it back<br>
            • State changes are reflected in real-time<br>
            • Try changing the step value!
        </div>
    </div>

    <script>
        const countDisplay = document.getElementById('count');
        const incrementBtn = document.getElementById('incrementBtn');
        const decrementBtn = document.getElementById('decrementBtn');
        const resetBtn = document.getElementById('resetBtn');
        const stepInput = document.getElementById('stepInput');

        let currentState = { count: 0, step: 1 };

        // Handle button clicks - send events to Python
        incrementBtn.addEventListener('click', () => {
            console.log('[JS] Sending increment event');
            window.sendToStreamlit('increment', {
                currentCount: currentState.count,
                step: currentState.step
            });
        });

        decrementBtn.addEventListener('click', () => {
            console.log('[JS] Sending decrement event');
            window.sendToStreamlit('decrement', {
                currentCount: currentState.count,
                step: currentState.step
            });
        });

        resetBtn.addEventListener('click', () => {
            console.log('[JS] Sending reset event');
            window.sendToStreamlit('reset', {});
        });

        stepInput.addEventListener('change', (e) => {
            const newStep = parseInt(e.target.value, 10);
            console.log('[JS] Step changed to:', newStep);
            currentState.step = newStep;
            window.sendToStreamlit('step_change', { step: newStep });
        });

        // Receive state updates from Python
        window.onStreamlitData = function(data) {
            console.log('[JS] Received state from Python:', data);

            if (data && typeof data === 'object') {
                if ('count' in data) {
                    currentState.count = data.count;
                    countDisplay.textContent = data.count;

                    // Animate count change
                    countDisplay.style.transform = 'scale(1.1)';
                    setTimeout(() => {
                        countDisplay.style.transform = 'scale(1)';
                    }, 200);
                }

                if ('step' in data) {
                    currentState.step = data.step;
                    stepInput.value = data.step;
                }
            }
        };

        console.log('[JS] Counter component initialized');
    </script>
</body>
</html>
"""

# Wrap HTML with bridge
html_with_bridge = bridge.wrap_with_bridge(html_content, 'counter')

# Simulate rendering and event handling
print("=" * 60)
print("Bidirectional Counter Demo")
print("=" * 60)
print("\nComponent initialized with state:", state_manager.get_state('counter'))
print("\nHTML content ready (with bridge injected)")
print(f"Bridge script length: {len(html_with_bridge) - len(html_content)} characters")

# Simulate some events
print("\n" + "=" * 60)
print("Simulating user interactions...")
print("=" * 60)

# Simulate increment click
print("\n[Simulation] User clicks increment button")
bridge.handle_event('counter', {
    'event': 'increment',
    'data': {'currentCount': 0, 'step': 1}
})

# Simulate another increment
print("\n[Simulation] User clicks increment again")
bridge.handle_event('counter', {
    'event': 'increment',
    'data': {'currentCount': 1, 'step': 1}
})

# Simulate step change
print("\n[Simulation] User changes step to 5")
bridge.handle_event('counter', {
    'event': 'step_change',
    'data': {'step': 5}
})

# Simulate increment with new step
print("\n[Simulation] User clicks increment with step=5")
bridge.handle_event('counter', {
    'event': 'increment',
    'data': {'currentCount': 2, 'step': 5}
})

# Simulate reset
print("\n[Simulation] User clicks reset")
bridge.handle_event('counter', {
    'event': 'reset',
    'data': {}
})

# Show event history
print("\n" + "=" * 60)
print("Event History")
print("=" * 60)
events = bridge.get_event_history('counter')
for i, event in enumerate(events, 1):
    print(f"{i}. {event.event_type} at {event.timestamp.strftime('%H:%M:%S')}")

# Show state history
print("\n" + "=" * 60)
print("State History")
print("=" * 60)
history = state_manager.get_history('counter')
for snapshot in history:
    print(f"v{snapshot.version} ({snapshot.source}): {snapshot.state}")

# Export state
print("\n" + "=" * 60)
print("Current State (JSON Export)")
print("=" * 60)
print(state_manager.export_state('counter'))

print("\n✅ Demo completed successfully!")
print("\nKey Features Demonstrated:")
print("- ✅ JavaScript → Python event communication")
print("- ✅ Python → JavaScript state updates")
print("- ✅ Real-time state synchronization")
print("- ✅ Event recording and history")
print("- ✅ State versioning and history")
print("- ✅ State export/import")
