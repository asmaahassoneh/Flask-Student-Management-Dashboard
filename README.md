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

### 6. Run the app

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

* SQLite is used for development only
* Data may reset on free Render (ephemeral storage)

---

## 💡 Future Improvements

* Switch to PostgreSQL (Render DB)
* Add user profile management
* Improve UI/UX design
* Add API authentication (JWT)
* Deploy frontend separately

---

## 👩‍💻 Author

**Asmaa Hassoneh**
Computer Engineering Student | Backend & Frontend Developer

---

## 📄 License

This project is for educational purposes.
