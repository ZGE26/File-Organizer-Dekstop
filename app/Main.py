from app.layouts import app
import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt

if __name__ == "__main__":
    app_instance = QApplication(sys.argv)

    custom_content = QLabel("This is a custom content area!", None)
    custom_content.setAlignment(Qt.AlignCenter)
    custom_content.setStyleSheet("font-size: 18px; padding: 20px;")


    main_window = app.AppLayout(content_widget=custom_content)
    main_window.show()
    sys.exit(app_instance.exec())
