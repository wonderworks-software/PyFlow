from Qt import QtWidgets
from Qt import QtGui, QtCore

from PyFlow.UI.Canvas.Painters import PinPainter
from PyFlow import findPinClassByType, getAllPinClasses
from PyFlow.Core.Common import PinDirection

from PyFlow.UI import RESOURCES_DIR


_PIN_SIZE = 15


class _FakeCanvas(object):
    def __init__(self):
        super(_FakeCanvas, self).__init__()

    def getLodValueFromCurrentScale(self, lod):
        return 1


class _FakeNode(object):
    def __init__(self):
        super(_FakeNode, self).__init__()
        self.fakeCanvas = _FakeCanvas()

    def canvasRef(self):
        return self.fakeCanvas


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
        self.fakeOwningNode = _FakeNode()
        self._rawPin = _FakePin()
        self._pinColor = QtGui.QColor(*findPinClassByType(self.dataType).color())
        self.labelColor = QtCore.Qt.white
        self.hovered = False
        self.pinSize = _PIN_SIZE
        self._font = QtGui.QFont("Consolas")
        self._font.setPointSize(14)
        self.direction = PinDirection.Input
        self.name = self.dataType
        self.bLabelHidden = False

        self.setMouseTracking(True) 
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

    def sizeHint(self):
        textWidth = QtGui.QFontMetrics(self._font).width(self.dataType) + _PIN_SIZE
        textHeight = max(QtGui.QFontMetrics(self._font).height(), _PIN_SIZE + 6)
        return QtCore.QSize(textWidth, textHeight)

    def pinCenter(self):
        return QtCore.QPointF(_PIN_SIZE, _PIN_SIZE / 2)

    def displayName(self):
        return self.dataType

    def owningNode(self):
        return self.fakeOwningNode

    def enterEvent(self, event):
        super(_PinWidget, self).enterEvent(event)
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        super(_PinWidget, self).leaveEvent(event)
        self.hovered = False
        self.update()

    def color(self):
        return self._pinColor

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


class _PinsListWidget(QtWidgets.QListWidget):
    """docstring for _PinsListWidget."""
    returnPressed = QtCore.Signal()

    def __init__(self, parent=None,validPins=None):
        super(_PinsListWidget, self).__init__()
        self.populate(pattern="",validPins=validPins)

    def filterContent(self, pattern):
        self.clear()
        self.populate(pattern)

    def createEntry(self, dataType):
        widget = _PinWidget(dataType)
        item = QtWidgets.QListWidgetItem(self)
        self.setItemWidget(item, widget)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.returnPressed.emit()
        super(_PinsListWidget, self).keyPressEvent(event)

    def populate(self, pattern="",validPins=[pin.__name__ for pin in getAllPinClasses()]):
        for pinClass in getAllPinClasses():
            className = pinClass.__name__
            if className in validPins:
                if len(pattern) > 0:
                    if pattern.lower() in className.lower():
                        self.createEntry(className)
                else:
                    self.createEntry(className)
        self.setCurrentRow(0)


class SelectPinDialog(QtWidgets.QDialog):
    """docstring for SelectPinDialog."""
    def __init__(self, parent=None,validPins=None):
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

        self.content = _PinsListWidget(validPins=validPins)
        self.mainLayout.addWidget(self.content)
        self.content.itemClicked.connect(self.onItemClicked)
        self.content.returnPressed.connect(self.onReturnPressed)

        self._result = None

    def onReturnPressed(self):
        widget = self.content.itemWidget(self.content.currentItem())
        self._result = widget.dataType
        self.close()

    def onItemClicked(self, item):
        widget = self.content.itemWidget(item)
        self._result = widget.dataType
        self.close()

    def showEvent(self, event):
        super(SelectPinDialog, self).showEvent(event)
        self.move(QtGui.QCursor.pos())

    def filterContent(self, pattern):
        self.content.filterContent(pattern)

    def getResult(self):
        return self._result


