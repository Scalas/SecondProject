from PySide6.QtCore import QDateTime, QTimer, Signal, Slot, QObject
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, QDialog, QPlainTextEdit, QPushButton, QTabWidget
from sqlalchemy.exc import IntegrityError

from controller.config_manager import set_geometry, get_geometry
from controller.db_manager import session
from models.models import DayCalOwner
from widgets.docs_window import DocTab


class MainWindow(QMainWindow, QObject):
    # 생성자
    def __init__(self):
        super().__init__()
        self.central_widget = CentralWidget()
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

        # 화주추가 액션 추가
        create_owner = QAction(QIcon('src/img/create_owner_icon.png'), '화주 추가', self)
        create_owner.setShortcut('Ctrl+Shift+A')
        create_owner.setStatusTip('화주 추가')
        create_owner.triggered.connect(self.create_owner)
        file_menu.addAction(create_owner)
        tool_bar.addAction(create_owner)

        # 화주삭제 액션 추가
        delete_owner = QAction(QIcon('src/img/delete_owner_icon.png'), '화주 삭제', self)
        delete_owner.setShortcut('Ctrl+Shift+A')
        delete_owner.setStatusTip('화주 추가')
        delete_owner.triggered.connect(self.delete_owner)
        #file_menu.addAction(delete_owner)
        #tool_bar.addAction(delete_owner)

        # 앱의 Central Widget 에 self.central_widget 설정
        self.setCentralWidget(self.central_widget)

        # 윈도우 타이틀 설정
        self.setWindowTitle('SSBS')

        # 윈도우 아이콘 설정
        self.setWindowIcon(QIcon('src/img/icon.png'))

        # 윈도우 위치, 크기 설정
        geometry = get_geometry()
        if not geometry:
            self.init_geometry()
        else:
            self.setGeometry(geometry[1], geometry[2], geometry[3], geometry[4])
            if geometry[0]:
                self.showMaximized()

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
        set_geometry(self.normalGeometry(), self.isMaximized())

    # 화주 추가
    def create_owner(self):
        # 다이얼로그 위젯 생성
        create_owner_dialog = Dialog()
        create_owner_dialog.setWindowTitle('화주 추가')
        create_owner_dialog.setGeometry(500, 500, 300, 50)

        # 화주 이름을 입력받기 위한 다이얼로그 ui 세팅
        grid = QGridLayout()
        input_name = QPlainTextEdit()
        input_name.setPlaceholderText('화주 이름')
        submit = QPushButton('추가')
        submit.clicked.connect(create_owner_dialog.close)
        grid.addWidget(QLabel('화주 이름: '), 0, 0, 1, 1)
        grid.addWidget(input_name, 0, 1, 1, 2)
        grid.addWidget(submit, 1, 0, 1, 3)
        create_owner_dialog.setLayout(grid)

        # 다이얼로그를 modal 하게 표시
        create_owner_dialog.show_modal()

        # 다이얼로그에서 입력이 완료되면 입력받은 이름으로 화주 추가
        name = input_name.toPlainText()
        new_owner = DayCalOwner(name)
        try:
            session.add(new_owner)
            session.commit()
            self.central_widget.doc_tab.tab1.owner_added(name)
        except IntegrityError:
            self.statusBar().showMessage('>> 이미 등록된 화주입니다.')

    # 화주 삭제
    def delete_owner(self):
        pass


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


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.doc_tab = DocTab()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #FFFFFF")

        # 그리드 레이아웃
        grid = QGridLayout()

        # 탭 위젯 추가
        grid.addWidget(self.doc_tab, 0, 0)

        # 중앙 위젯에 그리드 레이아웃 적용
        self.setLayout(grid)


# 다이얼로그(QDialog 상속)
class Dialog(QDialog):
    def __init__(self):
        super().__init__()

    def show_modal(self):
        return super().exec_()
