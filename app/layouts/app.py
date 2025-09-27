from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

from app.pages.dashboard import PageDashboard
from app.pages.list_folder import PageListFolder

class AppLayout(QWidget):
    def __init__(self, content_widget=None):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.resize(900, 600)

        # ===== MAIN LAYOUT =====
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(8)

        # Header
        header = QLabel("Header", self)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background-color: lightgray; font-size: 20px; padding: 10px;")
        self.main_layout.addWidget(header)

        # ===== BODY FRAME (supaya bisa di-style) =====
        self.center_frame = QFrame(self)
        self.center_frame.setStyleSheet("background-color: #111;")
        self.center_layout = QHBoxLayout(self.center_frame)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(12)

        # Sidebar
        self.sidebar_frame = QFrame(self.center_frame)
        self.sidebar_frame.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        btn_dashboard = QPushButton("Dashboard", self.sidebar_frame)
        btn_folders  = QPushButton("Folders", self.sidebar_frame)

        self.sidebar_layout.addWidget(btn_dashboard)
        self.sidebar_layout.addWidget(btn_folders)
        self.sidebar_layout.addWidget(QPushButton("Menu 3", self.sidebar_frame))
        self.sidebar_layout.addStretch()

        self.center_layout.addWidget(self.sidebar_frame)

        # Container konten
        self.content_container = QFrame(self.center_frame)
        self.content_container.setStyleSheet("background-color: #222; ")
        self.content_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(12, 12, 12, 12)
        self.content_layout.setSpacing(8)

        # Konten awal
        self.content = content_widget or QTextEdit("Default Content Area", aligtnment=Qt.AlignCenter)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.content)

        self.center_layout.addWidget(self.content_container, 1)  # stretch biar lebar

        # Masukkan BODY ke main
        self.main_layout.addWidget(self.center_frame)

        # Footer
        footer = QLabel("Footer", self)
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("background-color: lightgray; font-size: 16px; padding: 10px;")
        self.main_layout.addWidget(footer)

        # Event
        btn_dashboard.clicked.connect(self.show_dashboard)
        btn_folders.clicked.connect(self.show_list_folder)

    # ===== Helper ganti konten =====
    def _set_content(self, widget: QWidget):
        if self.content is not None:
            self.content.setParent(None)  # lepas konten lama
        self.content = widget
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.content)  # tambahkan ke container

    def show_dashboard(self):
        self._set_content(PageDashboard())

    def show_list_folder(self):
        self._set_content(PageListFolder())
