## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


# Input widgets for pins
from Qt import QtCore
from Qt.QtWidgets import *

from PyFlow.Core.Common import *
from PyFlow.UI.Widgets.EnumComboBox import EnumComboBox
from PyFlow.UI.Widgets.InputWidgets import *
from PyFlow.UI.Widgets.QtSliders import pyf_Slider, valueBox

FLOAT_SINGLE_STEP = 0.01
FLOAT_DECIMALS = 5


def _configDoubleSpinBox(sb):
    sb.setDecimals(FLOAT_DECIMALS)
    sb.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
    sb.setSingleStep(FLOAT_SINGLE_STEP)
    sb.setDisplayMinimun(0)
    sb.setDisplayMaximum(10)


def _configIntSpinBox(sb):
    sb.setRange(INT_RANGE_MIN, INT_RANGE_MAX)
    sb.setDisplayMinimun(0)
    sb.setDisplayMaximum(10)


class ExecInputWidget(InputWidgetSingle):
    """docstring for ExecInputWidget"""

    def __init__(self, parent=None, **kwds):
        super(ExecInputWidget, self).__init__(parent=parent, **kwds)
        self.pb = QPushButton('execute', self)
        self.setWidget(self.pb)
        self.pb.clicked.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLocked):
        pass


class FloatInputWidgetSimple(InputWidgetSingle):
    """
    Floating point data input widget without enhancements
    """

    def __init__(self, parent=None, **kwds):
        super(FloatInputWidgetSimple, self).__init__(parent=parent, **kwds)
        self.sb = valueBox("float", True)
        self.sb.setDecimals(FLOAT_DECIMALS)
        self.sb.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.sb.setSingleStep(FLOAT_SINGLE_STEP)
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLocked):
        self.sb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.sb.setValue(float(val))

    def setMaximum(self, max):
        self.sb.setMaximum(max)

    def setMinimum(self, min):
        self.sb.setMinimum(min)


class FloatInputWidget(InputWidgetSingle):
    """
    Floating point data input widget
    """

    def __init__(self, parent=None, **kwds):
        super(FloatInputWidget, self).__init__(parent=parent, **kwds)
        self.sb = pyf_Slider(self, "float", style=0)
        _configDoubleSpinBox(self.sb)
        self.sb.setDisplayMinimun(0)
        self.sb.setDisplayMaximum(10)
        self.setWidget(self.sb)
        # when spin box updated call setter function
        self.sb.valueChanged.connect(lambda val: self.dataSetCallback(val))

    def blockWidgetSignals(self, bLocked):
        self.sb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.sb.setValue(float(val))

    def setMaximum(self, max):
        self.sb.setMaximum(max)

    def setMinimum(self, min):
        self.sb.setMinimum(min)


class IntInputWidgetSimple(InputWidgetSingle):
    """
    Decimal number input widget without enhancements
    """

    def __init__(self, parent=None, **kwds):
        super(IntInputWidgetSimple, self).__init__(parent=parent, **kwds)
        self.sb = valueBox("int", True)
        self.sb.setRange(INT_RANGE_MIN, INT_RANGE_MAX)
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLocked):
        self.sb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.sb.setValue(int(val))


class IntInputWidget(InputWidgetSingle):
    """
    Decimal number input widget
    """

    def __init__(self, parent=None, **kwds):
        super(IntInputWidget, self).__init__(parent=parent, **kwds)
        self.sb = pyf_Slider(self, "int", style=1)
        _configIntSpinBox(self.sb)
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(self.dataSetCallback)

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
        self.le.editingFinished.connect(lambda: self.dataSetCallback(self.le.text()))

    def blockWidgetSignals(self, bLocked):
        self.le.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.le.setText(str(val))


class EnumInputWIdget(InputWidgetSingle):
    """docstring for EnumInputWIdget."""
    def __init__(self, parent=None, **kwds):
        super(EnumInputWIdget, self).__init__(parent=parent, **kwds)
        self.enumBox = EnumComboBox(kwds["pinAnnotations"]["ValueList"])
        self.enumBox.setEditable(False)
        self.setWidget(self.enumBox)
        self.enumBox.changeCallback.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLock=False):
        self.enumBox.blockSignals(bLock)

    def setWidgetValue(self, value):
        index = self.enumBox.findText(value)
        if index > 0:
            self.enumBox.setCurrentIndex(index)


class PathInputWidget(InputWidgetSingle):
    """
    Path input widget
    """

    def __init__(self, parent=None, **kwds):
        super(PathInputWidget, self).__init__(parent=parent, **kwds)
        self.content = QWidget()
        self.content.setContentsMargins(0, 0, 0, 0)
        self.pathLayout = QHBoxLayout(self.content)
        self.pathLayout.setContentsMargins(0, 0, 0, 0)
        self.le = QLineEdit()
        self.le.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.pathLayout.addWidget(self.le)
        self.pbGetPath = QPushButton("...")
        self.pbGetPath.clicked.connect(self.getPath)
        self.pathLayout.addWidget(self.pbGetPath)
        self.setWidget(self.content)
        self.le.textChanged.connect(lambda val: self.dataSetCallback(val))

    def getPath(self):
        directory = QFileDialog.getExistingDirectory(None, "Select dir", "")
        self.le.setText(directory)

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
        self.cb.stateChanged.connect(
            lambda val: self.dataSetCallback(bool(val)))

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


def getInputWidget(dataType, dataSetter, defaultValue, widgetVariant=DEFAULT_WIDGET_VARIANT, **kwds):
    '''
    factory method
    '''
    if dataType == 'FloatPin':
        if widgetVariant == DEFAULT_WIDGET_VARIANT:
            return FloatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
        elif widgetVariant == "FloatInputWidgetSimple":
            return FloatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
    if dataType == 'IntPin':
        if widgetVariant == DEFAULT_WIDGET_VARIANT:
            return IntInputWidgetSimple(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
        elif widgetVariant == "IntInputWidgetSimple":
            return IntInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
    if dataType == 'StringPin':
        if widgetVariant == DEFAULT_WIDGET_VARIANT:
            return StringInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
        elif widgetVariant == "PathWidget":
            return PathInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
        elif widgetVariant == "EnumWidget":
            return EnumInputWIdget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
    if dataType == 'BoolPin':
        return BoolInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
    if dataType == 'ExecPin':
        return ExecInputWidget(dataSetCallback=dataSetter, defaultValue=None, **kwds)
    if dataType == 'AnyPin':
        return NoneInputWidget(dataSetCallback=dataSetter, defaultValue=None, **kwds)
