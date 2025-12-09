"""Bidirectional communication bridge between JavaScript and Python."""

from typing import Callable, Optional, Any, Dict


class BidirectionalBridge:
    """
    Manages bidirectional communication between JavaScript and Python.

    Features:
    - JavaScript → Python communication via postMessage
    - Python → JavaScript data passing via component props
    - Event callback registration
    """

    def __init__(self):
        """Initialize the bidirectional bridge."""
        self._callbacks: Dict[str, Callable] = {}

    def wrap_with_bridge(self, html_content: str, component_name: str) -> str:
        """
        Inject communication bridge script into HTML content.

        The bridge enables:
        - window.sendToStreamlit(eventType, data) for JS → Python
        - window.onStreamlitData(args) for Python → JS

        Args:
            html_content: Original HTML content
            component_name: Name of the component (for event routing)

        Returns:
            HTML content with injected bridge script
        """
        bridge_script = f"""
<script>
// Streamlit HTML Components - Bidirectional Communication Bridge
(function() {{
    // Send data from JavaScript to Python
    window.sendToStreamlit = function(eventType, data) {{
        if (typeof eventType !== 'string') {{
            console.error('sendToStreamlit: eventType must be a string');
            return;
        }}

        const message = {{
            type: 'streamlit:setComponentValue',
            value: {{
                event: eventType,
                data: data || {{}},
                component: '{component_name}',
                timestamp: Date.now()
            }}
        }};

        console.log('Sending to Streamlit:', message);
        window.parent.postMessage(message, '*');
    }};

    // Receive data from Python (via Streamlit component API)
    window.addEventListener('message', function(event) {{
        if (event.data.type === 'streamlit:render') {{
            const args = event.data.args;

            if (window.onStreamlitData && typeof window.onStreamlitData === 'function') {{
                console.log('Received from Streamlit:', args);
                window.onStreamlitData(args);
            }}
        }}
    }});

    // Notify Streamlit that component is ready
    window.parent.postMessage({{
        type: 'streamlit:componentReady',
        apiVersion: 1
    }}, '*');

    console.log('Streamlit HTML Components bridge initialized for: {component_name}');
}})();
</script>
"""

        # Insert bridge script before closing body tag, or at the end if no body tag
        if "</body>" in html_content.lower():
            # Find the last occurrence of </body> (case insensitive)
            import re
            html_content = re.sub(
                r'</body>',
                f'{bridge_script}</body>',
                html_content,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            # No body tag, append at the end
            html_content += bridge_script

        return html_content

    def register_callback(
        self,
        component_name: str,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None]
    ):
        """
        Register a Python callback for JavaScript events.

        Args:
            component_name: Name of the component
            event_type: Type of event (e.g., 'click', 'submit', 'change')
            callback: Python function to call when event is triggered

        Example:
            >>> def on_button_click(data):
            ...     print(f"Button clicked with data: {data}")
            >>>
            >>> bridge.register_callback('my_button', 'click', on_button_click)
        """
        key = f"{component_name}:{event_type}"
        self._callbacks[key] = callback

    def handle_event(self, component_name: str, event_data: Dict[str, Any]):
        """
        Process an event received from JavaScript.

        Args:
            component_name: Name of the component that sent the event
            event_data: Event data including 'event' type and 'data' payload
        """
        event_type = event_data.get('event')
        if not event_type:
            return

        key = f"{component_name}:{event_type}"
        callback = self._callbacks.get(key)

        if callback:
            try:
                callback(event_data.get('data', {}))
            except Exception as e:
                # Log error but don't break Streamlit app
                print(f"Error in component callback: {e}")

    def unregister_callback(self, component_name: str, event_type: str):
        """
        Unregister a callback.

        Args:
            component_name: Name of the component
            event_type: Type of event
        """
        key = f"{component_name}:{event_type}"
        if key in self._callbacks:
            del self._callbacks[key]

    def clear_callbacks(self, component_name: Optional[str] = None):
        """
        Clear callbacks for a component or all callbacks.

        Args:
            component_name: If provided, only clear callbacks for this component.
                          If None, clear all callbacks.
        """
        if component_name is None:
            self._callbacks.clear()
        else:
            keys_to_remove = [
                key for key in self._callbacks.keys()
                if key.startswith(f"{component_name}:")
            ]
            for key in keys_to_remove:
                del self._callbacks[key]


# Global bridge instance
_bridge = BidirectionalBridge()


def get_bridge() -> BidirectionalBridge:
    """
    Get the global bidirectional bridge instance.

    Returns:
        Global BidirectionalBridge instance
    """
    return _bridge
