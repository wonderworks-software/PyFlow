import weakref
import uuid
from types import MethodType
from collections import OrderedDict

from Qt import QtGui
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QMenu

from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import *
from PyFlow.Core.NodeBase import NodeBase
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.PyCodeCompiler import Py3CodeCompiler


class pythonNode(NodeBase):
    def __init__(self, name):
        super(pythonNode, self).__init__(name)
        self._nodeData = ''
        self.bCacheEnabled = False

    @property
    def nodeData(self):
        return self._nodeData

    @nodeData.setter
    def nodeData(self, codeString):
        self._nodeData = codeString
        # compile and get symbols
        mem = Py3CodeCompiler().compile(codeString)

        # clear node pins
        for i in list(self.inputs.values()):
            i.kill()
        for o in list(self.outputs.values()):
            o.kill()

        # define pins
        pinsDefinitionFunction = mem["definePins"]
        pinsDefinitionFunction(self)
        self.autoAffectPins()

        # assign compute code
        computeFunction = mem["compute"]

        def nodeCompute(*args, **kwargs):
            computeFunction(self)

        self.compute = MethodType(nodeCompute, self)
        self.bCallable = self.isCallable()

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    def serialize(self):
        default = super(pythonNode, self).serialize()
        default['nodeData'] = self.nodeData
        return default

    def postCreate(self, jsonTemplate=None):
        super(pythonNode, self).postCreate(jsonTemplate)

        if jsonTemplate is None:
            return

        if 'nodeData' in jsonTemplate:
            self.nodeData = jsonTemplate['nodeData']

        for inpJson in jsonTemplate['inputs']:
            pin = self.getPin(inpJson["name"])
            pin.deserialize(inpJson)

        for outJson in jsonTemplate['outputs']:
            pin = self.getPin(outJson["name"])
            pin.deserialize(outJson)

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
