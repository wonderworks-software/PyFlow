from pyrr import Vector4
import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class Vector4Encoder(json.JSONEncoder):
    def default(self, vec4):
        if isinstance(vec4, Vector4):
            return {Vector4.__name__: vec4.xyzw.tolist()}
        json.JSONEncoder.default(self, vec4)


class Vector4Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(Vector4Decoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec4Dict):
        return Vector4(vec4Dict[Vector4.__name__])


class FloatVector4Pin(PinBase):
    """doc string for FloatVector4Pin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(FloatVector4Pin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(Vector4())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def isPrimitiveType():
        return False

    @staticmethod
    def jsonEncoderClass():
        return Vector4Encoder

    @staticmethod
    def jsonDecoderClass():
        return Vector4Decoder

    @staticmethod
    def supportedDataTypes():
        return ('FloatVector4Pin',)

    @staticmethod
    def pinDataTypeHint():
        return 'FloatVector4Pin', Vector4()

    @staticmethod
    def color():
        return (173, 216, 230, 255)

    def serialize(self, copying=False):
        data = PinBase.serialize(self)
        data['value'] = self.currentData().xyzw.tolist()
        return data

    @staticmethod
    def processData(data):
        if isinstance(data, Vector4):
            return data
        elif isinstance(data, list) and len(data) == 4:
            return Vector4(data)
        raise(Exception('Invalid Vector4 data'))

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
