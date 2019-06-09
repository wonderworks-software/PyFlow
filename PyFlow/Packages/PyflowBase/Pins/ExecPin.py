from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import Colors


# Execution pin
class ExecPin(PinBase):
    def __init__(self, name, parent, direction, **kwargs):
        super(ExecPin, self).__init__(name, parent, direction, **kwargs)
        self.dirty = False
        self._isArray = False
        if self.direction == PinDirection.Input:
            self.enableOptions(PinOptions.AllowMultipleConnections)

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
        return ('ExecPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'ExecPin', None

    @staticmethod
    def color():
        return (200, 200, 200, 255)

    def setData(self, data):
        pass
