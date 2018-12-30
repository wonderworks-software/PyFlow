from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class BoolPin(PinBase):
    """doc string for BoolPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(BoolPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(False)

    def supportedDataTypes(self):
        return ('BoolPin', 'IntPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'BoolPin', False

    def color(self):
        return (255, 0, 0, 255)

    def setData(self, data):
        try:
            self._data = bool(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
