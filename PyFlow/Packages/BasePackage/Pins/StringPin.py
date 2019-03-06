from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class StringPin(PinBase):
    """doc string for StringPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(StringPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue("")

    @staticmethod
    def IsValuePin():
        return True

    def supportedDataTypes(self):
        return ('StringPin',)

    @staticmethod
    def color():
        return (255, 8, 127, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'StringPin', ''

    @staticmethod
    def processData( data):
        return str(data)

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
