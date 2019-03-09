from pyrr import Matrix33

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class Matrix33Pin(PinBase):
    """doc string for Matrix33Pin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(Matrix33Pin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Matrix33())

    @staticmethod
    def IsValuePin():
        return True

    def supportedDataTypes(self):
        return ('Matrix33Pin',)

    @staticmethod
    def color():
        return (150, 69, 20, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'Matrix33Pin', Matrix33()

    def serialize(self):
        data = PinBase.serialize(self)
        m = self.currentData()
        data['value'] = [m.c1.tolist(), m.c2.tolist(), m.c3.tolist()]
        return data

    def setData(self, data):
        if isinstance(data, Matrix33):
            self._data = data
        elif isinstance(data, list) and len(data) == 3:
            self._data = Matrix33([data[0], data[1], data[2]])
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
