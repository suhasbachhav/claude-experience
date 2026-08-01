from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from db_config import get_db_context

app = Flask(__name__)
CORS(app)

def init_kanban_db():
    """Initialize kanban tables in the database."""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kanban_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                column_name TEXT NOT NULL,
                position INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks organized by column."""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, column_name, position
            FROM kanban_tasks
            ORDER BY column_name, position
        """)
        tasks = cursor.fetchall()

        result = {
            'todo': [],
            'inprogress': [],
            'done': []
        }

        for task in tasks:
            result[task[2]].append({
                'id': task[0],
                'title': task[1],
                'column': task[2]
            })

        return jsonify(result)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.json
    title = data.get('title', '').strip()
    column_name = data.get('column', 'todo')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    if column_name not in ['todo', 'inprogress', 'done']:
        return jsonify({'error': 'Invalid column'}), 400

    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(position) FROM kanban_tasks WHERE column_name = ?", (column_name,))
        max_pos = cursor.fetchone()[0]
        position = (max_pos or 0) + 1

        cursor.execute("""
            INSERT INTO kanban_tasks (title, column_name, position)
            VALUES (?, ?, ?)
        """, (title, column_name, position))

        task_id = cursor.lastrowid

        return jsonify({
            'id': task_id,
            'title': title,
            'column': column_name
        }), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kanban_tasks WHERE id = ?", (task_id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({'message': 'Task deleted'}), 200

@app.route('/api/tasks/<int:task_id>/move', methods=['PATCH'])
def move_task(task_id):
    """Move a task to a different column."""
    data = request.json
    new_column = data.get('column', 'todo')

    if new_column not in ['todo', 'inprogress', 'done']:
        return jsonify({'error': 'Invalid column'}), 400

    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM kanban_tasks WHERE id = ?", (task_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Task not found'}), 404

        old_column = result[0]

        if old_column != new_column:
            cursor.execute("SELECT MAX(position) FROM kanban_tasks WHERE column_name = ?", (new_column,))
            max_pos = cursor.fetchone()[0]
            new_position = (max_pos or 0) + 1

            cursor.execute("""
                UPDATE kanban_tasks
                SET column_name = ?, position = ?
                WHERE id = ?
            """, (new_column, new_position, task_id))

        return jsonify({'message': 'Task moved'}), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    init_kanban_db()
    print("Starting Kanban Server on http://localhost:5000")
    app.run(debug=True, port=5000)
