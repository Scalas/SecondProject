from PySide6.QtWidgets import QTabWidget, QWidget, QTableWidget, QGridLayout
from controller.db_manager import session
from models.models import DayCalOwner
from models.models import DayCalValues


# 일일 정산서 계산서 위젯
class DayCal(QWidget):
    # 생성자
    def __init__(self):
        super().__init__()
        self.init_ui()

    # ui 초기화
    def init_ui(self):
        # 화주 목록
        owners = [q.name for q in session.query(DayCalOwner)]
        input_table = QTableWidget()
        input_table.setColumnCount(len(owners))
        input_table.setHorizontalHeaderLabels(owners)
        input_table.setRowCount(19)
        input_table.setVerticalHeaderLabels([
            '강동총금액', '강동운임', '강동하차비', '강동수수료 4%', '공제후금액', '',
            '중매수수료 5%', '화주운임', '화주하차비', '상장수수료 4%', '강동선지급금', '공제합계', '선지급금포함 공제합계', '',
            '경매 사무실입금', '가라경매 강동입금', '직접지출', '우리경매', '강동사입'
                                       ])

        # 그리드 레이아웃
        grid = QGridLayout()

        # 테이블위젯 추가
        grid.addWidget(input_table, 0, 0)

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
