from Core.Pin import PinWidgetBase
from Core.AGraphCommon import *


class ExecPin(PinWidgetBase):
    """doc string for ExecPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(ExecPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.width = self.height = 10.0
        self.dirty = False

    def supportedDataTypes(self):
        return (DataTypes.Exec,)

    def call(self):
        super(ExecPin, self).call()
        # pass execution flow forward
        for p in [pin for pin in self.affects if pin.dataType == DataTypes.Exec]:
            p.call()
        # highlight wire
        for e in self.edge_list:
            e.highlight()

    @staticmethod
    def color():
        return Colors.Exec

    @staticmethod
    def pinDataTypeHint():
        return DataTypes.Exec, None

    def setData(self, data):
        pass
