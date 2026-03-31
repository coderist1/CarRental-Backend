# 🚗 Rental Car System — Backend API

A Django REST Framework backend for the Rental Car System, supporting user authentication (register/login) and car data management.

---

## 🛠️ Tech Stack

- Python 3.10+
- Django 4.2
- Django REST Framework
- Simple JWT (token-based auth)
- SQLite (development)

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/rentalcar-backend.git
cd rentalcar-backend
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (for Django Admin)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

---

## 📡 API Endpoints

| Method | Endpoint                    | Description          |
|--------|-----------------------------|----------------------|
| POST   | `/api/auth/register/`       | Register new user    |
| POST   | `/api/auth/login/`          | Login & get tokens   |
| POST   | `/api/auth/token/refresh/`  | Refresh access token |
| GET    | `/api/auth/profile/`        | Get current user     |
| GET    | `/api/cars/`                | List all cars        |
| POST   | `/api/cars/`                | Add a new car        |

---

## 🧪 Testing with HTTPie

```bash
# Register
http POST http://127.0.0.1:8000/api/auth/register/ username="johndoe" email="john@example.com" password="pass1234" first_name="John" last_name="Doe"

# Login
http POST http://127.0.0.1:8000/api/auth/login/ username="johndoe" password="pass1234"

# Get profile (use token from login)
http GET http://127.0.0.1:8000/api/auth/profile/ "Authorization: Bearer <access_token>"

# List cars (use token from login)
http GET http://127.0.0.1:8000/api/cars/ "Authorization: Bearer <access_token>"
```

---

## 👤 Author
- Your Name — AppDev Laboratory Activity No. 8
