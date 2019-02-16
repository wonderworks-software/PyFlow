from pyrr import Vector3

from PyFlow.Packages.Pyrr import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class FloatVector3Pin(PinBase):
    """doc string for FloatVector3Pin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(FloatVector3Pin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Vector3())

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    def supportedDataTypes(self):
        return ('FloatVector3Pin',)

    def color(self):
        return (170, 100, 200, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'FloatVector3Pin', Vector3()

    def serialize(self):
        data = PinBase.serialize(self)
        data['value'] = self.currentData().xyz.tolist()
        return data

    def setData(self, data):
        if isinstance(data, Vector3):
            self._data = data
        elif isinstance(data, list) and len(data) == 3:
            self._data = Vector3(data)
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
