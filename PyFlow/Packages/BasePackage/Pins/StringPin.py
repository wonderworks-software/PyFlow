from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class StringPin(PinBase):
    """doc string for StringPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(StringPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue("")

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    def supportedDataTypes(self):
        return ('StringPin',)

    def color(self):
        return (255, 8, 127, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'StringPin', ''

    def setData(self, data):
        try:
            self._data = str(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)
