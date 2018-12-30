from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *
from PyFlow.UI.Settings import Colors


class FloatPin(PinBase):
    """doc string for FloatPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(FloatPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(0.0)

    @staticmethod
    def pinDataTypeHint():
        '''data type index and default value'''
        return 'FloatPin', 0.0

    def color(self):
        return (96, 169, 23, 255)

    def supportedDataTypes(self):
        return ('FloatPin', 'IntPin')

    def setData(self, data):
        try:
            self._data = float(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
