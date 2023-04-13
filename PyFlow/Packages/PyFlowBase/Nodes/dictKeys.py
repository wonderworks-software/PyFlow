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


from PyFlow.PyFlow.Core import NodeBase
from PyFlow.PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.PyFlow.Core.Common import *


class dictKeys(NodeBase):
    def __init__(self, name):
        super(dictKeys, self).__init__(name)
        self.dict = self.createInputPin("dict", "AnyPin", structure=StructureType.Dict)
        self.dict.enableOptions(PinOptions.DictSupported)
        self.dict.onPinConnected.connect(self.dictConnected)
        self.dict.dictChanged.connect(self.dictChanged)
        self.keys = self.createOutputPin("keys", "AnyPin", structure=StructureType.Array)
        self.keys.disableOptions(PinOptions.ChangeTypeOnConnection)

    def dictConnected(self, other):
        self.keys.enableOptions(PinOptions.ChangeTypeOnConnection)
        self.keys.initType(other._data.keyType, True)
        self.keys.disableOptions(PinOptions.ChangeTypeOnConnection)

    def dictChanged(self, dataType):
        self.keys.enableOptions(PinOptions.ChangeTypeOnConnection)
        self.keys.initType(dataType, True)
        self.keys.disableOptions(PinOptions.ChangeTypeOnConnection)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(StructureType.Dict)
        helper.addOutputStruct(StructureType.Array)
        return helper

    @staticmethod
    def category():
        return 'Dictionary'

    @staticmethod
    def keywords():
        return ["keys"]

    @staticmethod
    def description():
        return 'Returns an array of dict keys.'

    def compute(self, *args, **kwargs):
        self.keys.setData(list(self.dict.getData().keys()))
