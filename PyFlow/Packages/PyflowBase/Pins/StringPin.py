from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from nine import str

class StringPin(PinBase):
    """doc string for StringPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(StringPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue("")

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('StringPin',)

    @staticmethod
    def color():
        return (255, 8, 127, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'StringPin', ''

    @staticmethod
    def internalDataStructure():
        return str

    @staticmethod
    def processData(data):
        return StringPin.internalDataStructure()(data)
