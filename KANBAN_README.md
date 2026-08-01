# Advanced Kanban Board

A comprehensive Kanban board application with a powerful Flask backend, SQLite database, and a modern, feature-rich frontend.

## 🚀 Features

### Frontend Features
✨ **Advanced UI Components:**
- Modern, responsive design with gradient backgrounds
- Dark mode toggle
- Real-time task statistics dashboard
- Priority filtering (High, Medium, Low)
- Search functionality
- Task categories with custom colors
- Due date tracking with overdue indicators
- Priority badges
- Drag-and-drop between columns
- Task editing modal with full details
- Keyboard shortcuts (Enter to add)
- Smooth animations and transitions

### Backend Features
🔧 **Powerful API:**
- RESTful API built with Flask
- Full task CRUD operations
- Search and filtering capabilities
- Category management
- Statistics endpoint
- Due date handling
- Priority levels
- Task descriptions
- Timestamp tracking (created_at, updated_at)

### Database Features
💾 **Persistent Storage:**
- SQLite database with robust schema
- Tasks table with rich fields
- Categories table with color coding
- Automatic sample data initialization
- Atomic transactions

## 📋 Task Properties

Each task includes:
- **Title**: Task name (required)
- **Description**: Detailed task information
- **Priority**: Low, Medium, or High
- **Category**: Organize by project/type
- **Due Date**: Track deadlines
- **Color**: Visual identifier
- **Column**: Current status (To Do, In Progress, Done)
- **Timestamps**: Creation and update times

## 🛠️ Setup & Installation

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Start the Backend Server

```bash
python3 kanban_server.py
```

Server runs on: `http://localhost:5001`

### 3. Open the Frontend

**Option A - Direct File:**
- Double-click `kanban_advanced.html` in Finder

**Option B - Local Web Server:**
```bash
python3 -m http.server 8000
```
Visit: `http://localhost:8000/kanban_advanced.html`

## 📚 API Reference

### Tasks

#### Get All Tasks (with filtering)
```
GET /api/tasks
Query Parameters:
  - search: Search in title/description
  - category: Filter by category name
  - priority: Filter by priority (low, medium, high)

Response:
{
  "todo": [{"id": 1, "title": "...", ...}],
  "inprogress": [...],
  "done": [...]
}
```

#### Create Task
```
POST /api/tasks
Content-Type: application/json

{
  "title": "Task title",
  "description": "Task description",
  "column": "todo",
  "priority": "medium",
  "due_date": "2026-08-15",
  "category": "Design",
  "color": "#667eea"
}
```

#### Get Single Task
```
GET /api/tasks/{task_id}
```

#### Update Task
```
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "priority": "high",
  "due_date": "2026-08-20",
  "category": "Backend",
  "color": "#4ecdc4"
}
```

#### Delete Task
```
DELETE /api/tasks/{task_id}
```

#### Move Task to Different Column
```
PATCH /api/tasks/{task_id}/move
Content-Type: application/json

{
  "column": "inprogress"
}
```

### Categories

#### Get All Categories
```
GET /api/categories
Response:
[
  {"id": 1, "name": "Design", "color": "#ff6b6b"},
  {"id": 2, "name": "Backend", "color": "#4ecdc4"}
]
```

#### Create Category
```
POST /api/categories
Content-Type: application/json

{
  "name": "Testing",
  "color": "#ffeaa7"
}
```

### Statistics

#### Get Board Statistics
```
GET /api/stats
Response:
{
  "total": 15,
  "completed": 8,
  "high_priority": 3,
  "overdue": 1
}
```

### Health Check
```
GET /health
Response: {"status": "ok"}
```

## 🎨 User Interface Guide

### Main Dashboard
- **Search Bar**: Find tasks by title or description
- **Statistics Cards**: View total, completed, high-priority, and overdue tasks
- **Priority Filters**: Quick filter by priority level
- **Dark Mode Toggle**: Switch theme (moon icon)

### Task Columns
- **To Do**: New tasks
- **In Progress**: Active tasks
- **Done**: Completed tasks

### Task Cards
- **Title & Priority Badge**: Task name with priority indicator
- **Description**: Preview of full description (max 2 lines)
- **Category & Due Date**: Organized metadata
- **Action Buttons**: Edit and Delete options
- **Color Bar**: Visual identifier from category/custom color

### Modal Window
- **Create/Edit Mode**: Auto-detects based on context
- **Form Fields**: Title, description, priority, category, due date
- **Auto-Save**: Submit and instantly see updates
- **Keyboard**: Esc to close

## ⌨️ Keyboard Shortcuts

- **Enter** in task input field: Add new task
- **Esc**: Close modal windows
- **Click Moon Icon (🌙)**: Toggle dark mode

## 🎯 Usage Examples

### Adding a Task
1. Click "+ New Task" button or type in a column
2. Fill in title (required)
3. Add description, priority, category, due date (optional)
4. Click "Save Task"

### Moving a Task
1. Click and drag a card between columns
2. Task status updates automatically
3. Watch the statistics refresh

### Editing a Task
1. Click "Edit" button on any card
2. Modal opens with task details
3. Modify any field
4. Click "Save Task"

### Searching
1. Type in search bar at top
2. Results filter in real-time
3. Clear search to show all tasks

### Filtering
1. Click priority buttons (All, High, Medium, Low)
2. Active filter highlighted in white
3. Task list updates instantly

## 🗄️ Database Schema

### kanban_tasks Table
```sql
CREATE TABLE kanban_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    column_name TEXT NOT NULL,
    position INTEGER NOT NULL,
    priority TEXT DEFAULT 'medium',
    due_date TEXT,
    category TEXT,
    color TEXT DEFAULT '#667eea',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### kanban_categories Table
```sql
CREATE TABLE kanban_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT DEFAULT '#667eea',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused on 5001 | Ensure server is running: `python3 kanban_server.py` |
| CORS errors | Flask-CORS enabled; check server logs |
| Tasks not saving | Verify database file exists: `orders.db` |
| Modal not closing | Click outside modal or press Esc |
| Search not working | Ensure server is running and responding |
| Drag-drop not working | Try different column; refresh page if stuck |

## 📦 Files

- `kanban_server.py` - Flask backend server
- `kanban_advanced.html` - Advanced UI with all features
- `kanban.html` - Basic UI (simple version)
- `db_config.py` - Database configuration
- `requirements.txt` - Python dependencies
- `orders.db` - SQLite database (auto-created)

## 🚀 Performance Tips

- Keep description text concise for better UX
- Use categories to organize large task sets
- Regular backups of `orders.db` for production
- Use due dates to prioritize workflow
- Monitor `/api/stats` for insights

## 🔮 Future Enhancements

- User authentication & multi-user support
- Task comments & collaboration
- Recurring tasks
- File attachments
- Activity history & audit logs
- Export to CSV/PDF
- Calendar view
- Notifications & reminders
