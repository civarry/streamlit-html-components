// ====================================
// CRUD Todo App - JavaScript
// ====================================

// State Management
let tasks = [];
let currentFilter = 'all';
let nextId = 1;

// ====================================
// Initialize App
// ====================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('Todo CRUD App initialized!');

    // Load tasks from localStorage
    loadTasksFromStorage();

    // Setup event listeners
    setupEventListeners();

    // Initial render
    renderTasks();
    updateStats();
});

// ====================================
// Event Listeners Setup
// ====================================
function setupEventListeners() {
    // Add task button
    document.getElementById('addBtn').addEventListener('click', createTask);

    // Enter key in inputs
    document.getElementById('taskTitle').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') createTask();
    });

    document.getElementById('taskDescription').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') createTask();
    });

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // Update active state
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            // Update filter and render
            currentFilter = this.dataset.filter;
            renderTasks();
        });
    });

    // Click outside modal to close
    document.getElementById('editModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeEditModal();
        }
    });
}

// ====================================
// CREATE - Add new task
// ====================================
function createTask() {
    const titleInput = document.getElementById('taskTitle');
    const descInput = document.getElementById('taskDescription');

    const title = titleInput.value.trim();
    const description = descInput.value.trim();

    // Validation
    if (!title) {
        alert('Please enter a task title!');
        titleInput.focus();
        return;
    }

    // Create task object
    const task = {
        id: nextId++,
        title: title,
        description: description,
        completed: false,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    };

    // Add to tasks array
    tasks.unshift(task); // Add to beginning

    // Save to storage
    saveTasksToStorage();

    // Clear inputs
    titleInput.value = '';
    descInput.value = '';
    titleInput.focus();

    // Re-render
    renderTasks();
    updateStats();

    // Send event to Python (if bridge available)
    sendToStreamlitIfAvailable('task_created', {
        task: task,
        total_tasks: tasks.length
    });

    console.log('Task created:', task);
}

// ====================================
// READ - Render tasks
// ====================================
function renderTasks() {
    const taskList = document.getElementById('taskList');

    // Filter tasks
    let filteredTasks = tasks;
    if (currentFilter === 'pending') {
        filteredTasks = tasks.filter(t => !t.completed);
    } else if (currentFilter === 'completed') {
        filteredTasks = tasks.filter(t => t.completed);
    }

    // Clear list
    taskList.innerHTML = '';

    // Check if empty
    if (filteredTasks.length === 0) {
        taskList.innerHTML = `
            <div class="empty-state">
                <p>${currentFilter === 'all' ? 'No tasks yet. Add your first task above!' :
                     currentFilter === 'pending' ? 'No pending tasks!' :
                     'No completed tasks yet!'}</p>
            </div>
        `;
        return;
    }

    // Render each task
    filteredTasks.forEach(task => {
        const taskElement = createTaskElement(task);
        taskList.appendChild(taskElement);
    });
}

function createTaskElement(task) {
    const div = document.createElement('div');
    div.className = `task-item ${task.completed ? 'completed' : ''}`;
    div.dataset.taskId = task.id;

    // Format date
    const createdDate = new Date(task.createdAt).toLocaleString();

    div.innerHTML = `
        <input
            type="checkbox"
            class="task-checkbox"
            ${task.completed ? 'checked' : ''}
            onchange="toggleTask(${task.id})"
        />
        <div class="task-content">
            <h3>${escapeHtml(task.title)}</h3>
            ${task.description ? `<p>${escapeHtml(task.description)}</p>` : ''}
            <div class="task-meta">Created: ${createdDate}</div>
        </div>
        <div class="task-actions">
            <button class="action-btn btn-edit" onclick="openEditModal(${task.id})" title="Edit">
                ✏️
            </button>
            <button class="action-btn btn-delete" onclick="deleteTask(${task.id})" title="Delete">
                🗑️
            </button>
        </div>
    `;

    return div;
}

// ====================================
// UPDATE - Edit task
// ====================================
function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        task.updatedAt = new Date().toISOString();

        saveTasksToStorage();
        renderTasks();
        updateStats();

        sendToStreamlitIfAvailable('task_toggled', {
            task_id: id,
            completed: task.completed
        });

        console.log('Task toggled:', task);
    }
}

function openEditModal(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    // Populate modal
    document.getElementById('editTaskId').value = task.id;
    document.getElementById('editTaskTitle').value = task.title;
    document.getElementById('editTaskDescription').value = task.description || '';

    // Show modal
    document.getElementById('editModal').classList.add('active');
    document.getElementById('editTaskTitle').focus();
}

function closeEditModal() {
    document.getElementById('editModal').classList.remove('active');
}

function saveEdit() {
    const id = parseInt(document.getElementById('editTaskId').value);
    const newTitle = document.getElementById('editTaskTitle').value.trim();
    const newDescription = document.getElementById('editTaskDescription').value.trim();

    if (!newTitle) {
        alert('Task title cannot be empty!');
        return;
    }

    const task = tasks.find(t => t.id === id);
    if (task) {
        task.title = newTitle;
        task.description = newDescription;
        task.updatedAt = new Date().toISOString();

        saveTasksToStorage();
        renderTasks();
        closeEditModal();

        sendToStreamlitIfAvailable('task_updated', {
            task: task
        });

        console.log('Task updated:', task);
    }
}

// ====================================
// DELETE - Remove task
// ====================================
function deleteTask(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    if (!confirm(`Are you sure you want to delete "${task.title}"?`)) {
        return;
    }

    // Remove from array
    tasks = tasks.filter(t => t.id !== id);

    saveTasksToStorage();
    renderTasks();
    updateStats();

    sendToStreamlitIfAvailable('task_deleted', {
        task_id: id,
        total_tasks: tasks.length
    });

    console.log('Task deleted:', id);
}

// ====================================
// Statistics
// ====================================
function updateStats() {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const pending = total - completed;

    document.getElementById('totalCount').textContent = total;
    document.getElementById('pendingCount').textContent = pending;
    document.getElementById('completedCount').textContent = completed;
}

// ====================================
// Local Storage
// ====================================
function saveTasksToStorage() {
    try {
        localStorage.setItem('streamlit_todo_tasks', JSON.stringify(tasks));
        localStorage.setItem('streamlit_todo_nextId', nextId.toString());
    } catch (e) {
        console.error('Failed to save to localStorage:', e);
    }
}

function loadTasksFromStorage() {
    try {
        const saved = localStorage.getItem('streamlit_todo_tasks');
        const savedId = localStorage.getItem('streamlit_todo_nextId');

        if (saved) {
            tasks = JSON.parse(saved);
            console.log('Loaded tasks from storage:', tasks.length);
        }

        if (savedId) {
            nextId = parseInt(savedId);
        }
    } catch (e) {
        console.error('Failed to load from localStorage:', e);
        tasks = [];
        nextId = 1;
    }
}

// ====================================
// Utility Functions
// ====================================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function sendToStreamlitIfAvailable(eventType, data) {
    if (typeof window.sendToStreamlit === 'function') {
        window.sendToStreamlit(eventType, data);
        console.log('Sent to Streamlit:', eventType, data);
    }
}

// ====================================
// Keyboard Shortcuts
// ====================================
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus on task input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('taskTitle').focus();
    }

    // Escape to close modal
    if (e.key === 'Escape') {
        closeEditModal();
    }
});

// ====================================
// Export for testing
// ====================================
window.TodoApp = {
    tasks,
    createTask,
    deleteTask,
    toggleTask,
    renderTasks,
    updateStats
};

console.log('Todo CRUD App ready! Press Ctrl+K to add a task.');
