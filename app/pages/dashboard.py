# app/pages/dashboard.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PageDashboard(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Ini halaman Dashboard"))

