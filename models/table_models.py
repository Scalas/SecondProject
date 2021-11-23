import operator

from PySide6.QtCore import QAbstractTableModel, Qt, SIGNAL, QModelIndex
from PySide6.QtGui import *


class DayCalTableModel(QAbstractTableModel):
    def __init__(self, parent, owner_list, data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.setParent(parent)
        self.table_data = data
        self.owner_list = owner_list
        self.vertical_header = ['강동총금액', '강동운임', '강동하차비', '강동수수료 4%', '공제후 금액', '중매수수료 5%', '화주운임', '화주하차비', '상장수수료 4%', '강동선지급금', '공제합계', '선지급금포함 공제합계']
        self.row_count = len(self.vertical_header)
        self.column_count = len(self.owner_list)

    def rowCount(self, parent):
        return self.row_count

    def columnCount(self, parent):
        return self.column_count

    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self.table_data[index.column()][index.row()]
                return value

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.owner_list[section][1]
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

    def setData(self, index: QModelIndex, value, role):
        if role == Qt.EditRole:
            r, c = index.row(), index.column()
            self.changed(r, c, self.table_data[c][r], value)
            self.table_data[c][r] = value
            return True
        return False

    def owner_added(self, owner_id, name, owner_type):
        self.beginInsertColumns(QModelIndex(), self.column_count, self.column_count)
        self.owner_list.append((owner_id, name, owner_type))
        self.table_data.append([0]*12)
        self.column_count += 1
        self.endInsertColumns()

    def owner_removed(self, owner_id):
        idx = 0
        for i in range(len(self.owner_list)):
            if self.owner_list[i][0] == owner_id:
                idx = i
                break

        self.beginRemoveColumns(QModelIndex(), idx, idx)
        self.table_data.pop(idx)
        self.owner_list.pop(idx)
        self.column_count -= 1
        self.endRemoveColumns()

    def owner_modified(self, owner_id, chg):
        idx = 0
        for i in range(len(self.owner_list)):
            if self.owner_list[i][0] == owner_id:
                idx = i
                break
        self.owner_list[idx][1] = chg

    def changed(self, r, c, org, chg):
        # 강동 총금액
        if r == 0:
            # => 강동수수료 4%
            # 생물 4%
            if self.owner_list[c][2]:
                self.setData(self.index(3, c), int(chg * 0.04), Qt.EditRole)
            # 냉동 2%
            else:
                self.setData(self.index(3, c), int(chg * 0.02), Qt.EditRole)

            # => 공제 후 금액
            val = self.table_data[c][4]
            val += (chg - org)
            self.setData(self.index(4, c), val, Qt.EditRole)

        # 강동운임 ~ 강동수수료
        elif 1 <= r <= 3:
            # => 공제후 금액
            val = self.table_data[c][4]
            val -= (chg - org)
            self.setData(self.index(4, c), val, Qt.EditRole)

        # 중매수수료 5% ~ 상장수수료 4%
        elif 5 <= r <= 8:
            # => 공제 합계
            val = self.table_data[c][10]
            val += (chg - org)
            self.setData(self.index(10, c), val, Qt.EditRole)

        # 강동선지급금
        elif r == 9:
            # => 선지급금 포함 공제합계
            val = self.table_data[c][11]
            val += (chg - org)
            self.setData(self.index(10, c), val, Qt.EditRole)

        # 공제합계
        elif r == 10:
            # => 선지급금 포함 공제합계
            val = self.table_data[c][11]
            val += (chg - org)
            self.setData(self.index(11, c), val, Qt.EditRole)


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
