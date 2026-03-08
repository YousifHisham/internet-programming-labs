class Task {
    constructor(description) {
        this.id = Date.now();
        this.description = description;
        this.completed = false;
    }

    toggle() {
        this.completed = !this.completed;
    }
}

const tasks = [];
const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const taskList = document.getElementById('taskList');

function renderTasks() {
    if (tasks.length === 0) {
        taskList.innerHTML = '<div class="empty-state">No tasks yet. Add one to get started!</div>';
        return;
    }

    taskList.innerHTML = tasks.map(task => `
        <li class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
            <span class="task-text">${task.description}</span>
            <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
        </li>
    `).join('');

    document.querySelectorAll('.task-item').forEach(item => {
        item.addEventListener('click', (e) => {
            if (!e.target.classList.contains('delete-btn')) {
                toggleTask(parseInt(item.dataset.id));
            }
        });
    });
}

function addTask() {
    const description = taskInput.value.trim();
    if (description === '') {
        alert('Please enter a task description!');
        return;
    }

    const task = new Task(description);
    tasks.push(task);
    taskInput.value = '';
    renderTasks();
}

function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.toggle();
        renderTasks();
    }
}

function deleteTask(id) {
    const index = tasks.findIndex(t => t.id === id);
    if (index !== -1) {
        tasks.splice(index, 1);
        renderTasks();
    }
}

addBtn.addEventListener('click', addTask);
taskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTask();
    }
});

renderTasks();
