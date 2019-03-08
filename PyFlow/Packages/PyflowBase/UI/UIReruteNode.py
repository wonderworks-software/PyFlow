from PyFlow.UI.UINodeBase import UINodeBase
from Qt import QtGui
from PyFlow.UI.NodePainter import NodePainter

class UIReruteNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIReruteNode, self).__init__(raw_node)
        self.label().hide()
        self.hover = False
        self.color = QtGui.QColor(255, 255, 255,255)
        self.minWidth = 0

    def boundingRect(self):
        self._rect.setWidth((self.getPinsWidth()+2)/2)
        self._rect.setTop(self.getPinsWidth()/-3)
        self._rect.setHeight(self.getPinsWidth()+2)
        self._rect.moveLeft((self.getPinsWidth()+2)/4)
        return self._rect
  
    def postCreate(self, jsonTemplate=None):
        super(UIReruteNode, self).postCreate(jsonTemplate)
        self.input = self.getPinByName("in").getWrapper()()
        self.input.getLabel()().hide()  
        self.input.OnPinConnected.connect(self.changeColor)
        self.input.setDisplayName("")
        self.output = self.getPinByName("out").getWrapper()()
        self.output.getLabel()().hide()
        self.output.OnPinConnected.connect(self.changeColor)
        self.output.setDisplayName("")
        self.displayName = ''
        self.minWidth = 0
        self.updateNodeShape("")
        #self.input.hide()
        #self.output.hide()

    def changeColor(self,pin):
        self.color= pin._color
        self.update()

    def mousePressEvent(self, event):
        super(UIReruteNode, self).mousePressEvent(event)
        self.hover = True
        self.input.show()
        self.input.update()
        self.output.show()

    def paint(self, painter, option, widget):
        NodePainter.asReruteNode(self, painter, option, widget)
