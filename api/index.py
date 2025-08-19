from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todos = []

class Todo(BaseModel):
    title: str
    done: bool = False

@app.get("/")
def home():
    return {"message": "Welcome to Todo API on Vercel with FastAPI!"}

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def add_todo(todo: Todo):
    new_todo = {"id": len(todos) + 1, "title": todo.title, "done": todo.done}
    todos.append(new_todo)
    return {"message": "Todo added!", "todo": new_todo}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    for t in todos:
        if t["id"] == todo_id:
            t["title"] = todo.title
            t["done"] = todo.done
            return {"message": "Todo updated!", "todo": t}
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return {"message": "Todo deleted!"}
