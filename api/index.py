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
    # HTML Todo List sederhana
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo List</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            ul { list-style-type: none; padding: 0; }
            li { padding: 8px; margin: 5px 0; background: #f4f4f4; border-radius: 4px; }
            button { margin-left: 10px; }
        </style>
    </head>
    <body>
        <h1>My Todo List</h1>
        <input id="taskInput" type="text" placeholder="New task">
        <button onclick="addTodo()">Add</button>
        <ul id="todoList"></ul>

        <script>
            async function fetchTodos() {
                const res = await fetch('/api/todos');
                const data = await res.json();
                const list = document.getElementById('todoList');
                list.innerHTML = '';
                data.forEach((todo, index) => {
                    const li = document.createElement('li');
                    li.textContent = todo.task;
                    const btn = document.createElement('button');
                    btn.textContent = '❌';
                    btn.onclick = () => deleteTodo(index);
                    li.appendChild(btn);
                    list.appendChild(li);
                });
            }

            async function addTodo() {
                const taskInput = document.getElementById('taskInput');
                if (!taskInput.value) return;
                await fetch('/api/todos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task: taskInput.value })
                });
                taskInput.value = '';
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
