from pyrr import Quaternion
import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class QuatEncoder(json.JSONEncoder):
    def default(self, q):
        if isinstance(q, Quaternion):
            return {Quaternion.__name__: q.tolist()}
        json.JSONEncoder.default(self, q)


class QuatDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(QuatDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, qDict):
        return Quaternion(qDict[Quaternion.__name__])


class QuatPin(PinBase):
    """doc string for QuatPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(QuatPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Quaternion())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def isPrimitiveType():
        return False

    @staticmethod
    def jsonEncoderClass():
        return QuatEncoder

    @staticmethod
    def jsonDecoderClass():
        return QuatDecoder

    def supportedDataTypes(self):
        return ('QuatlPin',)

    @staticmethod
    def color():
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

    @staticmethod
    def processData(data):
        if isinstance(data, Quaternion):
            return data
        elif isinstance(data, list) and len(data) == 4:
            # here serialized data will be handled
            # when node desirializes itself, it creates all pins
            # and then sets data to them. Here, data will be set fo the first time after deserialization
            return Quaternion(data)
        raise(Exception('Invalid Quaternion data'))

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
