import weakref
import pyrr

from PyFlow.Core.Common import *
from PyFlow.UI.Widgets.InputWidgets import *

from PyFlow.Packages.Pyrr.Widgets import Ui_FloatVector3InputWidget_ui
from PyFlow.Packages.Pyrr.Widgets import Ui_FloatVector4InputWidget_ui
from PyFlow.Packages.Pyrr.Widgets import Matrix33InputWidget_ui
from PyFlow.Packages.Pyrr.Widgets import Matrix44InputWidget_ui
from PyFlow.UI.Widgets.QtSliders import pyf_FloatSlider

from Qt import QtWidgets

FLOAT_SINGLE_STEP = 0.01
FLOAT_DECIMALS = 5


class FloatVector3InputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(FloatVector3InputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbX = pyf_FloatSlider(self, style=0)
        self.dsbY = pyf_FloatSlider(self, style=0)
        self.dsbZ = pyf_FloatSlider(self, style=0)
        self.pbReset = QtWidgets.QPushButton(self)
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)
        self.layout().addWidget(self.pbReset)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)
        self.pbReset.clicked.connect(self.onResetValue)

    def blockWidgetSignals(self, bLocked):
        for w in [self.dsbX, self.dsbY, self.dsbZ]:
            w.blockSignals(bLocked)

    def asDataTypeClass(self):
        return pyrr.Vector3([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX,self.dsbY,self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        self.dsbX.setValue(val.x)
        self.dsbY.setValue(val.y)
        self.dsbZ.setValue(val.z)


class FloatVector4InputWidget(InputWidgetRaw, Ui_FloatVector4InputWidget_ui.Ui_Form):
    """Vector4 data input widget"""

    def __init__(self, **kwds):
        super(FloatVector4InputWidget, self).__init__(**kwds)
        self.setupUi(self)
        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)
        self.dsbW.valueChanged.connect(self._onDataChangedW)
        self.pbReset.clicked.connect(self.onResetValue)

    def blockWidgetSignals(self, bLocked):
        for w in [self.dsbX, self.dsbY, self.dsbZ, self.dsbW]:
            w.blockSignals(bLocked)

    def asDataTypeClass(self):
        return pyrr.Vector4([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value(), self.dsbW.value()])

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

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def _onDataChangedW(self, val):
        v = self.asDataTypeClass()
        v.w = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        self.dsbX.setValue(val.x)
        self.dsbY.setValue(val.y)
        self.dsbZ.setValue(val.z)
        self.dsbW.setValue(val.w)


class QuatInputWidget(FloatVector4InputWidget):
    """Quaternion data input widget"""

    def __init__(self, **kwds):
        super(QuatInputWidget, self).__init__(**kwds)

    def asDataTypeClass(self):
        return pyrr.Quaternion([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value(), self.dsbW.value()])


class Matrix33InputWidget(InputWidgetRaw, Matrix33InputWidget_ui.Ui_Form):
    """Matrix33 data input widget"""

    def __init__(self, parent=None, **kwds):
        super(Matrix33InputWidget, self).__init__(parent=parent, **kwds)
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

        self.pbReset.clicked.connect(self.onResetValue)

    def blockWidgetSignals(self, bLocked):
        for w in [self.dsbm11, self.dsbm12, self.dsbm13,
                  self.dsbm21, self.dsbm22, self.dsbm23,
                  self.dsbm31, self.dsbm32, self.dsbm33]:
            w.blockSignals(bLocked)

    def asDataTypeClass(self):
        return pyrr.Matrix33([
            [self.dsbm11.value(), self.dsbm12.value(), self.dsbm13.value()],
            [self.dsbm21.value(), self.dsbm22.value(), self.dsbm23.value()],
            [self.dsbm31.value(), self.dsbm32.value(), self.dsbm33.value()]
        ])

    def _configSpinBoxes(self):
        ls = [self.dsbm11, self.dsbm12, self.dsbm13,
              self.dsbm21, self.dsbm22, self.dsbm23,
              self.dsbm31, self.dsbm32, self.dsbm33]
        for sb in ls:
            sb.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            sb.setSingleStep(FLOAT_SINGLE_STEP)
            sb.setDecimals(FLOAT_DECIMALS)

    def m11Changed(self, val):
        m = self.asDataTypeClass()
        m.m11 = val
        self.dataSetCallback(m)

    def m12Changed(self, val):
        m = self.asDataTypeClass()
        m.m12 = val
        self.dataSetCallback(m)

    def m13Changed(self, val):
        m = self.asDataTypeClass()
        m.m13 = val
        self.dataSetCallback(m)

    def m21Changed(self, val):
        m = self.asDataTypeClass()
        m.m21 = val
        self.dataSetCallback(m)

    def m22Changed(self, val):
        m = self.asDataTypeClass()
        m.m22 = val
        self.dataSetCallback(m)

    def m23Changed(self, val):
        m = self.asDataTypeClass()
        m.m23 = val
        self.dataSetCallback(m)

    def m31Changed(self, val):
        m = self.asDataTypeClass()
        m.m31 = val
        self.dataSetCallback(m)

    def m32Changed(self, val):
        m = self.asDataTypeClass()
        m.m32 = val
        self.dataSetCallback(m)

    def m33Changed(self, val):
        m = self.asDataTypeClass()
        m.m33 = val
        self.dataSetCallback(m)

    def setWidgetValue(self, val):
        self.dsbm11.setValue(val.m11)
        self.dsbm12.setValue(val.m12)
        self.dsbm13.setValue(val.m13)

        self.dsbm21.setValue(val.m21)
        self.dsbm22.setValue(val.m22)
        self.dsbm23.setValue(val.m23)

        self.dsbm31.setValue(val.m31)
        self.dsbm32.setValue(val.m32)
        self.dsbm33.setValue(val.m33)


class Matrix44InputWidget(InputWidgetRaw, Matrix44InputWidget_ui.Ui_Form):
    """Matrix44 data input widget"""

    def __init__(self, parent=None, **kwds):
        super(Matrix44InputWidget, self).__init__(parent=parent, **kwds)
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

        self.pbReset.clicked.connect(self.onResetValue)

    def blockWidgetSignals(self, bLocked):
        for w in [self.dsbm11, self.dsbm12, self.dsbm13, self.dsbm14,
                  self.dsbm21, self.dsbm22, self.dsbm23, self.dsbm24,
                  self.dsbm31, self.dsbm32, self.dsbm33, self.dsbm34,
                  self.dsbm41, self.dsbm42, self.dsbm43, self.dsbm44]:
            w.blockSignals(bLocked)

    def asDataTypeClass(self):
        return pyrr.Matrix44([
            [self.dsbm11.value(), self.dsbm12.value(),
             self.dsbm13.value(), self.dsbm14.value()],
            [self.dsbm21.value(), self.dsbm22.value(),
             self.dsbm23.value(), self.dsbm24.value()],
            [self.dsbm31.value(), self.dsbm32.value(),
             self.dsbm33.value(), self.dsbm34.value()],
            [self.dsbm41.value(), self.dsbm42.value(),
             self.dsbm43.value(), self.dsbm44.value()]
        ])

    def _configSpinBoxes(self):
        ls = [self.dsbm11, self.dsbm12, self.dsbm13, self.dsbm14,
              self.dsbm21, self.dsbm22, self.dsbm23, self.dsbm24,
              self.dsbm31, self.dsbm32, self.dsbm33, self.dsbm34,
              self.dsbm41, self.dsbm42, self.dsbm43, self.dsbm44]
        for sb in ls:
            sb.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            sb.setSingleStep(FLOAT_SINGLE_STEP)
            sb.setDecimals(FLOAT_DECIMALS)

    def m11Changed(self, val):
        m = self.asDataTypeClass()
        m.m11 = val
        self.dataSetCallback(m)

    def m12Changed(self, val):
        m = self.asDataTypeClass()
        m.m12 = val
        self.dataSetCallback(m)

    def m13Changed(self, val):
        m = self.asDataTypeClass()
        m.m13 = val
        self.dataSetCallback(m)

    def m14Changed(self, val):
        m = self.asDataTypeClass()
        m.m14 = val
        self.dataSetCallback(m)

    def m21Changed(self, val):
        m = self.asDataTypeClass()
        m.m21 = val
        self.dataSetCallback(m)

    def m22Changed(self, val):
        m = self.asDataTypeClass()
        m.m22 = val
        self.dataSetCallback(m)

    def m23Changed(self, val):
        m = self.asDataTypeClass()
        m.m23 = val
        self.dataSetCallback(m)

    def m24Changed(self, val):
        m = self.asDataTypeClass()
        m.m24 = val
        self.dataSetCallback(m)

    def m31Changed(self, val):
        m = self.asDataTypeClass()
        m.m31 = val
        self.dataSetCallback(m)

    def m32Changed(self, val):
        m = self.asDataTypeClass()
        m.m32 = val
        self.dataSetCallback(m)

    def m33Changed(self, val):
        m = self.asDataTypeClass()
        m.m33 = val
        self.dataSetCallback(m)

    def m34Changed(self, val):
        m = self.asDataTypeClass()
        m.m34 = val
        self.dataSetCallback(m)

    def m41Changed(self, val):
        m = self.asDataTypeClass()
        m.m41 = val
        self.dataSetCallback(m)

    def m42Changed(self, val):
        m = self.asDataTypeClass()
        m.m42 = val
        self.dataSetCallback(m)

    def m43Changed(self, val):
        m = self.asDataTypeClass()
        m.m43 = val
        self.dataSetCallback(m)

    def m44Changed(self, val):
        m = self.asDataTypeClass()
        m.m44 = val
        self.dataSetCallback(m)

    def setWidgetValue(self, val):
        self.dsbm11.setValue(val.m11)
        self.dsbm12.setValue(val.m12)
        self.dsbm13.setValue(val.m13)
        self.dsbm14.setValue(val.m14)

        self.dsbm21.setValue(val.m21)
        self.dsbm22.setValue(val.m22)
        self.dsbm23.setValue(val.m23)
        self.dsbm24.setValue(val.m24)

        self.dsbm31.setValue(val.m31)
        self.dsbm32.setValue(val.m32)
        self.dsbm33.setValue(val.m33)
        self.dsbm34.setValue(val.m34)

        self.dsbm41.setValue(val.m41)
        self.dsbm42.setValue(val.m42)
        self.dsbm43.setValue(val.m43)
        self.dsbm44.setValue(val.m44)


def getInputWidget(dataType, dataSetter, defaultValue, userStructClass):
    '''
    factory method
    '''
    if dataType == 'FloatVector3Pin':
        return FloatVector3InputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'FloatVector4Pin':
        return FloatVector4InputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'QuatPin':
        return QuatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'Matrix33Pin':
        return Matrix33InputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'Matrix44Pin':
        return Matrix44InputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    return None
