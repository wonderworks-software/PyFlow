from blinker import Signal
import json
from Qt import QtGui
from nine import str

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow import getAllPinClasses
from PyFlow import CreateRawPin
from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType

from PyFlow.Packages.PyflowBase.Pins.AnyPin import AnyPin
class dictElement(tuple):

    def __new__ (self, a=None, b=None):
        if a is None and b is None:
            new = ()
        elif b is None:
            if isinstance(a,tuple) and len(a)<=2:
                new = a
            else:
                raise Exception("non Valid Input")
        else:
            new = (a,b)
        return super(dictElement, self).__new__(self, tuple(new))


class dictElementPin(AnyPin):
    """doc string for dictElementPin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(dictElementPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(dictElement())

    @staticmethod
    def supportedDataTypes():
        return ('dictElementPin')

    @staticmethod
    def pinDataTypeHint():
        return 'dictElementPin', dictElement()

    @staticmethod
    def internalDataStructure():
        return dictElement

    @staticmethod
    def processData(data):
        return dictElement(data)
