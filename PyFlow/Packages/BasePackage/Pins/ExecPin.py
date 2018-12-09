from ..Core.AbstractGraph import PinBase
from ..Core.AGraphCommon import *


## Execution pin
class ExecPin(PinBase):
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(ExecPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.width = self.height = 10.0
        self.dirty = False

    def supportedDataTypes(self):
        return (DataTypes.Exec,)

    ## Controls execution flow
    def call(self):
        super(ExecPin, self).call()
        # pass execution flow forward
        for p in [pin for pin in self.affects if pin.dataType == DataTypes.Exec]:
            p.call()

    @staticmethod
    def color():
        return Colors.Exec

    @staticmethod
    def pinDataTypeHint():
        return DataTypes.Exec, None

    def setData(self, data):
        pass
