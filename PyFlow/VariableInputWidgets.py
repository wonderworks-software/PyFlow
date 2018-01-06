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
from AGraphCommon import DataTypes
from AGraphCommon import push
import Variable


class VarInputWidgetBase(object):
    """doc string for VarInputWidgetBase"""

    def __init__(self, var, **kwds):
        super(VarInputWidgetBase, self).__init__(**kwds)
        if not isinstance(var, Variable.VariableBase):
            raise TypeError("[ERROR] VariableBase expected, got {0}".format(type(var)))
        self.var = weakref.ref(var)
        self.varDataUpdated(self.var().value)

    def kill(self):
        pass

    def postCreate(self, data):
        pass

    def widgetValueUpdated(self, value):
        # update var
        self.var().value = value

    def varDataUpdated(self, data):
        # update widget
        pass


class FloatInputWidget(VarInputWidgetBase, QDoubleSpinBox):
    """doc string for FloatInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(FloatInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(-2147483648.01, 2147483647.01)
        self.setSingleStep(0.01)
        self.setMaximumWidth(70)
        self.setDecimals(20)
        self.valueChanged.connect(self.widgetValueUpdated)

    def varDataUpdated(self, data):
        self.setValue(float(data))


class IntInputWidget(VarInputWidgetBase, QSpinBox):
    """doc string for IntInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(IntInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(-2147483648, 2147483647)
        self.setMaximumWidth(70)
        self.valueChanged.connect(self.widgetValueUpdated)

    def varDataUpdated(self, data):
        self.setValue(int(data))


class StringInputWidget(VarInputWidgetBase, QLineEdit):
    """doc string for StringInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(StringInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.textChanged.connect(self.widgetValueUpdated)
        self.setMaximumWidth(70)

    def varDataUpdated(self, data):
        self.setText(str(data))


class BoolInputWidget(VarInputWidgetBase, QCheckBox):
    """doc string for BoolInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(BoolInputWidget, self).__init__(**kwds)
        self.stateChanged.connect(self.widgetValueUpdated)

    def varDataUpdated(self, data):
        if bool(data):
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)


class ArrayInputWidget(VarInputWidgetBase, QCheckBox):
    """doc string for BoolInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(BoolInputWidget, self).__init__(**kwds)
        self.stateChanged.connect(self.widgetValueUpdated)

    def varDataUpdated(self, data):
        if bool(data):
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)


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
    if var.dataType == DataTypes.Any:
        return StringInputWidget(var=var)
    # array ?
    return None
