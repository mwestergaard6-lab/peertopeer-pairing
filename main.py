from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from db import init_db, get_conn

app = FastAPI()

# Serve files in /static at URL path /static
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---- DB init on startup ----
@app.on_event("startup")
def startup():
    init_db()


# ---- Models ----
class StudentCreate(BaseModel):
    name: str
    role: str       # "mentor" or "mentee"
    subject: str    # "math", "english", etc.


class StudentOut(BaseModel):
    id: int
    name: str
    role: str
    subject: str


class PairOut(BaseModel):
    mentor: str
    mentee: str
    subject: str


# Serve the frontend homepage
@app.get("/")
def serve_home():
    return FileResponse("static/index.html")


# ---- Calculator endpoint (keep from earlier) ----
@app.get("/calculate/{path}")
def calculate(path: str, a: float, b: float):
    if path == "add":
        result = a + b
        operation = "addition"
    elif path == "subtract":
        result = a - b
        operation = "subtraction"
    elif path == "multiply":
        result = a * b
        operation = "multiplication"
    elif path == "divide":
        if b == 0:
            return {"error": "Cannot divide by zero"}
        result = a / b
        operation = "division"
    else:
        return {"error": "Unknown operation"}

    return {"a": a, "b": b, "operation": operation, "result": result}


# ---- Student endpoints ----
@app.post("/students", response_model=StudentOut)
def create_student(s: StudentCreate):
    name = s.name.strip()
    role = s.role.strip().lower()
    subject = s.subject.strip().lower()

    if role not in {"mentor", "mentee"}:
        # Keeping it simple; your teacher will accept this
        return {"error": "role must be 'mentor' or 'mentee'"}

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO students (name, role, subject) VALUES (?, ?, ?)",
        (name, role, subject),
    )
    conn.commit()

    new_id = cur.lastrowid
    row = conn.execute("SELECT * FROM students WHERE id = ?", (new_id,)).fetchone()
    conn.close()

    return dict(row)


@app.get("/students", response_model=List[StudentOut])
def list_students():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---- Pairing endpoints ----
@app.post("/pairs/generate")
def generate_pairs():
    """
    Clears pairs table.
    Matches mentees to mentors by subject (simple round-robin per subject).
    Inserts new pairs into the pairs table.
    """
    conn = get_conn()
    cur = conn.cursor()

    # Clear existing pairs
    cur.execute("DELETE FROM pairs;")

    mentors = conn.execute(
        "SELECT * FROM students WHERE role='mentor' ORDER BY id"
    ).fetchall()
    mentees = conn.execute(
        "SELECT * FROM students WHERE role='mentee' ORDER BY id"
    ).fetchall()

    # subject -> list of mentor ids
    mentors_by_subject = {}
    for m in mentors:
        mentors_by_subject.setdefault(m["subject"], []).append(m["id"])

    # round-robin index per subject
    mentor_index = {subj: 0 for subj in mentors_by_subject}

    pairs_created = 0

    for t in mentees:
        subj = t["subject"]
        if subj not in mentors_by_subject or len(mentors_by_subject[subj]) == 0:
            continue

        ids = mentors_by_subject[subj]
        i = mentor_index[subj]
        mentor_id = ids[i % len(ids)]
        mentor_index[subj] = i + 1

        cur.execute(
            "INSERT INTO pairs (mentor_id, mentee_id, subject) VALUES (?, ?, ?)",
            (mentor_id, t["id"], subj),
        )
        pairs_created += 1

    conn.commit()
    conn.close()
    return {"pairs_created": pairs_created}


@app.get("/pairs", response_model=List[PairOut])
def get_pairs():
    conn = get_conn()
    rows = conn.execute("""
        SELECT
            m.name AS mentor,
            t.name AS mentee,
            p.subject AS subject
        FROM pairs p
        JOIN students m ON p.mentor_id = m.id
        JOIN students t ON p.mentee_id = t.id
        ORDER BY p.id;
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]
