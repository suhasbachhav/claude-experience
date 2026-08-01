from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from db_config import get_db_context, init_db
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering."""
    search = request.args.get('search', '').lower()
    category = request.args.get('category', '')
    priority = request.args.get('priority', '')

    with get_db_context() as conn:
        cursor = conn.cursor()
        query = """
            SELECT id, title, description, column_name, position, priority,
                   due_date, category, color, created_at, updated_at
            FROM kanban_tasks
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.extend([f'%{search}%', f'%{search}%'])

        if category:
            query += " AND category = ?"
            params.append(category)

        if priority:
            query += " AND priority = ?"
            params.append(priority)

        query += " ORDER BY column_name, position"

        cursor.execute(query, params)
        tasks = cursor.fetchall()

        result = {
            'todo': [],
            'inprogress': [],
            'done': []
        }

        for task in tasks:
            task_obj = {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'column': task[3],
                'priority': task[5],
                'due_date': task[6],
                'category': task[7],
                'color': task[8],
                'created_at': task[9],
                'updated_at': task[10],
            }
            result[task[3]].append(task_obj)

        return jsonify(result)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.json
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    column_name = data.get('column', 'todo')
    priority = data.get('priority', 'medium')
    due_date = data.get('due_date')
    category = data.get('category')
    color = data.get('color', '#667eea')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    if column_name not in ['todo', 'inprogress', 'done']:
        return jsonify({'error': 'Invalid column'}), 400

    if priority not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Invalid priority'}), 400

    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(position) FROM kanban_tasks WHERE column_name = ?", (column_name,))
        max_pos = cursor.fetchone()[0]
        position = (max_pos or 0) + 1

        cursor.execute("""
            INSERT INTO kanban_tasks
            (title, description, column_name, position, priority, due_date, category, color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, description, column_name, position, priority, due_date, category, color))

        task_id = cursor.lastrowid

        return jsonify({
            'id': task_id,
            'title': title,
            'description': description,
            'column': column_name,
            'priority': priority,
            'due_date': due_date,
            'category': category,
            'color': color
        }), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task."""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, description, column_name, position, priority,
                   due_date, category, color, created_at, updated_at
            FROM kanban_tasks WHERE id = ?
        """, (task_id,))
        task = cursor.fetchone()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({
            'id': task[0],
            'title': task[1],
            'description': task[2],
            'column': task[3],
            'position': task[4],
            'priority': task[5],
            'due_date': task[6],
            'category': task[7],
            'color': task[8],
            'created_at': task[9],
            'updated_at': task[10],
        })

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    data = request.json

    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM kanban_tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Task not found'}), 404

        updates = []
        params = []

        for field in ['title', 'description', 'priority', 'due_date', 'category', 'color']:
            if field in data:
                updates.append(f"{field} = ?")
                params.append(data[field])

        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(task_id)

            query = f"UPDATE kanban_tasks SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)

        return jsonify({'message': 'Task updated'}), 200

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
                SET column_name = ?, position = ?, updated_at = ?
                WHERE id = ?
            """, (new_column, new_position, datetime.now().isoformat(), task_id))

        return jsonify({'message': 'Task moved'}), 200

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories."""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, color FROM kanban_categories ORDER BY name")
        categories = cursor.fetchall()
        return jsonify([{
            'id': cat[0],
            'name': cat[1],
            'color': cat[2]
        } for cat in categories])

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Create a new category."""
    data = request.json
    name = data.get('name', '').strip()
    color = data.get('color', '#667eea')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    with get_db_context() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO kanban_categories (name, color)
                VALUES (?, ?)
            """, (name, color))
            category_id = cursor.lastrowid
            return jsonify({
                'id': category_id,
                'name': name,
                'color': color
            }), 201
        except Exception as e:
            return jsonify({'error': 'Category already exists'}), 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get board statistics."""
    with get_db_context() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM kanban_tasks")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM kanban_tasks WHERE column_name = ?", ('done',))
        completed = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM kanban_tasks WHERE priority = ?", ('high',))
        high_priority = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM kanban_tasks
            WHERE due_date IS NOT NULL AND due_date < date('now')
        """)
        overdue = cursor.fetchone()[0]

        return jsonify({
            'total': total,
            'completed': completed,
            'high_priority': high_priority,
            'overdue': overdue
        })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    init_db()
    print("Starting Kanban Server on http://localhost:5001")
    app.run(debug=True, port=5001)
