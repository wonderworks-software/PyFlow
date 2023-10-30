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

from PyFlow.Packages.PyFlowBase import PACKAGE_NAME
from PyFlow import GET_PACKAGES
from PyFlow.Core.PathsRegistry import PathsRegistry
from PyFlow.UI.Widgets.EnumComboBox import EnumComboBox
from PyFlow.UI.Widgets.InputWidgets import *
from PyFlow.UI.Widgets.QtSliders import *
from PyFlow.UI.Widgets.FileDialog import FileDialog


class ExecInputWidget(InputWidgetSingle):
    """docstring for ExecInputWidget"""

    def __init__(self, parent=None, **kwargs):
        super(ExecInputWidget, self).__init__(parent=parent, **kwargs)
        self.pb = QPushButton("execute", self)
        self.setWidget(self.pb)
        self.pb.clicked.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLock=False):
        pass


class FloatInputWidgetSimple(InputWidgetSingle):
    """
    Floating point data input widget without enhancements
    """

    def __init__(self, parent=None, **kwargs):
        super(FloatInputWidgetSimple, self).__init__(parent=parent, **kwargs)
        self.sb = valueBox(type="float", buttons=True)
        self.sb.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        self.sb.setSingleStep(0.01)
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLock=False):
        self.sb.blockSignals(bLock)

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

    def __init__(self, parent=None, **kwargs):
        super(FloatInputWidget, self).__init__(parent=parent, **kwargs)
        valueRange = (FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
        if "pinAnnotations" in kwargs:
            if PinSpecifiers.VALUE_RANGE in kwargs["pinAnnotations"]:
                valueRange = kwargs["pinAnnotations"][PinSpecifiers.VALUE_RANGE]

        steps = copy(FLOAT_SLIDER_DRAG_STEPS)

        if "pinAnnotations" in kwargs:
            if PinSpecifiers.DRAGGER_STEPS in kwargs["pinAnnotations"]:
                steps = kwargs["pinAnnotations"][PinSpecifiers.DRAGGER_STEPS]

        self.sb = pyf_Slider(
            self, "float", style=0, sliderRange=valueRange, draggerSteps=steps
        )
        self.setWidget(self.sb)
        # when spin box updated call setter function
        self.sb.valueChanged.connect(lambda val: self.dataSetCallback(val))

    def blockWidgetSignals(self, bLock=False):
        self.sb.blockSignals(bLock)

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

    def __init__(self, parent=None, **kwargs):
        super(IntInputWidgetSimple, self).__init__(parent=parent, **kwargs)
        self.sb = valueBox(type="int", buttons=True)
        self.sb.setRange(INT_RANGE_MIN, INT_RANGE_MAX)
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLock=False):
        self.sb.blockSignals(bLock)

    def setWidgetValue(self, val):
        self.sb.setValue(int(val))


class IntInputWidget(InputWidgetSingle):
    """
    Decimal number input widget
    """

    def __init__(self, parent=None, **kwargs):
        super(IntInputWidget, self).__init__(parent=parent, **kwargs)
        valueRange = (INT_RANGE_MIN, INT_RANGE_MAX)
        if "pinAnnotations" in kwargs:
            if "ValueRange" in kwargs["pinAnnotations"]:
                valueRange = kwargs["pinAnnotations"]["ValueRange"]
        self.sb = pyf_Slider(self, "int", style=1, sliderRange=valueRange)
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLock=False):
        self.sb.blockSignals(bLock)

    def setWidgetValue(self, val):
        self.sb.setValue(int(val))


class StringInputWidget(InputWidgetSingle):
    """
    String data input widget
    """

    def __init__(self, parent=None, **kwargs):
        super(StringInputWidget, self).__init__(parent=parent, **kwargs)
        self.le = QLineEdit(self)
        self.le.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setWidget(self.le)
        self.le.editingFinished.connect(lambda: self.dataSetCallback(self.le.text()))

    def blockWidgetSignals(self, bLock=False):
        self.le.blockSignals(bLock)

    def setWidgetValue(self, val):
        self.le.setText(str(val))


class EnumInputWidget(InputWidgetSingle):
    """docstring for EnumInputWidget."""

    def __init__(self, parent=None, **kwargs):
        super(EnumInputWidget, self).__init__(parent=parent, **kwargs)
        values = []
        if PinSpecifiers.VALUE_LIST in kwargs["pinAnnotations"]:
            values = kwargs["pinAnnotations"][PinSpecifiers.VALUE_LIST]
        self.enumBox = EnumComboBox(values)
        self.enumBox.setEditable(False)
        if "editable" in kwargs["pinAnnotations"]:
            self.enumBox.setEditable(kwargs["pinAnnotations"]["editable"])
        self.setWidget(self.enumBox)
        self.enumBox.changeCallback.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLock=False):
        self.enumBox.blockSignals(bLock)

    def setWidgetValue(self, value):
        index = self.enumBox.findText(value)
        if index > 0:
            self.enumBox.setCurrentIndex(index)


class ObjectPathWidget(InputWidgetSingle):
    """docstring for ObjectPathWidget."""

    def __init__(self, parent=None, **kwargs):
        super(ObjectPathWidget, self).__init__(parent=parent, **kwargs)
        self.enumBox = EnumComboBox(PathsRegistry().getAllPaths())
        self.setWidget(self.enumBox)
        self.enumBox.changeCallback.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLock=False):
        self.enumBox.blockSignals(bLock)

    def setWidgetValue(self, value):
        self.enumBox.setCurrentText(value)


class PathInputWidget(InputWidgetSingle):
    """
    Path input widget
    """

    def __init__(self, mode="all", parent=None, **kwargs):
        super(PathInputWidget, self).__init__(parent=parent, **kwargs)
        self.mode = mode
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
        dlg = FileDialog(self.mode)
        if dlg.exec_() == QFileDialog.Accepted and len(dlg.selectedFiles()) > 0:
            self.le.setText(dlg.selectedFiles()[0])

    def blockWidgetSignals(self, bLock=False):
        self.le.blockSignals(bLock)

    def setWidgetValue(self, val):
        self.le.setText(str(val))


class BoolInputWidget(InputWidgetSingle):
    """Boolean data input widget"""

    def __init__(self, parent=None, **kwargs):
        super(BoolInputWidget, self).__init__(parent=parent, **kwargs)
        self.cb = QCheckBox(self)
        self.setWidget(self.cb)
        self.cb.stateChanged.connect(lambda val: self.dataSetCallback(bool(val)))

    def blockWidgetSignals(self, bLock=False):
        self.cb.blockSignals(bLock)

    def setWidgetValue(self, val):
        if bool(val):
            self.cb.setCheckState(QtCore.Qt.Checked)
        else:
            self.cb.setCheckState(QtCore.Qt.Unchecked)


class NoneInputWidget(InputWidgetSingle):
    """
    String data input widget
    """

    def __init__(self, parent=None, **kwargs):
        super(NoneInputWidget, self).__init__(parent=parent, **kwargs)
        self.le = QLineEdit(self)
        self.le.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setWidget(self.le)
        self.le.textChanged.connect(lambda val: self.dataSetCallback(val))
        self.le.setEnabled(False)

    def blockWidgetSignals(self, bLock=False):
        self.le.blockSignals(bLock)

    def setWidgetValue(self, val):
        self.le.setText(str(val))


def getInputWidget(
    dataType, dataSetter, defaultValue, widgetVariant=DEFAULT_WIDGET_VARIANT, **kwds
):
    """
    factory method
    """

    # try to find factory in other packages first
    for pkgName, pkg in GET_PACKAGES().items():
        # skip self
        if pkgName == PACKAGE_NAME:
            continue

        try:
            widget = pkg.PinsInputWidgetFactory()(
                dataType, dataSetter, defaultValue, widgetVariant=widgetVariant, **kwds
            )
            if widget is not None:
                return widget
        except Exception as e:
            print(
                "Failed to override input widget.{0} Package - {1}".format(
                    dataType, pkgName
                ),
                e,
            )
            continue

    if dataType == "FloatPin":
        if kwds is not None and "pinAnnotations" in kwds:
            if (
                kwds["pinAnnotations"] is not None
                and "ValueRange" in kwds["pinAnnotations"]
            ):
                return FloatInputWidget(
                    dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds
                )
        return FloatInputWidgetSimple(
            dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds
        )
    if dataType == "IntPin":
        if kwds is not None and "pinAnnotations" in kwds:
            if (
                kwds["pinAnnotations"] is not None
                and "ValueRange" in kwds["pinAnnotations"]
            ):
                return IntInputWidget(
                    dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds
                )
        return IntInputWidgetSimple(
            dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds
        )
    if dataType == "StringPin":
        if widgetVariant == DEFAULT_WIDGET_VARIANT:
            return StringInputWidget(
                dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds
            )
        elif widgetVariant == "PathWidget":
            return PathInputWidget(
                mode="all",
                dataSetCallback=dataSetter,
                defaultValue=defaultValue,
                **kwds,
            )
        elif widgetVariant == "FilePathWidget":
            return PathInputWidget(
                mode="file",
                dataSetCallback=dataSetter,
                defaultValue=defaultValue,
                **kwds,
            )
        elif widgetVariant == "FolderPathWidget":
            return PathInputWidget(
                mode="directory",
                dataSetCallback=dataSetter,
                defaultValue=defaultValue,
                **kwds,
            )
        elif widgetVariant == "EnumWidget":
            return EnumInputWidget(
                dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds
            )
        elif widgetVariant == "ObjectPathWidget":
            return ObjectPathWidget(
                dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds
            )
    if dataType == "BoolPin":
        return BoolInputWidget(
            dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds
        )
    if dataType == "ExecPin":
        return ExecInputWidget(dataSetCallback=dataSetter, defaultValue=None, **kwds)
    if dataType == "AnyPin":
        return NoneInputWidget(dataSetCallback=dataSetter, defaultValue=None, **kwds)
