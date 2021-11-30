from PySide6.QtCore import QObject, QEvent
from PySide6.QtGui import QIcon, QAction, QMouseEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout

from controller.config_manager import set_geometry, get_geometry
from controller.db_manager import close_db
from controller import actions
from widgets.docs_window import DocTab, DayCal, SH, BalancedSheet
from widgets.simple import TimeLabel, StatusBar


class MainWindow(QMainWindow, QObject):
    # 생성자
    def __init__(self):
        super().__init__()
        self.central_widget = CentralWidget(self)
        self.init_ui()

    # ui 초기화
    def init_ui(self):
        # 상태표시줄
        status_bar = self.statusBar()

        # 시간 레이블 추가
        time_label = TimeLabel()
        time_label.clicked.connect(lambda: actions.date_query(self, self.central_widget.get_selected_tab()))
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
        create_owner.triggered.connect(lambda: actions.create_owner(self, self.central_widget.doc_tab.tab1))
        file_menu.addAction(create_owner)
        tool_bar.addAction(create_owner)

        # 화주삭제 액션 추가
        delete_owner = QAction(QIcon('src/img/delete_owner_icon.png'), '화주 삭제', self)
        delete_owner.setShortcut('Ctrl+Shift+R')
        delete_owner.setStatusTip('화주 삭제')
        delete_owner.triggered.connect(lambda: actions.delete_owner(self, self.central_widget.doc_tab.tab1))
        file_menu.addAction(delete_owner)
        tool_bar.addAction(delete_owner)

        # 화주 이름 변경 액션 추가
        modify_owner = QAction(QIcon('src/img/modify_owner_icon.png'), '화주 이름 변경', self)
        modify_owner.setShortcut('Ctrl+Shift+C')
        modify_owner.setStatusTip('화주 이름 변경')
        modify_owner.triggered.connect(lambda: actions.modify_owner(self, self.central_widget.doc_tab.tab1))
        file_menu.addAction(modify_owner)
        tool_bar.addAction(modify_owner)

        # 저장 액션 추가
        save_data = QAction(QIcon('src/img/save_icon.png'), '저장하기', self)
        save_data.setShortcut('Ctrl+S')
        save_data.setStatusTip('화주 이름 변경')
        save_data.triggered.connect(actions.save)
        file_menu.addAction(save_data)
        tool_bar.addAction(save_data)

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
        close_db()

    # 상태표시줄 생성(오버라이드)
    def statusBar(self):
        status_bar = StatusBar()
        self.setStatusBar(status_bar)
        return status_bar


# 중앙 위젯
class CentralWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.doc_tab = DocTab()
        self.doc_tab.setParent(self)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #FFFFFF")

        # 그리드 레이아웃
        grid = QGridLayout()

        # 탭 위젯 추가
        grid.addWidget(self.doc_tab, 0, 0)

        # 중앙 위젯에 그리드 레이아웃 적용
        self.setLayout(grid)

    def get_selected_tab(self):
        cur = self.doc_tab.currentWidget()
        return 0 if cur == self.doc_tab.tab1 else 1 if self.doc_tab.tab2 else 2