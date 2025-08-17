# Teacher Portal

A Django-based web application that allows teachers to manage students, their subjects, and marks. Includes authentication, CSRF/session handling, and a modern TailwindCSS-powered UI.

---

## 🚀 Features

- Teacher login & logout  
- Home dashboard with student list  
- Add student (name, subject, marks)  
- Edit student details via modal  
- Delete student  
- Secure session & CSRF handling  
- PostgreSQL database with `.env` for credentials  
- TailwindCSS-based responsive UI  

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Harshitakar/teacher-portal.git
cd teacher-portal
```

### 2. Create and activate a virtual environment
```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

Make sure PostgreSQL is installed and running.  
Create a database named `portal`:

```bash
psql -U postgres
CREATE DATABASE portal;
\q
```

### 5. Configure environment variables

Create a `.env` file in the project root with:

```ini
DATABASE_NAME=portal
DATABASE_USER=postgres
DATABASE_PASSWORD=root
DATABASE_HOSTNAME=localhost
POSTGRES_PORT=5432
```

### 6. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Teacher (admin)
```bash
python manage.py createteacher username password  # create test teacher
```

### 8. Run the development server
```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Login using the superuser credentials you just created.

---

## 🔐 Security Considerations

- **Secret Key** is kept in `.env` (not hardcoded).  
- CSRF protection is enforced with tokens.  
- Sessions stored securely (move to Redis/DB for production).  
- Debug mode should be disabled in production.  
- Database credentials should never be committed to GitHub.  

---

## 💡 Challenges Faced

- Avoiding **circular imports** when implementing custom middleware.  
- Ensuring **CSRF & session management** without Django’s default `SessionMiddleware`.  
- Making dropdown menus and modals behave correctly across all table rows with Tailwind.  
- Debugging PostgreSQL connection with `.env`.  

---



## Following Are the screenshots attached for referance
<img width="1366" height="768" alt="Screenshot (4)" src="https://github.com/user-attachments/assets/4ca7f425-0203-4c58-89db-a010904ec694" />
<img width="1366" height="768" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/ae4a5f82-b379-4d71-9700-0136b71faf9f" />
<img width="1366" height="768" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/6f46e7af-b770-4c38-a07f-5afc3bc9c32a" />
<img width="1366" height="768" alt="Screenshot (7)" src="https://github.com/user-attachments/assets/9f83c857-3fba-4c51-966c-d0df73de356c" />
<img width="1366" height="768" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/d9873deb-e948-4a0c-a969-44dee7fb9d6a" />


