from PySide6.QtWidgets import QDialog, QGridLayout, QCalendarWidget, QPushButton, QHeaderView, QHBoxLayout
from PySide6.QtCore import Signal, Qt

from widgets.simple import TableView, SelectedTotalLabel
from models.table_models import DayCalTableModel, DayCalOthersTableModel, DayCalResultTableModel
from models.db_models import DayCalOwner
from controller import actions


# 날짜로 조회한 데이터를 표시하기 위한 위젯
# 기본적으로 DayCal 위젯과 거의 동일한 구조를 가짐
class DayCalQueryResult(QDialog):
    submitted = Signal()

    # 생성자
    def __init__(self, parent, owner_values, other_values, result, today):
        super().__init__(parent)
        # 화주별 데이터, 기타 데이터, 결과 데이터, 조회날짜를 인자로 받아온다
        self.owner_values = owner_values
        self.other_values = other_values
        self.result = result

        # 인쇄, 저장 버튼
        self.buttons = QHBoxLayout()
        self.save_button = QPushButton('저장')
        self.save_button.clicked.connect(lambda: self.submitted.emit())
        self.print_button = QPushButton('인쇄')
        self.print_button.clicked.connect(self.print_result)

        # 선택된 셀의 합계
        self.selected_total_label = SelectedTotalLabel(self)
        self.selected_total_label.setAlignment(Qt.AlignRight)

        # 오늘 날짜
        self.today = today

        # 화주별 데이터를 기반으로 임시 화주 명단을 생성
        self.owner_list = []
        for values in self.owner_values:
            self.owner_list.append(DayCalOwner(values.get_owner_name(), values.get_owner_type(), values.get_owner_id()))

        # 테이블 리스트
        self.tables = []

        # 입력 테이블 생성(화주별 데이터)
        input_table = TableView(self, 0)
        input_table.setModel(DayCalTableModel(self, self.owner_list, self.owner_values))
        input_table.selected_total_changed.connect(self.selection_changed)
        input_table.verticalHeader().setMinimumWidth(170)
        self.tables.append(input_table)

        # 기타 테이블 생성(기타 데이터)
        other_table = TableView(self, 1)
        other_table.setModel(DayCalOthersTableModel(self, self.other_values))
        other_table.selected_total_changed.connect(self.selection_changed)
        other_table.verticalHeader().setMinimumWidth(170)
        other_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tables.append(other_table)

        # 결과 테이블 생성
        result_table = TableView(self, 2)
        result_table.setModel(DayCalResultTableModel(self, self.result))
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

        # 버튼 추가
        self.buttons.addWidget(self.print_button)
        self.buttons.addWidget(self.save_button)
        grid.addLayout(self.buttons, 2, 1)
        grid.setRowStretch(0, 5)
        grid.setColumnStretch(0, 5)

        # 선택된 셀의 합계 추가
        grid.addWidget(self.selected_total_label, 2, 0)

        # 레이아웃 세팅
        self.setLayout(grid)

        # 초기 윈도우사이즈 설정
        self.setGeometry(100, 100, 1446, 643)

        # 스타일 설정
        self.setStyleSheet("background-color: #FFFFFF")

        # 타이틀 설정
        self.setWindowTitle("일일정산서 계산서: " + self.today)

    # 인쇄
    def print_result(self):
        self.save_button.hide()
        self.print_button.hide()
        self.selected_total_label.hide()
        actions.daycal_print(self)
        self.save_button.show()
        self.print_button.show()
        self.selected_total_label.show()

    # 선택된 셀의 합계 갱신
    def selection_changed(self, table_type):
        self.selected_total_label.set_sum(self.tables[table_type].selected_total)

    def close(self):
        self.parent().repaint()


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