from copy import copy

from PyFlow.Packages.PyflowBase import PACKAGE_NAME
from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow import CreateRawPin


class setVar(NodeBase):
    def __init__(self, name, var=None):
        super(setVar, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self._var = var
        self.inp = CreateRawPin("inp", self, self.var.dataType, PinDirection.Input)
        self.inp.disableOptions(PinOptions.RenamingEnabled)
        self.out = CreateRawPin("out", self, self.var.dataType, PinDirection.Output)
        self.out.disableOptions(PinOptions.RenamingEnabled)

        self._var.structureChanged.connect(self.onVarStructureChanged)

    def updateStructure(self):
        self.out.disconnectAll()
        self.inp.disconnectAll()
        if self._var.structure == PinStructure.Single:
            self.out.setAsArray(False)
            self.inp.setAsArray(False)
        if self._var.structure == PinStructure.Array:
            self.out.setAsArray(True)
            self.inp.setAsArray(True)
        if self._var.structure == PinStructure.Multi:
            self.out.setAsArray(False)
            self.inp.setAsArray(False)

    def onVarStructureChanged(self, newStructure):
        self.out.structureType = newStructure
        self.updateStructure()

    def postCreate(self, jsonTemplate=None):
        super(setVar, self).postCreate(jsonTemplate)
        self.updateStructure()

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, newVar):
        self._var = newVar

    @var.setter
    def var(self, newVar):
        oldDataType = self._var.dataType
        self._var = newVar
        if self._var.dataType != oldDataType:
            self.recreateInput(self._var.dataType)
            self.recreateOutput(self._var.dataType)

    def recreateInput(self, dataType):
        self.inp.kill()
        del self.inp
        self.inp = None
        self.inp = CreateRawPin('inp', self, dataType, PinDirection.Input)
        self.inp.disableOptions(PinOptions.RenamingEnabled)
        return self.inp

    def recreateOutput(self, dataType):
        self.out.kill()
        del self.out
        self.out = None
        self.out = CreateRawPin('out', self, dataType, PinDirection.Output)
        self.out.disableOptions(PinOptions.RenamingEnabled)
        return self.out

    def variableUid(self):
        return self.var.uid

    def serialize(self):
        default = NodeBase.serialize(self)
        default['varUid'] = str(self.var.uid)
        return default

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return PACKAGE_NAME

    @staticmethod
    def keywords():
        return ["set", "var"]

    @staticmethod
    def description():
        return 'Set variable value'

    def compute(self, *args, **kwargs):
        newValue = self.inp.getData()
        self.var.value = newValue
        self.out.setData(copy(self.var.value))
        self.outExec.call(*args, **kwargs)
