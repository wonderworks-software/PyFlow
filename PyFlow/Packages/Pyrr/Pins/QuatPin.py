from pyrr import Quaternion

from PyFlow.Packages.Pyrr import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class QuatPin(PinBase):
    """doc string for QuatPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(QuatPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Quaternion())

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    def supportedDataTypes(self):
        return ('QuatlPin',)

    def color(self):
        return (32, 178, 170, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'QuatlPin', Quaternion()

    def serialize(self):
        # note how custom class can be serialized
        # here we store quats xyzw as list
        data = PinBase.serialize(self)
        data['value'] = self.currentData().xyzw.tolist()
        return data

    def setData(self, data):
        if isinstance(data, Quaternion):
            self._data = data
        elif isinstance(data, list) and len(data) == 4:
            # here serialized data will be handled
            # when node desirializes itself, it creates all pins
            # and then sets data to them. Here, data will be set fo the first time after deserialization
            self._data = Quaternion(data)
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
