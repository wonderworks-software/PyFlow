from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class StringPin(PinBase):
    """doc string for StringPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(StringPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue("")

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('StringPin',)

    @staticmethod
    def color():
        return (255, 8, 127, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'StringPin', ''

    @staticmethod
    def processData(data):
        return str(data)

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
