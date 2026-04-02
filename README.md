# 🎓 Flask Student Management Dashboard

A full-featured Flask web application for managing students, courses, and users with authentication, REST APIs, and a clean dashboard UI.

---
## 🌐 Live Demo

https://flask-student-management-dashboard-fvhv.onrender.com

---
## 🚀 Features

* 🔐 Authentication system (Register / Login / Logout)
* 👤 User roles (Admin & Normal User)
* 🎓 Student management (CRUD + course assignment)
* 📘 Course management (CRUD + descriptions)
* 🧑‍💻 Admin panel for managing users
* 🌐 REST API for all resources
* 🔍 Search + pagination for students
* 🎨 Clean UI using HTML, CSS, and Jinja templates
* ⚠️ Error handling (404, 403, 500)
* 🧪 Flask test suite
* 🔒 Protected routes using Flask-Login
* 🛡️ Admin-only access for user management
---

## 🏗️ Project Structure

```
.
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── utils/
│   ├── config.py
│   ├── extensions.py
│   └── __init__.py
│
├── tests/
├── run.py
├── requirements.txt
└── README.md
```
---
## 🧠 Architecture

The project follows a modular architecture:

- **Routes (Blueprints)** → handle HTTP requests
- **Services** → contain business logic
- **Models** → define database structure
- **Utils** → validation and helpers
---

## ⚙️ Technologies Used

* Python 3
* Flask
* Flask-Login
* Flask-SQLAlchemy
* SQLite (for development)
* Gunicorn (for production)
* Jinja2 Templates
* HTML/CSS

---
## 🧩 Database Initialization

On first run, the application automatically:

- Creates the database
- Seeds a default admin user

No manual seeding is required.
---

## 🛠️ Installation (Local)

### 1. Clone the repository

```
git clone https://github.com/asmaahassoneh/Flask-Student-Management-Dashboard.git 
cd Flask-Student-Management-Dashboard
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Create `.env` file

```
SECRET_KEY=super-secret-key
DATABASE_URL=sqlite:///students.db
FLASK_ENV=development
```

---

### 5. Run the app

```
python run.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 🔑 Default Admin Account

```
Email: admin@gmail.com
Password: Admin123
```
### ⚠️ Important Notes

* This is for training only
---

## 🌐 REST API Endpoints
> ⚠️ All API endpoints require authentication.
> User endpoints require admin privileges.
### Students

* GET `/api/students`
* GET `/api/students/<student_id>`
* POST `/api/students`
* PUT `/api/students/<student_id>`
* DELETE `/api/students/<student_id>`

### Courses

* GET `/api/courses`
* POST `/api/courses`
* PUT `/api/courses/<id>`
* DELETE `/api/courses/<id>`

### Users (Admin only)

* GET `/api/users`
* POST `/api/users`
* PUT `/api/users/<id>`
* DELETE `/api/users/<id>`

---

## 🧪 Running Tests

```
python -m pytest
```

---

## 🚀 Deployment (Render)

### Build Command

```
pip install -r requirements.txt
```

### Start Command

```
gunicorn run:app
```

### Environment Variables (Render)

```
SECRET_KEY=your-production-secret
FLASK_ENV=production
DATABASE_URL=sqlite:///students.db
```

---

## ⚠️ Important Notes

> ⚠️ SQLite is used for demo purposes.
> On free Render instances, data resets on redeploy due to ephemeral storage.

---

## 💡 Future Improvements

* Switch to PostgreSQL (Render DB)
* Improve UI/UX design
* Deploy frontend separately

---

## 👩‍💻 Author

**Asmaa Hassoneh**
Computer Engineering Student | Backend & Frontend Developer

---

## 📄 License

This project is for educational purposes.
