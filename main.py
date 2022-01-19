import sys
from datetime import date

from PySide6.QtWidgets import QApplication

from widgets import main_window
from models.db_models import DayCalOwnerValues, DayCalOtherValues, DayCalResult
from controller.db_manager import session

if __name__ == '__main__':
    # 매달 5일이 되면 이번달의 데이터를 제외한 데이터를 모두 삭제
    today = date.today()
    if today.day == 19:
        first_day = date(today.year, today.month, 1)
        target = session.query(DayCalOwnerValues).filter(DayCalOwnerValues.date < first_day).all()
        for t in target:
            session.delete(t)
        target = session.query(DayCalOtherValues).filter(DayCalOtherValues.date < first_day).all()
        for t in target:
            session.delete(t)
        target = session.query(DayCalResult).filter(DayCalResult.date < first_day).all()
        for t in target:
            session.delete(t)
        session.commit()

    app = QApplication(sys.argv)
    app.setStyleSheet("TableView { border: 1px solid; font-size: 15px; margin: 0px; padding: 0px; }"
                      "QHeaderView::section:horizontal {"
                      " font-size: 15px;"
                      " font-weight: bold;"
                      " border: 1px solid;"
                      " margin: 0px;"
                      " border-bottom: 2px solid "
                      "}"
                      "QHeaderView::section:horizontal:last {"
                      " font-size: 15px;"
                      " font-weight: bold;"
                      " border: 1px solid;"
                      " margin: 0px;"
                      " border-bottom: 2px solid;"
                      " border-right: 2px solid }"
                      "QHeaderView::section:vertical {"
                      " font-size: 15px;"
                      " font-weight: bold;"
                      " border: 1px solid;"
                      " margin: 0px;"
                      " border-right: 2px solid }"
                      "QTableCornerButton::section {"
                      " border: 1px solid;"
                      " margin: 0px;"
                      "}"
                      )
    screen = main_window.MainWindow()
    sys.exit(app.exec())
