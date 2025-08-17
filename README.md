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
<img width="1366" height="768" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/0766cce4-1490-4403-a91c-b65f6d25740b" />
<img width="1366" height="768" alt="Screenshot (10)" src="https://github.com/user-attachments/assets/efcee51f-1196-4361-a286-b6154a5c47c3" />
<img width="1366" height="768" alt="Screenshot (11)" src="https://github.com/user-attachments/assets/e4b20bd1-a6e2-405f-b0aa-900c5cd2b7c6" />
<img width="1366" height="768" alt="Screenshot (12)" src="https://github.com/user-attachments/assets/fb2c342b-a725-4964-988b-903b703829db" />
<img width="1366" height="768" alt="Screenshot (13)" src="https://github.com/user-attachments/assets/6f5843aa-416b-42bd-905f-77976e7466d5" />




