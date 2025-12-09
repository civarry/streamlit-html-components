# Todo CRUD App Example

A complete **CRUD (Create, Read, Update, Delete)** application built with streamlit-html-components.

## Features

✅ **CREATE** - Add new tasks with title and description
📖 **READ** - View and filter tasks (All/Pending/Completed)
✏️ **UPDATE** - Edit tasks and toggle completion status
🗑️ **DELETE** - Remove tasks with confirmation
💾 **Auto-save** - Persistence using browser localStorage
📊 **Statistics** - Track total, pending, and completed tasks
🎨 **Responsive** - Works on desktop and mobile
⌨️ **Keyboard shortcuts** - Ctrl+K to add task, Escape to close modal

## How to Run

### 1. Install the package (if not already installed)

```bash
cd /Users/cjcarito/Documents/streamlit-html-components
pip install -e .
```

### 2. Run the app

```bash
cd examples/crud_todo
streamlit run app.py
```

### 3. Open in browser

The app will open at `http://localhost:8501`

## File Structure

```
crud_todo/
├── templates/
│   └── index.html      # HTML structure with Jinja2 variables
├── styles/
│   └── styles.css      # Complete styling (no framework needed)
├── scripts/
│   └── main.js         # CRUD operations and event handling
├── app.py              # Streamlit application
└── README.md           # This file
```

## CRUD Operations Explained

### CREATE - Add New Task

**JavaScript:**
```javascript
function createTask() {
    const task = {
        id: nextId++,
        title: title,
        description: description,
        completed: false,
        createdAt: new Date().toISOString()
    };
    tasks.unshift(task);
    saveTasksToStorage();
    renderTasks();
}
```

### READ - Display Tasks

**JavaScript:**
```javascript
function renderTasks() {
    let filteredTasks = tasks;
    if (currentFilter === 'pending') {
        filteredTasks = tasks.filter(t => !t.completed);
    }
    // Create HTML elements for each task
    filteredTasks.forEach(task => {
        const taskElement = createTaskElement(task);
        taskList.appendChild(taskElement);
    });
}
```

### UPDATE - Edit Task

**JavaScript:**
```javascript
function saveEdit() {
    const task = tasks.find(t => t.id === id);
    task.title = newTitle;
    task.description = newDescription;
    saveTasksToStorage();
    renderTasks();
}

function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    task.completed = !task.completed;
    saveTasksToStorage();
    renderTasks();
}
```

### DELETE - Remove Task

**JavaScript:**
```javascript
function deleteTask(id) {
    if (!confirm('Are you sure?')) return;
    tasks = tasks.filter(t => t.id !== id);
    saveTasksToStorage();
    renderTasks();
}
```

## State Management

Tasks are stored in browser's `localStorage`:

```javascript
// Save
localStorage.setItem('streamlit_todo_tasks', JSON.stringify(tasks));

// Load
const saved = localStorage.getItem('streamlit_todo_tasks');
tasks = JSON.parse(saved);
```

## Event Communication (JavaScript → Python)

Events are sent to Streamlit when tasks are modified:

```javascript
// In JavaScript
window.sendToStreamlit('task_created', {
    task: task,
    total_tasks: tasks.length
});
```

```python
# In Python (app.py)
def on_todo_event(data):
    st.session_state.events.insert(0, data)

render_component('index', on_event=on_todo_event)
```

## Customization

You can customize the app through the Streamlit sidebar:
- Change app title and subtitle
- Adjust component height
- View live events

Or modify the component files:
- `templates/index.html` - Change structure
- `styles/styles.css` - Customize styling
- `scripts/main.js` - Modify behavior

## Key Learning Points

### 1. Traditional Web Development in Streamlit
Write standard HTML/CSS/JS and render it in Streamlit with one function call.

### 2. Component Isolation
Each component has its own files, making it easy to organize and maintain.

### 3. Template Variables
Pass data from Python to JavaScript using Jinja2:

```python
render_component('index', props={
    'app_title': 'My Custom Title',
    'subtitle': 'My subtitle'
})
```

### 4. Bidirectional Communication
JavaScript can send events back to Python for state management.

### 5. No Framework Lock-in
Pure HTML/CSS/JS - no React, Vue, or other framework required.

## Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Keyboard Shortcuts

- `Ctrl+K` or `Cmd+K` - Focus on task input
- `Enter` - Add task (when input is focused)
- `Escape` - Close edit modal

## Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Flexbox, Grid, animations
- **JavaScript ES6+** - Modern syntax, arrow functions
- **localStorage API** - Data persistence
- **Jinja2** - Template variables
- **Streamlit** - Python web framework

## Next Steps

1. **Extend functionality:**
   - Add task priorities (high/medium/low)
   - Add due dates
   - Add categories/tags
   - Add search functionality

2. **Backend integration:**
   - Save to database instead of localStorage
   - User authentication
   - Multi-user support

3. **Deploy:**
   - Deploy to Streamlit Cloud
   - Share with others

## Troubleshooting

**Tasks not persisting?**
- Check browser's localStorage is enabled
- Open browser console to see any errors

**Component not rendering?**
- Ensure all three files exist (index.html, styles.css, main.js)
- Check browser console for JavaScript errors

**Want to reset all tasks?**
```javascript
// In browser console:
localStorage.removeItem('streamlit_todo_tasks');
location.reload();
```

## License

MIT License - Feel free to use and modify!
