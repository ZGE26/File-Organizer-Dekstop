import os, sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QToolButton
from PySide6.QtGui import QKeySequence, QShortcut

def make_tool_button(parent, std_icon, tooltip: str, size: int = 32):
    """Buat QToolButton square 1:1 dengan icon standar."""
    btn = QToolButton(parent)
    btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
    btn.setIcon(parent.style().standardIcon(std_icon))
    btn.setIconSize(QSize(18, 18))
    btn.setFixedSize(size, size)
    btn.setToolTip(tooltip)
    return btn

def open_path_with_os(path: str):
    """Buka file/folder pakai default OS."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            os.system(f'open "{path}"')
        else:
            os.system(f'xdg-open "{path}"')
    except Exception as e:
        raise e

def bind_shortcuts(widget, back_cb, fwd_cb, up_cb=None):
    """Pasang shortcut navigasi umum."""
    QShortcut(QKeySequence("Alt+Left"),  widget, activated=back_cb)
    QShortcut(QKeySequence("Alt+Right"), widget, activated=fwd_cb)
    if up_cb:
        QShortcut(QKeySequence("Backspace"), widget, activated=up_cb)
