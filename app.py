import os
import sys
import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "school_db"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
    )
    conn.autocommit = False
    return conn

def getAllStudents():
    """Retrieve and print all students."""
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT student_id, first_name, last_name, email, enrollment_date
            FROM students
            ORDER BY student_id;
        """)
        rows = cur.fetchall()
        if not rows:
            print("No students found.")
            return rows

        print(f"{'ID':<4}  {'First':<12} {'Last':<12} {'Email':<30} {'Enrolled'}")
        print("-" * 85)
        for r in rows:
            print(f"{r['student_id']:<4}  {r['first_name']:<12} {r['last_name']:<12} "
                  f"{r['email']:<30} {r['enrollment_date']}")
        return rows

def addStudent(first_name, last_name, email, enrollment_date):
    """
    Insert a new student.
    - first_name/last_name/email are required (email must be unique)
    - enrollment_date can be None or 'YYYY-MM-DD'
    Returns the new student_id.
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO students(first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id;
            """,
            (first_name, last_name, email, enrollment_date),
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"Inserted student_id={new_id}")
        return new_id

def updateStudentEmail(student_id, new_email):
    """Update email for the given student_id. Returns 1 on success, 0 if not found."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE students SET email = %s WHERE student_id = %s RETURNING student_id;",
            (new_email, student_id),
        )
        row = cur.fetchone()
        if not row:
            conn.rollback()
            print(f"No student found with id={student_id}")
            return 0
        conn.commit()
        print(f"Updated email for student_id={student_id}")
        return 1

def deleteStudent(student_id):
    """Delete the student with the given id. Returns 1 on success, 0 if not found."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id = %s RETURNING student_id;", (student_id,))
        row = cur.fetchone()
        if not row:
            conn.rollback()
            print(f"No student found with id={student_id}")
            return 0
        conn.commit()
        print(f"Deleted student_id={student_id}")
        return 1

def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()
    print("Initialized schema and seeded data.")

def main():
    parser = argparse.ArgumentParser(description="Students CRUD demo (PostgreSQL)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init-db", help="Create table and seed data from schema.sql")
    sub.add_parser("list", help="List all students")

    p_add = sub.add_parser("add", help="Add a new student")
    p_add.add_argument("--first", required=True, help="First name")
    p_add.add_argument("--last", required=True, help="Last name")
    p_add.add_argument("--email", required=True, help="Email (unique)")
    p_add.add_argument("--date", required=False, default=None, help="Enrollment date (YYYY-MM-DD)")

    p_upd = sub.add_parser("update-email", help="Update a student's email")
    p_upd.add_argument("--id", type=int, required=True, help="student_id")
    p_upd.add_argument("--email", required=True, help="New email")

    p_del = sub.add_parser("delete", help="Delete a student by id")
    p_del.add_argument("--id", type=int, required=True, help="student_id")

    args = parser.parse_args()

    try:
        if args.cmd == "init-db":
            init_db()
        elif args.cmd == "list":
            getAllStudents()
        elif args.cmd == "add":
            addStudent(args.first, args.last, args.email, args.date)
        elif args.cmd == "update-email":
            updateStudentEmail(args.id, args.email)
        elif args.cmd == "delete":
            deleteStudent(args.id)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()