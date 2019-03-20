from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.NodePainter import NodePainter
from Qt import QtGui
from Qt.QtWidgets import QGraphicsItem


class UIReruteNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIReruteNode, self).__init__(raw_node)
        self.label().hide()
        self.hover = False
        self.color = QtGui.QColor(255, 255, 255, 255)
        self.minWidth = 0
        self.setAcceptHoverEvents(True)

    def kill(self):
        inputs = self.inputs
        outputs = self.outputs
        inp = list(inputs.values())[0]
        out = list(outputs.values())[0]
        if inp.dataType == "ExecPin":
            newIns = []
            for i in inputs.values():
                for connection in i.connections:
                    newIns.append(connection.source())
            if out.connections:
                dst = out.connections[0].destination()
                for inpt in newIns:
                    self.graph().connectPins(inpt, dst)
        else:
            newOuts = []
            for i in outputs.values():
                for connection in i.connections:
                    newOuts.append(connection.destination())
            if inp.connections:
                source = inp.connections[0].source()
                for out in newOuts:
                    self.graph().connectPins(source, out)

        super(UIReruteNode, self).kill()

    def boundingRect(self):
        self._rect.setWidth((self.getPinsWidth() + 2) / 2)
        self._rect.setTop(self.getPinsWidth() / -3)
        self._rect.setHeight(self.getPinsWidth() + 2)
        self._rect.moveLeft((self.getPinsWidth() + 2) / 4)
        return self._rect

    def postCreate(self, jsonTemplate=None):
        super(UIReruteNode, self).postCreate(jsonTemplate)
        self.input = self.getPinByName("in").getWrapper()()
        self.input.getLabel()().hide()
        self.input.setDisplayName("")
        self.output = self.getPinByName("out").getWrapper()()
        self.output.getLabel()().hide()
        self.output.setDisplayName("")
        self.input.OnPinChanged.connect(self.setColor)
        self.output.OnPinChanged.connect(self.setColor)
        self.displayName = ''
        self.minWidth = 0
        self.updateNodeShape("")
        self.hidePins()

    def setColor(self, item):
        self.color = item._color
        self.update()

    def showPins(self):
        self.input.show()
        self.output.show()

    def hidePins(self):
        self.input.hide()
        self.output.hide()

    def mousePressEvent(self, event):
        super(UIReruteNode, self).mousePressEvent(event)
        self.hidePins()

    def hoverEnterEvent(self, event):
        super(UIReruteNode, self).hoverEnterEvent(event)
        self.showPins()

    def hoverLeaveEvent(self, event):
        super(UIReruteNode, self).hoverLeaveEvent(event)
        self.hidePins()

    def paint(self, painter, option, widget):
        self.color = self.input._color
        NodePainter.asReruteNode(self, painter, option, widget)
