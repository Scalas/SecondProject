from PySide6.QtWidgets import QLabel, QGridLayout, QPushButton, QLineEdit
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.exc import UnmappedInstanceError

from controller.db_manager import session
from models.models import DayCalOwner
from widgets.simple import Dialog


# 화주 추가
def create_owner(main_window, table_widget, name_data=None):
    # 입력받은 이름이 이미 있는 경우
    if name_data:
        name = name_data

    # 이름을 입력받아야 하는 경우
    else:
        # 다이얼로그 위젯 생성
        create_owner_dialog = Dialog()
        create_owner_dialog.setWindowTitle('화주 추가')
        create_owner_dialog.setGeometry(500, 500, 300, 50)

        # 화주 이름을 입력받기 위한 다이얼로그 ui 세팅
        grid = QGridLayout()
        input_name = QLineEdit()
        input_name.setPlaceholderText('화주 이름')
        input_name.returnPressed.connect(create_owner_dialog.success)
        submit = QPushButton('추가')
        submit.clicked.connect(create_owner_dialog.success)
        grid.addWidget(QLabel('화주 이름: '), 0, 0, 1, 1)
        grid.addWidget(input_name, 0, 1, 1, 2)
        grid.addWidget(submit, 1, 0, 1, 3)
        create_owner_dialog.setLayout(grid)

        # 다이얼로그를 modal 하게 표시
        create_owner_dialog.show_modal()

        # 입력이 취소된경우 (다이얼로그를 그냥 종료한 경우) 추가절차 종료
        if create_owner_dialog.canceled:
            return

        # 다이얼로그에서 입력이 완료되면 입력받은 이름을 name 으로 설정
        name = input_name.text()

    # 새 화주 추가
    new_owner = DayCalOwner(name)
    try:
        session.add(new_owner)
        session.commit()
        table_widget.owner_added(name)
    except DatabaseError:
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
        delete_owner_dialog = Dialog()
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
        session.commit()
        table_widget.owner_removed(target.name)
    except UnmappedInstanceError:
        main_window.statusBar().showMessage('>> 등록되지 않은 화주입니다.')


# 화주 이름 변경
def modify_owner(main_window, table_widget, name_data=None):
    # 다이얼로그 위젯 생성
    modify_owner_dialog = Dialog()
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
        table_widget.owner_modified(name, changed)
    except AttributeError:
        main_window.statusBar().showMessage('>> 등록되지 않은 화주입니다.')
    except DatabaseError:
        main_window.statusBar().showMessage('>> 이미 등록된 화주입니다.')
        session.rollback()
