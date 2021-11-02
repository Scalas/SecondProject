from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtWidgets import QLabel, QDialog


# 시간레이블 클래스(QLabel 상속)
# 1초마다 현재 날짜/시간을 갱신하여 표시하는 레이블
class TimeLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(100)

    def timeout(self):
        self.setText(QDateTime.currentDateTime().toString('yyyy년 MM월 dd일 ddd hh:mm:ss'))


# 다이얼로그(QDialog 상속)
class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.canceled = True

    def show_modal(self):
        return super().exec_()

    def success(self):
        self.canceled = False
        self.close()
