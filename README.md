# Cloud-Based Student Management System

A full-stack Student Management System built using React.js, Python Flask and PostgreSQL. The application allows users to manage student records through a simple web interface.

## Technologies Used

- **Frontend:** React.js, JavaScript, CSS
- **Backend:** Python, Flask, REST API
- **Database:** PostgreSQL
- **HTTP Client:** Axios
- **Version Control:** Git and GitHub
- **Cloud:** AWS (deployment planned)

## Features

- Add new student records
- View all student records
- Edit existing student details
- Delete student records
- Store student information in PostgreSQL
- Connect frontend and backend through REST APIs

## Project Structure

```text
Cloud-Based-Student-Management-System/
├── backend/
│   └── app.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
└── .gitignore
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/rayasrujanareddy/Cloud-Based-Student-Management-System.git
cd Cloud-Based-Student-Management-System
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install flask flask-cors flask-sqlalchemy psycopg2-binary python-dotenv
```

Create a `.env` file inside the backend folder with your PostgreSQL connection settings:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

Start the Flask server:

```bash
python app.py
```

Backend runs at `http://127.0.0.1:5000`.

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Project Status

- React frontend implemented.
- Flask REST API implemented.
- PostgreSQL database integration implemented.
- Student CRUD operations implemented and tested.
- GitHub repository created.
- AWS deployment pending.

## Author

Raya Srujana Reddy