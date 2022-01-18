from PySide6.QtWidgets import QTabWidget, QWidget, QGridLayout, QTableView, QHeaderView

from controller import actions, db_manager
from models.table_models import DayCalTableModel, DayCalOthersTableModel, DayCalResultTableModel
from widgets.simple import TableView


# 일일 정산서 계산서 위젯
class DayCal(QWidget):
    # 생성자
    def __init__(self):
        super().__init__()
        # 화주명단, 화주별 데이터, 기타 데이터, 결과 데이터를 DB 에서 읽어온다
        self.owner_list = actions.get_daycal_owner_list()
        self.owner_values = actions.get_daycal_owner_values()
        self.other_values = actions.get_daycal_other_values()
        self.result = actions.get_daycal_result()

        # 입력 테이블 생성(화주별 데이터)
        self.input_table = TableView(0)
        self.data_model = DayCalTableModel(self, actions.get_daycal_owner_list(), actions.get_daycal_owner_values())
        self.input_table.setModel(self.data_model)
        self.input_table.verticalHeader().setMinimumWidth(170)

        # 기타 테이블 생성(기타 데이터)
        self.other_table = TableView(1)
        self.other_data_model = DayCalOthersTableModel(self, actions.get_daycal_other_values())
        self.other_table.setModel(self.other_data_model)
        self.other_table.verticalHeader().setMinimumWidth(170)
        self.other_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 결과 테이블 생성
        self.result_table = TableView(2)
        self.result_data_model = DayCalResultTableModel(self, actions.get_daycal_result())
        self.result_table.setModel(self.result_data_model)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.init_ui()

    # ui 초기화
    def init_ui(self):
        # 그리드 레이아웃
        grid = QGridLayout()

        # 테이블위젯 추가
        grid.addWidget(self.input_table, 0, 0)
        grid.addWidget(self.other_table, 1, 0)
        grid.addWidget(self.result_table, 0, 1, 2, 1)
        grid.setRowStretch(0, 5)
        grid.setColumnStretch(0, 5)

        # 레이아웃 세팅
        self.setLayout(grid)

    # 화주 추가 반영
    def owner_added(self, new_owner, today_values):
        self.data_model.owner_added(new_owner, today_values)

    # 화주 삭제 반영
    def owner_removed(self, removed_id):
        self.data_model.owner_removed(removed_id)

    # 화주 이름 변경 반영
    def owner_modified(self, modified_id, chg_name):
        self.data_model.owner_modified(modified_id, chg_name)


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
        self.tab1 = DayCal()
        self.tab1.setParent(self)
        self.tab2 = BalancedSheet()
        self.tab2.setParent(self)
        self.tab3 = SH()
        self.tab3.setParent(self)
        self.init_ui()

    def init_ui(self):
        self.addTab(self.tab1, '일일정산서 계산서')
        self.addTab(self.tab2, '대차대조표')
        self.addTab(self.tab3, '수협 입금')
