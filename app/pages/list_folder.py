# app/pages/ListFolder.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
import os

class PageListFolder(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 12, 12, 12)
        lay.setSpacing(6)

        lay.addWidget(QLabel("Ini halaman List Folder"))

        import os
        base_dir = r"C:\Users\Arya Ersi Putra\Downloads"
        for name in os.listdir(base_dir):
            lay.addWidget(QLabel(name))

        lay.addStretch()