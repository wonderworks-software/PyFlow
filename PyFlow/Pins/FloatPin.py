from Core.Pin import _Pin
from Core.AGraphCommon import *


class FloatPin(_Pin):
    """doc string for FloatPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(FloatPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(0.0)

    @staticmethod
    def color():
        return Colors.Float

    @staticmethod
    def pinDataTypeHint():
        '''data type index and default value'''
        return DataTypes.Float, 0.0

    def supportedDataTypes(self):
        return (DataTypes.Float, DataTypes.Int)

    def setData(self, data):
        try:
            self._data = float(data)
        except:
            self._data = self.defaultValue()
        _Pin.setData(self, self._data)
