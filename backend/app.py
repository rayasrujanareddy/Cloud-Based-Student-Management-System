import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

app = Flask(__name__)

CORS(app, resources={
    r"/students(/.*)?": {
        "origins": ["http://localhost:5173"]
    }
})

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@contextmanager
def database_cursor(cursor_factory=None):
    conn = get_db_connection()
    cur = None

    try:
        cur = conn.cursor(cursor_factory=cursor_factory)
        yield cur
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        if cur is not None:
            cur.close()
        conn.close()

def validate_student(data):
    if not isinstance(data, dict):
        return "Invalid request data"

    required_fields = ["name", "email", "course"]

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return f"{field.capitalize()} is required"

    if len(data["name"].strip()) > 100:
        return "Name must not exceed 100 characters"

    if len(data["email"].strip()) > 150:
        return "Email must not exceed 150 characters"

    if len(data["course"].strip()) > 100:
        return "Course must not exceed 100 characters"

    return None

@app.route("/")
def home():
    return "Student Management System API is running!"

@app.route("/students", methods=["GET"])
def get_students():
    with database_cursor(RealDictCursor) as cur:
        cur.execute("SELECT * FROM students ORDER BY id")
        students = cur.fetchall()

    return jsonify(students)



@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    error = validate_student(data)

    if error:
        return jsonify({"error": error}), 400

    try:
        with database_cursor(RealDictCursor) as cur:
            cur.execute(
                """INSERT INTO students (name, email, course)
                   VALUES (%s, %s, %s)
                   RETURNING *""",
                (
                    data["name"].strip(),
                    data["email"].strip(),
                    data["course"].strip()
                )
            )

            student = cur.fetchone()

        return jsonify(student), 201

    except psycopg2.errors.UniqueViolation:
        return jsonify({
            "error": "This email address is already registered."
        }), 409


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True)

    error = validate_student(data)

    if error:
        return jsonify({"error": error}), 400

    try:
        with database_cursor(RealDictCursor) as cur:
            cur.execute(
                """UPDATE students
                   SET name = %s, email = %s, course = %s
                   WHERE id = %s
                   RETURNING *""",
                (
                    data["name"].strip(),
                    data["email"].strip(),
                    data["course"].strip(),
                    student_id
                )
            )

            student = cur.fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(student), 200

    except psycopg2.errors.UniqueViolation:
        return jsonify({
            "error": "This email address is already registered."
        }), 409

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    with database_cursor() as cur:
        cur.execute(
            "DELETE FROM students WHERE id = %s RETURNING id",
            (student_id,)
        )

        deleted = cur.fetchone()

    if deleted is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=False)