from ..Core.AbstractGraph import PinBase
from ..Core.AGraphCommon import *
from pyrr import Vector3


class FloatVector3Pin(PinBase):
    """doc string for FloatVector3Pin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(FloatVector3Pin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Vector3())

    def supportedDataTypes(self):
        return (DataTypes.FloatVector3,)

    @staticmethod
    def color():
        return Colors.FloatVector3

    @staticmethod
    def pinDataTypeHint():
        return DataTypes.FloatVector3, Vector3()

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
