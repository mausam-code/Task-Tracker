from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import time

app = FastAPI()

# Remove CORS middleware — not needed when serving HTML from same origin
# (unless you plan to host frontend separately later)

# Template folder
templates = Jinja2Templates(directory="templates")

# In-memory tasks storage
tasks = {}
task_counter = 1

# Helper to format time
def format_time(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# Task class
class Task:
    def __init__(self, title, description):
        global task_counter
        self.id = task_counter
        task_counter += 1
        self.title = title
        self.description = description
        self.status = "pending"
        self.time_spent = 0
        self.is_running = False
        self.start_time = None
        self.created_at = datetime.now()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = int(time.time())

    def stop(self):
        if self.is_running:
            elapsed = int(time.time()) - self.start_time
            self.time_spent += elapsed
            self.is_running = False
            self.start_time = None

    def reset(self):
        self.time_spent = 0
        self.is_running = False
        self.start_time = None

    def format_time(self, seconds=None):
        if seconds is None:
            seconds = self.time_spent
            if self.is_running:
                seconds += int(time.time()) - self.start_time
        return format_time(seconds)

# Routes
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": list(tasks.values())})

@app.post("/add_task")
def add_task(title: str = Form(...), description: str = Form("")):
    task = Task(title, description)
    tasks[task.id] = task
    return RedirectResponse("/", status_code=303)

@app.get("/toggle_status/{task_id}")
def toggle_status(task_id: int):
    if task_id in tasks:
        task = tasks[task_id]
        task.status = "completed" if task.status == "pending" else "pending"
    return RedirectResponse("/", status_code=303)

@app.get("/delete_task/{task_id}")
def delete_task(task_id: int):
    if task_id in tasks:
        del tasks[task_id]
    return RedirectResponse("/", status_code=303)

# Timer APIs
@app.get("/start_timer/{task_id}")
def start_timer(task_id: int):
    if task_id not in tasks:
        return JSONResponse({"error": "Task not found"}, status_code=404)
    tasks[task_id].start()
    return {"status": "started"}

@app.get("/stop_timer/{task_id}")
def stop_timer(task_id: int):
    if task_id not in tasks:
        return JSONResponse({"error": "Task not found"}, status_code=404)
    tasks[task_id].stop()
    return {"status": "stopped"}

@app.get("/reset_timer/{task_id}")
def reset_timer(task_id: int):
    if task_id not in tasks:
        return JSONResponse({"error": "Task not found"}, status_code=404)
    tasks[task_id].reset()
    return {"status": "reset"}

@app.get("/get_task_time/{task_id}")
def get_task_time(task_id: int):
    if task_id not in tasks:
        return JSONResponse({"error": "Task not found"}, status_code=404)
    task = tasks[task_id]
    return {
        "formatted_time": task.format_time(),
        "is_running": task.is_running
    }