from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE SETUP
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll TEXT,
    branch TEXT,
    year TEXT
)
""")
conn.commit()

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.post("/login")
def login(data: dict):
    roll = data.get("roll")
    branch = data.get("branch")
    year = data.get("year")

    cursor.execute(
        "SELECT * FROM students WHERE roll=? AND branch=? AND year=?",
        (roll, branch, year)
    )
    student = cursor.fetchone()

    if student:
        return {"status": "success"}
    else:
        return {"status": "fail"}
cursor.execute("""
CREATE TABLE IF NOT EXISTS doubts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT
)
""")
conn.commit()

@app.post("/add_doubt")
def add_doubt(data: dict):
    question = data.get("question")

    cursor.execute(
        "INSERT INTO doubts (question, answer) VALUES (?, ?)",
        (question, "")
    )
    conn.commit()

    return {"status": "success"}

@app.get("/get_doubts")
def get_doubts():
    cursor.execute("SELECT * FROM doubts")
    doubts = cursor.fetchall()

    result = []
    for d in doubts:
        result.append({
            "id": d[0],
            "question": d[1],
            "answer": d[2]
        })

    return result

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    topic TEXT,
    content TEXT
)
""")
conn.commit()

@app.post("/add_note")
def add_note(data: dict):

    subject = data.get("subject")
    topic = data.get("topic")
    content = data.get("content")

    cursor.execute(
        "INSERT INTO notes (subject, topic, content) VALUES (?, ?, ?)",
        (subject, topic, content)
    )
    conn.commit()

    return {"status": "note added"}
@app.post("/answer_doubt")
def answer_doubt(data: dict):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE doubts SET answer=? WHERE id=?",
        (data["answer"], data["doubt_id"])
    )

    conn.commit()
    conn.close()

    return {"status": "Answer saved"}

@app.get("/get_notes")
def get_notes():

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    result = []

    for n in notes:
        result.append({
            "id": n[0],
            "subject": n[1],
            "topic": n[2],
            "content": n[3]
        })

    return result

from fastapi.responses import FileResponse
import os

@app.get("/get_books")
def get_books():

    files = os.listdir("library")

    pdfs = [f for f in files if f.endswith(".pdf")]

    return pdfs

@app.get("/book/{filename}")
def get_book(filename: str):

    path = f"library/{filename}"

    return FileResponse(path)

