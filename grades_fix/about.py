from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

# the address of the GitHub repository of this exercise
GITHUB_URL = "https://github.com/gorenlevy-crypto/exc4-files-and-graphs"


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(420, 300)

        self.title_label = QLabel("Grades Correction")
        self.title_label.setObjectName("aboutTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.info_label = QLabel(
            "Shows the students' grades from a csv file,\n"
            "adds bonus points to everyone (up to 100)\n"
            "and saves the corrected grades back to the file."
        )
        self.info_label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel("Created by: Goren Levy")
        self.name_label.setObjectName("aboutName")
        self.name_label.setAlignment(Qt.AlignCenter)

        self.course_label = QLabel("Files and Graphs exercise - Afeka")
        self.course_label.setObjectName("hint")
        self.course_label.setAlignment(Qt.AlignCenter)

        self.github_label = QLabel(f'GitHub: <a href="{GITHUB_URL}">{GITHUB_URL}</a>')
        self.github_label.setAlignment(Qt.AlignCenter)
        self.github_label.setOpenExternalLinks(True)
        self.github_label.setTextInteractionFlags(Qt.TextBrowserInteraction)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        layout.addWidget(self.title_label)
        layout.addWidget(self.info_label)
        layout.addStretch()
        layout.addWidget(self.name_label)
        layout.addWidget(self.course_label)
        layout.addWidget(self.github_label)
