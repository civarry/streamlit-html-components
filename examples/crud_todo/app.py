"""
CRUD Todo App Example - streamlit-html-components

This example demonstrates a complete CRUD application:
- CREATE: Add new tasks
- READ: View and filter tasks
- UPDATE: Edit tasks and toggle completion
- DELETE: Remove tasks

Features:
- Full CRUD operations
- Local storage persistence
- Filter by status (All/Pending/Completed)
- Task statistics
- Edit modal
- Keyboard shortcuts (Ctrl+K to add task)
- Responsive design
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from streamlit_html_components import render_component, configure, cache_stats

# Configure the package
configure(
    templates_dir='templates',
    styles_dir='styles',
    scripts_dir='scripts',
    default_cache=False  # Disable cache for interactive app
)

# Streamlit app configuration
st.set_page_config(
    page_title="Todo CRUD App",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Streamlit
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main > div {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📝 Todo CRUD App")
    st.markdown("---")

    st.markdown("""
    ### Features
    - ✅ **Create** new tasks
    - 👀 **Read** and filter tasks
    - ✏️ **Update** task details
    - 🗑️ **Delete** tasks
    - 💾 **Auto-save** to localStorage
    - 📊 **Statistics** tracking
    - 🎨 **Responsive** design

    ### How to Use
    1. **Add Task**: Enter title and description, click "Add Task"
    2. **Toggle**: Click checkbox to mark complete/incomplete
    3. **Edit**: Click ✏️ to edit task details
    4. **Delete**: Click 🗑️ to remove task
    5. **Filter**: Use All/Pending/Completed buttons

    ### Keyboard Shortcuts
    - `Ctrl+K` or `Cmd+K`: Focus on task input
    - `Enter`: Add task (when input focused)
    - `Escape`: Close edit modal

    ### Technical Details
    This app demonstrates:
    - Traditional HTML/CSS/JS structure
    - Component-based architecture
    - State management with localStorage
    - Event handling and DOM manipulation
    - Responsive CSS Grid/Flexbox
    """)

    st.markdown("---")

    # Customization options
    st.subheader("Customize")

    app_title = st.text_input(
        "App Title",
        "My Todo List",
        help="Change the main heading"
    )

    subtitle = st.text_input(
        "Subtitle",
        "Manage your tasks efficiently",
        help="Change the subtitle"
    )

    component_height = st.slider(
        "Component Height",
        min_value=400,
        max_value=1200,
        value=800,
        step=50,
        help="Adjust the component height"
    )

    st.markdown("---")

    # Event callbacks
    st.subheader("Live Events")

    if 'events' not in st.session_state:
        st.session_state.events = []

    def on_todo_event(data):
        """Callback for todo events"""
        st.session_state.events.insert(0, data)
        # Keep only last 5 events
        st.session_state.events = st.session_state.events[:5]

    if st.session_state.events:
        st.markdown("**Recent Events:**")
        for i, event in enumerate(st.session_state.events):
            event_type = event.get('event', 'unknown')
            event_data = event.get('data', {})

            if event_type == 'task_created':
                st.success(f"✅ Task created: {event_data.get('total_tasks', 0)} total")
            elif event_type == 'task_deleted':
                st.error(f"🗑️ Task deleted: {event_data.get('total_tasks', 0)} total")
            elif event_type == 'task_toggled':
                status = "completed" if event_data.get('completed') else "pending"
                st.info(f"🔄 Task marked as {status}")
            elif event_type == 'task_updated':
                st.warning(f"✏️ Task updated")
    else:
        st.info("No events yet. Interact with the app!")

# Main content
st.title("📝 Todo CRUD Application")
st.markdown("### Built with streamlit-html-components")

st.info("""
👈 **Check the sidebar** for features, instructions, and customization options!

This is a **fully functional CRUD app** using traditional HTML/CSS/JS files.
All tasks are saved in your browser's localStorage.
""")

# Render the component
result = render_component(
    'index',  # Component name (index.html)
    props={
        'app_title': app_title,
        'subtitle': subtitle
    },
    styles=['styles'],  # Explicitly load styles.css
    scripts=['main'],   # Explicitly load main.js
    height=component_height,
    on_event=on_todo_event,  # Python callback for events
    key='todo_app'
)

# Display result if any
if result:
    st.write("Component returned:", result)

# Additional information
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("📁 File Structure"):
        st.code("""
crud_todo/
├── templates/
│   └── index.html      # HTML structure
├── styles/
│   └── styles.css      # Complete styling
├── scripts/
│   └── main.js         # CRUD operations
└── app.py              # This Streamlit app
        """, language="text")

with col2:
    with st.expander("💡 CRUD Operations"):
        st.markdown("""
        **CREATE:**
        - `createTask()` - Add new task
        - Validates input
        - Saves to localStorage
        - Updates UI

        **READ:**
        - `renderTasks()` - Display tasks
        - `createTaskElement()` - Build HTML
        - Filter by status

        **UPDATE:**
        - `toggleTask()` - Mark complete
        - `saveEdit()` - Update details
        - Edit modal for editing

        **DELETE:**
        - `deleteTask()` - Remove task
        - Confirmation dialog
        - Updates statistics
        """)

with col3:
    with st.expander("🎨 Technologies"):
        st.markdown("""
        **Frontend:**
        - HTML5 semantic markup
        - CSS3 with Flexbox/Grid
        - Vanilla JavaScript (ES6+)

        **Features:**
        - localStorage API
        - Event delegation
        - DOM manipulation
        - Responsive design
        - CSS animations

        **Framework:**
        - streamlit-html-components
        - Jinja2 templates
        - Component caching
        - Event callbacks
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 20px;">
    <p>Built with ❤️ using <strong>streamlit-html-components</strong></p>
    <p>A framework for traditional HTML/CSS/JS in Streamlit</p>
</div>
""", unsafe_allow_html=True)
