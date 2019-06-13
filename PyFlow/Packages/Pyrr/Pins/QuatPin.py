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
    def __init__(self, name, parent, direction, **kwargs):
        super(QuatPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(Quaternion())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def jsonEncoderClass():
        return QuatEncoder

    @staticmethod
    def jsonDecoderClass():
        return QuatDecoder

    @staticmethod
    def supportedDataTypes():
        return ('QuatPin',)

    @staticmethod
    def color():
        return (32, 178, 170, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'QuatPin', Quaternion()

    @staticmethod
    def internalDataStructure():
        return Quaternion

    @staticmethod
    def processData(data):
        return QuatPin.internalDataStructure()(data)
