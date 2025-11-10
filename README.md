# PostgreSQL Application Programming — COMP3005A — Assignment 3

## Student Information
**Name:** Musab Farah  
**Student ID:** 101274894  

## Demo Video
https://drive.google.com/file/d/1sqsW7XOKYUg8MEMvydDknYpph47hrYda/view?usp=sharing

---

## Install & Setup Instructions

```bash
# Clone or open the project directory
cd 3005a3

# OPTIONAL but recommended: create virtual environment
python -m venv venv

# Windows activation
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 1. Create PostgreSQL Database
Use psql or pgAdmin:

```sql
CREATE DATABASE school_db;
```

### 2. Configure `.env`
Create a file named `.env`:

```
PGHOST=localhost
PGPORT=5432
PGDATABASE=school_db
PGUSER=postgres
PGPASSWORD=<YOUR_POSTGRES_PASSWORD>
```

### 3. Initialize Schema & Seed Data
```bash
python app.py init-db
```

### 4. Run CRUD Functions
```bash
python app.py list
python app.py add --first Alice --last Lee --email alice.lee@example.com --date 2023-09-05
python app.py update-email --id 1 --email john.updated@example.com
python app.py delete --id 2
python app.py list
```

---

## Functions Overview

- **get_connection()** — Connects to PostgreSQL using environment variables.  
- **getAllStudents()** — Fetches and displays all student records.  
- **addStudent()** — Adds a new student to the database.  
- **updateStudentEmail()** — Updates a student’s email using their ID.  
- **deleteStudent()** — Deletes a student by ID.  
- **init_db()** — Creates the students table and inserts initial data.  

---

## Database Schema (from pgAdmin)

```sql
CREATE TABLE IF NOT EXISTS public.students
(
    student_id integer NOT NULL DEFAULT nextval('students_student_id_seq'::regclass),
    first_name text COLLATE pg_catalog."default" NOT NULL,
    last_name text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    enrollment_date date,
    CONSTRAINT students_pkey PRIMARY KEY (student_id),
    CONSTRAINT students_email_key UNIQUE (email)
);
```

---

## Notes to the TA
- CRUD operations demonstrated using terminal + pgAdmin  
- Schema shown in SQL tab  
- Data refreshed after each operation  

---

## Repository Structure
```
3005a3/
│── app.py
│── schema.sql
│── requirements.txt
│── .env.example
└── README.md
```
