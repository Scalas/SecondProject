from PySide6.QtCore import QDateTime, QTimer, QEvent, QObject, Signal
from PySide6.QtWidgets import QLabel, QDialog, QTableView, QAbstractItemView, QStyledItemDelegate, QStatusBar
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtCore import Qt


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()


# 시간레이블 클래스(QLabel 상속)
# 1초마다 현재 날짜/시간을 갱신하여 표시하는 레이블
class TimeLabel(QLabel):
    clicked = Signal()

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(100)
        self.init_ui()

    def init_ui(self):
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))

    def timeout(self):
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit()


# 다이얼로그(QDialog 상속)
class Dialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.canceled = True

    def show_modal(self):
        return super().exec_()

    def success(self):
        self.canceled = False
        self.close()


# QTableView 커스터마이징(QTableView 상속)
class TableView(QTableView):
    def __init__(self):
        super().__init__()
        self.setItemDelegate(ItemDelegate(self))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key_Delete:
            idx = self.currentIndex()
            if self.model().flags(idx) & Qt.ItemIsEditable:
                self.model().setData(idx, 0, Qt.EditRole)
            self.repaint()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            index = self.moveCursor(QAbstractItemView.MoveDown, Qt.NoModifier)
            command = self.selectionCommand(index, event)
            self.selectionModel().setCurrentIndex(index, command)
        else:
            return super().keyPressEvent(event)


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, parent: TableView):
        super().__init__()
        self.setParent(parent)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            key_event = QKeyEvent(event)
            key = key_event.key()
            if key in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right):
                self.parent().keyPressEvent(key_event)
                return True
        super().eventFilter(object, event)
        return False
