from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# ------------------ HOME ROUTE ------------------
@app.route("/")
def home():
    return {
        "message": "Student API is running",
        "endpoints": {
            "GET /students": "View all students",
            "POST /add": "Add new student",
            "GET /add-test": "Add test student"
        }
    }

# ------------------ DATABASE INIT ------------------
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ------------------ ADD STUDENT (POST) ------------------
@app.route("/add", methods=["POST"])
def add_student():
    data = request.json
    name = data["name"]
    age = data["age"]

    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

    return jsonify({"message": "Student added successfully"})

# ------------------ ADD TEST STUDENT ------------------
@app.route("/add-test")
def add_test():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Deepa", 20))
    conn.commit()
    conn.close()

    return {"message": "Test student added"}

# ------------------ GET STUDENTS ------------------
@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()

    students = []
    for row in rows:
        students.append({
            "id": row[0],
            "name": row[1],
            "age": row[2]
        })

    return jsonify(students)

# ------------------ RUN APP ------------------
if __name__ == "__main__":
    app.run(debug=True)