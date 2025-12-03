# Task-Tracker

A simple working system:
-Start a tsak(25 min default)
-complete a task
-Track progress in Redis (fast for counters + TTL)
-Expose 4 REST endpoints.
-Minimal frontend(just html + js timer OR Postman testing).

Should Implement:
    System Architecture(satoring state cleanly)
    FastAPI practice
    Redis usage
    JWT

Redis Keys.

user:{id}:current_task -> hash

Hash Fields:
    status : running | completed
    start_time : unix timestamp
    duration : seconds (1500 default)

API Endpoints(only 4 required):

    1. POST/login -> returns JWT
    2. POST/task/start -> create/start task
    3. POST/task/complete -> complete task
    4. Get /task/status -> check task progress


