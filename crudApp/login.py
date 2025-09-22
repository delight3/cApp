
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox)
from db import connect_db


class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        self.on_success = on_success

        # Create layout and widgets
        layout = QVBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)

        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)

    def handle_login(self):
        # Connect to database using pymysql 
        conn = connect_db()
        cursor = conn.cursor()
        # Check credentials
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                       (self.user_input.text(), self.pass_input.text()))
        if cursor.fetchone():
            self.on_success()  # Call the success callback
            self.close()       # Close login window
        else:
            QMessageBox.warning(self, "Login Failed",
                                "Invalid username or password")
        cursor.close()
        conn.close()
