# Tambahan import
import os, sys, shutil
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox, QMenu
)

from app.functions.delete import delete_selected
from app.functions.rename import rename_selected
from app.functions.create import create_folder

try:
    from send2trash import send2trash
except Exception:
    send2trash = None

BASE_DIR  = r"C:\Users\Arya Ersi Putra"
START_DIR = os.path.join(BASE_DIR, "Downloads")

class PageListFolder(QWidget):
    def __init__(self, start_dir: str = START_DIR):
        super().__init__()
        self.current_path = start_dir

        root = QVBoxLayout(self)
        head = QHBoxLayout()
        self.up_btn = QPushButton("⬆ Up")
        self.up_btn.clicked.connect(self.go_up)
        self.path_label = QLabel()
        self.path_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        head.addWidget(self.up_btn); head.addWidget(self.path_label, 1)
        root.addLayout(head)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            padding: 8px; background-color: #222; border: 1px solid #444;
            color: white; font-size: 15px;
        """)
        root.addWidget(self.list_widget)

        # Double click buka
        self.list_widget.itemDoubleClicked.connect(self.on_open_selected)

        # ==== Context menu (klik kanan) ====
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        self.populate_list(self.current_path)

    # --------- data/populate ----------
    def populate_list(self, folder_path: str):
        self.list_widget.clear()
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

    # --------- klik kanan ----------
    def show_context_menu(self, pos: QPoint):
        # Pastikan item di bawah kursor jadi current
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
            self.populate_list(self.current_path)

    # --------- aksi utama ----------
    def on_open_selected(self, item: QListWidgetItem):
        if not item:
            return
        path = item.data(Qt.UserRole)
        if os.path.isdir(path):
            self.populate_list(path)
        else:
            self.open_file(path)

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.populate_list(parent)


    # --------- util ---------
    def open_file(self, path: str):
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            else:
                os.system(f'xdg-open "{path}"')
        except Exception as e:
            QMessageBox.warning(self, "Open Failed", f"Gagal membuka:\n{path}\n\n{e}")
