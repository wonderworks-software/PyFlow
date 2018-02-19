from Core.Pin import PinWidgetBase
from Core.AGraphCommon import *
from pyrr import Quaternion


class QuatPin(PinWidgetBase):
    """doc string for QuatPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(QuatPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Quaternion())

    def supportedDataTypes(self):
        return (DataTypes.Quaternion,)

    @staticmethod
    def color():
        return Colors.Quaternion

    @staticmethod
    def pinDataTypeHint():
        return DataTypes.Quaternion, Quaternion()

    def serialize(self):
        # note how custom class can be serialized
        # here we store quats xyzw as list
        data = PinWidgetBase.serialize(self)
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
        PinWidgetBase.setData(self, self._data)
