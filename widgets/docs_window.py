from PySide6.QtWidgets import QTabWidget, QWidget, QTableWidget, QGridLayout


# 일일 정산서 계산서 위젯
class DayCal(QWidget):
    # 생성자
    def __init__(self):
        super().__init__()
        self.init_ui()

    # ui 초기화
    def init_ui(self):
        # 테이블
        table = QTableWidget()

        # 예시코드
        table.setColumnCount(3)
        table.setRowCount(8)
        table.setHorizontalHeaderLabels(['화주1', '화주2', '화주3'])

        # 그리드 레이아웃
        grid = QGridLayout()

        # 테이블위젯 추가
        grid.addWidget(table, 0, 0)

        # 레이아웃 세팅
        self.setLayout(grid)


# 대차대조표 위젯
class BalancedSheet(QWidget):
    pass


# 수협 입금 위젯
class SH(QWidget):
    pass


# 문서 탭 위젯
class DocTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        tab1 = DayCal()
        tab2 = BalancedSheet()
        tab3 = SH()

        self.addTab(tab1, '일일정산서 계산서')
        self.addTab(tab2, '대차대조표')
        self.addTab(tab3, '수협 입금')
