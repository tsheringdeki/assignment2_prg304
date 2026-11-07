
import sqlite3
from pathlib import Path

# Database location
BASE_DIR = Path(__file__).resolve().parent
DB_FOLDER = BASE_DIR / "database"
DB_FOLDER.mkdir(exist_ok=True)

DB_NAME = DB_FOLDER / "library.db"


# Connect to database
def connect():

    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# Create database tables
def create_tables():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'Issued',

            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


# Insert, update and delete
def execute_query(query, values=()):

    conn = connect()

    try:

        cursor = conn.cursor()
        cursor.execute(query, values)

        conn.commit()

    finally:
        conn.close()


# Retrieve records
def fetch_all(query, values=()):

    conn = connect()

    try:

        cursor = conn.cursor()
        cursor.execute(query, values)

        result = cursor.fetchall()

        return result

    finally:
        conn.close()


# Issue book using a database transaction
def issue_book_transaction(book_id, student_id, issue_date):

    conn = connect()

    try:

        cursor = conn.cursor()

        cursor.execute(
            "SELECT quantity FROM books WHERE id = ?",
            (book_id,)
        )

        book = cursor.fetchone()

        if book is None:
            return False, "Book not found."

        if book[0] <= 0:
            return False, "No copies of this book are available."

        cursor.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            return False, "Student not found."

        cursor.execute("""
            INSERT INTO loans
            (book_id, student_id, issue_date, status)
            VALUES (?, ?, ?, 'Issued')
        """, (book_id, student_id, issue_date))

        cursor.execute("""
            UPDATE books
            SET quantity = quantity - 1
            WHERE id = ?
        """, (book_id,))

        conn.commit()

        return True, "Book issued successfully!"

    except Exception as error:

        conn.rollback()

        return False, str(error)

    finally:
        conn.close()


# Return book using a database transaction
def return_book_transaction(loan_id, return_date):

    conn = connect()

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT book_id
            FROM loans
            WHERE id = ? AND status = 'Issued'
        """, (loan_id,))

        loan = cursor.fetchone()

        if loan is None:
            return False, "No active issue record found."

        book_id = loan[0]

        cursor.execute("""
            UPDATE loans
            SET status = 'Returned',
                return_date = ?
            WHERE id = ?
        """, (return_date, loan_id))

        cursor.execute("""
            UPDATE books
            SET quantity = quantity + 1
            WHERE id = ?
        """, (book_id,))

        conn.commit()

        return True, "Book returned successfully!"

    except Exception as error:

        conn.rollback()

        return False, str(error)

    finally:
        conn.close()
