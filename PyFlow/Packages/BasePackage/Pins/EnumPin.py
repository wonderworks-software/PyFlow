from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *
from PyFlow.Core.Enums import ENone


class EnumPin(PinBase):
    '''doc string for EnumPin'''
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(EnumPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self._userStruct = kwargs['userStructClass']
        self.setDefaultValue(self._userStruct(0))

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    def serialize(self):
        dt = super(PinWidgetBase, self).serialize()
        dt['value'] = int(dt['value'])
        return dt

    def color(self):
        return (255, 211, 25, 255)

    def supportedDataTypes(self):
        return ('IntPin', 'EnumPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'EnumPin', ENone

    def setData(self, data):
        if isinstance(data, self._userStruct) and data != self._userStruct:
            self._data = data
        if isinstance(data, int):
            try:
                self._data = self._userStruct(data)
            except:
                self._data = self.defaultValue()
        PinBase.setData(self, self._data)
