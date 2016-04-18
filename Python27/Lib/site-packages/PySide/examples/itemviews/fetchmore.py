#!/usr/bin/python

# Fetch More Example
# Ported to PyQt4 by Darryl Wallace, 2009 - wallacdj@gmail.com

from PySide import QtCore, QtGui


class FileListModel(QtCore.QAbstractListModel):
    numberPopulated = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(FileListModel, self).__init__(parent)

        self.fileCount = 0
        self.fileList = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.fileCount

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if index.row() >= len(self.fileList) or index.row() < 0:
            return None

        if role == QtCore.Qt.DisplayRole:
            return self.fileList[index.row()]

        if role == QtCore.Qt.BackgroundRole:
            batch = (index.row() // 100) % 2
            if batch == 0:
                return QtGui.qApp.palette().base()

            return QtGui.qApp.palette().alternateBase()

        return None

    def canFetchMore(self, index):
        return self.fileCount < len(self.fileList)

    def fetchMore(self, index):
        remainder = len(self.fileList) - self.fileCount
        itemsToFetch = min(100, remainder)

        self.beginInsertRows(QtCore.QModelIndex(), self.fileCount,
                self.fileCount + itemsToFetch)

        self.fileCount += itemsToFetch

        self.endInsertRows()

        self.numberPopulated.emit(itemsToFetch)

    def setDirPath(self, path):
        dir = QtCore.QDir(path)

        self.fileList = list(dir.entryList())
        self.fileCount = 0
        self.reset()


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        model = FileListModel(self)
        model.setDirPath(QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PrefixPath))

        label = QtGui.QLabel("Directory")
        lineEdit = QtGui.QLineEdit()
        label.setBuddy(lineEdit)

        view = QtGui.QListView()
        view.setModel(model)

        self.logViewer = QtGui.QTextBrowser()
        self.logViewer.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))

        lineEdit.textChanged.connect(model.setDirPath)
        lineEdit.textChanged.connect(self.logViewer.clear)
        model.numberPopulated.connect(self.updateLog)

        layout = QtGui.QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(lineEdit, 0, 1)
        layout.addWidget(view, 1, 0, 1, 2)
        layout.addWidget(self.logViewer, 2, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle("Fetch More Example")

    def updateLog(self, number):
        self.logViewer.append("%d items added." % number)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
