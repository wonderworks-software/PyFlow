from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import Colors


# Execution pin
class ExecPin(PinBase):
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(ExecPin, self).__init__(
            name, parent, dataType, direction, **kwargs)
        self.width = self.height = 10.0
        self.dirty = False
        self._isArray = False

    def pinConnected(self, other):
        # connect execution signals
        if self.direction == PinDirection.Output:
            self.onExecute.connect(other.call)
        super(ExecPin, self).pinConnected(other)

    def setAsArray(self, bIsArray):
        # exec is not a type, it cannot be an array
        self._isArray = False

    @staticmethod
    def isPrimitiveType():
        return True

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
        return (255, 255, 255, 255)

    def setData(self, data):
        pass
