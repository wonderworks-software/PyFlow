from Core.Pin import _Pin
from Core.AGraphCommon import *


class ListPin(_Pin):
    """doc string for ListPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(ListPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue([])

    def supportedDataTypes(self):
        return (DataTypes.Array,)

    @staticmethod
    def color():
        return Colors.Array

    @staticmethod
    def pinDataType():
        return DataTypes.Array, []

    def setData(self, data):
        if isinstance(data, list):
            self._data = data
        else:
            self._data = self.defaultValue()
        _Pin.setData(self, self._data)
