from pyrr import Matrix33
import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class M33Encoder(json.JSONEncoder):
    def default(self, m33):
        if isinstance(m33, Matrix33):
            return {Matrix33.__name__: m33.tolist()}
        json.JSONEncoder.default(self, m33)


class M33Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(M33Decoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, m33Dict):
        return Matrix33(m33Dict[Matrix33.__name__])


class Matrix33Pin(PinBase):
    """doc string for Matrix33Pin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(Matrix33Pin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Matrix33())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def isPrimitiveType():
        return False

    @staticmethod
    def jsonEncoderClass():
        return M33Encoder

    @staticmethod
    def jsonDecoderClass():
        return M33Decoder

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

    @staticmethod
    def processData(data):
        if isinstance(data, Matrix33):
            return data
        elif isinstance(data, list) and len(data) == 3:
            return Matrix33([data[0], data[1], data[2]])
        raise(Exception('Invalid Matrix33 data'))

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
