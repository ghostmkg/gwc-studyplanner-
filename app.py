from flask import Flask, jsonify, request
from tasks_manager import load_tasks, save_tasks

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to GWC Study Planner!"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    new_task = request.get_json()
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify({"message": "Task added successfully!", "task": new_task}), 201

@app.route('/update_task/<int:index>', methods=['PUT'])
def update_task(index):
    tasks = load_tasks()
    if index >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    tasks[index].update(request.get_json())
    save_tasks(tasks)
    return jsonify({"message": "Task updated!", "task": tasks[index]})

@app.route('/delete_task/<int:index>', methods=['DELETE'])
def delete_task(index):
    tasks = load_tasks()
    if index >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    tasks.pop(index)
    save_tasks(tasks)
    return jsonify({"message": "Task deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
