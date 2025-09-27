import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import Qt, QTimer

BASE_DIR = r"C:\Users\Arya Ersi Putra\Downloads"

class PageOrganizerFile(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Input pencarian
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari file atau folder...")
        layout.addWidget(self.search_input)

        # List hasil
        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        # Placeholder "Data Kosong"
        self.placeholder = QLabel("Data Kosong")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("color: gray; font-size: 14px;")
        layout.addWidget(self.placeholder, alignment=Qt.AlignCenter)
        self.placeholder.hide()  # default disembunyikan

        # Timer debounce
        self.search_timer = QTimer(self)
        self.search_timer.setInterval(500)  # 0.5 detik
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.search_files)

        # Trigger pencarian saat teks berubah
        self.search_input.textChanged.connect(self.restart_timer)

    def restart_timer(self, _text):
        self.search_timer.start()

    def search_files(self):
        keyword = self.search_input.text().lower().strip()
        self.result_list.clear()

        if not keyword:
            self.result_list.hide()
            self.placeholder.show()
            self.placeholder.setText("Masukkan kata kunci...")
            return
        
        found = False

        # os.walk -> jalanin rekursif ke semua folder
        for root, dirs, files in os.walk(BASE_DIR):
            for name in dirs + files:
                if keyword in name.lower():
                    path = os.path.join(root, name)
                    icon = "📁 " if os.path.isdir(path) else "📄 "
                    item = QListWidgetItem(icon + name)
                    item.setData(Qt.UserRole, path)
                    found = True
                    self.result_list.addItem(item)

        if not found:
            self.result_list.hide()
            self.placeholder.setText("Data Kosong")
            self.placeholder.show()
        else:
            self.placeholder.hide()
            self.result_list.show()
