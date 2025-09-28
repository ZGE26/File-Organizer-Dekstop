from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class FileOrganizer(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignTop)

        label = QLabel("Organizer File")
        label.setStyleSheet("""
            padding : 8px;
            border: 1px solid white
        """)

        lay.addWidget(label)