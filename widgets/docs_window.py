from PySide6.QtWidgets import QTabWidget, QWidget, QGridLayout, QTableView, QHeaderView
from PySide6.QtCore import Signal

from controller import actions
from models.table_models import DayCalTableModel, DayCalOthersTableModel, DayCalResultTableModel
from widgets.simple import TableView


# 일일 정산서 계산서 위젯
class DayCal(QWidget):
    selected_total_changed = Signal(int)

    # 생성자
    def __init__(self, parent):
        super().__init__(parent)
        # 선택된 셀의 합
        self.selected_total = 0

        # 화주명단, 화주별 데이터, 기타 데이터, 결과 데이터를 DB 에서 읽어온다
        self.owner_list = actions.get_daycal_owner_list()
        self.owner_values = actions.get_daycal_owner_values()
        self.other_values = actions.get_daycal_other_values()
        self.result = actions.get_daycal_result()

        # 테이블 목록
        self.tables = []

        # 입력 테이블 생성(화주별 데이터)
        input_table = TableView(self, 0)
        input_table.setModel(DayCalTableModel(self, actions.get_daycal_owner_list(), actions.get_daycal_owner_values()))
        input_table.selected_total_changed.connect(self.selection_changed)
        input_table.verticalHeader().setMinimumWidth(200)
        self.tables.append(input_table)

        # 기타 테이블 생성(기타 데이터)
        other_table = TableView(self, 1)
        other_table.setModel(DayCalOthersTableModel(self, actions.get_daycal_other_values()))
        other_table.selected_total_changed.connect(self.selection_changed)
        other_table.verticalHeader().setMinimumWidth(200)
        other_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tables.append(other_table)

        # 결과 테이블 생성
        result_table = TableView(self, 2)
        result_table.setModel(DayCalResultTableModel(self, actions.get_daycal_result()))
        result_table.selected_total_changed.connect(self.selection_changed)
        result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tables.append(result_table)

        self.init_ui()

    # ui 초기화
    def init_ui(self):
        # 그리드 레이아웃
        grid = QGridLayout()

        # 테이블위젯 추가
        grid.addWidget(self.tables[0], 0, 0)
        grid.addWidget(self.tables[1], 1, 0)
        grid.addWidget(self.tables[2], 0, 1, 2, 1)
        grid.setRowStretch(0, 5)
        grid.setColumnStretch(0, 7.5)
        grid.setColumnStretch(1, 2.5)

        # 레이아웃 세팅
        self.setLayout(grid)

    # 화주 추가 반영
    def owner_added(self, new_owner, today_values):
        self.tables[0].model().owner_added(new_owner, today_values)

    # 화주 삭제 반영
    def owner_removed(self, removed_id):
        self.tables[0].model().owner_removed(removed_id)

    # 화주 이름 변경 반영
    def owner_modified(self, modified_id, chg_name):
        self.tables[0].model().owner_modified(modified_id, chg_name)

    def selection_changed(self, table_type):
        self.selected_total = self.tables[table_type].selected_total
        self.selected_total_changed.emit(0)


# 대차대조표 위젯
class BalancedSheet(QWidget):
    pass


# 수협 입금 위젯
class SH(QWidget):
    pass


# 문서 탭 위젯
class DocTab(QTabWidget):
    selected_total_changed = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        # 선택된 셀의 합
        self.selected_total = 0

        self.tabs = []
        tab1 = DayCal(self)
        tab1.selected_total_changed.connect(self.selection_changed)
        self.tabs.append(tab1)
        # self.tab2 = BalancedSheet(self)
        # self.tab3 = SH(self)
        self.init_ui()

    def init_ui(self):
        self.addTab(self.tabs[0], '일일정산서 계산서')
        # self.addTab(self.tabs[1], '대차대조표')
        # self.addTab(self.tabs[2], '수협 입금')

    def selection_changed(self, tab_type):
        self.selected_total = self.tabs[tab_type].selected_total
        self.selected_total_changed.emit()