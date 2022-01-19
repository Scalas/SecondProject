import operator

from PySide6.QtCore import QAbstractTableModel, Qt, SIGNAL, QModelIndex
from PySide6.QtGui import *


class DayCalTableModel(QAbstractTableModel):
    def __init__(self, parent, owner_list, data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.setParent(parent)
        self.table_data = data
        self.owner_list = owner_list
        self.vertical_header = [
            ' 강동총금액',
            ' 강동운임',
            ' 강동하차비',
            ' 강동수수료 4%',
            ' 공제후 금액',
            '       중매수수료 5%',
            '       화주운임',
            '       화주하차비',
            '       상장수수료 4%',
            '       강동선지급금',
            '       공제합계',
            ' 선지급금포함 공제합계']
        self.row_count = len(self.vertical_header)
        self.column_count = len(self.owner_list)

    def rowCount(self, parent):
        return self.row_count

    def columnCount(self, parent):
        return self.column_count

    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole:
                value = self.table_data[index.column()].get(index.row())
                return format(value, ',')
            elif role == Qt.EditRole:
                value = str(self.table_data[index.column()].get(index.row()))
                return value
            elif role == Qt.TextAlignmentRole:
                return int(Qt.AlignRight | Qt.AlignVCenter)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.owner_list[section].get(1)
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

    def setData(self, index: QModelIndex, value: int, role):
        if role == Qt.EditRole:
            try:
                value = int(value)
            except ValueError:
                return False
            r, c = index.row(), index.column()
            self.changed(r, c, self.table_data[c].get(r), int(value))
            self.table_data[c].set(r, int(value))
            return True
        return False

    def owner_added(self, new_owner, today_values):
        self.beginInsertColumns(QModelIndex(), self.column_count, self.column_count)
        self.owner_list.append(new_owner)
        self.table_data.append(today_values)
        self.column_count += 1
        self.endInsertColumns()

    def owner_removed(self, owner_id):
        idx = 0
        for i in range(len(self.owner_list)):
            if self.owner_list[i].get(0) == owner_id:
                idx = i
                break
        for row in range(12):
            self.setData(self.index(row, idx), 0, Qt.EditRole)
        self.beginRemoveColumns(QModelIndex(), idx, idx)
        self.table_data.pop(idx)
        self.owner_list.pop(idx)
        self.column_count -= 1
        self.endRemoveColumns()

    def owner_modified(self, owner_id, chg):
        idx = 0
        for i in range(len(self.owner_list)):
            if self.owner_list[i].get(0) == owner_id:
                idx = i
                break
        self.owner_list[idx].set(1, chg)

    def changed(self, row, column, org, chg):
        # 강동 총금액
        if row == 0:
            # => 강동수수료 4%
            # 생물 4%
            if self.owner_list[column].get(2):
                self.setData(self.index(3, column), int(chg * 0.04), Qt.EditRole)
            # 냉동 2%
            else:
                self.setData(self.index(3, column), int(chg * 0.02), Qt.EditRole)

            # => 공제 후 금액
            val = self.table_data[column].get(4)
            val += (chg - org)
            self.setData(self.index(4, column), val, Qt.EditRole)

            # => 결과테이블 합계값
            self.parent().tables[2].model().out_changed(0, row, org, chg)
            self.parent().tables[2].repaint()

        # 강동운임 ~ 강동수수료
        elif 1 <= row <= 3:
            # => 공제후 금액
            val = self.table_data[column].get(4)
            val -= (chg - org)
            self.setData(self.index(4, column), val, Qt.EditRole)

            # => 결과테이블 합계값
            self.parent().tables[2].model().out_changed(0, row, org, chg)
            self.parent().tables[2].repaint()

        elif row == 4:
            # => 결과테이블 합계값
            self.parent().tables[2].model().out_changed(0, row, org, chg)
            self.parent().tables[2].repaint()

        # 중매수수료 5% ~ 상장수수료 4%
        elif 5 <= row <= 8:
            # => 공제 합계
            val = self.table_data[column].get(10)
            val += (chg - org)
            self.setData(self.index(10, column), val, Qt.EditRole)

            # => 결과테이블 합계값
            self.parent().tables[2].model().out_changed(0, row, org, chg)
            self.parent().tables[2].repaint()

        # 강동선지급금
        elif row == 9:
            # => 선지급금 포함 공제합계
            val = self.table_data[column].get(11)
            val += (chg - org)
            self.setData(self.index(10, column), val, Qt.EditRole)

        # 공제합계
        elif row == 10:
            # => 선지급금 포함 공제합계
            val = self.table_data[column].get(11)
            val += (chg - org)
            self.setData(self.index(11, column), val, Qt.EditRole)


class DayCalOthersTableModel(QAbstractTableModel):
    def __init__(self, parent, data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.setParent(parent)
        self.table_data = [data]
        self.horizontal_header = ['금액']
        self.vertical_header = [' 경매 사무실 입금', ' 가라경매 강동 입금', ' 직접 지출', ' 우리 경매', ' 강동 사입']
        self.row_count = len(self.vertical_header)
        self.column_count = 1

    def rowCount(self, parent):
        return self.row_count

    def columnCount(self, parent):
        return self.column_count

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self.table_data[index.column()].get(index.row())
            return format(value, ',')
        elif role == Qt.EditRole:
            value = str(self.table_data[index.column()].get(index.row()))
            return value
        elif role == Qt.TextAlignmentRole:
            return int(Qt.AlignRight | Qt.AlignVCenter)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return self.vertical_header[section]
            else:
                return self.horizontal_header[section]
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index: QModelIndex, value: int, role):
        if role == Qt.EditRole:
            try:
                value = int(value)
            except ValueError:
                return False
            r, c = index.row(), index.column()
            self.changed(r, c, self.table_data[c].get(r), int(value))
            self.table_data[c].set(r, int(value))
            return True
        return False

    def changed(self, row, column, org, chg):
        self.parent().tables[2].model().out_changed(1, row, org, chg)
        self.parent().tables[2].repaint()


class DayCalResultTableModel(QAbstractTableModel):
    def __init__(self, parent, result_data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.setParent(parent)
        self.horizontal_header = ['합계']
        self.vertical_header = [
            '  강동총금액 합계',
            '  운임 합계',
            '  하차비 합계',
            '  수수료 4% 합계',
            ' 공제후금액 합계',
            '       중매수수료계',
            '       화주운임계',
            '       화주하차비계',
            '       상장4%계',
            '  경매확인',
            '  경매 차액',
            '  중개수수료 5%',
            '  경매 차익']
        self.row_count = len(self.vertical_header)
        self.column_count = 1

        self.table_data = [result_data]

    def rowCount(self, parent):
        return self.row_count

    def columnCount(self, parent):
        return self.column_count

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self.table_data[index.column()].get(index.row())
            return format(value, ',')
        elif role == Qt.EditRole:
            value = str(self.table_data[index.column()].get(index.row()))
            return value
        elif role == Qt.TextAlignmentRole:
            return int(Qt.AlignRight | Qt.AlignVCenter)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return self.vertical_header[section]
            else:
                return self.horizontal_header[section]
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index: QModelIndex, value: int, role):
        if role == Qt.EditRole:
            try:
                value = int(value)
            except ValueError:
                return False
            r, c = index.row(), index.column()
            self.changed(r, c, self.table_data[c].get(r), int(value))
            self.table_data[c].set(r, int(value))
            return True
        return False

    def changed(self, row, column, org, chg):
        # 강동 운임합계 ~ 강동 수수료 4% 합계
        if 1 <= row <= 3:
            # => 경매차익
            val = self.table_data[column].get(12) - (chg - org)
            self.setData(self.index(12, column), val, Qt.EditRole)

        # 공제후 금액 합계
        elif row == 4:
            val = self.table_data[column].get(10) + (chg - org)
            self.setData(self.index(10, column), val, Qt.EditRole)

        # 중매 수수료 5% 합계
        elif row == 5:
            self.setData(self.index(11, column), chg, Qt.EditRole)

        # 화주 운임합계 ~ 상장 수수료 4% 합계
        elif 6 <= row <= 8:
            # => 경매차익
            val = self.table_data[column].get(12) + (chg - org)
            self.setData(self.index(12, column), val, Qt.EditRole)

    def out_changed(self, table_type, row, org, chg):
        # DayCalTable 테이블의 변경사항
        if table_type == 0:
            # 강동 총금액 ~ 공제후 금액
            if 0 <= row <= 4:
                # => 각 합계
                val = self.table_data[0].get(row) + (chg - org)
                self.setData(self.index(row, 0), val, Qt.EditRole)

            # 중매수수료 5% ~ 상장수수료 5%
            elif 5 <= row <= 8:
                # => 각 합계
                val = self.table_data[0].get(row) + (chg - org)
                self.setData(self.index(row, 0), val, Qt.EditRole)

        # DayCalOthersTable 테이블의 변경사항
        elif table_type == 1:
            # 경매사무실 입금
            if row == 0:
                # => 경매 확인
                val = self.table_data[0].get(9) + (chg - org)
                self.setData(self.index(9, 0), val, Qt.EditRole)

            # 경매 사무실 입금 ~ 강동사입
            elif 1 <= row <= 4:
                # => 경매 확인
                val = self.table_data[0].get(9) + (chg - org)
                self.setData(self.index(9, 0), val, Qt.EditRole)

                # => 경매 차액
                val = self.table_data[0].get(10) - (chg - org)
                self.setData(self.index(10, 0), val, Qt.EditRole)