from pyrr import Vector4

from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class FloatVector4Pin(PinBase):
    """doc string for FloatVector4Pin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(FloatVector4Pin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Vector4())

    @staticmethod
    def IsValuePin():
        return True

    def supportedDataTypes(self):
        return ('FloatVector4Pin',)

    @staticmethod
    def pinDataTypeHint():
        return 'FloatVector4Pin', Vector4()

    @staticmethod
    def color():
        return (173, 216, 230, 255)

    def serialize(self):
        data = PinBase.serialize(self)
        data['value'] = self.currentData().xyzw.tolist()
        return data

    def setData(self, data):
        if isinstance(data, Vector4):
            self._data = data
        elif isinstance(data, list) and len(data) == 4:
            self._data = Vector4(data)
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
