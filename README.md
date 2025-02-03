# 🚀 FastAPI Boilerplate

This project is a **boilerplate** for **FastAPI** applications with authentication, permissions, async tasks, Redis caching, and much more! 🔥

## 📌 Features

✅ **Authentication & Authorization (JWT)**  
✅ **Role-Based Access Control (RBAC)**  
✅ **WebSockets for Real-Time Updates**  
✅ **Redis Caching for Performance Optimization**  
✅ **Asynchronous Task Execution with Celery**  
✅ **Automated Testing with Pytest & Coverage**  

---

## 🚀 **Installation & Setup**

### 🔹 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 🔹 2️⃣ Create and Activate the Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### 🔹 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 4️⃣ Configure `.env` File
Create a **`.env`** file with the following variables:
```ini
DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
SECRET_KEY=supersecret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SENTRY_DSN=
```

### 🔹 5️⃣ Run Database Migrations
```bash
alembic upgrade head
```

### 🔹 6️⃣ Start FastAPI Server
```bash
uvicorn app.main:app --reload
```
Now access:  
🔗 **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
🔗 **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔥 **Detailed Features**

### 🔐 **Authentication & RBAC (Role-Based Access Control)**
- **JWT Login** (`/auth/login`)
- **User Registration with Role Selection (admin, manager, user)** (`/users/register`)
- **Protected Routes by Role**
  - `/users/admin-only` → **Admin Only**
  - `/users/manager-only` → **Manager Only**
  - `/users/user-data` → **Regular Users Only**

### 🔄 **WebSockets for Real-Time Communication**
```javascript
const socket = new WebSocket("ws://127.0.0.1:8000/ws");
socket.onmessage = (event) => console.log("Received message:", event.data);
socket.send("Hello, WebSocket!");
```

### ⚡ **Redis Caching**
Redis stores frequently accessed data such as users:
```bash
redis-cli
GET user:testuser
```

### ⏳ **Asynchronous Tasks with Celery**
```bash
celery -A app.core.celery.celery worker --loglevel=info
```
Trigger an async task:
```bash
curl -X POST "http://127.0.0.1:8000/tasks/start-task/test-task"
```

### 🧪 **Automated Testing**
Run unit and integration tests:
```bash
pytest
```
Measure test coverage:
```bash
pytest --cov=app --cov-report=term-missing
```
Generate an **HTML coverage report**:
```bash
pytest --cov=app --cov-report=html
```
Then open `htmlcov/index.html` in your browser.

---

## 📜 **Project Structure**
```
📂 app/
│── 📂 api/                 # API Endpoints
│    ├── endpoints/
│    │   ├── auth.py        # JWT Authentication
│    │   ├── users.py       # Users & RBAC
│    │   ├── ws.py          # WebSockets
│    │   ├── tasks.py       # Async Task Execution (Celery)
│── 📂 core/                # Config & Security
│    ├── config.py          # Environment Config (.env)
│    ├── security.py        # Password Hashing & JWT
│    ├── permissions.py     # Role-Based Access Control (RBAC)
│    ├── redis.py           # Redis Integration
│    ├── celery.py          # Celery Configuration
│── 📂 db/                  # Database & Models
│    ├── session.py         # PostgreSQL Connection
│    ├── models.py          # SQLAlchemy Models (Users, Roles)
│── 📂 schemas/             # Data Validation (Pydantic)
│    ├── user.py            # Schemas for Users & Authentication
│── 📂 tests/               # Automated Tests
│    ├── test_users.py      # User & RBAC Tests
│    ├── test_auth.py       # JWT Authentication Tests
│    ├── test_tasks.py      # Celery Task Tests
│── main.py                 # FastAPI Initialization
│── requirements.txt        # Project Dependencies
│── README.md               # Documentation
```

---

## 🤝 **Contributing**
Feel free to contribute! Clone the repository, create a branch, and submit a PR.  

```bash
git checkout -b feature/new-feature
git commit -m ":sparkles: feat: Description of the new feature"
git push origin feature/new-feature
```