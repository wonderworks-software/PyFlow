import weakref
from Qt import QtCore
from Qt import QtGui
import ArrayInputWidget_ui
from Qt.QtWidgets import QDoubleSpinBox
from Qt.QtWidgets import QSpinBox
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QListWidgetItem
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QGraphicsProxyWidget
from AGraphCommon import *
import Variable
import FloatVector4InputWidget_ui


class VarInputWidgetBase(object):
    """doc string for VarInputWidgetBase"""

    def __init__(self, var, **kwds):
        super(VarInputWidgetBase, self).__init__(**kwds)
        if not isinstance(var, Variable.VariableBase):
            raise TypeError("[ERROR] VariableBase expected, got {0}".format(type(var)))
        self.var = weakref.ref(var)
        self.varValueUpdated(self.var().value)

    def kill(self):
        pass

    def postCreate(self, data):
        pass

    def widgetValueUpdated(self, value):
        # update var
        self.var().value = value

    def varValueUpdated(self, value):
        # update widget
        pass


class FloatInputWidget(VarInputWidgetBase, QDoubleSpinBox):
    """doc string for FloatInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(FloatInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.setSingleStep(FLOAT_SINGLE_STEP)
        self.setMaximumWidth(70)
        self.setDecimals(FLOAT_DECIMALS)
        self.valueChanged.connect(self.widgetValueUpdated)

    def varValueUpdated(self, value):
        self.setValue(float(value))


class IntInputWidget(VarInputWidgetBase, QSpinBox):
    """doc string for IntInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(IntInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(INT_RANGE_MIN, INT_RANGE_MAX)
        self.setMaximumWidth(70)
        self.valueChanged.connect(self.widgetValueUpdated)

    def varValueUpdated(self, value):
        self.setValue(int(value))


class StringInputWidget(VarInputWidgetBase, QLineEdit):
    """doc string for StringInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(StringInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.textChanged.connect(self.widgetValueUpdated)
        self.setMaximumWidth(70)

    def varValueUpdated(self, value):
        self.setText(str(value))


class BoolInputWidget(VarInputWidgetBase, QCheckBox):
    """doc string for BoolInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(BoolInputWidget, self).__init__(**kwds)
        self.stateChanged.connect(self.widgetValueUpdated)

    def varValueUpdated(self, value):
        if bool(value):
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)


class QuatInputWidget(QWidget, VarInputWidgetBase, FloatVector4InputWidget_ui.Ui_Form):
    """doc string for QuatInputWidget"""
    def __init__(self, parent=None, **kwds):
        VarInputWidgetBase.__init__(self, **kwds)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self._configSpinBoxes()

    def _configSpinBoxes(self):
        self.dsbX.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.dsbY.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.dsbZ.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.dsbW.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.dsbX.setSingleStep(FLOAT_SINGLE_STEP)
        self.dsbY.setSingleStep(FLOAT_SINGLE_STEP)
        self.dsbZ.setSingleStep(FLOAT_SINGLE_STEP)
        self.dsbW.setSingleStep(FLOAT_SINGLE_STEP)
        self.dsbX.setDecimals(FLOAT_DECIMALS)
        self.dsbY.setDecimals(FLOAT_DECIMALS)
        self.dsbZ.setDecimals(FLOAT_DECIMALS)
        self.dsbW.setDecimals(FLOAT_DECIMALS)

    def varValueUpdated(self, value):
        pass

    def widgetValueUpdated(self, value):
        pass


def getVarWidget(var):
    '''
    fabric method
    '''
    if not isinstance(var, Variable.VariableBase):
        raise TypeError("[ERROR] VariableBase expected, got {0}".format(type(var)))
    if var.dataType == DataTypes.Float:
        return FloatInputWidget(var=var)
    if var.dataType == DataTypes.Int:
        return IntInputWidget(var=var)
    if var.dataType == DataTypes.String:
        return StringInputWidget(var=var)
    if var.dataType == DataTypes.Bool:
        return BoolInputWidget(var=var)
    if var.dataType in (DataTypes.Quaternion, DataTypes.FloatVector4):
        return QuatInputWidget(var=var)
    return None
