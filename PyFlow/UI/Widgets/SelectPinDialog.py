from Qt import QtWidgets
from Qt import QtGui, QtCore

from PyFlow.UI.Canvas.Painters import PinPainter
from PyFlow import findPinClassByType, getAllPinClasses

from PyFlow.UI import RESOURCES_DIR


_PIN_SIZE = 15


class _FakePin(object):
    def __init__(self):
        super(_FakePin, self).__init__()
        self.connected = False

    def setConnected(self, connected):
        self.connected = connected

    def hasConnections(self):
        return self.connected


class _PinWidget(QtWidgets.QWidget):
    """docstring for _PinWidget."""
    def __init__(self, dataType, parent=None):
        super(_PinWidget, self).__init__(parent)
        self.dataType = dataType
        self._rawPin = _FakePin()
        self._color = QtGui.QColor(*findPinClassByType(self.dataType).color())
        self.hovered = False
        self.setMinimumHeight(_PIN_SIZE + 10)
        self.setMinimumWidth(_PIN_SIZE + 10)
        self.setMouseTracking(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

    def enterEvent(self, event):
        super(_PinWidget, self).enterEvent(event)
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        super(_PinWidget, self).leaveEvent(event)
        self.hovered = False
        self.update()

    def color(self):
        return self._color

    @property
    def width(self):
        return self.minimumWidth() - 5

    @property
    def height(self):
        return self.minimumHeight() - 5

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(QtCore.Qt.NoPen)
        if self.dataType == "ExecPin":
            self._rawPin.setConnected(True)
            PinPainter.asExecPin(self, painter, None, None)
        else:
            PinPainter.asValuePin(self, painter, None, None)
        painter.end()


class _PinWidgetEntry(QtWidgets.QWidget):
    def __init__(self, dataType, parent=None):
        super(_PinWidgetEntry, self).__init__(parent)
        self.dataType = dataType
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(1, 1, 1, 1)
        self.mainLayout.addWidget(_PinWidget(dataType))
        self.mainLayout.addWidget(QtWidgets.QLabel(dataType))


class _PinsListWidget(QtWidgets.QListWidget):
    """docstring for _PinsListWidget."""
    def __init__(self, parent=None):
        super(_PinsListWidget, self).__init__()
        self.populate(pattern="")

    def filterContent(self, pattern):
        self.clear()
        self.populate(pattern)

    def createEntry(self, dataType):
        widget = _PinWidgetEntry(dataType)
        item = QtWidgets.QListWidgetItem(self)
        item.setSizeHint(QtCore.QSize(_PIN_SIZE, _PIN_SIZE + 20))
        self.setItemWidget(item, widget)

    def populate(self, pattern=""):
        for pinClass in getAllPinClasses():
            className = pinClass.__name__
            if len(pattern) > 0:
                if pattern.lower() in className.lower():
                    self.createEntry(className)
            else:
                self.createEntry(className)
        self.setCurrentRow(0)


class SelectPinDialog(QtWidgets.QDialog):
    """docstring for SelectPinDialog."""
    def __init__(self, parent=None):
        super(SelectPinDialog, self).__init__(None)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Select pin")
        self.setWindowIcon(QtGui.QIcon(RESOURCES_DIR + "/pin.png"))
        self.resize(QtCore.QSize(400, 300))

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(2, 2, 2, 2)
        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("search...")
        self.searchBox.textChanged.connect(self.filterContent)
        self.mainLayout.addWidget(self.searchBox)

        self.content = _PinsListWidget()
        self.mainLayout.addWidget(self.content)

        self.dialogButtonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.dialogButtonBox.accepted.connect(self.onAccept)
        self.dialogButtonBox.rejected.connect(self.onReject)
        self.mainLayout.addWidget(self.dialogButtonBox)
        self.setModal(True)
        self._result = None

    def showEvent(self, event):
        super(SelectPinDialog, self).showEvent(event)
        self.move(QtGui.QCursor.pos())

    def filterContent(self, pattern):
        self.content.filterContent(pattern)

    def getResult(self):
        return self._result

    def onReject(self):
        self.close()

    def onAccept(self):
        widget = self.content.itemWidget(self.content.currentItem())
        self._result = widget.dataType
        self.close()
