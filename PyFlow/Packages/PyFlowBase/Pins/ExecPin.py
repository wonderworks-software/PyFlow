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


from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


# Execution pin
class ExecPin(PinBase):
    def __init__(self, name, parent, direction):
        super(ExecPin, self).__init__(name, parent, direction)
        self.dirty = False
        self._isArray = False
        if self.direction == PinDirection.Input:
            self.enableOptions(PinOptions.AllowMultipleConnections)
        self._lastCallTime = 0.0

    def isExec(self):
        return True

    def pinConnected(self, other):
        super(ExecPin, self).pinConnected(other)

    def setAsArray(self, bIsArray):
        # exec is not a type, it cannot be an list
        self._isArray = False

    @staticmethod
    def IsValuePin():
        return False

    @staticmethod
    def supportedDataTypes():
        return ("ExecPin",)

    @staticmethod
    def pinDataTypeHint():
        return "ExecPin", None

    @staticmethod
    def internalDataStructure():
        return None

    @staticmethod
    def color():
        return 200, 200, 200, 255

    def setData(self, data):
        pass

    def getLastExecutionTime(self):
        return self._lastCallTime

    def call(self, *args, **kwargs):
        if self.owningNode().isValid():
            self._lastCallTime = currentProcessorTime()
        super(ExecPin, self).call(*args, **kwargs)
