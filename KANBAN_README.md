# Kanban Board with Python Backend

An enhanced Kanban board application with a Flask backend and SQLite database for persistent task storage.

## Features

✨ **Enhanced Frontend:**
- Modern, responsive UI with gradient background
- Drag-and-drop task management
- Real-time task count per column
- Smooth animations and transitions
- Error notifications
- Loading states
- Empty state messages

🔧 **Backend API:**
- RESTful API built with Flask
- SQLite database for persistence
- Task CRUD operations (Create, Read, Update, Delete)
- Column management (To Do, In Progress, Done)
- CORS enabled for frontend-backend communication

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
python kanban_server.py
```

The server will start on `http://localhost:5000`

### 3. Open the Frontend

Open `kanban.html` in your web browser:
- Double-click the file, or
- Use a local server: `python -m http.server 8000` and visit `http://localhost:8000/kanban.html`

## API Endpoints

### Get All Tasks
```
GET /api/tasks
```
Returns tasks organized by column (todo, inprogress, done)

### Create a Task
```
POST /api/tasks
Content-Type: application/json

{
  "title": "Task description",
  "column": "todo"
}
```

### Delete a Task
```
DELETE /api/tasks/{task_id}
```

### Move a Task
```
PATCH /api/tasks/{task_id}/move
Content-Type: application/json

{
  "column": "inprogress"
}
```

### Health Check
```
GET /health
```

## Database

Tasks are stored in SQLite at `orders.db` in the `kanban_tasks` table with:
- `id`: Unique identifier
- `title`: Task description
- `column_name`: Current column (todo, inprogress, done)
- `position`: Order within column
- `created_at`: Timestamp of creation

## Usage

1. **Add a Task**: Type in the input field of any column and click "Add Task" or press Enter
2. **Move a Task**: Drag and drop a card between columns
3. **Delete a Task**: Click the ✕ button on a card

## Troubleshooting

**Connection Error**: Make sure the backend server is running on port 5000
**CORS Error**: Flask-CORS is configured to allow cross-origin requests
**Database Error**: Check that `orders.db` is in the same directory as the scripts
