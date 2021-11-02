from PySide6.QtWidgets import QTabWidget, QWidget, QTableWidget, QGridLayout, QTableWidgetItem
from controller.db_manager import session
from models.models import DayCalOwner


# 일일 정산서 계산서 위젯
class DayCal(QWidget):
    # 생성자
    def __init__(self):
        super().__init__()
        self.owners = [q.name for q in session.query(DayCalOwner).order_by(DayCalOwner.id)]
        self.num_of_owners = len(self.owners)
        self.input_table = QTableWidget()
        self.input_table.setParent(self)
        self.init_ui()

    # ui 초기화
    def init_ui(self):
        # 화주 목록
        self.input_table.setColumnCount(self.num_of_owners)
        self.input_table.setHorizontalHeaderLabels(self.owners)
        self.input_table.setRowCount(19)
        self.input_table.setVerticalHeaderLabels([
            '강동총금액', '강동운임', '강동하차비', '강동수수료 4%', '공제후금액', '',
            '중매수수료 5%', '화주운임', '화주하차비', '상장수수료 4%', '강동선지급금', '공제합계', '선지급금포함 공제합계', '',
            '경매 사무실입금', '가라경매 강동입금', '직접지출', '우리경매', '강동사입'
                                       ])

        # 그리드 레이아웃
        grid = QGridLayout()

        # 테이블위젯 추가
        grid.addWidget(self.input_table, 0, 0)

        # 레이아웃 세팅
        self.setLayout(grid)

    # 화주 추가 반영
    def owner_added(self, added_user):
        self.owners.append(added_user)
        self.input_table.insertColumn(self.input_table.columnCount())
        self.input_table.setHorizontalHeaderItem(self.input_table.columnCount()-1, QTableWidgetItem(added_user))

    # 화주 삭제 반영
    def owner_removed(self, removed_name):
        idx = self.owners.index(removed_name)
        self.input_table.removeColumn(idx)
        del self.owners[idx]

    # 화주 이름 변경 반영
    def owner_modified(self, org_name, chg_name):
        idx = self.owners.index(org_name)
        self.owners[idx] = chg_name
        self.input_table.setHorizontalHeaderItem(idx, QTableWidgetItem(chg_name))


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
