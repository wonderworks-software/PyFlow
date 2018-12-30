from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class ListPin(PinBase):
    """doc string for ListPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(ListPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue([])

    def supportedDataTypes(self):
        return ('ListPin',)

    def color(self):
        return (110, 110, 110, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'ListPin', []

    def setData(self, data):
        if isinstance(data, list):
            self._data = data
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
