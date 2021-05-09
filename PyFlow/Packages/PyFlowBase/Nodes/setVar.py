## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from copy import copy

from PyFlow.Packages.PyFlowBase import PACKAGE_NAME
from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow import CreateRawPin


class setVar(NodeBase):
    def __init__(self, name, var=None):
        super(setVar, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self._var = var
        if var.structure == StructureType.Dict:
            self.out = self.createOutputPin('out', self._var.value.valueType, structure=self._var.structure, constraint="2")
            self.inp = self.createInputPin('inp', self._var.value.valueType, structure=self._var.structure, constraint="2")
        else:
            self.out = self.createOutputPin('out', self._var.dataType, structure=self._var.structure)
            self.inp = self.createInputPin('inp', self._var.dataType, structure=self._var.structure)
        self.inp.disableOptions(PinOptions.RenamingEnabled)
        self.out.disableOptions(PinOptions.RenamingEnabled)

        self._var.dataTypeChanged.connect(self.onVarDataTypeChanged)
        self._var.structureChanged.connect(self.onVarStructureChanged)
        self.bCacheEnabled = False

    def updateStructure(self):
        self.out.disconnectAll()
        self.inp.disconnectAll()
        if self.var.structure == StructureType.Single:
            self.out.setAsArray(False)
            self.inp.setAsArray(False)
        if self.var.structure == StructureType.Array:
            self.out.setAsArray(True)
            self.inp.setAsArray(True)
        if self.var.structure == StructureType.Dict:
            self.out.setAsDict(True)
            self.out.updateConnectedDicts([], self.var.value.keyType)

    def checkForErrors(self):
        super(setVar, self).checkForErrors()
        if self._var is None:
            self.setError("Undefined variable")

    def onVarStructureChanged(self, newStructure):
        self.out.structureType = newStructure
        self.inp.structureType = newStructure
        self.updateStructure()

    def onVarDataTypeChanged(self, dataType):
        self.recreateInput(dataType)
        self.recreateOutput(dataType)
        self.autoAffectPins()
        self.updateStructure()
        self.checkForErrors()
        wrapper = self.getWrapper()
        if wrapper:
            wrapper.onVariableWasChanged()

    def postCreate(self, jsonTemplate=None):
        super(setVar, self).postCreate(jsonTemplate)
        self.updateStructure()

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, newVar):
        if self._var is not None:
            self._var.structureChanged.disconnect(self.onVarStructureChanged)
            self._var.dataTypeChanged.disconnect(self.onVarDataTypeChanged)
        self._var = newVar
        if self._var is not None:
            self._var.structureChanged.connect(self.onVarStructureChanged)
            self._var.dataTypeChanged.connect(self.onVarDataTypeChanged)
            self.recreateInput(newVar.dataType)
            self.recreateOutput(newVar.dataType)
            self.autoAffectPins()
            self.updateStructure()
        self.checkForErrors()
        wrapper = self.getWrapper()
        if wrapper:
            wrapper.onVariableWasChanged()

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
