import sys

from PySide6.QtWidgets import QApplication

from widgets import main_window
from controller.db_manager import init_db

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = main_window.MainWindow()
    sys.exit(app.exec())
