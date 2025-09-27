# app/pages/dashboard.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class PageDashboard(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignTop)

        label = QLabel("""
            Aplikasi Pengelola File Sederhana
            ---------------------------------
            Dashboard
            ---------------------------------
            Halaman ini menampilkan informasi umum
            tentang aplikasi dan fungsionalitasnya.
            ---------------------------------
            Dibuat oleh Arya Ersi Putra
                       """)
        label.setStyleSheet("""
            border: 1px solid #444;
        """)

        label.setWordWrap(True)
        
        lay.addWidget(label)
