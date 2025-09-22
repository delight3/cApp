# Import required modules
import csv  # For exporting table data to CSV

# Import PyQt5 widgets and core classes for UI creation
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QWidget, QAction
)
from PyQt5.QtGui import QIntValidator, QIcon  # For input validation and icons
from PyQt5.QtCore import Qt  # For alignment and Qt-related constants

# Import our pymysql database connection function
from db import connect_db

# Main CRUD window class


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set basic window properties
        self.setWindowTitle("Student Management")
        self.setGeometry(100, 100, 800, 500)

        # Create a central widget container
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize the UI, menu bar, styling, and data
        self.setupUI()
        self.setupMenu()
        self.applyStyle()
        self.load_data()

    def setupUI(self):
        layout = QVBoxLayout()  # Main vertical layout

        # Input form layout
        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")  # Placeholder text

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age") 
        # Allow only integers for age
        self.age_input.setValidator(QIntValidator())

        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Course")

        # Add inputs to form layout
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.age_input)
        form_layout.addWidget(self.course_input)

        layout.addLayout(form_layout)  # Add form to main layout

        # Buttons layout
        btn_layout = QHBoxLayout()

        # Create buttons with icons
        self.add_btn = QPushButton(QIcon("resources/add.png"), "Add")
        self.update_btn = QPushButton(QIcon("resources/update.png"), "Update")
        self.delete_btn = QPushButton(QIcon("resources/delete.png"), "Delete")
        self.export_btn = QPushButton(
            QIcon("resources/export.png"), "Export CSV")

        # Add buttons to layout
        for btn in [self.add_btn, self.update_btn, self.delete_btn, self.export_btn]:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        # Connect button actions to their respective methods
        self.add_btn.clicked.connect(self.add_record)
        self.update_btn.clicked.connect(self.update_record)
        self.delete_btn.clicked.connect(self.delete_record)
        self.export_btn.clicked.connect(self.export_csv)

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name...")
        self.search_input.textChanged.connect(self.search)  # Live search
        layout.addWidget(self.search_input)

        # Table for displaying student data
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # ID, Name, Age, Course
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Course"])
        # Load data to inputs on click
        self.table.cellClicked.connect(self.load_row)
        layout.addWidget(self.table)

        # Set layout to central widget
        self.central_widget.setLayout(layout)

    def setupMenu(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        export_action = QAction("Export to CSV", self)
        export_action.triggered.connect(self.export_csv)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(export_action)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: QMessageBox.information(
            self, "About", "Student Manager v1.0\nBuilt with PyQt5"))
        help_menu.addAction(about_action)

    def applyStyle(self):
        # Apply a custom dark theme using QSS
        dark_theme = """
        QWidget { background-color: #2e2e2e; color: #ffffff; font-size: 14px; }
        QLineEdit, QTableWidget { background-color: #3c3c3c; border: 1px solid #5a5a5a; padding: 6px; }
        QPushButton { background-color: #444; color: white; padding: 6px; border-radius: 6px; }
        QPushButton:hover { background-color: #555; }
        QHeaderView::section { background-color: #444; color: white; padding: 4px; border: 1px solid #555; }
        """
        self.setStyleSheet(dark_theme)

    def load_data(self):
        # Load all student records into the table
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()

        self.table.setRowCount(0)  # Clear current table
        for row_num, row_data in enumerate(records):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(
                    row_num, col_num, QTableWidgetItem(str(data)))

        cursor.close()
        conn.close()

    def add_record(self):
        # Add a new student record
        name = self.name_input.text()
        age = self.age_input.text()
        course = self.course_input.text()
        if name and age and course:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
                (name, age, course)
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.load_data()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Input Error", "Fill all fields.")

    def update_record(self):
        # Update the selected student record
        row = self.table.currentRow()
        if row != -1:
            student_id = self.table.item(row, 0).text()
            name = self.name_input.text()
            age = self.age_input.text()
            course = self.course_input.text()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s",
                (name, age, course, student_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.load_data()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Select Row",
                                "Please select a student to update.")

    def delete_record(self):
        # Delete the selected student record
        row = self.table.currentRow()
        if row != -1:
            student_id = self.table.item(row, 0).text()
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_data()
            self.clear_inputs()

    def load_row(self):
        # Load clicked table row into input fields
        row = self.table.currentRow()
        self.name_input.setText(self.table.item(row, 1).text())
        self.age_input.setText(self.table.item(row, 2).text())
        self.course_input.setText(self.table.item(row, 3).text())

    def clear_inputs(self):
        # Clear all input fields
        self.name_input.clear()
        self.age_input.clear()
        self.course_input.clear()

    def search(self, text):
        # Search by name and update the table display
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s", ('%' + text + '%',))
        records = cursor.fetchall()
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(records):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(
                    row_num, col_num, QTableWidgetItem(str(data)))
        cursor.close()
        conn.close()

    def export_csv(self):
        # Export current table data to a CSV file
        path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", "", "CSV Files (*.csv)")
        if path:
            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)

                # Write header
                headers = [self.table.horizontalHeaderItem(
                    i).text() for i in range(self.table.columnCount())]
                writer.writerow(headers)

                # Write each row
                for row in range(self.table.rowCount()):
                    row_data = [self.table.item(row, col).text(
                    ) for col in range(self.table.columnCount())]
                    writer.writerow(row_data)

            QMessageBox.information(
                self, "Export", "CSV Exported successfully!")
