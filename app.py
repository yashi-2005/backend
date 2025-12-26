from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = []
task_id_counter = 1
comment_id_counter = 1

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    global task_id_counter
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Task title required"}), 400
    task = {"id": task_id_counter, "title": data["title"], "comments": []}
    tasks.append(task)
    task_id_counter += 1
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200

@app.route("/tasks/<int:task_id>/comments", methods=["POST"])
def add_comment(task_id):
    global comment_id_counter
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            comment = {"id": comment_id_counter, "text": data["text"]}
            task["comments"].append(comment)
            comment_id_counter += 1
            return jsonify(comment), 201
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>/comments/<int:comment_id>", methods=["PUT"])
def edit_comment(task_id, comment_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            for comment in task["comments"]:
                if comment["id"] == comment_id:
                    comment["text"] = data.get("text", comment["text"])
                    return jsonify(comment)
    return jsonify({"error": "Comment not found"}), 404

@app.route("/tasks/<int:task_id>/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(task_id, comment_id):
    for task in tasks:
        if task["id"] == task_id:
            task["comments"] = [c for c in task["comments"] if c["id"] != comment_id]
            return jsonify({"message": "Comment deleted"}), 200
    return jsonify({"error": "Comment not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
