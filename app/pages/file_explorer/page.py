import os, sys
from PySide6.QtCore import Qt, QPoint, QTimer, QDir, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QListWidget, QListWidgetItem, QMessageBox, QMenu, QStackedLayout,
    QComboBox, QFileDialog, QToolButton, QFrame, QStyle
)
from PySide6.QtGui import QKeySequence, QShortcut

# fungsi app kamu (biarkan seperti semula)
from app.functions.delete import delete_selected
from app.functions.rename import rename_selected
from app.functions.create import create_folder
from app.functions.open_file import open_file  # pakai punyamu sendiri

# modul lokal
from .theme import THEME
from .helpers import make_tool_button, bind_shortcuts

BASE_DIR  = r"C:\Users\Arya Ersi Putra"
START_DIR = os.path.join(BASE_DIR, "Downloads")


class PageFileExplorer(QWidget):
    def __init__(self, start_dir: str = START_DIR):
        super().__init__()
        self.current_path = start_dir
        self.back_stack: list[str] = []
        self.fwd_stack: list[str]  = []

        # theme
        self.setStyleSheet(THEME)

        # ===== layout utama =====
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # ===== toolbar header =====
        tool_card = QFrame()
        tool_card.setProperty("class", "QCard")
        tool_lay = QHBoxLayout(tool_card)
        tool_lay.setContentsMargins(8, 8, 8, 8)
        tool_lay.setSpacing(8)

        self.back_btn = make_tool_button(self, QStyle.SP_ArrowBack, "Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)

        self.fwd_btn  = make_tool_button(self, QStyle.SP_ArrowForward, "Forward")
        self.fwd_btn.clicked.connect(self.go_forward)
        self.fwd_btn.setEnabled(False)

        self.path_label = QLabel()
        self.path_label.setObjectName("PathLabel")
        self.path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        tool_lay.addWidget(self.back_btn)
        tool_lay.addWidget(self.fwd_btn)
        tool_lay.addSpacing(6)
        tool_lay.addWidget(self.path_label, 1)
        root.addWidget(tool_card)

        # ===== drive + search bar =====
        bar_card = QFrame()
        bar_card.setProperty("class", "QCard")
        bar = QHBoxLayout(bar_card)
        bar.setContentsMargins(8, 8, 8, 8)
        bar.setSpacing(8)

        self.drive_combo = QComboBox()
        self.drive_combo.setMinimumWidth(120)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari file/folder (mis. png)…")
        self.search_input.setClearButtonEnabled(True)

        self.chk_recursive = QCheckBox("Recursive")
        self.chk_recursive.setChecked(True)

        bar.addWidget(self.drive_combo)
        bar.addSpacing(6)
        bar.addWidget(self.search_input, 1)
        bar.addWidget(self.chk_recursive)
        root.addWidget(bar_card)

        # ===== list / placeholder =====
        self.list_widget = QListWidget()

        self.placeholder = QLabel("Masukkan kata kunci…")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setMinimumHeight(200)

        content_card = QFrame()
        content_card.setProperty("class", "QCard")
        content_lay = QVBoxLayout(content_card)
        content_lay.setContentsMargins(8, 8, 8, 8)

        self.stack_host = QWidget()
        self.stacked = QStackedLayout(self.stack_host)
        self.stacked.addWidget(self.list_widget)
        self.stacked.addWidget(self.placeholder)
        self.stacked.setCurrentIndex(0)

        content_lay.addWidget(self.stack_host)
        root.addWidget(content_card)

        # ===== wiring =====
        self.refresh_drives()
        self.drive_combo.currentTextChanged.connect(self._on_drive_changed)

        # debounce search
        self.search_timer = QTimer(self)
        self.search_timer.setInterval(500)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.run_search)
        self.search_input.textChanged.connect(lambda _t: self.search_timer.start())
        self.search_input.returnPressed.connect(self.run_search)

        # double click & menu
        self.list_widget.itemDoubleClicked.connect(self.on_open_selected)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        # init
        self.navigate_to(self.current_path, add_to_history=False)

        # shortcuts
        bind_shortcuts(self, self.go_back, self.go_forward)

    # ====== event handlers ======
    def _on_drive_changed(self, text: str):
        if not text:
            return
        self.search_input.clear()
        self.navigate_to(text)

    # ====== core ======
    def populate_list(self, folder_path: str):
        self.list_widget.clear()
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
                item.setData(Qt.UserRole, entry.path)
                self.list_widget.addItem(item)

    def navigate_to(self, folder_path: str, add_to_history: bool = True):
        if not os.path.isdir(folder_path):
            QMessageBox.warning(self, "Error", f"Bukan folder:\n{folder_path}")
            return
        if add_to_history and getattr(self, "current_path", None) and folder_path != self.current_path:
            self.back_stack.append(self.current_path)
            self.fwd_stack.clear()

        self.populate_list(folder_path)
        self.update_nav_buttons()

    def update_nav_buttons(self):
        self.back_btn.setEnabled(len(self.back_stack) > 0)
        self.fwd_btn.setEnabled(len(self.fwd_stack) > 0)

    # ====== search ======
    def run_search(self):
        keyword = self.search_input.text().strip().lower()
        if not keyword:
            self.populate_list(self.current_path)
            return

        self.list_widget.clear()
        found = False
        if self.chk_recursive.isChecked():
            for base_dir, dirs, files in os.walk(self.current_path):
                for name in dirs + files:
                    if keyword in name.lower():
                        path = os.path.join(base_dir, name)
                        icon = "📁 " if os.path.isdir(path) else "📄 "
                        item = QListWidgetItem(icon + name)
                        item.setData(Qt.UserRole, path)
                        self.list_widget.addItem(item)
                        found = True
        else:
            with os.scandir(self.current_path) as it:
                for entry in it:
                    if keyword in entry.name.lower():
                        icon = "📁 " if entry.is_dir() else "📄 "
                        item = QListWidgetItem(icon + entry.name)
                        item.setData(Qt.UserRole, entry.path)
                        self.list_widget.addItem(item)
                        found = True

        self.stacked.setCurrentIndex(0 if found else 1)
        if not found:
            self.placeholder.setText("Data Kosong")

    # ====== context menu ======
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
            if self.search_input.text().strip():
                self.run_search()
            else:
                self.populate_list(self.current_path)

    # ====== navigation ======
    def on_open_selected(self, item: QListWidgetItem):
        if not item:
            return
        path = item.data(Qt.UserRole)
        if os.path.isdir(path):
            self.search_input.clear()
            self.navigate_to(path)
        else:
            # pakai implementasi open_file kamu sendiri
            open_file(self, path)

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.search_input.clear()
            self.navigate_to(parent)

    def go_back(self):
        if not self.back_stack:
            return
        target = self.back_stack.pop()
        if self.current_path and os.path.isdir(self.current_path):
            self.fwd_stack.append(self.current_path)
        self.populate_list(target)
        self.update_nav_buttons()

    def go_forward(self):
        if not self.fwd_stack:
            return
        target = self.fwd_stack.pop()
        if self.current_path and os.path.isdir(self.current_path):
            self.back_stack.append(self.current_path)
        self.populate_list(target)
        self.update_nav_buttons()

    # ====== drive helpers ======
    def refresh_drives(self):
        self.drive_combo.blockSignals(True)
        self.drive_combo.clear()

        if sys.platform.startswith("win"):
            drives = [fi.absoluteFilePath() for fi in QDir.drives()]
            if not drives:
                drives = [f"{chr(c)}:/" for c in range(ord('A'), ord('Z')+1)
                          if os.path.exists(f"{chr(c)}:/")]
            self.drive_combo.addItems(drives)
            root_drive = os.path.splitdrive(self.current_path)[0].replace("\\", "/") + "/"
            idx = self.drive_combo.findText(root_drive, Qt.MatchFixedString)
            if idx >= 0:
                self.drive_combo.setCurrentIndex(idx)
        else:
            self.drive_combo.addItem("/")
            self.drive_combo.setCurrentIndex(0)

        self.drive_combo.blockSignals(False)

    def choose_folder(self):
        start = self.current_path if os.path.isdir(self.current_path) else os.path.expanduser("~")
        folder = QFileDialog.getExistingDirectory(self, "Pilih Folder", start)
        if folder:
            self.search_input.clear()
            self.back_stack.clear()
            self.fwd_stack.clear()
            self.navigate_to(folder, add_to_history=False)
            if sys.platform.startswith("win"):
                root_drive = os.path.splitdrive(folder)[0].replace("\\", "/") + "/"
                idx = self.drive_combo.findText(root_drive, Qt.MatchFixedString)
                if idx >= 0:
                    self.drive_combo.blockSignals(True)
                    self.drive_combo.setCurrentIndex(idx)
                    self.drive_combo.blockSignals(False)
