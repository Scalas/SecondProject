from datetime import date

from PySide6.QtWidgets import QTabWidget, QWidget, QGridLayout, QTableView

from controller import actions
from models.table_models import DayCalTableModel, DayCalOthersTableModel, DayCalResultTableModel


# 일일 정산서 계산서 위젯
class DayCal(QWidget):
    # 생성자
    def __init__(self):
        super().__init__()
        self.input_table = QTableView()
        self.other_table = QTableView()
        self.result_table = QTableView()
        self.init_ui()

    # ui 초기화
    def init_ui(self):
        # 화주별 데이터 입력테이블
        owner_list = actions.get_daycal_owner_list()
        owner_data = actions.get_daycal_owner_values()
        self.data_model = DayCalTableModel(self, owner_list, owner_data)
        self.input_table.setModel(self.data_model)

        # 기타 데이터 입력 테이블
        other_data = actions.get_daycal_other_values()
        self.other_data_model = DayCalOthersTableModel(self, other_data)
        self.other_table.setModel(self.other_data_model)

        # 결과 테이블
        self.result_data_model = DayCalResultTableModel(self, owner_data, other_data)
        self.result_table.setModel(self.result_data_model)

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
    def owner_added(self, added_user):
        self.data_model.owner_added(added_user)

    # 화주 삭제 반영
    def owner_removed(self, removed_name):
        self.data_model.owner_removed(removed_name)

    # 화주 이름 변경 반영
    def owner_modified(self, org_name, chg_name):
        self.data_model.owner_modified(org_name, chg_name)


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
