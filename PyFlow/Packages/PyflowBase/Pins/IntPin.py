from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class IntPin(PinBase):
    """doc string for IntPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(IntPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(0)

    @staticmethod
    def isPrimitiveType():
        return True

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def pinDataTypeHint():
        return 'IntPin', 0

    @staticmethod
    def color():
        return (0, 168, 107, 255)

    @staticmethod
    def supportedDataTypes():
        return ('IntPin', 'FloatPin',)

    @staticmethod
    def processData(data):
        return int(data)

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
