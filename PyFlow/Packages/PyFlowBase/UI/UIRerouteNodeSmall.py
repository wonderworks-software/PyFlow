from Qt import QtCore
from Qt.QtWidgets import QSizePolicy

from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UINodeBase import UINodeBase


class UIRerouteNodeSmall(UINodeBase):
    def __init__(self, raw_node):
        self.drawlabel = False
        super(UIRerouteNodeSmall, self).__init__(raw_node)
        self.hover = False
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray
        self._size = 10
        self.nodeLayout.removeItem(self.headerLayout)
        self.headerLayout.removeItem(self.nodeNameWidget)
        self.nodeNameWidget.hide()
        self.setAcceptHoverEvents(True)
        self.drawRect = QtCore.QRectF(0, 0, 10, 10)
        self.hiddenPins = True

    def createActionButtons(self):
        pass

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(self.boundingRect().width(), self.boundingRect().height())

    def boundingRect(self):
        if self.hiddenPins:
            self._rect.setWidth(self._size)
            self._rect.moveLeft(0)
        else:
            self._rect.setWidth(self._size * 2)
            self._rect.moveLeft(-self._size / 2)
        self._rect.setHeight(self._size)
        return self._rect

    def showPins(self):
        self.hiddenPins = False
        self.input.show()
        self.output.show()
        self.input.setPos(self.boundingRect().left() - self.input.pinSize, 1.5)
        self.output.setPos(self.boundingRect().right() - self.input.pinSize, 1.5)

    def hidePins(self):
        self.hiddenPins = True
        self.input.hide()
        self.output.hide()
        self.input.setPos(0, 1.5)
        self.output.setPos(0, 1.5)

    def mousePressEvent(self, event):
        super(UIRerouteNodeSmall, self).mousePressEvent(event)
        self.hidePins()

    def hoverEnterEvent(self, event):
        super(UIRerouteNodeSmall, self).hoverEnterEvent(event)
        self.showPins()

    def hoverLeaveEvent(self, event):
        super(UIRerouteNodeSmall, self).hoverLeaveEvent(event)
        self.hidePins()

    def kill(self, *args, **kwargs):
        inp = list(self.UIinputs.values())[0]
        out = list(self.UIoutputs.values())[0]
        newOuts = []
        for i in self.UIoutputs.values():
            for connection in i.connections:
                newOuts.append([connection.destination(),
                                connection.drawDestination])
        if inp.connections:
            source = inp.connections[0].source()
            for out in newOuts:
                drawSource = inp.connections[0].drawSource
                self.canvasRef().connectPinsInternal(source, out[0])
        super(UIRerouteNodeSmall, self).kill()

    def postCreate(self, jsonTemplate=None):
        super(UIRerouteNodeSmall, self).postCreate(jsonTemplate)
        self.input = self.getPinSG("in")
        self.output = self.getPinSG("out")
        self.input.bLabelHidden = True
        self.output.bLabelHidden = True
        self.inputsLayout.removeItem(self.input)
        self.outputsLayout.removeItem(self.output)
        self.input.setDisplayName("")
        self.output.setDisplayName("")
        self.input.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.output.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.input.setPos(-self.input.pinSize, 1.5)
        self.output.setPos(self._size + self.input.pinSize / 1.5, 1.5)
        self.hidePins()
        self.updateNodeShape()

    def paint(self, painter, option, widget):
        #painter.setPen(QtGui.QPen(QtCore.Qt.green, 0.75))
        # painter.drawRect(self.boundingRect())
        NodePainter.asRerouteNode(self, painter, option, widget)
