from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

todos = []

class Todo(BaseModel):
    task: str

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo List</title>
        <style>
            body { margin: 0; font-family: Arial, sans-serif; background: #f5f7fb; }
            header {
                background: linear-gradient(135deg, #0078d7, #005a9e);
                color: white;
                padding: 15px 25px;
                font-size: 20px;
                font-weight: bold;
            }
            .container {
                display: flex;
                height: calc(100vh - 60px);
            }
            aside {
                width: 220px;
                background: #f0f0f0;
                padding: 15px;
                border-right: 1px solid #ddd;
            }
            aside ul { list-style: none; padding: 0; }
            aside li {
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 5px;
                cursor: pointer;
            }
            aside li.active { background: #0078d7; color: white; }
            main {
                flex: 1;
                padding: 20px;
                display: flex;
                flex-direction: column;
            }
            input {
                padding: 10px;
                width: 70%;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 15px;
                border: none;
                background: #0078d7;
                color: white;
                border-radius: 5px;
                cursor: pointer;
                margin-left: 5px;
            }
            ul#todoList { list-style: none; padding: 0; margin-top: 20px; }
            ul#todoList li {
                background: white;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 6px;
                border: 1px solid #ddd;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            ul#todoList li:hover { background: #f8f8f8; }
            .delete-btn {
                background: none;
                border: none;
                color: #ff4d4d;
                font-size: 18px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <header>Tasks</header>
        <div class="container">
            <aside>
                <ul>
                    <li>My Day</li>
                    <li>Important</li>
                    <li>Planned</li>
                    <li class="active">Tasks</li>
                </ul>
            </aside>
            <main>
                <div>
                    <input id="taskInput" type="text" placeholder="Add a task...">
                    <button onclick="addTodo()">Add</button>
                </div>
                <ul id="todoList"></ul>
            </main>
        </div>

        <script>
            async function fetchTodos() {
                const res = await fetch('/api/todos');
                const data = await res.json();
                const list = document.getElementById('todoList');
                list.innerHTML = '';
                data.forEach((todo, index) => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <span>${todo.task}</span>
                        <button class="delete-btn" onclick="deleteTodo(${index})">×</button>
                    `;
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
                fetchTodos();
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
