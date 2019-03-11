import weakref
import uuid
from types import MethodType
from collections import OrderedDict

from Qt import QtGui
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QMenu

from PyFlow.Core.Common import *
from PyFlow.UI.Settings import *
from PyFlow.Core.NodeBase import NodeBase


class pythonNode(NodeBase):
    def __init__(self, name):
        super(pythonNode, self).__init__(name)
        self.currentComputeCode = ''

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return ['Code', 'Expression', 'py']

    @staticmethod
    def description():
        return 'Python script node'
