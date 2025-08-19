from flask import Flask, request, jsonify

app = Flask(__name__)

# Simpan data todo di memori (nanti bisa diganti DB)
todos = []

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Todo API!"})

# GET semua todo
@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

# POST tambah todo
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    todo = {
        "id": len(todos) + 1,
        "title": data.get("title"),
        "done": False
    }
    todos.append(todo)
    return jsonify({"message": "Todo added!", "todo": todo}), 201

# PUT update todo (ubah title/done)
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            data = request.json
            todo["title"] = data.get("title", todo["title"])
            todo["done"] = data.get("done", todo["done"])
            return jsonify({"message": "Todo updated!", "todo": todo})
    return jsonify({"error": "Todo not found"}), 404

# DELETE hapus todo
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return jsonify({"message": "Todo deleted!"})

if __name__ == "__main__":
    app.run(debug=True)
