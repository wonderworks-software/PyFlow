from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from copy import copy


class ListPin(PinBase):
    """Python list() class"""
    def __init__(self, name, parent, direction, **kwargs):
        super(ListPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(False)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('ListPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'ListPin', list()

    @staticmethod
    def color():
        return (255, 200, 0, 255)

    @staticmethod
    def processData(data):
        # shallow copy here
        # same as copy(data)
        return list(data)

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
