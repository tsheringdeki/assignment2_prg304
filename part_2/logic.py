from database import (
    execute_query,
    fetch_all,
    issue_book_transaction
)

from datetime import date


# ========== BOOK FUNCTIONS ==========

def add_book(title, author, category, quantity):

    if not title or not author or not category:
        return False, "Please fill in all book details."

    if quantity <= 0:
        return False, "Quantity must be greater than zero."

    execute_query("""
        INSERT INTO books
        (title, author, category, quantity)
        VALUES (?, ?, ?, ?)
    """, (title, author, category, quantity))

    return True, "Book added successfully!"


def get_books():

    return fetch_all(
        "SELECT * FROM books ORDER BY id DESC"
    )


def delete_book(book_id):

    active = fetch_all("""
        SELECT id FROM loans
        WHERE book_id = ? AND status = 'Issued'
    """, (book_id,))

    if active:
        return False, "Return this book before deleting it."

    execute_query(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )

    return True, "Book deleted successfully!"


# ========== STUDENT FUNCTIONS ==========

def add_student(name, student_id, class_name):

    if not name or not student_id or not class_name:
        return False, "Please fill in all student details."

    try:

        execute_query("""
            INSERT INTO students
            (name, student_id, class_name)
            VALUES (?, ?, ?)
        """, (name, student_id, class_name))

        return True, "Student registered successfully!"

    except Exception:

        return False, "Student ID already exists."


def get_students():

    return fetch_all(
        "SELECT * FROM students ORDER BY id DESC"
    )


# ========== ISSUE BOOK FUNCTION ==========

def issue_book(book_id, student_id):

    return issue_book_transaction(
        book_id,
        student_id,
        str(date.today())
    )


# ========== RETURN BOOK FUNCTION ==========

def return_book(loan_id):

    loans = fetch_all("""
        SELECT book_id
        FROM loans
        WHERE id = ? AND status = 'Issued'
    """, (loan_id,))

    if not loans:
        return False, "No active issue record found."

    book_id = loans[0][0]

    execute_query("""
        UPDATE loans
        SET status = 'Returned',
            return_date = ?
        WHERE id = ?
    """, (str(date.today()), loan_id))

    execute_query("""
        UPDATE books
        SET quantity = quantity + 1
        WHERE id = ?
    """, (book_id,))

    return True, "Book returned successfully!"


# ========== RECORD FUNCTIONS ==========

def get_records():

    return fetch_all("""
        SELECT
            loans.id,
            books.title,
            students.name,
            students.student_id,
            loans.issue_date,
            loans.return_date,
            loans.status

        FROM loans

        JOIN books
        ON loans.book_id = books.id

        JOIN students
        ON loans.student_id = students.id

        ORDER BY loans.id DESC
    """)


def get_active_loans():

    return fetch_all("""
        SELECT
            loans.id,
            books.title,
            students.name,
            students.student_id,
            loans.issue_date

        FROM loans

        JOIN books
        ON loans.book_id = books.id

        JOIN students
        ON loans.student_id = students.id

        WHERE loans.status = 'Issued'

        ORDER BY loans.id DESC
    """)


# ========== DASHBOARD FUNCTION ==========

def get_dashboard():

    total_books = fetch_all(
        "SELECT COUNT(*) FROM books"
    )[0][0]

    total_students = fetch_all(
        "SELECT COUNT(*) FROM students"
    )[0][0]

    issued_books = fetch_all(
        "SELECT COUNT(*) FROM loans WHERE status='Issued'"
    )[0][0]

    returned_books = fetch_all(
        "SELECT COUNT(*) FROM loans WHERE status='Returned'"
    )[0][0]

    return (
        total_books,
        total_students,
        issued_books,
        returned_books
    )
