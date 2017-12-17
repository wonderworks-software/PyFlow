from AbstractGraph import *
from Settings import *
from Node import Node
from Qt import QtGui
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QMenu
from CodeEditor import CodeEditor


class PythonNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(PythonNode, self).__init__(name, graph)
        self.menu = QMenu()
        self.actionEdit = self.menu.addAction('edit')
        self.actionEdit.triggered.connect(self.openEditor)
        self.actionEdit.setIcon(QtGui.QIcon(':/icons/resources/py.png'))
        self.editor = CodeEditor(self)

    def openEditor(self):
        self.editor.show()

    @staticmethod
    def category():
        return 'Utils'

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def keywords():
        return ['Code', 'Expression']

    @staticmethod
    def description():
        return 'default description'

    def compute(self):
        str_data = self.inp0.get_data()
        try:
            self.out0.set_data(str_data.upper())
        except Exception as e:
            print(e)
