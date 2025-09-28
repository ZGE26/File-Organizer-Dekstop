import os
from PySide6.QtWidgets import QMessageBox


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
