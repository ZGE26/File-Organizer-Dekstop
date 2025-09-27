import os
from PySide6.QtWidgets import QInputDialog, QMessageBox

def create_folder(self):
    name, ok = QInputDialog.getText(self, "Folder Baru", "Nama folder:")
    if not ok or not name.strip():
        return
    target = os.path.join(self.current_path, name.strip())
    try:
        os.mkdir(target)
        self.populate_list(self.current_path)
    except Exception as e:
        QMessageBox.warning(self, "Gagal", str(e))