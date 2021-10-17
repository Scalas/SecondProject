import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QDateTime, QTimer


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 상태표시줄
        status_bar = self.statusBar()
        status_bar.showMessage('Ready', 3000)

        # 시간 레이블 추가
        time_label = TimeLabel()
        status_bar.addPermanentWidget(time_label)

        # 메뉴바 생성
        menu_bar = self.menuBar()

        # File 메뉴 추가
        file_menu = menu_bar.addMenu('&File')

        # 툴바 생성
        tool_bar = self.addToolBar('Toolbar')

        # exit 액션 추가
        exit_action = QAction(QIcon('src/img/exit_icon.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit Action')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        tool_bar.addAction(exit_action)

        # 윈도우 타이틀 설정
        self.setWindowTitle('MyFirstApplication')

        # 윈도우 아이콘 설정
        self.setWindowIcon(QIcon('src/img/icon.png'))

        # 윈도우 사이즈 재지정
        self.resize(300, 300)

        # 화면을 가운데로 위치시킨다
        self.center()

        # 윈도우를 화면에 띄운다
        self.show()

    def center(self):
        # 창의 현재 위치
        cur_pos = self.frameGeometry()

        # 모니터 화면의 가운데 위치 정보
        center_pos = self.screen().availableGeometry().center()

        # 창의 가운데 위치를 모니터 화면의 가운데 위치로 이동
        cur_pos.moveCenter(center_pos)


# 시간레이블 클래스(QLabel 상속)
class TimeLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(100)

    def timeout(self):
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
