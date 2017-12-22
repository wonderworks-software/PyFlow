from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt import QtCore
from Qt import QtGui

DESC = '''node desc
'''


class ConvertNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(ConvertNode, self).__init__(name, graph, w=100, spacings=Spacings)
        self.label().hide()
        self.roundFactor = 10
        self.bg = QtGui.QImage(':/icons/resources/white.png')

    def addInputPin(self, *args, **kwargs):
        # allow single input
        if len(self.inputs) == 0:
            return super(ConvertNode, self).addInputPin(*args, **kwargs)

    def addOutputPin(self, *args, **kwargs):
        # allow single output
        if len(self.outputs) == 0:
            return super(ConvertNode, self).addOutputPin(*args, **kwargs)

    @staticmethod
    def category():
        return 'Convert'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return DESC

    def boundingRect(self):
        return QtCore.QRectF(0, -4, 50, 23)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            if self.options:
                pen.setColor(Colors.Yellow)
                pen.setStyle(self.opt_pen_selected_type)
            else:
                pen.setColor(opt_selected_pen_color)
                pen.setStyle(self.opt_pen_selected_type)
        painter.setPen(pen)
        painter.setBrush(self.bg)
        painter.drawRoundedRect(self.boundingRect(), self.roundFactor, self.roundFactor)

    def compute(self):
        pass
