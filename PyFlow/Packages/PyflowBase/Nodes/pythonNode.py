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
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.PyCodeCompiler import Py3FunctionCompiler


class pythonNode(NodeBase):
    def __init__(self, name):
        super(pythonNode, self).__init__(name)
        self.currentComputeCode = ''

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    def serialize(self):
        default = super(pythonNode, self).serialize()
        default['computeCode'] = self.currentComputeCode
        return default

    def postCreate(self, jsonTemplate=None):
        super(pythonNode, self).postCreate(jsonTemplate)

        if jsonTemplate is None:
            return

        if 'computeCode' in jsonTemplate:
            self.currentComputeCode = jsonTemplate['computeCode']
            compute = Py3FunctionCompiler('compute').compile(self.currentComputeCode)
            self.compute = MethodType(compute, self)

        # recreate pins
        for i in jsonTemplate['inputs']:
            inPin = self.addInputPin(i['name'],
                                     i['dataType'],
                                     getPinDefaultValueByType(i['dataType']))
            inPin.setData(i['value'])
            inPin.dirty = i['bDirty']

        for o in jsonTemplate['outputs']:
            compute = self.compute if o['dataType'] in ('AnyPin', 'ExecPin') else None
            outPin = self.addOutputPin(o['name'],
                                       o['dataType'],
                                       getPinDefaultValueByType(o['dataType']),
                                       compute)

        self.autoAffectPins()

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return ['Code', 'Expression', 'py']

    @staticmethod
    def description():
        return 'Python script node'
