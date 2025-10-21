from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Simpan todo di memory
todos = []

class Todo(BaseModel):
    task: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>My Tasks</title>
        <style>
            body {
                margin: 0;
                font-family: "Segoe UI", Arial, sans-serif;
                display: flex;
                height: 100vh;
                background: #f8f9fa;
            }
            /* Sidebar */
            .sidebar {
                width: 250px;
                background: #f0f0f0;
                border-right: 1px solid #ddd;
                padding: 20px;
                display: flex;
                flex-direction: column;
            }
            .sidebar h2 {
                font-size: 20px;
                margin-bottom: 20px;
                color: #333;
            }
            .sidebar ul {
                list-style: none;
                padding: 0;
            }
            .sidebar li {
                padding: 10px;
                border-radius: 6px;
                cursor: pointer;
                margin-bottom: 5px;
                transition: background 0.2s;
            }
            .sidebar li:hover {
                background: #e1e1e1;
            }
            .sidebar .active {
                background: #0078d7;
                color: white;
            }
            /* Main content */
            .main {
                flex: 1;
                display: flex;
                flex-direction: column;
            }
            .header {
                background: linear-gradient(135deg, #0078d7, #005a9e);
                color: white;
                padding: 20px;
                font-size: 22px;
                font-weight: bold;
            }
            .content {
                padding: 20px;
                flex: 1;
                overflow-y: auto;
            }
            .task-input {
                display: flex;
                margin-bottom: 20px;
            }
            .task-input input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px 0 0 4px;
                outline: none;
            }
            .task-input button {
                padding: 10px 20px;
                border: none;
                background: #0078d7;
                color: white;
                border-radius: 0 4px 4px 0;
                cursor: pointer;
            }
            ul.tasks {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            ul.tasks li {
                background: white;
                border: 1px solid #ddd;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 6px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: box-shadow 0.2s;
            }
            ul.tasks li:hover {
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }
            ul.tasks button {
                border: none;
                background: transparent;
                cursor: pointer;
                color: #ff4d4d;
                font-size: 18px;
            }
            /* Detail panel (kanan) */
            .detail {
                width: 300px;
                border-left: 1px solid #ddd;
                background: #fff;
                padding: 20px;
            }
            .detail h3 {
                margin-top: 0;
            }
            .empty-detail {
                color: #888;
                text-align: center;
                margin-top: 40px;
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Lists</h2>
            <ul>
                <li>My Day</li>
                <li>Important</li>
                <li>Planned</li>
                <li class="active">Tasks</li>
            </ul>
        </div>
        <div class="main">
            <div class="header">Tasks</div>
            <div class="content">
                <div class="task-input">
                    <input id="taskInput" type="text" placeholder="Add a new task...">
                    <button onclick="addTodo()">Add</button>
                </div>
                <ul id="todoList" class="tasks"></ul>
            </div>
        </div>
        <div class="detail" id="detailPanel">
            <div class="empty-detail">Select a task to view details</div>
        </div>

        <script>
            let selectedTaskIndex = null;

            async function fetchTodos() {
                const res = await fetch('/api/todos');
                const data = await res.json();
                const list = document.getElementById('todoList');
                list.innerHTML = '';
                data.forEach((todo, index) => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <span>${todo.task}</span>
                        <button onclick="deleteTodo(${index})">❌</button>
                    `;
                    li.onclick = () => showDetail(todo, index);
                    list.appendChild(li);
                });
            }

            async function addTodo() {
                const input = document.getElementById('taskInput');
                if (!input.value) return;
                await fetch('/api/todos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task: input.value })
                });
                input.value = '';
                fetchTodos();
            }

            async function deleteTodo(index) {
                await fetch('/api/todos/' + index, { method: 'DELETE' });
                document.getElementById('detailPanel').innerHTML = '<div class="empty-detail">Select a task to view details</div>';
                fetchTodos();
            }

            function showDetail(todo, index) {
                selectedTaskIndex = index;
                document.getElementById('detailPanel').innerHTML = `
                    <h3>${todo.task}</h3>
                    <p><b>Status:</b> Incomplete</p>
                    <p><b>Created:</b> Just now</p>
                    <button onclick="deleteTodo(${index})" style="background:#ff4d4d;color:white;border:none;padding:8px 12px;border-radius:4px;cursor:pointer;">Delete Task</button>
                `;
            }

            fetchTodos();
        </script>
    </body>
    </html>
    """

@app.get("/api/todos")
async def get_todos():
    return todos

@app.post("/api/todos")
async def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo added", "todo": todo}

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    if 0 <= todo_id < len(todos):
        removed = todos.pop(todo_id)
        return {"message": "Todo removed", "todo": removed}
    return {"error": "Invalid ID"}
