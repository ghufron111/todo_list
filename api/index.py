from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS biar bisa diakses dari browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simpan todo di memory
todos = []

@app.get("/")
async def root():
    return {"message": "Welcome to Todo API on Vercel with FastAPI!"}

@app.get("/todos")
async def get_todos():
    return {"todos": todos}

@app.post("/todos")
async def add_todo(request: Request):
    data = await request.json()
    task = data.get("task")
    if task:
        todos.append({"task": task, "done": False})
    return {"todos": todos}

@app.post("/todos/{index}/toggle")
async def toggle(index: int):
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
    return {"todos": todos}

@app.get("/ui", response_class=HTMLResponse)
async def ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo List</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            li.done { text-decoration: line-through; color: gray; }
        </style>
    </head>
    <body>
        <h1>Todo List</h1>
        <input id="taskInput" type="text" placeholder="Enter a task" />
        <button onclick="addTodo()">Add</button>
        <ul id="todoList"></ul>

        <script>
            async function loadTodos() {
                const res = await fetch('/api/todos');
                const data = await res.json();
                const list = document.getElementById('todoList');
                list.innerHTML = '';
                data.todos.forEach((todo, i) => {
                    const li = document.createElement('li');
                    li.textContent = todo.task;
                    if (todo.done) li.classList.add('done');
                    li.onclick = async () => {
                        await fetch(`/api/todos/${i}/toggle`, { method: 'POST' });
                        loadTodos();
                    };
                    list.appendChild(li);
                });
            }
            async function addTodo() {
                const task = document.getElementById('taskInput').value;
                await fetch('/api/todos', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ task })
                });
                document.getElementById('taskInput').value = '';
                loadTodos();
            }
            loadTodos();
        </script>
    </body>
    </html>
    """
