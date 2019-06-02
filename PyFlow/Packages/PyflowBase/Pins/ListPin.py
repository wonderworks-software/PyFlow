from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class ListPin(PinBase):
    """doc string for ListPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(ListPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue([])
        self.disableOptions(PinOptions.Storable)

    def setAsArray(self, bIsArray):
        pass

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def pinDataTypeHint():
        return 'ListPin', []

    @staticmethod
    def color():
        return (50, 50, 200, 255)

    @staticmethod
    def supportedDataTypes():
        return ('ListPin',)

    @staticmethod
    def processData(data):
        return data

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
