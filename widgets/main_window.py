from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout

from controller.config_manager import set_geometry, get_geometry
from widgets.docs_window import DocTab


class MainWindow(QMainWindow):
    # 생성자
    def __init__(self):
        super().__init__()
        self.init_ui()

    # ui 초기화
    def init_ui(self):
        # 상태표시줄
        status_bar = self.statusBar()

        # 시간 레이블 추가
        time_label = TimeLabel()
        status_bar.addPermanentWidget(time_label)

        # 메뉴바 생성
        menu_bar = self.menuBar()

        # File 메뉴 추가
        file_menu = menu_bar.addMenu('&File(F)')

        # 툴바 생성
        tool_bar = self.addToolBar('Toolbar')

        # exit 액션 추가
        exit_action = QAction(QIcon('src/img/exit_icon.png'), '&Exit(E)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit Action')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        tool_bar.addAction(exit_action)

        # 중앙 위젯
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #FFFFFF")

        # 그리드 레이아웃
        grid = QGridLayout()

        # 탭 위젯 추가
        grid.addWidget(DocTab(), 0, 0)

        # 중앙 위젯에 그리드 레이아웃 적용
        central_widget.setLayout(grid)

        # 앱의 Central Widget 에 central_widget 설정
        self.setCentralWidget(central_widget)

        # 윈도우 타이틀 설정
        self.setWindowTitle('SSBS')

        # 윈도우 아이콘 설정
        self.setWindowIcon(QIcon('src/img/icon.png'))

        # 윈도우 위치, 크기 설정
        geometry = get_geometry()
        if not geometry:
            self.init_geometry()
        else:
            self.setGeometry(*geometry)

        # 윈도우를 화면에 띄운다
        self.show()

    # 윈도우 크기 초기설정
    def init_geometry(self):
        # 윈도우 초기 사이즈 지정
        self.resize(1000, 800)

        # 모니터 화면의 중앙 위치 정보
        center_pos = self.screen().availableGeometry().center()

        # 윈도우의 중앙위치를 모니터 화면의 중앙으로 이동
        self.frameGeometry().moveCenter(center_pos)

    # 종료시 윈도우의 위치와 크기를 설정파일에 저장
    def closeEvent(self, event):
        QMainWindow.closeEvent(self, event)
        set_geometry(self.geometry())


# 시간레이블 클래스(QLabel 상속)
# 1초마다 현재 날짜/시간을 갱신하여 표시하는 레이블
class TimeLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(100)

    def timeout(self):
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))
