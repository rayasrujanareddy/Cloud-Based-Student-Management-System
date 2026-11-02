import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


@app.route("/")
def home():
    return "Student Management System API is running!"


@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM students ORDER BY id")
    students = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(students)


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """INSERT INTO students (name, email, course)
           VALUES (%s, %s, %s)
           RETURNING *""",
        (data["name"], data["email"], data["course"])
    )

    student = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(student), 201

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """UPDATE students
           SET name = %s, email = %s, course = %s
           WHERE id = %s
           RETURNING *""",
        (data["name"], data["email"], data["course"], student_id)
    )

    student = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student), 200

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM students WHERE id = %s RETURNING id",
        (student_id,)
    )

    deleted = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if deleted is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})
if __name__ == "__main__":
    app.run(debug=True)