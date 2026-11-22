from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

# the address of the GitHub repository of this exercise
GITHUB_URL = "https://github.com/gorenlevy-crypto/exc4-files-and-graphs"


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(420, 300)

        self.title_label = QLabel("Ice Cream Revenue")
        self.title_label.setObjectName("aboutTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.info_label = QLabel(
            "Shows the revenue of an ice cream truck (USA)\n"
            "against the outside temperature of the same day,\n"
            "with the straight trend line that fits the data."
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
