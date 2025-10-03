from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

from app.pages.dashboard import PageDashboard
from app.pages.file_explorer.page import PageFileExplorer
from app.pages.organizer_file import FileOrganizer


class AppLayout(QWidget):
    def __init__(self, content_widget=None, default_page="dashboard"):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.resize(900, 600)

        # state halaman aktif
        self.active_page = None  
        self.buttons = {}

        # ===== MAIN LAYOUT =====
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(8)

        # Header
        header = QLabel("File Manager and File Organizer", self)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background-color: black; font-size: 20px; padding: 10px;")
        self.main_layout.addWidget(header)

        # ===== BODY FRAME =====
        self.center_frame = QFrame(self)
        self.center_frame.setStyleSheet("background-color: #111;")
        self.center_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.center_layout = QHBoxLayout(self.center_frame)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(12)

        # Sidebar
        self.sidebar_frame = QFrame(self.center_frame)
        self.sidebar_frame.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # buat tombol
        btn_dashboard = QPushButton("Dashboard", self.sidebar_frame)
        btn_folders  = QPushButton("Folders", self.sidebar_frame)
        btn_organizer = QPushButton("Organizer", self.sidebar_frame)

        for btn in [btn_dashboard, btn_folders, btn_organizer]:
            btn.setStyleSheet("font-weight: bold; padding: 8px; color: white; background-color: transparent;")
            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()
        self.center_layout.addWidget(self.sidebar_frame)

        # simpan tombol ke dict biar gampang akses
        self.buttons = {
            "dashboard": btn_dashboard,
            "folders": btn_folders,
            "organizer": btn_organizer
        }

        # Container konten
        self.content = content_widget or QTextEdit("Default Content Area")
        if isinstance(self.content, QTextEdit):
            self.content.setAlignment(Qt.AlignLeft)

        self.content_container = QFrame(self.center_frame)
        self.content_container.setObjectName("contentContainer")
        self.content_container.setStyleSheet("#contentContainer { border: 2px solid white; }")
        self.content_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(12, 12, 12, 12)
        self.content_layout.setSpacing(8)
        self.content_layout.setAlignment(Qt.AlignTop)

        self.content = content_widget or QTextEdit("Default Content Area")
        if isinstance(self.content, QTextEdit):
            self.content.setAlignment(Qt.AlignLeft)
        self.content_layout.addWidget(self.content)

        self.center_layout.addWidget(self.content_container, 1)
        self.main_layout.addWidget(self.center_frame, 1)

        # Footer
        footer = QLabel("Footer", self)
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("background-color: lightgray; font-size: 16px; padding: 10px;")
        self.main_layout.addWidget(footer)

        # Event klik
        btn_dashboard.clicked.connect(lambda: self.show_page("dashboard"))
        btn_folders.clicked.connect(lambda: self.show_page("folders"))
        btn_organizer.clicked.connect(lambda: self.show_page("organizer"))

        # default ke dashboard
        if default_page:
            self.show_page(default_page)
        else:
            self._highlight_button(None)

    def _set_content(self, widget: QWidget):
        if self.content is not None:
            self.content.setParent(None)
        self.content = widget
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.content)

    def _highlight_button(self, name: str | None):
        # reset semua tombol
        for _, btn in self.buttons.items():
            btn.setStyleSheet("font-weight: bold; padding: 8px; color: white; background-color: transparent;")
        # highlight tombol aktif
        if name and name in self.buttons:
            self.buttons[name].setStyleSheet("font-weight: bold; padding: 8px; color: black; background-color: white;")

    def show_page(self, name: str):
        if name == "dashboard":
            self._set_content(PageDashboard())
        elif name == "folders":
            self._set_content(PageFileExplorer())
        elif name == "organizer":
            self._set_content(FileOrganizer())

        self._highlight_button(name)
        self.active_page = name
