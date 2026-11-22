import os
import sys

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QFrame,
    QHBoxLayout, QVBoxLayout,
)

from about import About

# the folder of this file - so style.qss is found no matter where we run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Revenue")
        self.resize(950, 700)

        # ============================ TODO - your part ============================
        # Define here the two lists that the data of the file will be loaded into
        # (one for the temperatures and one for the revenues).
        # ==========================================================================

        # ---------- title ----------
        self.title_label = QLabel("Ice Cream Revenue vs. Temperature")
        self.title_label.setObjectName("title")
        self.subtitle_label = QLabel("Load the ice cream truck file to see the graph and its trend line")
        self.subtitle_label.setObjectName("subtitle")

        # ---------- choose file + about ----------
        self.load_button = QPushButton("Load File...")
        self.load_button.setObjectName("primary")
        self.load_button.clicked.connect(self.load_file)

        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("fileLabel")

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.open_about)

        top_row = QHBoxLayout()
        top_row.addWidget(self.load_button)
        top_row.addWidget(self.file_label, 1)
        top_row.addWidget(self.about_button)

        # ---------- matplotlib graph + toolbar (zoom, pan, save as file) ----------
        self.figure = Figure(figsize=(8, 5), tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.graph_card = QFrame()
        self.graph_card.setObjectName("graphCard")
        card_layout = QVBoxLayout(self.graph_card)
        card_layout.setContentsMargins(10, 6, 10, 10)
        card_layout.addWidget(self.toolbar)
        card_layout.addWidget(self.canvas, 1)

        # ---------- put everything together ----------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(12)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)
        main_layout.addLayout(top_row)
        main_layout.addWidget(self.graph_card, 1)

        self.show_empty_graph()

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Choose the ice cream file", "", "CSV files (*.csv);;All files (*)"
        )
        if file_name == '':
            return  # the user pressed Cancel

        # ============================ TODO - your part ============================
        # file_name holds the full path of the file the user chose.
        # 1. Empty your two lists (in case a file was already loaded before)
        # 2. Open the file for reading and go over its lines.
        #    The first line is the header (Temperature,Revenue) - skip it.
        # 3. Split every other line by ',' and add the two values (as float)
        #    to the two lists you defined in __init__.
        # ==========================================================================

        self.file_label.setText(os.path.basename(file_name))
        self.draw_graph()

    def show_empty_graph(self):
        """What the graph shows before a file is loaded."""
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Load a file to see the graph", ha="center", va="center",
                     transform=self.ax.transAxes, fontsize=14, color="#8a94a6")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def draw_graph(self):
        """Draw the graph. Right now it draws a TEMPORARY graph - replace it with the real one."""
        self.ax.clear()

        # ============================ TODO - your part ============================
        # Replace the temporary graph below with the real one:
        # - a scatter of the data with point size 1 (the 's' argument of self.ax.scatter)
        # - the revenues on the Y axis and the outside temperature on the X axis
        # - remove the top and right lines of the frame (self.ax.spines[...])
        # - a correct title and correct axis titles (set_title, set_xlabel, set_ylabel)
        #
        # Trend line - after the scatter:
        # - use np.polyfit(x, y, 1) to get the slope m and the intercept b
        #   of the straight line that fits the data best
        # - then call: self.draw_trend_line(x, m, b)
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 4, 6]
        self.ax.plot(x, y, marker="o")
        self.ax.set_title("Temporary graph")
        # ==========================================================================

        self.canvas.draw()

    def draw_trend_line(self, x_values, m, b):
        """Draw the straight trend line y = m*x + b over the range of x_values and write its equation."""
        x_line = np.array([min(x_values), max(x_values)])
        y_line = m * x_line + b
        self.ax.plot(x_line, y_line, color="#e4572e", linewidth=2, label="Trend line")

        sign = "+" if b >= 0 else "-"
        equation = f"y = {m:.2f}x {sign} {abs(b):.2f}"
        self.ax.text(0.03, 0.95, equation, transform=self.ax.transAxes,
                     fontsize=12, verticalalignment="top", color="#e4572e",
                     bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#e4572e"))
        self.ax.legend(loc="lower right")

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
