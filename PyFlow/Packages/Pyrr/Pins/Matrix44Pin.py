from pyrr import Matrix44
import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class M44Encoder(json.JSONEncoder):
    def default(self, m44):
        if isinstance(m44, Matrix44):
            return {Matrix44.__name__: m44.tolist()}
        json.JSONEncoder.default(self, m44)


class M44Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(M44Decoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, m44Dict):
        return Matrix44(m44Dict[Matrix44.__name__])


class Matrix44Pin(PinBase):
    """doc string for Matrix44Pin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(Matrix44Pin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(Matrix44())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def jsonEncoderClass():
        return M44Encoder

    @staticmethod
    def jsonDecoderClass():
        return M44Decoder

    @staticmethod
    def color():
        return (150, 0, 20, 255)

    @staticmethod
    def supportedDataTypes():
        return ('Matrix44Pin',)

    @staticmethod
    def pinDataTypeHint():
        return 'Matrix44Pin', Matrix44()

    @staticmethod
    def processData(data):
        if isinstance(data, Matrix44):
            return data
        raise(Exception('Invalid Matrix44 data'))

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
