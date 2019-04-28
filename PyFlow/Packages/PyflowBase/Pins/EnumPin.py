from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.Core.Enums import ENone


class EnumPin(PinBase):
    '''doc string for EnumPin'''
    def __init__(self, name, parent, direction, **kwargs):
        super(EnumPin, self).__init__(name, parent, direction, **kwargs)
        self._userStruct = kwargs['userStructClass']
        self.setDefaultValue(self._userStruct(0))

    @staticmethod
    def IsValuePin():
        return True

    def serialize(self, copying=False):
        dt = super(EnumPin, self).serialize(copying=copying)
        dt['value'] = int(dt['value'])
        return dt

    @staticmethod
    def color():
        return (255, 211, 25, 255)

    @staticmethod
    def supportedDataTypes():
        return ('IntPin', 'EnumPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'EnumPin', ENone

    @staticmethod
    def processData(data):
        return data

    def setData(self, data):
        if isinstance(data, self._userStruct) and data != self._userStruct:
            self._data = data
        if isinstance(data, int):
            try:
                self._data = self._userStruct(data)
            except:
                self._data = self.defaultValue()
        PinBase.setData(self, self._data)
