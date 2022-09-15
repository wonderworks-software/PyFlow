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
import uuid

from PyFlow.Packages.PyFlowBase import PACKAGE_NAME
from PyFlow.Core import NodeBase
from PyFlow.Core.Variable import Variable
from PyFlow.Core.Common import *
from PyFlow import CreateRawPin


class getVar(NodeBase):
    def __init__(self, name, var=None):
        super(getVar, self).__init__(name)
        assert(isinstance(var, Variable))
        self._var = var
        if var.structure == StructureType.Dict:
            self.out = self.createOutputPin('out', var.value.valueType, structure=StructureType.Dict, constraint="2")
        else:
            self.out = self.createOutputPin('out', var.dataType)
        self.out.disableOptions(PinOptions.RenamingEnabled)

        self._var.valueChanged.connect(self.onVarValueChanged)
        self._var.structureChanged.connect(self.onVarStructureChanged)
        self._var.dataTypeChanged.connect(self.onDataTypeChanged)
        self.bCacheEnabled = False

    def checkForErrors(self):
        super(getVar, self).checkForErrors()
        if self._var is None:
            self.setError("Undefined variable")

    def onDataTypeChanged(self, dataType):
        self.recreateOutput(dataType)
        self.checkForErrors()
        wrapper = self.getWrapper()
        if wrapper:
            wrapper.onVariableWasChanged()

    def updateStructure(self):
        self.out.disconnectAll()
        if self._var.structure == StructureType.Single:
            self.out.setAsArray(False)
        if self._var.structure == StructureType.Array:
            self.out.setAsArray(True)
        if self._var.structure == StructureType.Dict:
            self.out.setAsDict(True)
            self.out.updateConnectedDicts([], self._var.value.keyType)

    def onVarStructureChanged(self, newStructure):
        self.out.structureType = newStructure
        self.updateStructure()

    def recreateOutput(self, dataType):
        self.out.kill()
        del self.out
        self.out = None
        self.out = CreateRawPin('out', self, dataType, PinDirection.Output)
        self.out.disableOptions(PinOptions.RenamingEnabled)
        self.updateStructure()
        return self.out

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, newVar):
        if self._var is not None:
            self._var.dataTypeChanged.disconnect(self.onDataTypeChanged)
            self._var.structureChanged.disconnect(self.onVarStructureChanged)
            self._var.valueChanged.disconnect(self.onVarValueChanged)
        self._var = newVar
        if newVar is not None:
            self._var.valueChanged.connect(self.onVarValueChanged)
            self._var.structureChanged.connect(self.onVarStructureChanged)
            self._var.dataTypeChanged.connect(self.onDataTypeChanged)
            self.recreateOutput(self._var.dataType)
        else:
            # self.out.kill()
            # del self.out
            # self.out = None
            pass
        self.checkForErrors()
        wrapper = self.getWrapper()
        if wrapper:
            wrapper.onVariableWasChanged()

    def postCreate(self, jsonTemplate=None):
        super(getVar, self).postCreate(jsonTemplate)
        self.updateStructure()

    def variableUid(self):
        return self.var.uid

    def onVarValueChanged(self, *args, **kwargs):
        push(self.out)

    def serialize(self):
        default = NodeBase.serialize(self)
        if self.var is not None:
            default['varUid'] = str(self.var.uid)
        return default

    @staticmethod
    def category():
        return PACKAGE_NAME

    @staticmethod
    def keywords():
        return ["get", "var"]

    @staticmethod
    def description():
        return 'Access variable value'

    def compute(self, *args, **kwargs):
        self.out.setData(copy(self.var.value))
