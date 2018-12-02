from ..Core.AbstractGraph import PinBase
from ..Core.AGraphCommon import *


class BoolPin(PinBase):
    """doc string for BoolPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(BoolPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(False)

    def supportedDataTypes(self):
        return (DataTypes.Bool, DataTypes.Int,)

    @staticmethod
    def pinDataTypeHint():
        return DataTypes.Bool, False

    def setData(self, data):
        try:
            self._data = bool(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
