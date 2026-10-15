import os
import time

import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

store = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

# Wait briefly for Redis to become ready.
for attempt in range(30):
    try:
        store.ping()
        break
    except redis.RedisError:
        if attempt == 29:
            raise
        time.sleep(1)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/api/notes", methods=["GET", "POST", "OPTIONS"])
def notes():
    if request.method == "OPTIONS":
        return "", 204

    if request.method == "POST":
        text = (request.get_json(silent=True) or {}).get("text", "").strip()
        if text:
            store.rpush("notes", text)
        return jsonify({"saved": bool(text)})

    return jsonify(store.lrange("notes", 0, -1))


print("Notes backend listening on port 5000")
app.run(host="0.0.0.0", port=5000)