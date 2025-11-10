# comp3005a3
COMP 3005 Assignmnent 3 by Musab Farah - 101274894
Student: Musab Farah
Student Number: 101274894
This project implements a PostgreSQL database and Python application that performs CRUD
operations on a students table.

Requirements:
- Python 3.9+
- PostgreSQL 15+
- pgAdmin recommended
- pip package manager

Setup:
1. Install dependencies:
cd C:\Users\Capta\OneDrive\Desktop\3005a3
python -m venv .venv
. .\.venv\Scripts\Activate
pip install --upgrade pip
pip install -r requirements.txt
2. Create PostgreSQL database:
psql -U postgres -h localhost -p 5432 -W -d postgres
CREATE DATABASE school_db;
\l
\q
3. Configure .env:
PGHOST=localhost
PGPORT=5432
PGDATABASE=school_db
PGUSER=postgres
PGPASSWORD=
4. Initialize:
python app.py init-db
CRUD Commands:
- python app.py list
- python app.py add --first Alice --last Lee --email alice.lee@example.com --date 2023-09-05
- python app.py update-email --id 1 --email john.updated@example.com
- python app.py delete --id 2
