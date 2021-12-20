import sys

from PySide6.QtWidgets import QApplication

from widgets import main_window
from controller.db_manager import init_db

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("TableView { border: 1px solid; font-size: 15px; margin: 0px; padding: 0px; }"
                      "QHeaderView::section:horizontal {"
                      " font-size: 15px;"
                      " font-weight: bold;"
                      " border: 1px solid;"
                      " margin: 0px;"
                      " border-bottom: 2px solid "
                      "}"
                      "QHeaderView::section:horizontal:last {"
                      " font-size: 15px;"
                      " font-weight: bold;"
                      " border: 1px solid;"
                      " margin: 0px;"
                      " border-bottom: 2px solid;"
                      " border-right: 2px solid }"
                      "QHeaderView::section:vertical {"
                      " font-size: 15px;"
                      " font-weight: bold;"
                      " border: 1px solid;"
                      " margin: 0px;"
                      " border-right: 2px solid }"
                      "QTableCornerButton::section {"
                      " border: 1px solid;"
                      " margin: 0px;"
                      "}"
                      )
    screen = main_window.MainWindow()
    sys.exit(app.exec())
