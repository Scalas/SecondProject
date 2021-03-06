from datetime import date

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QApplication, QLabel, QGridLayout, QPushButton, QLineEdit, QComboBox, QRadioButton
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtGui import QPageLayout, QPainter, QPageSize
from PySide6.QtWidgets import QWidget

from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy import and_

from controller.db_manager import session, commit_db
from models.db_models import DayCalOwner, DayCalOwnerValues, DayCalOtherValues, DayCalResult
from widgets.simple import Dialog
from widgets.date_query import DayCalQueryResult, DateSelect


# 화주 추가
def create_owner(main_window, table_view, name_data=None, owner_type_data=None):
    # 입력받은 이름이 이미 있는 경우
    if name_data:
        name = name_data
        owner_type = owner_type_data

    # 이름을 입력받아야 하는 경우
    else:
        # 다이얼로그 위젯 생성
        create_owner_dialog = Dialog(main_window)
        create_owner_dialog.setWindowTitle('화주 추가')
        create_owner_dialog.setGeometry(500, 500, 300, 50)

        # 화주 이름을 입력받기 위한 다이얼로그 ui 세팅
        grid = QGridLayout()
        input_name = QLineEdit()
        input_name.setPlaceholderText('화주 이름')
        input_name.returnPressed.connect(create_owner_dialog.success)
        submit = QPushButton('추가')
        submit.clicked.connect(create_owner_dialog.success)
        type_0 = QRadioButton('냉동')
        type_1 = QRadioButton('생물')
        type_1.setChecked(True)
        grid.addWidget(QLabel('화주 이름: '), 0, 0, 1, 1)
        grid.addWidget(input_name, 0, 1, 1, 2)
        grid.addWidget(QLabel('화주 종류: '), 1, 0, 1, 1)
        grid.addWidget(type_0, 1, 1, 1, 1)
        grid.addWidget(type_1, 1, 2, 1, 1)
        grid.addWidget(submit, 2, 0, 1, 3)
        create_owner_dialog.setLayout(grid)

        # 다이얼로그를 modal 하게 표시
        create_owner_dialog.show_modal()

        # 입력이 취소된경우 (다이얼로그를 그냥 종료한 경우) 추가절차 종료
        if create_owner_dialog.canceled:
            return

        # 다이얼로그에서 입력이 완료되면 입력받은 이름을 name 으로 설정
        name = input_name.text()
        owner_type = 0 if type_0.isChecked() else 1

    # 새 화주 추가
    new_owner = DayCalOwner(name, owner_type)
    try:
        session.add(new_owner)
        session.flush()
        session.refresh(new_owner)
        today_values = DayCalOwnerValues(date.today(), new_owner.id, new_owner.name, new_owner.owner_type)
        session.add(today_values)
        session.commit()
        table_view.owner_added(new_owner, today_values)
    except ValueError:
        main_window.statusBar().showMessage('>> 이미 등록된 화주입니다.')
        session.rollback()


# 화주 삭제
def delete_owner(main_window, table_widget, name_data=None):
    # 입력받은 이름이 이미 있는 경우
    if name_data:
        name = name_data

    # 이름을 입력받아야 하는 경우
    else:
        # 다이얼로그 위젯 생성
        delete_owner_dialog = Dialog(main_window)
        delete_owner_dialog.setWindowTitle('화주 삭제')
        delete_owner_dialog.setGeometry(500, 500, 300, 50)

        # 화주 이름을 입력받기 위한 다이얼로그 ui 세팅
        grid = QGridLayout()
        input_name = QLineEdit()
        input_name.setPlaceholderText('화주 이름')
        input_name.returnPressed.connect(delete_owner_dialog.success)
        submit = QPushButton('삭제')
        submit.clicked.connect(delete_owner_dialog.success)
        grid.addWidget(QLabel('화주 이름: '), 0, 0, 1, 1)
        grid.addWidget(input_name, 0, 1, 1, 2)
        grid.addWidget(submit, 1, 0, 1, 3)
        delete_owner_dialog.setLayout(grid)

        # 다이얼로그를 modal 하게 표시
        delete_owner_dialog.show_modal()

        # 입력이 취소된경우 (다이얼로그를 그냥 종료한 경우) 삭제절차 종료
        if delete_owner_dialog.canceled:
            return

        # 다이얼로그에서 입력이 완료되면 입력받은 이름을 name 으로 설정
        name = input_name.text()

    # 화주 삭제
    try:
        target = session.query(DayCalOwner).filter(DayCalOwner.name == name).first()
        session.delete(target)
        target_data = session.query(DayCalOwnerValues).filter(and_(DayCalOwnerValues.owner_id == target.id, DayCalOwnerValues.date == date.today())).first()
        session.delete(target_data)
        session.commit()
        table_widget.owner_removed(target.id)
    except UnmappedInstanceError:
        main_window.statusBar().showMessage('>> 등록되지 않은 화주입니다.')


# 화주 이름 변경
def modify_owner(main_window, table_widget, name_data=None):
    # 다이얼로그 위젯 생성
    modify_owner_dialog = Dialog(main_window)
    modify_owner_dialog.setWindowTitle('화주 이름 변경')
    modify_owner_dialog.setGeometry(500, 500, 300, 50)
    grid = QGridLayout()

    # 화주 이름을 미리 입력받지 않은 경우(메뉴바나 툴바에서 변경액션에 접근한 경우)
    org_name = QLineEdit()
    if not name_data:
        # 화주 이름을 입력받기 위한 다이얼로그 ui 세팅
        org_name.setPlaceholderText('화주 이름')
        grid.addWidget(QLabel('화주 이름: '), 0, 0, 1, 1)
        grid.addWidget(org_name, 0, 1, 1, 2)

    chg_name = QLineEdit()
    chg_name.setPlaceholderText('바꿀 이름')
    chg_name.returnPressed.connect(modify_owner_dialog.success)
    submit = QPushButton('변경')
    submit.clicked.connect(modify_owner_dialog.success)

    grid.addWidget(QLabel('바꿀 이름: '), 1, 0, 1, 1)
    grid.addWidget(chg_name, 1, 1, 1, 2)
    grid.addWidget(submit, 2, 0, 1, 3)
    modify_owner_dialog.setLayout(grid)

    # 다이얼로그를 modal 하게 표시
    modify_owner_dialog.show_modal()

    # 입력이 취소된경우 (다이얼로그를 그냥 종료한 경우) 삭제절차 종료
    if modify_owner_dialog.canceled:
        return

    # 대상 화주이름 name 과 바꿀 이름 changed 를 설정
    name = name_data if name_data else org_name.text()
    changed = chg_name.text()

    # 화주 이름 변경
    try:
        target = session.query(DayCalOwner).filter(DayCalOwner.name == name).first()
        target.name = changed
        session.commit()
        table_widget.owner_modified(target.id, changed)
    except AttributeError:
        main_window.statusBar().showMessage('>> 등록되지 않은 화주입니다.')
    except DatabaseError:
        main_window.statusBar().showMessage('>> 이미 등록된 화주입니다.')
        session.rollback()


# 인쇄 기능
def daycal_print(print_widget: QWidget):
    printer = QPrinter(QPrinter.HighResolution)
    printer.setPageOrientation(QPageLayout.Landscape)
    printer.setPageSize(QPageSize.A4Small)
    printer.setFullPage(False)
    painter = QPainter()
    painter.begin(printer)
    rect = printer.pageLayout().paintRectPixels(printer.resolution())
    scale = min(rect.width() / print_widget.width(), rect.height() / print_widget.height())
    painter.scale(scale, scale)
    print_widget.render(painter, QPoint(5, 5))
    painter.end()


# DB 액션
# 화주 명단 가져오기
def get_daycal_owner_list():
    return session.query(DayCalOwner).order_by(DayCalOwner.id).all()


# 화주별 데이터 가져오기
def get_daycal_owner_values(today=None):
    if today:
        return session.query(DayCalOwnerValues).filter(DayCalOwnerValues.date == today).order_by(DayCalOwnerValues.owner_id).all()

    today = date.today()
    values = []
    owner_list = get_daycal_owner_list()
    for owner in owner_list:
        id = owner.get_id()
        name = owner.get_name()
        owner_type = owner.get_type()
        value = session.query(DayCalOwnerValues).filter(and_(DayCalOwnerValues.owner_id == id, DayCalOwnerValues.date == today)).first()
        if not value:
            value = DayCalOwnerValues(today, id, name, owner_type)
            session.add(value)
            session.commit()
        values.append(value)
    return values


# 기타 데이터 가져오기
def get_daycal_other_values(today=date.today()):
    value = session.query(DayCalOtherValues).filter(DayCalOtherValues.date == today).first()
    if not value:
        value = DayCalOtherValues(today)
        session.add(value)
        session.commit()
    return value


# 결과 데이터 가져오기
def get_daycal_result(today=date.today()):
    value = session.query(DayCalResult).filter(DayCalResult.date == today).first()
    if not value:
        value = DayCalResult(today)
        session.add(value)
        session.commit()

    return value


# 날짜로 데이터 조회
def date_query(parent, tab):
    date_select = DateSelect(parent)
    date_select.show_modal()

    if not date_select.canceled:
        if tab == 0:
            today = date_select.calendar.selectedDate().toString('yyyy-MM-dd')
            result = DayCalQueryResult(parent, get_daycal_owner_values(today), get_daycal_other_values(today), get_daycal_result(today), today)
            result.submitted.connect(commit_db)
            result.show()
