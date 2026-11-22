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

        # ============================ TODO - your part ============================
        # file_name holds the full path of the file the user chose.
        # 1. Save file_name in self.selected_file
        # 2. Empty the three lists (in case a file was already loaded before)
        # 3. Open the file for reading and go over its lines.
        #    The first line is the header (ID,Grade) - skip it.
        # 4. For every other line: split it by ',' and add the ID (keep it as text)
        #    to self.student_ids and the grade (as int) to self.original_grades
        # 5. Put the same grades in self.corrected_grades too
        #    (careful: a copy of the values, not the same list object!)
        # ==========================================================================

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

            # show a corrected grade that changed in green
            if corrected != original:
                corrected_item = self.table.item(row, 2)
                corrected_item.setForeground(QColor("#15803d"))
                corrected_item.setFont(bold)

    def add_bonus(self):
        bonus = self.bonus_input.value()

        # ============================ TODO - your part ============================
        # Go over self.original_grades and self.corrected_grades (with an index).
        # Each corrected grade = the original grade + bonus, but not more than 100.
        # ==========================================================================

        self.update_table()

    def update_file(self):
        if self.selected_file == '':
            QMessageBox.warning(self, "No file", "Please load a students file first.")
            return

        # ============================ TODO - your part ============================
        # Overwrite the file self.selected_file with the new data:
        # - first the same header line as in the original file
        #   (tip: read it from the file before you open it for writing)
        # - then one line for every student: the ID and the CORRECTED grade, with ','
        # The file must stay exactly like the original - only the grades change.
        # ==========================================================================

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
