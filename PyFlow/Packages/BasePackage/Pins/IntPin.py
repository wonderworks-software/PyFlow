from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class IntPin(PinBase):
    """doc string for IntPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(IntPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(0)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    @staticmethod
    def pinDataTypeHint():
        return 'IntPin', 0

    @staticmethod
    def color():
        return (0, 168, 107, 255)

    def supportedDataTypes(self):
        return ('IntPin', 'FloatPin')

    def setData(self, data):
        try:
            self._data = int(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
