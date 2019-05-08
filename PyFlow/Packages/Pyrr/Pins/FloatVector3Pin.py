from pyrr import Vector3
import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class Vector3Encoder(json.JSONEncoder):
    def default(self, vec3):
        if isinstance(vec3, Vector3):
            return {Vector3.__name__: vec3.xyz.tolist()}
        json.JSONEncoder.default(self, vec3)


class Vector3Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(Vector3Decoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return Vector3(vec3Dict[Vector3.__name__])


class FloatVector3Pin(PinBase):
    """doc string for FloatVector3Pin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(FloatVector3Pin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(Vector3())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('FloatVector3Pin',)

    @staticmethod
    def color():
        return (170, 100, 200, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'FloatVector3Pin', Vector3()

    @staticmethod
    def jsonEncoderClass():
        return Vector3Encoder

    @staticmethod
    def jsonDecoderClass():
        return Vector3Decoder

    @staticmethod
    def processData(data):
        if isinstance(data, Vector3):
            return data
        raise(Exception('Invalid Vector3 data'))

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
