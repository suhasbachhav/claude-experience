# 🚀 Quick Start Guide - Advanced Kanban Board

## One-Time Setup

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Start the Server
```bash
python3 kanban_server.py
```

The server will run on: **http://localhost:5001**

### 3. Open the Application
Open **`kanban_advanced.html`** in your web browser

---

## Features at a Glance

### Dashboard
- 📊 **Statistics**: Total tasks, completed, high priority, overdue count
- 🔍 **Search**: Real-time search across all tasks
- 🎨 **Dark Mode**: Toggle with moon icon
- ⚡ **Filters**: Quick filter by priority level

### Task Management
- ✏️ **Edit**: Click "Edit" button on any card to modify details
- 🗑️ **Delete**: Remove tasks instantly
- 🎯 **Priority**: Mark as Low, Medium, or High
- 📅 **Due Dates**: Track deadlines (overdue marked in red)
- 🏷️ **Categories**: Organize by Design, Backend, Frontend, etc.
- 📝 **Descriptions**: Add detailed notes to tasks

### Workflow
- **To Do**: New tasks start here
- **In Progress**: Drag tasks here when working
- **Done**: Complete tasks to track progress

---

## Common Tasks

### Add a New Task
1. Click **"+ New Task"** button
2. Enter title (required)
3. Add optional details (description, priority, due date, category)
4. Click **"Save Task"**

### Move a Task
- **Drag & Drop**: Click and drag card to another column
- **Watch Stats**: Board updates automatically

### Edit a Task
1. Click **"Edit"** on any card
2. Modify any field in the modal
3. Click **"Save Task"**

### Search Tasks
- Type in search bar (top left)
- Results filter in real-time
- Searches title and description

### Filter by Priority
1. Click priority buttons: **All, High, Medium, Low**
2. Active filter shows in white
3. Click **"All"** to reset

---

## Sample Data

The app comes with 3 sample tasks:
- **Design landing page** (To Do, High Priority)
- **Setup database** (In Progress, High Priority)
- **Write documentation** (To Do, Medium Priority)

Feel free to edit or delete these to get started!

---

## Tips & Tricks

🎨 **Color Coding**: Each category has a color - cards display matching color bar
⏰ **Due Dates**: Red background indicates overdue tasks (not in Done column)
🔔 **Overdue Count**: Check statistics card for total overdue tasks
💡 **Descriptions**: Good for context - visible in task cards (2 lines max)
🏷️ **Categories**: Use consistently to organize large boards

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to server | Run `python3 kanban_server.py` |
| Port 5001 already in use | Kill process: `lsof -ti:5001 \| xargs kill -9` |
| Database error | Delete `orders.db` and restart server |
| Drag/drop not working | Refresh browser page |
| Modal won't close | Click outside modal or press Esc |

---

## File Structure

```
📦 Project Root
├── kanban_server.py          # Backend API server
├── kanban_advanced.html      # Advanced UI (recommended)
├── kanban.html               # Basic UI
├── db_config.py              # Database configuration
├── requirements.txt          # Python dependencies
├── orders.db                 # Database (auto-created)
├── KANBAN_README.md          # Full documentation
├── QUICKSTART.md             # This file
└── agent.py                  # Claude API agent (optional)
```

---

## Full Documentation

For complete API reference, database schema, and advanced features, see **`KANBAN_README.md`**

---

## Next Steps

1. ✅ Server running on **http://localhost:5001**
2. ✅ Open **kanban_advanced.html** in browser
3. ✅ Try adding a task
4. ✅ Drag tasks between columns
5. ✅ Edit and organize your workflow

**Happy task management! 🎯**
