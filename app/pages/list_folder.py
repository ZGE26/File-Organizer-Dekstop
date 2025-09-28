import os, sys, shutil
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QListWidget, QListWidgetItem, QPushButton, QMessageBox, QMenu, QStackedLayout, QSizePolicy
)

# kalau kamu sudah punya fungsi2 ini di app/functions, keep importnya:
from app.functions.delete import delete_selected
from app.functions.rename import rename_selected
from app.functions.create import create_folder
from app.functions.open_file import open_file

try:
    from send2trash import send2trash
except Exception:
    send2trash = None

BASE_DIR  = r"C:\Users\Arya Ersi Putra"
START_DIR = os.path.join(BASE_DIR, "Downloads")


class PageFileExplorer(QWidget):
    def __init__(self, start_dir: str = START_DIR):
        super().__init__()
        self.current_path = start_dir

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        # ===== Header: Up + path + (opsional) tombol lain =====
        head = QHBoxLayout()
        self.up_btn = QPushButton("⬆ Up")
        self.up_btn.clicked.connect(self.go_up)
        self.path_label = QLabel()
        self.path_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        head.addWidget(self.up_btn)
        head.addWidget(self.path_label, 1)
        root.addLayout(head)

        # ===== Bar pencarian + opsi recursive =====
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari file/folder (mis. png)…")
        self.chk_recursive = QCheckBox("Recursive")
        self.chk_recursive.setChecked(True)
        search_row.addWidget(self.search_input, 1)
        search_row.addWidget(self.chk_recursive)
        root.addLayout(search_row)

        # Debounce timer
        self.search_timer = QTimer(self)
        self.search_timer.setInterval(500)  # 0.5s
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.run_search)
        self.search_input.textChanged.connect(lambda _t: self.search_timer.start())
        self.search_input.returnPressed.connect(self.run_search)

        # ===== List hasil / isi folder =====
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            padding: 8px; background-color: #222;
            border: 1px solid #444; color: white; font-size: 15px;
            border-radius: 4px;
        """)
        # root.addWidget(self.list_widget)

        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        # Placeholder saat kosong
        self.placeholder = QLabel("Masukkan kata kunci…")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("color: gray; font-size: 14px;")
        self.placeholder.setMinimumHeight(160) 
        # root.addWidget(self.placeholder)
        # self.placeholder.hide()

        # Stacked layout dibungkus widget
        self.stack_host = QWidget()
        self.stacked = QStackedLayout(self.stack_host)
        self.stacked.addWidget(self.list_widget)   # index 0
        self.stacked.addWidget(self.placeholder)   # index 1
        self.stacked.setCurrentIndex(0) 

        root.addWidget(self.stack_host)

        # Double click buka & Context menu (klik kanan)
        self.list_widget.itemDoubleClicked.connect(self.on_open_selected)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Muat awal
        self.populate_list(self.current_path)

    # ---------- tampilan isi folder ----------
    def populate_list(self, folder_path: str):
        self.list_widget.clear()
        # self.placeholder.hide()
        # self.list_widget.show()

        self.stacked.setCurrentIndex(0)

        self.current_path = folder_path
        self.path_label.setText(folder_path)

        if not os.path.isdir(folder_path):
            QMessageBox.warning(self, "Error", f"Bukan folder:\n{folder_path}")
            return

        with os.scandir(folder_path) as it:
            entries = sorted(it, key=lambda e: (not e.is_dir(), e.name.lower()))
            for entry in entries:
                icon = "📁 " if entry.is_dir() else "📄 "
                item = QListWidgetItem(icon + entry.name)
                item.setData(Qt.UserRole, entry.path)  # simpan full path
                self.list_widget.addItem(item)

        self.up_btn.setEnabled(os.path.dirname(self.current_path) != self.current_path)

    # ---------- pencarian ----------
    def run_search(self):
        keyword = self.search_input.text().strip().lower()
        if not keyword:
            # kosong -> kembali tampil isi folder biasa
            self.populate_list(self.current_path)
            return

        self.list_widget.clear()

        found = False
        if self.chk_recursive.isChecked():
            # Rekursif (os.walk)
            for root, dirs, files in os.walk(self.current_path):
                for name in dirs + files:
                    if keyword in name.lower():
                        path = os.path.join(root, name)
                        icon = "📁 " if os.path.isdir(path) else "📄 "
                        item = QListWidgetItem(icon + name)
                        item.setData(Qt.UserRole, path)
                        self.list_widget.addItem(item)
                        found = True
        else:
            # Hanya level saat ini (os.scandir)
            with os.scandir(self.current_path) as it:
                for entry in it:
                    if keyword in entry.name.lower():
                        icon = "📁 " if entry.is_dir() else "📄 "
                        item = QListWidgetItem(icon + entry.name)
                        item.setData(Qt.UserRole, entry.path)
                        self.list_widget.addItem(item)
                        found = True

        if not found:
            # self.list_widget.hide()
            self.placeholder.setText("Data Kosong")
            # self.placeholder.show()
            self.stacked.setCurrentIndex(1)
        else:
            # self.placeholder.hide()
            # self.list_widget.show()
            self.stacked.setCurrentIndex(0)

    # ---------- context menu ----------
    def show_context_menu(self, pos: QPoint):
        item = self.list_widget.itemAt(pos)
        if item:
            self.list_widget.setCurrentItem(item)

        menu = QMenu(self)
        act_open   = menu.addAction("Open")
        act_rename = menu.addAction("Rename")
        act_delete = menu.addAction("Delete")
        menu.addSeparator()
        act_newdir = menu.addAction("New Folder")
        act_refresh= menu.addAction("Refresh")

        chosen = menu.exec_(self.list_widget.mapToGlobal(pos))
        if not chosen:
            return

        if chosen == act_open:
            self.on_open_selected(self.list_widget.currentItem())
        elif chosen == act_rename:
            rename_selected(self)
        elif chosen == act_delete:
            delete_selected(self)
        elif chosen == act_newdir:
            create_folder(self)
        elif chosen == act_refresh:
            # refresh tergantung mode: kalau ada keyword, ulangi search; kalau tidak, populate
            if self.search_input.text().strip():
                self.run_search()
            else:
                self.populate_list(self.current_path)

    # ---------- aksi utama ----------
    def on_open_selected(self, item: QListWidgetItem):
        if not item:
            return
        path = item.data(Qt.UserRole)
        if os.path.isdir(path):
            # kalau lagi dalam mode search, buka folder & bersihkan keyword
            self.search_input.clear()
            self.populate_list(path)
        else:
            open_file(self, path)

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.search_input.clear()  # keluar dari mode search
            self.populate_list(parent)