from PyFlow.Core.Common import *
from qtpy import QtCore
from qtpy.QtWidgets import QCheckBox
from PyFlow.UI.Widgets.InputWidgets import *


class DemoInputWidget(InputWidgetSingle):
    """Boolean data input widget"""

    def __init__(self, parent=None, **kwds):
        super(DemoInputWidget, self).__init__(parent=parent, **kwds)
        self.cb = QCheckBox(self)
        self.setWidget(self.cb)
        self.cb.stateChanged.connect(lambda val: self.dataSetCallback(bool(val)))

    def blockWidgetSignals(self, bLocked):
        self.cb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        if bool(val):
            self.cb.setCheckState(QtCore.Qt.Checked)
        else:
            self.cb.setCheckState(QtCore.Qt.Unchecked)


def getInputWidget(dataType, dataSetter, defaultValue, widgetVariant=DEFAULT_WIDGET_VARIANT, **kwds):
    if dataType == 'DemoPin':
        return DemoInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
