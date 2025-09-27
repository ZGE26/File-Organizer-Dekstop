import os
from PySide6.QtWidgets import QInputDialog, QMessageBox
from PySide6.QtCore import Qt

def rename_selected(self):
    item = self.list_widget.currentItem()
    if not item:
        return
    src = item.data(Qt.UserRole)
    new_name, ok = QInputDialog.getText(self, "Rename", "Nama baru:", text=os.path.basename(src))
    if not ok or not new_name.strip():
        return
    dst = os.path.join(os.path.dirname(src), new_name.strip())
    try:
        os.replace(src, dst)
        self.populate_list(self.current_path)
    except Exception as e:
        QMessageBox.warning(self, "Gagal Rename", f"{e}")