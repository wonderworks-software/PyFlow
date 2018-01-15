from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt import QtCore
from Qt import QtGui


class ConvertNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(ConvertNode, self).__init__(name, graph, w=100, spacings=Spacings)
        self.label().hide()
        self.roundFactor = 4
        self.bg = QtGui.QBrush(QtGui.QImage(':/icons/resources/white.png'))
        self.bg.setStyle(QtCore.Qt.TexturePattern)

    def addInputPin(self, *args, **kwargs):
        # allow single input
        if len(self.inputs) == 0:
            pin = super(ConvertNode, self).addInputPin(*args, **kwargs)
            pin.getLayout().setMaximumWidth(10)
            pin._container.layout().setMaximumWidth(10)
            # pin._container.layout().setMinimumHeight(50)
            pin._container.setMaximumWidth(10)
            return pin

    def addOutputPin(self, *args, **kwargs):
        # allow single output
        if len(self.outputs) == 0:
            pin = super(ConvertNode, self).addOutputPin(*args, **kwargs)
            pin.getLayout().setMaximumWidth(10)
            pin._container.layout().setMaximumWidth(10)
            pin._container.setMaximumWidth(10)
            return pin

    @staticmethod
    def category():
        return 'Convert'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Converts A into B'

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 42, 14)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            pen.setColor(opt_selected_pen_color)
            pen.setStyle(self.opt_pen_selected_type)
        painter.setPen(pen)
        painter.setBrush(self.bg)
        painter.drawRoundedRect(self.boundingRect(), self.roundFactor, self.roundFactor)

    def compute(self):
        pass
