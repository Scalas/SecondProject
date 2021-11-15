import operator

from PySide6.QtCore import QAbstractTableModel, Qt, SIGNAL, QModelIndex
from PySide6.QtGui import *


class DayCalTableModel(QAbstractTableModel):
    def __init__(self, parent, horizontal_header, vertical_header, data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.setParent(parent)
        self.table_data = list(map(list, data))
        self.horizontal_header = horizontal_header
        self.vertical_header = vertical_header
        self.row_count = 12
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
