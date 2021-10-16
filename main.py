import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QIcon


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MyFirstApplication')
        self.setWindowIcon(QIcon('src/img/icon.png'))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
