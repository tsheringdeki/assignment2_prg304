
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Hello PyQt6")
window.setGeometry(200, 200, 400, 250)

heading = QLabel("Hello World!")

button = QPushButton("Click Me")


def button_clicked():
    heading.setText("Welcome to PyQt6!")


button.clicked.connect(button_clicked)

layout = QVBoxLayout()

layout.addWidget(heading)
layout.addWidget(button)

window.setLayout(layout)

window.show()

sys.exit(app.exec())
