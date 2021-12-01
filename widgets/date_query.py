from PySide6.QtWidgets import QDialog, QGridLayout, QCalendarWidget, QPushButton

from widgets.simple import TableView
from models.table_models import DayCalTableModel, DayCalOthersTableModel, DayCalResultTableModel
from models.db_models import DayCalOwner


# 날짜로 조회한 데이터를 표시하기 위한 위젯
# 기본적으로 DayCal 위젯과 거의 동일한 구조를 가짐
class DayCalQueryResult(QDialog):
    # 생성자
    def __init__(self, parent, owner_values, other_values, result, today):
        super().__init__(parent)
        # 화주별 데이터, 기타 데이터, 결과 데이터, 조회날짜를 인자로 받아온다
        self.owner_values = owner_values
        self.other_values = other_values
        self.result = result
        self.today = today

        # 화주별 데이터를 기반으로 임시 화주 명단을 생성
        self.owner_list = []
        for values in self.owner_values:
            self.owner_list.append(DayCalOwner(values.get_owner_name(), values.get_owner_type(), values.get_owner_id()))

        # 입력 테이블 생성(화주별 데이터)
        self.input_table = TableView()
        self.data_model = DayCalTableModel(self, self.owner_list, self.owner_values)
        self.input_table.setModel(self.data_model)

        # 기타 테이블 생성(기타 데이터)
        self.other_table = TableView()
        self.other_data_model = DayCalOthersTableModel(self, self.other_values)
        self.other_table.setModel(self.other_data_model)

        # 결과 테이블 생성
        self.result_table = TableView()
        self.result_data_model = DayCalResultTableModel(self, self.result)
        self.result_table.setModel(self.result_data_model)

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

        # 초기 윈도우사이즈 설정
        self.setGeometry(100, 100, 1446, 620)

        # 스타일 설정
        self.setStyleSheet("background-color: #FFFFFF")

        # 타이틀 설정
        self.setWindowTitle("일일정산서 계산서: " + self.today)


# 날짜로 데이터 조회를 위한 달력 위젯
# 다이얼로그(QDialog 상속)
class DateSelect(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.calendar = QCalendarWidget()
        self.submit = QPushButton('조회')
        self.submit.clicked.connect(self.success)
        self.canceled = True
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        grid.addWidget(self.calendar, 0, 0, 1, 3)
        grid.addWidget(self.submit, 1, 0, 1, 1)
        self.setLayout(grid)

    def show_modal(self):
        return super().exec_()

    def success(self):
        self.canceled = False
        self.close()