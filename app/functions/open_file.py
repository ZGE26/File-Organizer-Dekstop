import os
import sys
from PySide6.QtWidgets import QMessageBox

def open_file(self, path: str):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            os.system(f'open "{path}"')
        else:
            os.system(f'xdg-open "{path}"')
    except Exception as e:
        QMessageBox.warning(self, "Open Failed", f"Gagal membuka:\n{path}\n\n{e}")
