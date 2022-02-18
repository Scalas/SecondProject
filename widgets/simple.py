from PySide6.QtCore import QDateTime, QTimer, QEvent, QObject, Signal
from PySide6.QtWidgets import QLabel, QDialog, QTableView, QAbstractItemView, QStyledItemDelegate, QStatusBar, QLineEdit, QItemDelegate, QGridLayout, QPushButton
from PySide6.QtGui import QKeyEvent, QMouseEvent, QPainter, QPalette, QColor
from PySide6.QtCore import Qt, QItemSelection


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()


# 시간레이블 클래스(QLabel 상속)
# 1초마다 현재 날짜/시간을 갱신하여 표시하는 레이블
class TimeLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(100)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("font-size: 17px;")
        self.setText(QDateTime.currentDateTime().toString(' yyyy년 MM월 dd일 ddd hh:mm:ss'))

    def timeout(self):
        self.setText(QDateTime.currentDateTime().toString(' yyyy년 MM월 dd일 ddd hh:mm:ss'))

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit()


# 선택된 셀의 합을 표시하는 레이블
class SelectedTotalLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.total = 0
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("font-size: 20px;")
        self.setText("0")

    def set_sum(self, sum_val):
        self.total = sum_val
        self.setText(format(sum_val, ','))


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
    selected_total_changed = Signal(int)

    def __init__(self, parent, table_type):
        super().__init__(parent)
        self.setItemDelegate(ItemDelegate(self, table_type))
        self.selected_total = 0
        self.type = table_type

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key_Delete:
            for idx in self.selectionModel().selectedIndexes():
                if self.model().flags(idx) & Qt.ItemIsEditable:
                    self.model().setData(idx, 0, Qt.EditRole)
            self.repaint()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            index = self.moveCursor(QAbstractItemView.MoveDown, Qt.NoModifier)
            command = self.selectionCommand(index, event)
            self.selectionModel().setCurrentIndex(index, command)
        else:
            return super().keyPressEvent(event)

    def selectionChanged(self, selected:QItemSelection, deselected:QItemSelection) -> None:
        total = 0
        for index in self.selectionModel().selectedIndexes():
            total += int(self.model().data(index, Qt.EditRole))
        self.selected_total = total
        self.selected_total_changed.emit(self.type)
        super().selectionChanged(selected, deselected)


class ItemDelegate(QItemDelegate):
    def __init__(self, parent: TableView, table_type):
        super().__init__()
        self.setParent(parent)
        self.table_type = table_type

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            key_event = QKeyEvent(event)
            key = key_event.key()
            if key in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right):
                self.parent().keyPressEvent(key_event)
                return True
        super().eventFilter(object, event)
        return False


class CellEditor(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)


class SaveDialog(Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.save_data = False

    def init_ui(self):
        grid = QGridLayout()
        grid.addWidget(QLabel('변경 사항을 저장하시겠습니까?'), 0, 0, 1, 4)
        yes, no = QPushButton('Yes'), QPushButton('No')
        yes.clicked.connect(self.agree)
        no.clicked.connect(self.success)
        grid.addWidget(yes, 1, 0, 1, 2)
        grid.addWidget(no, 1, 2, 1, 2)
        self.setLayout(grid)
        self.setFixedWidth(280)
        self.setFixedHeight(100)
        self.setWindowTitle('저장되지 않은 변경사항이 존재합니다.')

    def agree(self):
        self.save_data = True
        self.success()
