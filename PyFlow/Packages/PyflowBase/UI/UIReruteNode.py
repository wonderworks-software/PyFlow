from PyFlow.UI.UINodeBase import UINodeBase
from Qt import QtGui
from PyFlow.UI.NodePainter import NodePainter

class UIReruteNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIReruteNode, self).__init__(raw_node)
        self.label().hide()
        self.hover = False
        self.color = QtGui.QColor(255, 160, 47)
        self.minWidth = 0

    def boundingRect(self):
        self._rect.setWidth(self.getPinsWidth()+2)
        self._rect.setTop(self.getPinsWidth()/-3)
        self._rect.setHeight(self.getPinsWidth()+2)
        return self._rect
  
    def postCreate(self, jsonTemplate=None):
        super(UIReruteNode, self).postCreate(jsonTemplate)
        self.input = self.getPinByName("in").getWrapper()()
        self.input.getLabel()().hide()  
        self.input.setDisplayName("")
        self.output = self.getPinByName("out").getWrapper()()
        self.output.getLabel()().hide()
        self.output.setDisplayName("")
        self.displayName = ''
        self.label().setPlainText(self.displayName)
        self.setName(self.displayName)
        self.minWidth = 0
        self.updateNodeShape("")


    def mouseMoveEvent(self, event):
        super(UIReruteNode, self).mouseMoveEvent(event)
        self.hover = True

    def paint(self, painter, option, widget):
        NodePainter.asReruteNode(self, painter, option, widget)
