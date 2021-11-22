import operator

from PySide6.QtCore import QAbstractTableModel, Qt, SIGNAL, QModelIndex
from PySide6.QtGui import *


class DayCalTableModel(QAbstractTableModel):
    def __init__(self, parent, horizontal_header, data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.setParent(parent)
        self.table_data = data
        self.horizontal_header = horizontal_header
        self.vertical_header = ['강동총금액', '강동운임', '강동하차비', '강동수수료 4%', '공제후 금액', '중매수수료 5%', '화주운임', '화주하차비', '상장수수료 4%', '강동선지급금', '공제합계', '선지급금포함 공제합계']
        self.row_count = len(self.vertical_header)
        self.column_count = len(self.horizontal_header)

    def rowCount(self, parent):
        return self.row_count

    def columnCount(self, parent):
        return self.column_count

    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self.table_data[index.column()][index.row()]
                return str(value)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.horizontal_header[section]
            else:
                return self.vertical_header[section]
        return None

    def sort(self, col, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.table_data = sorted(self.table_data, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.table_data.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def flags(self, index):
        if index.row() in [3, 4, 10, 11]:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.table_data[index.column()][index.row()] = value
            return True
        return False

    def owner_added(self, name):
        self.beginInsertColumns(QModelIndex(), self.column_count, self.column_count)
        self.horizontal_header.append(name)
        self.table_data.append([0]*12)
        self.column_count += 1
        self.endInsertColumns()

    def owner_removed(self, name):
        idx = self.horizontal_header.index(name)
        self.beginRemoveColumns(QModelIndex(), idx, idx)
        self.table_data.pop(idx)
        self.horizontal_header.pop(idx)
        self.column_count -= 1
        self.endRemoveColumns()

    def owner_modified(self, org, chg):
        idx = self.horizontal_header.index(org)
        self.horizontal_header[idx] = chg


class DayCalOthersTableModel(QAbstractTableModel):
    def __init__(self, parent, data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.setParent(parent)
        self.table_data = [data]
        self.vertical_header = ['경매 사무실 입금', '가라경매 강동 입금', '직접 지출', '우리 경매', '강동 사입']
        self.row_count = len(self.vertical_header)
        self.column_count = 1

    def rowCount(self, parent):
        return self.row_count

    def columnCount(self, parent):
        return self.column_count

    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self.table_data[index.column()][index.row()]
                return str(value)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return self.vertical_header[section]
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.table_data[index.column()][index.row()] = value
            return True
        return False


class DayCalResultTableModel(QAbstractTableModel):
    def __init__(self, parent, result_data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.setParent(parent)
        self.horizontal_header = ['계']
        self.vertical_header = ['강동총금액 합계', '강동운임 합계', '강동하차비 합계', '강동수수료 4% 합계', '공제후금액 합계',
                                '중매수수료 5% 합계', '화주운임 합계', '화주하차비 합계', '상장수수료 4% 합계', '경매확인',
                                '경매 차액', '중개수수료 5%', '경매 차익']
        self.row_count = len(self.vertical_header)
        self.column_count = 1

        self.table_data = [result_data]

    def rowCount(self, parent):
        return self.row_count

    def columnCount(self, parent):
        return self.column_count

    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self.table_data[index.column()][index.row()]
                return str(value)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return self.vertical_header[section]
            else:
                return self.horizontal_header[section]
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
