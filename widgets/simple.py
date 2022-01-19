from PySide6.QtCore import QDateTime, QTimer, QEvent, QObject, Signal
from PySide6.QtWidgets import QLabel, QDialog, QTableView, QAbstractItemView, QStyledItemDelegate, QStatusBar, QStyleOptionViewItem, QFrame
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
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))

    def timeout(self):
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit()


# 선택된 셀의 합을 표시하는 레이블
class SelectedTotalLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.total = 0
        self.init_ui()

    def init_ui(self):
        self.setText("  선택된 셀 합계: 0")

    def set_sum(self, sum_val):
        self.total = sum_val
        self.setText("  선택된 셀 합계: %d" % sum_val)


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

    def selectionChanged(self, selected:QItemSelection, deselected:QItemSelection) -> None:
        total = 0
        for index in self.selectionModel().selectedIndexes():
            total += self.model().data(index, Qt.EditRole)
        self.selected_total_changed.emit(total)
        super().selectionChanged(selected, deselected)


class ItemDelegate(QStyledItemDelegate):
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

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index) -> None:
        # 일일정산서 - 화주별 데이터 테이블인 경우
        if self.table_type == 0:
            '''
            if index.row() in [3, 4, 10, 11]:
                painter.fillRect(option.rect, QColor(255,229,204))
            else:
                painter.fillRect(option.rect, QColor(204,229,255))
            '''
        super().paint(painter, option, index)


