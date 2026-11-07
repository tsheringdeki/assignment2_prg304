
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QLabel, QPushButton,
    QLineEdit, QSpinBox, QComboBox,
    QTableWidget, QTableWidgetItem,
    QMessageBox, QGroupBox, QHeaderView
)

from PyQt6.QtCore import Qt

# IMPORTANT: These imports are correct for your folder arrangement
import logic
from database import create_tables


# ================= HELPER FUNCTIONS =================

def show_message(parent, title, message, error=False):

    if error:
        QMessageBox.critical(parent, title, message)
    else:
        QMessageBox.information(parent, title, message)


def create_table(headers):

    table = QTableWidget()

    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)

    table.setEditTriggers(
        QTableWidget.EditTrigger.NoEditTriggers
    )

    table.setSelectionBehavior(
        QTableWidget.SelectionBehavior.SelectRows
    )

    table.setSelectionMode(
        QTableWidget.SelectionMode.SingleSelection
    )

    table.setAlternatingRowColors(True)

    table.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch
    )

    return table


def fill_table(table, rows):

    table.setRowCount(len(rows))

    for r, row_data in enumerate(rows):

        for c, value in enumerate(row_data):

            item = QTableWidgetItem(
                "" if value is None else str(value)
            )

            item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            table.setItem(r, c, item)


def selected_id(table):

    row = table.currentRow()

    if row < 0:
        return None

    item = table.item(row, 0)

    if item is None:
        return None

    return int(item.text())


# ================= MAIN APPLICATION =================

class BookTrack(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "BookTrack - Library Management System | Tshering Deki"
        )

        self.setGeometry(100, 100, 1100, 720)
        self.setMinimumSize(900, 600)

        self.setStyleSheet("""

            QMainWindow {
                background-color: #F4F7FC;
            }

            QWidget {
                font-family: Arial;
                font-size: 13px;
                color: #1B2A4A;
            }

            QLabel#heading {
                font-size: 25px;
                font-weight: bold;
                color: #1B2A4A;
            }

            QLabel#subtitle {
                color: #64748B;
                font-size: 13px;
            }

            QGroupBox {
                background-color: white;
                border: 1px solid #DCE3EF;
                border-radius: 8px;
                margin-top: 12px;
                padding: 12px;
                font-weight: bold;
            }

            QLineEdit, QSpinBox, QComboBox {
                background-color: white;
                border: 1px solid #CBD5E1;
                border-radius: 5px;
                padding: 8px;
            }

            QPushButton {
                background-color: #1B2A4A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 9px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #344B78;
            }

            QPushButton#deleteButton {
                background-color: #DC3545;
            }

            QPushButton#deleteButton:hover {
                background-color: #B52A37;
            }

            QTabWidget::pane {
                background: white;
                border: 1px solid #DCE3EF;
            }

            QTabBar::tab {
                background: #E8EDF5;
                padding: 12px 16px;
            }

            QTabBar::tab:selected {
                background: #1B2A4A;
                color: white;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #F1F5FA;
                gridline-color: #E2E8F0;
            }

            QHeaderView::section {
                background-color: #1B2A4A;
                color: white;
                padding: 8px;
                font-weight: bold;
            }

        """)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_dashboard()
        self.create_books()
        self.create_students()
        self.create_issue()
        self.create_return()
        self.create_records()

        self.refresh_all()


    # ================= DASHBOARD =================

    def create_dashboard(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        heading = QLabel("Welcome to BookTrack")
        heading.setObjectName("heading")

        subtitle = QLabel(
            "Library Book Issue and Return Management System"
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(heading)
        layout.addWidget(subtitle)

        self.dashboard_labels = []

        names = [
            "Total Books",
            "Registered Students",
            "Books Issued",
            "Books Returned"
        ]

        cards = QHBoxLayout()

        for name in names:

            group = QGroupBox(name)
            card_layout = QVBoxLayout(group)

            number = QLabel("0")

            number.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            number.setStyleSheet("""
                font-size: 30px;
                font-weight: bold;
                color: #F59E0B;
                padding: 15px;
            """)

            card_layout.addWidget(number)
            cards.addWidget(group)

            self.dashboard_labels.append(number)

        layout.addLayout(cards)

        info = QLabel(
            "Manage your library books, students, borrowing "
            "and returning records using the tabs above."
        )

        info.setWordWrap(True)

        layout.addWidget(info)
        layout.addStretch()

        self.tabs.addTab(page, "Dashboard")


    # ================= MANAGE BOOKS =================

    def create_books(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        heading = QLabel("Manage Books")
        heading.setObjectName("heading")

        layout.addWidget(heading)

        group = QGroupBox("Add New Book")
        form = QFormLayout(group)

        self.book_title = QLineEdit()
        self.book_author = QLineEdit()
        self.book_category = QLineEdit()

        self.book_quantity = QSpinBox()
        self.book_quantity.setRange(1, 10000)
        self.book_quantity.setValue(1)

        form.addRow("Book Title:", self.book_title)
        form.addRow("Author:", self.book_author)
        form.addRow("Category:", self.book_category)
        form.addRow("Quantity:", self.book_quantity)

        add_button = QPushButton("Add Book")
        add_button.clicked.connect(self.add_book)

        form.addRow(add_button)

        layout.addWidget(group)

        self.books_table = create_table([
            "ID", "Title", "Author", "Category", "Quantity"
        ])

        layout.addWidget(self.books_table)

        delete_button = QPushButton("Delete Selected Book")
        delete_button.setObjectName("deleteButton")
        delete_button.clicked.connect(self.delete_book)

        layout.addWidget(delete_button)

        self.tabs.addTab(page, "Manage Books")


    def add_book(self):

        title = self.book_title.text().strip()
        author = self.book_author.text().strip()
        category = self.book_category.text().strip()
        quantity = self.book_quantity.value()

        success, message = logic.add_book(
            title, author, category, quantity
        )

        show_message(
            self, "Book Information", message, not success
        )

        if success:

            self.book_title.clear()
            self.book_author.clear()
            self.book_category.clear()
            self.book_quantity.setValue(1)

            self.refresh_all()


    def delete_book(self):

        book_id = selected_id(self.books_table)

        if book_id is None:

            show_message(
                self, "Warning",
                "Please select a book first.", True
            )

            return

        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this book?"
        )

        if answer == QMessageBox.StandardButton.Yes:

            success, message = logic.delete_book(book_id)

            show_message(
                self, "Book Information", message, not success
            )

            self.refresh_all()


    # ================= MANAGE STUDENTS =================

    def create_students(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        heading = QLabel("Manage Students")
        heading.setObjectName("heading")

        layout.addWidget(heading)

        group = QGroupBox("Register New Student")
        form = QFormLayout(group)

        self.student_name = QLineEdit()
        self.student_id = QLineEdit()
        self.student_class = QLineEdit()

        form.addRow("Student Name:", self.student_name)
        form.addRow("Student ID:", self.student_id)
        form.addRow("Class:", self.student_class)

        add_button = QPushButton("Register Student")
        add_button.clicked.connect(self.add_student)

        form.addRow(add_button)

        layout.addWidget(group)

        self.students_table = create_table([
            "ID", "Name", "Student ID", "Class"
        ])

        layout.addWidget(self.students_table)

        self.tabs.addTab(page, "Manage Students")


    def add_student(self):

        name = self.student_name.text().strip()
        student_id = self.student_id.text().strip()
        class_name = self.student_class.text().strip()

        success, message = logic.add_student(
            name, student_id, class_name
        )

        show_message(
            self, "Student Information", message, not success
        )

        if success:

            self.student_name.clear()
            self.student_id.clear()
            self.student_class.clear()

            self.refresh_all()


    # ================= ISSUE BOOKS =================

    def create_issue(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        heading = QLabel("Issue Books")
        heading.setObjectName("heading")

        layout.addWidget(heading)

        group = QGroupBox("Issue Book to Student")
        form = QFormLayout(group)

        self.issue_book_combo = QComboBox()
        self.issue_student_combo = QComboBox()

        form.addRow("Select Book:", self.issue_book_combo)
        form.addRow("Select Student:", self.issue_student_combo)

        issue_button = QPushButton("Issue Book")
        issue_button.clicked.connect(self.issue_book)

        form.addRow(issue_button)

        layout.addWidget(group)

        layout.addWidget(QLabel("Currently Issued Books"))

        self.active_table = create_table([
            "Loan ID", "Book Title", "Student Name",
            "Student ID", "Issue Date"
        ])

        layout.addWidget(self.active_table)

        self.tabs.addTab(page, "Issue Books")


    def issue_book(self):

        book_id = self.issue_book_combo.currentData()
        student_id = self.issue_student_combo.currentData()

        if book_id is None:

            show_message(
                self, "Warning",
                "Please add an available book first.", True
            )

            return

        if student_id is None:

            show_message(
                self, "Warning",
                "Please register a student first.", True
            )

            return

        success, message = logic.issue_book(
            book_id, student_id
        )

        show_message(
            self, "Issue Book", message, not success
        )

        self.refresh_all()


    # ================= RETURN BOOKS =================

    def create_return(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        heading = QLabel("Return Books")
        heading.setObjectName("heading")

        layout.addWidget(heading)

        instruction = QLabel(
            "Select an issued book and click Return Book."
        )

        layout.addWidget(instruction)

        self.return_table = create_table([
            "Loan ID", "Book Title", "Student Name",
            "Student ID", "Issue Date"
        ])

        layout.addWidget(self.return_table)

        return_button = QPushButton("Return Selected Book")
        return_button.clicked.connect(self.return_book)

        layout.addWidget(return_button)

        self.tabs.addTab(page, "Return Books")


    def return_book(self):

        loan_id = selected_id(self.return_table)

        if loan_id is None:

            show_message(
                self, "Warning",
                "Please select an issued book first.", True
            )

            return

        answer = QMessageBox.question(
            self,
            "Confirm Return",
            "Are you sure you want to return this book?"
        )

        if answer == QMessageBox.StandardButton.Yes:

            success, message = logic.return_book(loan_id)

            show_message(
                self, "Return Book", message, not success
            )

            self.refresh_all()


    # ================= RECORDS =================

    def create_records(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        heading = QLabel("Library Records")
        heading.setObjectName("heading")

        layout.addWidget(heading)

        self.records_table = create_table([
            "Loan ID", "Book Title", "Student Name",
            "Student ID", "Issue Date",
            "Return Date", "Status"
        ])

        layout.addWidget(self.records_table)

        self.tabs.addTab(page, "Records")


    # ================= REFRESH DATA =================

    def refresh_all(self):

        fill_table(
            self.books_table,
            logic.get_books()
        )

        fill_table(
            self.students_table,
            logic.get_students()
        )

        fill_table(
            self.active_table,
            logic.get_active_loans()
        )

        fill_table(
            self.return_table,
            logic.get_active_loans()
        )

        fill_table(
            self.records_table,
            logic.get_records()
        )

        # Available books
        self.issue_book_combo.clear()

        for book in logic.get_books():

            if book[4] > 0:

                self.issue_book_combo.addItem(
                    f"{book[1]} ({book[4]} available)",
                    book[0]
                )

        # Registered students
        self.issue_student_combo.clear()

        for student in logic.get_students():

            self.issue_student_combo.addItem(
                f"{student[1]} - {student[2]}",
                student[0]
            )

        # Dashboard numbers
        values = logic.get_dashboard()

        for label, value in zip(
            self.dashboard_labels, values
        ):

            label.setText(str(value))


# ================= RUN APPLICATION =================

if __name__ == "__main__":

    create_tables()

    app = QApplication(sys.argv)

    window = BookTrack()
    window.show()

    sys.exit(app.exec())
