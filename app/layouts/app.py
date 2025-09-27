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

        # Header (tetap fixed)
        header = QLabel("Header", self)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background-color: lightgray; font-size: 20px; padding: 10px;")
        self.main_layout.addWidget(header)

        # ===== BODY FRAME (ambil sisa tinggi: 100vh-Header-Footer) =====
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

        btn_dashboard = QPushButton("Dashboard", self.sidebar_frame)
        btn_dashboard.setStyleSheet("font-weight: bold; padding: 8px;")
        btn_folders  = QPushButton("Folders", self.sidebar_frame)
        btn_folders.setStyleSheet("font-weight: bold; padding: 8px;")

        self.sidebar_layout.addWidget(btn_dashboard)
        self.sidebar_layout.addWidget(btn_folders)
        self.sidebar_layout.addStretch()

        self.center_layout.addWidget(self.sidebar_frame)

        # Container konten
        self.content_container = QFrame(self.center_frame)
        self.content_container.setObjectName("contentContainer")
        self.content_container.setStyleSheet("""
              #contentContainer {
                border: 2px solid white;
            }
        """)
        self.content_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(12, 12, 12, 12)
        self.content_layout.setSpacing(8)

        # *** Kunci 1: top align konten ***
        self.content_layout.setAlignment(Qt.AlignTop)

        # Konten awal
        self.content = content_widget or QTextEdit("Default Content Area")
        # (opsional) paragraf kiri:
        if isinstance(self.content, QTextEdit):
            self.content.setAlignment(Qt.AlignLeft)

        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.content)

        # Masukkan content_container, beri stretch di HBox (biar lebar)
        self.center_layout.addWidget(self.content_container, 1)

        # *** Kunci 2: center_frame diberi stretch di main_layout (biar full tinggi) ***
        self.main_layout.addWidget(self.center_frame, 1)

        # Footer (tetap fixed)
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
        # Pastikan setiap page punya layout yang Top Align juga:
        #   kalau page kamu QVBoxLayout, setAlignment(Qt.AlignTop)
        self.content_layout.addWidget(self.content)

    def show_dashboard(self):
        self._set_content(PageDashboard())

    def show_list_folder(self):
        self._set_content(PageListFolder())
