import weakref
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QDoubleSpinBox
from Qt.QtWidgets import QSpinBox
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QGraphicsProxyWidget
from AGraphCommon import DataTypes
from AGraphCommon import push
from AbstractGraph import PinBase
import FloatVector3InputWidget_ui
import FloatVector4InputWidget_ui
import Matrix33InputWidget_ui
import Matrix44InputWidget_ui


FLOAT_SINGLE_STEP = 0.01
FLOAT_DECIMALS = 10
FLOAT_RANGE_MIN = -2147483648.01
FLOAT_RANGE_MAX = 2147483647.01
INT_RANGE_MIN = -2147483648
INT_RANGE_MAX = 2147483647


class PinInputWidgetBase(object):
    """doc string for PinInputWidgetBase"""
    def __init__(self, pin, **kwds):
        super(PinInputWidgetBase, self).__init__(**kwds)
        if not isinstance(pin, PinBase):
            raise TypeError("[ERROR] Pin expected, got {0}".format(type(pin)))
        self.pin = weakref.ref(pin)

    def dataUpdated(self, data):
        # from widget to pin
        self.pin().setData(data)
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
        self.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.setSingleStep(FLOAT_SINGLE_STEP)
        self.setMaximumWidth(70)
        self.setDecimals(FLOAT_DECIMALS)
        if not self.pin().hasConnections():
            self.valueChanged.connect(self.dataUpdated)

    def setData(self, data):
        self.setValue(float(data))


class IntInputWidget(PinInputWidgetBase, QSpinBox):
    """doc string for IntInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(IntInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(INT_RANGE_MIN, INT_RANGE_MAX)
        self.setMaximumWidth(70)
        if not self.pin().hasConnections():
            self.valueChanged.connect(self.dataUpdated)

    def setData(self, data):
        self.setValue(int(data))


class StringInputWidget(PinInputWidgetBase, QLineEdit):
    """doc string for StringInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(StringInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        if not self.pin().hasConnections():
            self.textChanged.connect(self.dataUpdated)
        self.setMaximumWidth(70)

    def setData(self, data):
        self.setText(str(data))


class BoolInputWidget(PinInputWidgetBase, QCheckBox):
    """doc string for BoolInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(BoolInputWidget, self).__init__(**kwds)
        if not self.pin().hasConnections():
            self.stateChanged.connect(self.dataUpdated)

    def setData(self, data):
        if bool(data):
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)


class FloatVector3InputWidget(PinInputWidgetBase, QWidget, FloatVector3InputWidget_ui.Ui_Form):
    """doc string for FloatVector3InputWidget"""
    def __init__(self, parent=None, **kwds):
        super(FloatVector3InputWidget, self).__init__(**kwds)
        self.setupUi(self)
        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self.OnDataChangedX)
        self.dsbY.valueChanged.connect(self.OnDataChangedY)
        self.dsbZ.valueChanged.connect(self.OnDataChangedZ)
        self.pbReset.clicked.connect(self.OnResetToDefaults)

    def _configSpinBoxes(self):
        self.dsbX.setDecimals(FLOAT_DECIMALS)
        self.dsbY.setDecimals(FLOAT_DECIMALS)
        self.dsbZ.setDecimals(FLOAT_DECIMALS)

        self.dsbX.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.dsbY.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.dsbZ.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)

        self.dsbX.setSingleStep(FLOAT_SINGLE_STEP)
        self.dsbY.setSingleStep(FLOAT_SINGLE_STEP)
        self.dsbZ.setSingleStep(FLOAT_SINGLE_STEP)

    def OnResetToDefaults(self):
        d = self.pin().defaultValue()
        self.dsbX.setValue(d.x)
        self.dsbY.setValue(d.y)
        self.dsbZ.setValue(d.z)

    def OnDataChangedX(self, val):
        self.pin().currentData().x = val

    def OnDataChangedY(self, val):
        self.pin().currentData().y = val

    def OnDataChangedZ(self, val):
        self.pin().currentData().z = val

    def setData(self, data):
        self.dsbX.setValue(data.x)
        self.dsbY.setValue(data.y)
        self.dsbZ.setValue(data.z)


class FloatVector4InputWidget(PinInputWidgetBase, QWidget, FloatVector4InputWidget_ui.Ui_Form):
    """doc string for FloatVector4InputWidget"""
    def __init__(self, parent=None, **kwds):
        super(FloatVector4InputWidget, self).__init__(**kwds)
        self.setupUi(self)
        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self.OnDataChangedX)
        self.dsbY.valueChanged.connect(self.OnDataChangedY)
        self.dsbZ.valueChanged.connect(self.OnDataChangedZ)
        self.dsbW.valueChanged.connect(self.OnDataChangedW)
        self.pbReset.clicked.connect(self.OnResetToDefaults)

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

    def OnResetToDefaults(self):
        d = self.pin().defaultValue()
        self.dsbX.setValue(d.x)
        self.dsbY.setValue(d.y)
        self.dsbZ.setValue(d.z)
        self.dsbW.setValue(d.w)

    def OnDataChangedX(self, val):
        self.pin().currentData().x = val

    def OnDataChangedY(self, val):
        self.pin().currentData().y = val

    def OnDataChangedZ(self, val):
        self.pin().currentData().z = val

    def OnDataChangedW(self, val):
        self.pin().currentData().w = val

    def setData(self, data):
        self.dsbX.setValue(data.x)
        self.dsbY.setValue(data.y)
        self.dsbZ.setValue(data.z)
        self.dsbW.setValue(data.w)


class Matrix33InputWidget(PinInputWidgetBase, QWidget, Matrix33InputWidget_ui.Ui_Form):
    """doc string for Matrix33InputWidget"""
    def __init__(self, parent=None, **kwds):
        super(Matrix33InputWidget, self).__init__(**kwds)
        self.setupUi(self)
        self._configSpinBoxes()

        self.dsbm11.valueChanged.connect(self.m11Changed)
        self.dsbm12.valueChanged.connect(self.m12Changed)
        self.dsbm13.valueChanged.connect(self.m13Changed)

        self.dsbm21.valueChanged.connect(self.m21Changed)
        self.dsbm22.valueChanged.connect(self.m22Changed)
        self.dsbm23.valueChanged.connect(self.m23Changed)

        self.dsbm31.valueChanged.connect(self.m31Changed)
        self.dsbm32.valueChanged.connect(self.m32Changed)
        self.dsbm33.valueChanged.connect(self.m33Changed)

        self.pbReset.clicked.connect(self.OnResetToDefaults)

    def _configSpinBoxes(self):
        ls = [self.dsbm11, self.dsbm12, self.dsbm13,
              self.dsbm21, self.dsbm22, self.dsbm23,
              self.dsbm31, self.dsbm32, self.dsbm33]
        for sb in ls:
            sb.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            sb.setSingleStep(FLOAT_SINGLE_STEP)
            sb.setDecimals(FLOAT_DECIMALS)

    def OnResetToDefaults(self):
        d = self.pin().defaultValue()
        self.dsbm11.setValue(d.m11)
        self.dsbm12.setValue(d.m12)
        self.dsbm13.setValue(d.m13)

        self.dsbm21.setValue(d.m21)
        self.dsbm22.setValue(d.m22)
        self.dsbm23.setValue(d.m23)

        self.dsbm31.setValue(d.m31)
        self.dsbm32.setValue(d.m32)
        self.dsbm33.setValue(d.m33)

    def m11Changed(self, val):
        self.pin().currentData().m11 = val

    def m12Changed(self, val):
        self.pin().currentData().m12 = val

    def m13Changed(self, val):
        self.pin().currentData().m13 = val

    def m21Changed(self, val):
        self.pin().currentData().m21 = val

    def m22Changed(self, val):
        self.pin().currentData().m22 = val

    def m23Changed(self, val):
        self.pin().currentData().m23 = val

    def m31Changed(self, val):
        self.pin().currentData().m31 = val

    def m32Changed(self, val):
        self.pin().currentData().m32 = val

    def m33Changed(self, val):
        self.pin().currentData().m33 = val

    def setData(self, data):
        self.dsbm11.setValue(data.m11)
        self.dsbm12.setValue(data.m12)
        self.dsbm13.setValue(data.m13)

        self.dsbm21.setValue(data.m21)
        self.dsbm22.setValue(data.m22)
        self.dsbm23.setValue(data.m23)

        self.dsbm31.setValue(data.m31)
        self.dsbm32.setValue(data.m32)
        self.dsbm33.setValue(data.m33)


class Matrix44InputWidget(PinInputWidgetBase, QWidget, Matrix44InputWidget_ui.Ui_Form):
    """doc string for Matrix44InputWidget"""
    def __init__(self, parent=None, **kwds):
        super(Matrix44InputWidget, self).__init__(**kwds)
        self.setupUi(self)
        self._configSpinBoxes()

        self.dsbm11.valueChanged.connect(self.m11Changed)
        self.dsbm12.valueChanged.connect(self.m12Changed)
        self.dsbm13.valueChanged.connect(self.m13Changed)
        self.dsbm14.valueChanged.connect(self.m14Changed)

        self.dsbm21.valueChanged.connect(self.m21Changed)
        self.dsbm22.valueChanged.connect(self.m22Changed)
        self.dsbm23.valueChanged.connect(self.m23Changed)
        self.dsbm24.valueChanged.connect(self.m24Changed)

        self.dsbm31.valueChanged.connect(self.m31Changed)
        self.dsbm32.valueChanged.connect(self.m32Changed)
        self.dsbm33.valueChanged.connect(self.m33Changed)
        self.dsbm34.valueChanged.connect(self.m34Changed)

        self.dsbm41.valueChanged.connect(self.m41Changed)
        self.dsbm42.valueChanged.connect(self.m42Changed)
        self.dsbm43.valueChanged.connect(self.m43Changed)
        self.dsbm44.valueChanged.connect(self.m44Changed)

        self.pbReset.clicked.connect(self.OnResetToDefaults)

    def _configSpinBoxes(self):
        ls = [self.dsbm11, self.dsbm12, self.dsbm13, self.dsbm14,
              self.dsbm21, self.dsbm22, self.dsbm23, self.dsbm24,
              self.dsbm31, self.dsbm32, self.dsbm33, self.dsbm34,
              self.dsbm41, self.dsbm42, self.dsbm43, self.dsbm44]
        for sb in ls:
            sb.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            sb.setSingleStep(FLOAT_SINGLE_STEP)
            sb.setDecimals(FLOAT_DECIMALS)

    def OnResetToDefaults(self):
        d = self.pin().defaultValue()
        self.dsbm11.setValue(d.m11)
        self.dsbm12.setValue(d.m12)
        self.dsbm13.setValue(d.m13)
        self.dsbm14.setValue(d.m14)

        self.dsbm21.setValue(d.m21)
        self.dsbm22.setValue(d.m22)
        self.dsbm23.setValue(d.m23)
        self.dsbm24.setValue(d.m24)

        self.dsbm31.setValue(d.m31)
        self.dsbm32.setValue(d.m32)
        self.dsbm33.setValue(d.m33)
        self.dsbm34.setValue(d.m34)

        self.dsbm41.setValue(d.m41)
        self.dsbm42.setValue(d.m42)
        self.dsbm43.setValue(d.m43)
        self.dsbm44.setValue(d.m44)

    def m11Changed(self, val):
        self.pin().currentData().m11 = val

    def m12Changed(self, val):
        self.pin().currentData().m12 = val

    def m13Changed(self, val):
        self.pin().currentData().m13 = val

    def m14Changed(self, val):
        self.pin().currentData().m14 = val

    def m21Changed(self, val):
        self.pin().currentData().m21 = val

    def m22Changed(self, val):
        self.pin().currentData().m22 = val

    def m23Changed(self, val):
        self.pin().currentData().m23 = val

    def m24Changed(self, val):
        self.pin().currentData().m24 = val

    def m31Changed(self, val):
        self.pin().currentData().m31 = val

    def m32Changed(self, val):
        self.pin().currentData().m32 = val

    def m33Changed(self, val):
        self.pin().currentData().m33 = val

    def m34Changed(self, val):
        self.pin().currentData().m34 = val

    def m41Changed(self, val):
        self.pin().currentData().m41 = val

    def m42Changed(self, val):
        self.pin().currentData().m42 = val

    def m43Changed(self, val):
        self.pin().currentData().m43 = val

    def m44Changed(self, val):
        self.pin().currentData().m44 = val

    def setData(self, data):
        self.dsbm11.setValue(data.m11)
        self.dsbm12.setValue(data.m12)
        self.dsbm13.setValue(data.m13)
        self.dsbm14.setValue(data.m14)

        self.dsbm21.setValue(data.m21)
        self.dsbm22.setValue(data.m22)
        self.dsbm23.setValue(data.m23)
        self.dsbm24.setValue(data.m24)

        self.dsbm31.setValue(data.m31)
        self.dsbm32.setValue(data.m32)
        self.dsbm33.setValue(data.m33)
        self.dsbm34.setValue(data.m34)

        self.dsbm41.setValue(data.m41)
        self.dsbm42.setValue(data.m42)
        self.dsbm43.setValue(data.m43)
        self.dsbm44.setValue(data.m44)


def getPinWidget(pin):
    '''
    fabric method
    '''
    if not isinstance(pin, PinBase):
        raise TypeError("[ERROR] Pin expected, got {0}".format(type(pin)))
    if pin.dataType == DataTypes.Float:
        return FloatInputWidget(pin=pin)
    if pin.dataType == DataTypes.Int:
        return IntInputWidget(pin=pin)
    if pin.dataType == DataTypes.String:
        return StringInputWidget(pin=pin)
    if pin.dataType == DataTypes.Bool:
        return BoolInputWidget(pin=pin)
    if pin.dataType == DataTypes.FloatVector3:
        return FloatVector3InputWidget(pin=pin)
    if pin.dataType in (DataTypes.FloatVector4, DataTypes.Quaternion):
        return FloatVector4InputWidget(pin=pin)
    if pin.dataType == DataTypes.Matrix33:
        return Matrix33InputWidget(pin=pin)
    if pin.dataType == DataTypes.Matrix44:
        return Matrix44InputWidget(pin=pin)
    return None
