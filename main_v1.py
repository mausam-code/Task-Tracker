from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import time
import jwt
import redis

SECRET = "season-secret-key"

app = FastAPI()

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# CORS for minimal frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
def login():
    token = jwt.encode({"user_id": "1"}, SECRET, algorithm="HS256")
    return {"token": token}

@app.post("/task/start")
def start_task(user_id: str = Depends(get_current_user)):
    start = int(time.time())
    key = f"user:{user_id}:current_task"

    r.hset(key, mapping={
        "status": "running",
        "start_time": start,
        "duration": 25 * 60
    })

    return {"message": "Task started", "start": start}

@app.post("/task/complete")
def complete_task(user_id: str = Depends(get_current_user)):
    key = f"user:{user_id}:current_task"

    if not r.exists(key):
        raise HTTPException(404, "No active task")

    r.hset(key, "status", "completed")

    return {"message": "Task completed"}

@app.get("/task/status")
def task_status(user_id: str = Depends(get_current_user)):
    key = f"user:{user_id}:current_task"

    if not r.exists(key):
        return {"status": "no_task"}

    data = r.hgetall(key)
    now = int(time.time())
    elapsed = now - int(data["start_time"])
    remaining = int(data["duration"]) - elapsed

    return {
        "status": data["status"],
        "elapsed": elapsed,
        "remaining": max(remaining, 0)
    }
