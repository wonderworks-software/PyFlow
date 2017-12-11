import weakref
from Port import Port
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QDoubleSpinBox
from Qt.QtWidgets import QSpinBox
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QGraphicsProxyWidget
from AGraphCommon import DataTypes
from AGraphCommon import push


class PinInputWidgetBase(object):
    """doc string for PinInputWidgetBase"""

    def __init__(self, pin, **kwds):
        super(PinInputWidgetBase, self).__init__(**kwds)
        if not isinstance(pin, Port):
            raise TypeError("[ERROR] Port expected, got {0}".format(type(pin)))
        self.pin = weakref.ref(pin)
        pin.inputWidget = self

    def dataUpdated(self, data):
        # from widget to pin
        self.pin().set_data(data)
        push(self.pin())

    def setData(self, data):
        # from pin to widget
        pass

    def asProxy(self):
        prx = QGraphicsProxyWidget()
        prx.setWidget(self)
        return prx


class FloatInputWidget(PinInputWidgetBase, QDoubleSpinBox):
    """doc string for FloatInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(FloatInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(-2147483648.01, 2147483647.01)
        self.setSingleStep(0.01)
        self.setMaximumWidth(70)
        self.setDecimals(20)
        self.valueChanged.connect(self.dataUpdated)

    def setData(self, data):
        self.setValue(float(data))


class IntInputWidget(PinInputWidgetBase, QSpinBox):
    """doc string for IntInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(IntInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(-2147483648, 2147483647)
        self.setMaximumWidth(70)
        self.valueChanged.connect(self.dataUpdated)

    def setData(self, data):
        self.setValue(int(data))


class StringInputWidget(PinInputWidgetBase, QLineEdit):
    """doc string for StringInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(StringInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.textChanged.connect(self.dataUpdated)
        self.setMaximumWidth(70)

    def setData(self, data):
        self.setText(str(data))


class BoolInputWidget(PinInputWidgetBase, QCheckBox):
    """doc string for BoolInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(BoolInputWidget, self).__init__(**kwds)
        self.stateChanged.connect(self.dataUpdated)

    def setData(self, data):
        if bool(data):
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)
        push(self.pin())


def getPinWidget(pin):
    '''
    fabric method
    '''
    if not isinstance(pin, Port):
        raise TypeError("[ERROR] Port expected, got {0}".format(type(pin)))
    if pin.data_type == DataTypes.Float:
        return FloatInputWidget(pin=pin)
    if pin.data_type == DataTypes.Int:
        return IntInputWidget(pin=pin)
    if pin.data_type == DataTypes.String:
        return StringInputWidget(pin=pin)
    if pin.data_type == DataTypes.Bool:
        return BoolInputWidget(pin=pin)
    return None
