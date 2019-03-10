from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.UI.Settings import Colors


## Execution pin
class ExecPin(PinBase):
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(ExecPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.width = self.height = 10.0
        self.dirty = False

    @staticmethod
    def isPrimitiveType():
        return True

    @staticmethod
    def IsValuePin():
        return False

    def supportedDataTypes(self):
        return ('ExecPin',)

    ## Controls execution flow
    def call(self):
        super(ExecPin, self).call()
        # pass execution flow forward
        for p in [pin for pin in self.affects if pin.dataType == 'ExecPin']:
            p.call()

    @staticmethod
    def pinDataTypeHint():
        return 'ExecPin', None

    @staticmethod
    def color():
        return (255, 255, 255, 255)

    def setData(self, data):
        pass
