import os
import shutil
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from send2trash import send2trash


def delete_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        path = item.data(Qt.UserRole)
        if QMessageBox.question(self, "Hapus", f"Hapus item ini?\n{path}") != QMessageBox.Yes:
            return
        try:
            if send2trash:
                send2trash(path)
            else:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            self.populate_list(self.current_path)
        except Exception as e:
            QMessageBox.warning(self, "Gagal Hapus", f"{e}")