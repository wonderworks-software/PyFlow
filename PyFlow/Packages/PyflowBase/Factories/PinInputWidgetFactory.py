# Input widgets for pins
import weakref

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QDoubleSpinBox
from Qt.QtWidgets import QSpinBox
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QComboBox
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QGridLayout

from PyFlow.Core.AGraphCommon import *
from PyFlow.UI.InputWidgets import *


FLOAT_SINGLE_STEP = 0.01
FLOAT_DECIMALS = 10


def _configDoubleSpinBox(sb):
    sb.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
    sb.setSingleStep(FLOAT_SINGLE_STEP)
    sb.setDecimals(FLOAT_DECIMALS)


def _configIntSpinBox(sb):
    sb.setRange(INT_RANGE_MIN, INT_RANGE_MAX)


class ExecInputWidget(InputWidgetSingle):
    """docstring for ExecInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(ExecInputWidget, self).__init__(parent=parent, **kwds)
        self.pb = QPushButton('execute', self)
        self.setWidget(self.pb)
        self.pb.clicked.connect(self.dataSetCallback)
        self.pbReset.deleteLater()

    def blockWidgetSignals(self, bLocked):
        pass


class EnumInputWidget(InputWidgetSingle):
    """
    Enum input widget
    """
    def __init__(self, parent=None, **kwds):
        super(EnumInputWidget, self).__init__(parent=parent, **kwds)
        # self._userStruct = kwds['userStructClass']
        self.cb = QComboBox(self)
        self.setWidget(self.cb)
        for i in list(kwds['userStructClass']):
            self.cb.addItem(i.name, i.value)
        self.cb.currentIndexChanged[int].connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLocked):
        self.cb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.cb.setCurrentIndex(val)


class FloatInputWidget(InputWidgetSingle):
    """
    Floating point data input widget
    """

    def __init__(self, parent=None, **kwds):
        super(FloatInputWidget, self).__init__(parent=parent, **kwds)
        self.sb = QDoubleSpinBox(self)
        _configDoubleSpinBox(self.sb)
        self.setWidget(self.sb)
        # when spin box updated call setter function
        self.sb.valueChanged.connect(lambda val: self.dataSetCallback(val))

    def blockWidgetSignals(self, bLocked):
        self.sb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.sb.setValue(float(val))


class IntInputWidget(InputWidgetSingle):
    """
    Decimal number input widget
    """
    def __init__(self, parent=None, **kwds):
        super(IntInputWidget, self).__init__(parent=parent, **kwds)
        self.sb = QSpinBox(self)
        _configIntSpinBox(self.sb)
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(lambda val: self.dataSetCallback(val))

    def blockWidgetSignals(self, bLocked):
        self.sb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.sb.setValue(int(val))


class StringInputWidget(InputWidgetSingle):
    """
    String data input widget
    """
    def __init__(self, parent=None, **kwds):
        super(StringInputWidget, self).__init__(parent=parent, **kwds)
        self.le = QLineEdit(self)
        self.le.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setWidget(self.le)
        self.le.textChanged.connect(lambda val: self.dataSetCallback(val))

    def blockWidgetSignals(self, bLocked):
        self.le.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.le.setText(str(val))


class BoolInputWidget(InputWidgetSingle):
    """Boolean data input widget"""
    def __init__(self, parent=None, **kwds):
        super(BoolInputWidget, self).__init__(parent=parent, **kwds)
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


class NoneInputWidget(InputWidgetSingle):
    """
    String data input widget
    """
    def __init__(self, parent=None, **kwds):
        super(NoneInputWidget, self).__init__(parent=parent, **kwds)
        self.le = QLineEdit(self)
        self.le.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setWidget(self.le)
        self.le.textChanged.connect(lambda val: self.dataSetCallback(val))
        self.le.setEnabled(False)

    def blockWidgetSignals(self, bLocked):
        self.le.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.le.setText(str(val))


def getInputWidget(dataType, dataSetter, defaultValue, userStructClass):
    '''
    factory method
    '''
    if dataType == 'FloatPin':
        return FloatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'IntPin':
        return IntInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'StringPin':
        return StringInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'BoolPin':
        return BoolInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'ExecPin':
        return ExecInputWidget(dataSetCallback=dataSetter, defaultValue=None)
    if dataType == 'EnumPin':
        return EnumInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, userStructClass=userStructClass)
    if dataType == 'AnyPin':
        return NoneInputWidget(dataSetCallback=dataSetter, defaultValue=None)
    if dataType == 'ListPin':
        return NoneInputWidget(dataSetCallback=dataSetter, defaultValue=None)
