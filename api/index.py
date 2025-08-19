from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Memory storage (tidak ada DB)
todos = []

# Middleware biar aman di Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint JSON
@app.get("/api", response_model=dict)
async def root():
    return {"message": "Welcome to Todo API on Vercel with FastAPI!"}

@app.get("/api/todos")
async def get_todos():
    return {"todos": todos}

@app.post("/api/todos")
async def add_todo(item: str = Form(...)):
    todos.append(item)
    return {"message": "Todo added!", "todos": todos}

@app.post("/api/todos/delete")
async def delete_todo(index: int = Form(...)):
    if 0 <= index < len(todos):
        todos.pop(index)
        return {"message": "Todo deleted!", "todos": todos}
    return {"error": "Invalid index"}


# HTML Frontend
@app.get("/", response_class=HTMLResponse)
async def todo_page(request: Request):
    todo_list_html = "".join(
        f"<li>{todo} <form method='post' action='/delete' style='display:inline;'>"
        f"<input type='hidden' name='index' value='{i}'>"
        f"<button type='submit'>❌</button></form></li>"
        for i, todo in enumerate(todos)
    )
    return f"""
    <html>
      <head>
        <title>Todo List</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 20px; }}
          ul {{ list-style: none; padding: 0; }}
          li {{ margin: 5px 0; }}
          input, button {{ padding: 5px; }}
        </style>
      </head>
      <body>
        <h2>📝 Todo List</h2>
        <form method="post" action="/add">
          <input type="text" name="item" placeholder="New todo..." required>
          <button type="submit">Add</button>
        </form>
        <ul>{todo_list_html}</ul>
      </body>
    </html>
    """

@app.post("/add")
async def add_todo_page(item: str = Form(...)):
    todos.append(item)
    return RedirectResponse("/", status_code=303)

@app.post("/delete")
async def delete_todo_page(index: int = Form(...)):
    if 0 <= index < len(todos):
        todos.pop(index)
    return RedirectResponse("/", status_code=303)
