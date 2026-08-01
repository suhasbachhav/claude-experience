from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from db_config import get_db_context

app = Flask(__name__)
CORS(app)

# In-memory task storage (for demo; can be moved to database)
tasks = {
    "todo": [
        {"id": "1", "title": "Design homepage mockup"},
        {"id": "2", "title": "Set up project repository"},
    ],
    "inprogress": [
        {"id": "3", "title": "Implement user authentication"},
    ],
    "done": [
        {"id": "4", "title": "Create project plan"},
    ],
}

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks organized by column."""
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Add a new task to a column."""
    data = request.get_json()
    title = data.get('title', '').strip()
    column = data.get('column', 'todo')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    if column not in tasks:
        return jsonify({"error": "Invalid column"}), 400

    task_id = str(uuid.uuid4())[:8]
    new_task = {"id": task_id, "title": title}
    tasks[column].append(new_task)

    return jsonify(new_task), 201

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task from any column."""
    for column in tasks.values():
        for i, task in enumerate(column):
            if task['id'] == task_id:
                column.pop(i)
                return jsonify({"message": "Task deleted"}), 200

    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<task_id>/move', methods=['PATCH'])
def move_task(task_id):
    """Move a task to a different column."""
    data = request.get_json()
    new_column = data.get('column')

    if new_column not in tasks:
        return jsonify({"error": "Invalid column"}), 400

    # Find and remove task from current column
    current_task = None
    for column in tasks.values():
        for i, task in enumerate(column):
            if task['id'] == task_id:
                current_task = column.pop(i)
                break
        if current_task:
            break

    if not current_task:
        return jsonify({"error": "Task not found"}), 404

    # Add task to new column
    tasks[new_column].append(current_task)

    return jsonify(current_task), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')
