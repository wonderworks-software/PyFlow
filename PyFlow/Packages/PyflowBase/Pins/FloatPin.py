from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import Colors


class FloatPin(PinBase):
    """doc string for FloatPin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(FloatPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(0.0)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def pinDataTypeHint():
        '''data type index and default value'''
        return 'FloatPin', 0.0

    @staticmethod
    def color():
        return (96, 169, 23, 255)

    @staticmethod
    def supportedDataTypes():
        return ('FloatPin', 'IntPin',)

    @staticmethod
    def processData(data):
        return float(data)

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
