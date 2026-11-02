
import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:5000";

function App() {
  const [students, setStudents] = useState([]);
  const [form, setForm] = useState({
    name: "",
    email: "",
    course: "",
  });
  const [message, setMessage] = useState("");
  const [editingId, setEditingId] = useState(null);

  // Fetch all students
  const loadStudents = async () => {
    try {
      const response = await axios.get(`${API}/students`);
      setStudents(response.data);
    } catch {
      setMessage("Cannot connect to backend.");
    }
  };

  useEffect(() => {
    loadStudents();
  }, []);

  // Handle input changes
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Load selected student details into the form
  const handleEdit = (student) => {
    setForm({
      name: student.name,
      email: student.email,
      course: student.course,
    });

    setEditingId(student.id);
    setMessage("Editing student details.");
  };

  // Add a new student or update an existing student
  const addStudent = async (e) => {
    e.preventDefault();

    try {
      if (editingId !== null) {
        await axios.put(`${API}/students/${editingId}`, form);
        setMessage("Student updated successfully!");
        setEditingId(null);
      } else {
        await axios.post(`${API}/students`, form);
        setMessage("Student added successfully!");
      }

      setForm({ name: "", email: "", course: "" });
      await loadStudents();
    } catch (error) {
      setMessage(
        error.response?.data?.error || "Unable to save student details."
      );
    }
  };

  // Cancel editing
  const cancelEdit = () => {
    setEditingId(null);
    setForm({ name: "", email: "", course: "" });
    setMessage("");
  };

  // Delete a student
  const deleteStudent = async (id) => {
    try {
      await axios.delete(`${API}/students/${id}`);

      if (editingId === id) {
        cancelEdit();
      }

      setMessage("Student deleted successfully!");
      await loadStudents();
    } catch {
      setMessage("Unable to delete student.");
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Cloud-Based Student Management System</h1>
        <p>Manage student information in one place</p>
      </header>

      <main>
        {/* Student Form */}
        <section className="form-section">
          <h2>
            {editingId !== null ? "Edit Student" : "Add New Student"}
          </h2>

          <form onSubmit={addStudent}>
            <input
              name="name"
              placeholder="Student Name"
              value={form.name}
              onChange={handleChange}
              required
            />

            <input
              name="email"
              type="email"
              placeholder="Email Address"
              value={form.email}
              onChange={handleChange}
              required
            />

            <input
              name="course"
              placeholder="Course"
              value={form.course}
              onChange={handleChange}
              required
            />

            <button type="submit">
              {editingId !== null ? "Update Student" : "Add Student"}
            </button>

            {editingId !== null && (
              <button type="button" onClick={cancelEdit}>
                Cancel
              </button>
            )}
          </form>

          {message && <p className="message">{message}</p>}
        </section>

        {/* Student Records Table */}
        <section className="students-section">
          <h2>Student Records ({students.length})</h2>

          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Course</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {students.map((student) => (
                <tr key={student.id}>
                  <td>{student.id}</td>
                  <td>{student.name}</td>
                  <td>{student.email}</td>
                  <td>{student.course}</td>
                  <td>
                    <button
                      type="button"
                      className="edit-button"
                      onClick={() => handleEdit(student)}
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      className="delete-button"
                      onClick={() => deleteStudent(student.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}

              {students.length === 0 && (
                <tr>
                  <td colSpan="5">No student records found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

export default App;
