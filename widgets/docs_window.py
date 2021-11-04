from datetime import date

from PySide6.QtWidgets import QTabWidget, QWidget, QTableWidget, QGridLayout, QTableWidgetItem, QTableView

from controller import actions
from controller.db_manager import init_db, session
from models.table_models import DayCalTableModel
from models.db_models import DayCalOwnerValues


# 일일 정산서 계산서 위젯
class DayCal(QWidget):
    # 생성자
    def __init__(self):
        super().__init__()
        self.input_table = QTableView()
        self.input_table.setParent(self)
        self.init_ui()

    # ui 초기화
    def init_ui(self):
        self.data_model = DayCalTableModel(self, actions.get_daycal_owner_list(), ['강동총금액', '강동운임', '강동하차비', '강동수수료 4%', '공제후 금액', '중매수수료 5%', '화주운임', '화주하차비', '상장수수료 4%', '강동선지급금', '공제합계', '선지급금포함 공제합계'], actions.get_daycal_owner_values())
        self.input_table.setModel(self.data_model)

        # 그리드 레이아웃
        grid = QGridLayout()

        # 테이블위젯 추가
        grid.addWidget(self.input_table, 0, 0)

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
