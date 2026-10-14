import os
import sqlite3
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
DATABASE = os.getenv("DATABASE", "/data/notes.db")
APP_NAME = os.getenv("APP_NAME", "Fatima's Notes")

PAGE = """
<!doctype html>
<html>
<head>
  <title>{{ app_name }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { max-width: 700px; margin: 40px auto; padding: 0 16px;
           font: 16px Arial, sans-serif; background: #f4f6f8; }
    h1 { color: #233; }
    form, li { background: white; padding: 14px; margin: 12px 0;
               border-radius: 8px; }
    input { padding: 10px; width: 70%; }
    button { padding: 10px; cursor: pointer; }
    li { display: flex; justify-content: space-between; gap: 12px; }
  </style>
</head>
<body>
  <h1>{{ app_name }}</h1>
  <form method="post" action="/add">
    <input name="text" placeholder="Write a note..." required>
    <button type="submit">Add note</button>
  </form>
  <ul>
    {% for note in notes %}
      <li>
        <span>{{ note[1] }}</span>
        <form method="post" action="/delete/{{ note[0] }}">
          <button type="submit">Delete</button>
        </form>
      </li>
    {% else %}
      <li>No notes yet.</li>
    {% endfor %}
  </ul>
</body>
</html>
"""


def connect():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    return sqlite3.connect(DATABASE)


def initialize():
    with connect() as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL)"
        )


@app.get("/")
def home():
    with connect() as db:
        notes = db.execute("SELECT id, text FROM notes ORDER BY id DESC").fetchall()
    return render_template_string(PAGE, notes=notes, app_name=APP_NAME)


@app.post("/add")
def add_note():
    text = request.form.get("text", "").strip()
    if text:
        with connect() as db:
            db.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    return redirect("/")


@app.post("/delete/<int:note_id>")
def delete_note(note_id):
    with connect() as db:
        db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    return redirect("/")


initialize()
print(f"{APP_NAME} is ready on port 5000")
app.run(host="0.0.0.0", port=5000)