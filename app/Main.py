from app.layouts import app
import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class ImageLabel(QLabel):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap(image_path)
        self.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        if not self.original_pixmap.isNull():
            scaled = self.original_pixmap.scaledToWidth(
                self.width(), Qt.SmoothTransformation
            )
            self.setPixmap(scaled)
        super().resizeEvent(event)

if __name__ == "__main__":  
    app_instance = QApplication(sys.argv)

    label = ImageLabel("assets/images.png")

    main_window = app.AppLayout(content_widget=label, default_page=None)
    main_window.show()

    sys.exit(app_instance.exec())
