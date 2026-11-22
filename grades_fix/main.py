import os
import subprocess
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QSpinBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QFileDialog,
    QMessageBox, QHBoxLayout, QVBoxLayout,
)

from about import About

# the folder of this file - so style.qss is found no matter where we run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grades Correction")
        self.resize(620, 760)

        # the data of the window
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        # ---------- title ----------
        self.title_label = QLabel("Grades Correction")
        self.title_label.setObjectName("title")
        self.subtitle_label = QLabel("Load the students file, add bonus points and update the file")
        self.subtitle_label.setObjectName("subtitle")

        # ---------- choose file ----------
        self.load_button = QPushButton("Load File...")
        self.load_button.clicked.connect(self.load_file)

        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("fileLabel")

        file_row = QHBoxLayout()
        file_row.addWidget(self.load_button)
        file_row.addWidget(self.file_label, 1)

        # ---------- table: 3 columns, 50 rows ----------
        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)

        # ---------- bonus points (whole number, reacts to ENTER) ----------
        self.bonus_label = QLabel("Bonus points:")
        self.bonus_input = QSpinBox()
        self.bonus_input.setRange(0, 100)
        self.bonus_input.lineEdit().returnPressed.connect(self.add_bonus)

        self.bonus_hint = QLabel("type a number and press Enter")
        self.bonus_hint.setObjectName("hint")

        bonus_row = QHBoxLayout()
        bonus_row.addWidget(self.bonus_label)
        bonus_row.addWidget(self.bonus_input)
        bonus_row.addWidget(self.bonus_hint)
        bonus_row.addStretch()

        # ---------- bottom buttons ----------
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.open_about)

        self.update_button = QPushButton("Update File")
        self.update_button.setObjectName("primary")
        self.update_button.clicked.connect(self.update_file)

        buttons_row = QHBoxLayout()
        buttons_row.addWidget(self.about_button)
        buttons_row.addStretch()
        buttons_row.addWidget(self.update_button)

        # ---------- put everything together ----------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(12)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)
        main_layout.addLayout(file_row)
        main_layout.addWidget(self.table, 1)
        main_layout.addLayout(bonus_row)
        main_layout.addLayout(buttons_row)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Choose the students file", "", "CSV files (*.csv);;All files (*)"
        )
        if file_name == '':
            return  # the user pressed Cancel

        self.selected_file = file_name

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(self.selected_file, 'r') as file:
            file.readline()  # skip the header line (ID,Grade)
            for line in file:
                parts = line.strip().split(',')
                self.student_ids.append(parts[0])
                self.original_grades.append(int(parts[1]))

        self.corrected_grades = self.original_grades.copy()

        self.file_label.setText(os.path.basename(file_name))
        self.update_table()

    def update_table(self):
        """Fill the table from the three lists: student_ids, original_grades, corrected_grades."""
        self.table.clearContents()
        if len(self.student_ids) > self.table.rowCount():
            self.table.setRowCount(len(self.student_ids))

        bold = QFont()
        bold.setBold(True)

        for row, (student_id, original, corrected) in enumerate(
            zip(self.student_ids, self.original_grades, self.corrected_grades)
        ):
            values = [student_id, original, corrected]
            for col in range(3):
                item = QTableWidgetItem(str(values[col]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

            if corrected != original:
                corrected_item = self.table.item(row, 2)
                corrected_item.setForeground(QColor("#15803d"))
                corrected_item.setFont(bold)

    def add_bonus(self):
        bonus = self.bonus_input.value()

        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade

        self.update_table()

    def update_file(self):
        if self.selected_file == '':
            QMessageBox.warning(self, "No file", "Please load a students file first.")
            return

        with open(self.selected_file, 'r') as file:
            header = file.readline().strip()

        with open(self.selected_file, 'w') as file:
            file.write(header + '\n')
            for i in range(len(self.student_ids)):
                file.write(self.student_ids[i] + ',' + str(self.corrected_grades[i]) + '\n')

        self.open_file(self.selected_file)

    def open_file(self, path):
        """Open the file with the default program of the OS (Excel for csv) - works on Windows, Mac and Linux."""
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def open_about(self):
        self.about_window = About()
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open(os.path.join(BASE_DIR, "style.qss"), encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())
    window = MainWindow()
    window.show()
    app.exec()
