"""@file Variable.py

Variable related classes.
"""
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QComboBox
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QSpacerItem
from Qt.QtWidgets import QSizePolicy
from uuid import uuid4
import inspect
from AbstractGraph import *
import InputWidgets
from .. import Pins


## Colored rounded rect
# color corresponds to pin data type color
class TypeWidget(QWidget):
    def __init__(self, color, parent=None):
        super(TypeWidget, self).__init__()
        self.color = color
        self.setMinimumWidth(24)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)

        painter.setBrush(QtGui.QColor(self.color))
        rect = event.rect()
        rect.setHeight(10)
        rect.setWidth(20)
        rect.moveTop(12)
        painter.drawRoundedRect(rect, 5, 5)

        painter.end()


## Changes type of variable
class VarTypeComboBox(QComboBox):
    def __init__(self, var, parent=None):
        super(VarTypeComboBox, self).__init__(parent)
        self._bJustSpawned = True
        self.var = var
        for i in self.var.types:
            self.addItem(i[0], i[1])
        self.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.setCurrentIndex(self.findData(var.dataType))
        self._bJustSpawned = False

    def onCurrentIndexChanged(self, index):
        if self._bJustSpawned:
            val = self.var.value

        self.var.setDataType(self.itemData(index), self._bJustSpawned)

        if self._bJustSpawned:
            self.var.value = val


## Variable class
class VariableBase(QWidget):
    ## executed when value been set
    valueChanged = QtCore.Signal()
    ## executed when name been changed
    nameChanged = QtCore.Signal(str)
    ## executed when variable been killed
    killed = QtCore.Signal()
    ## executed when variable data type been changed
    dataTypeChanged = QtCore.Signal(int)

    def __init__(self, name, value, graph, varsListWidget, dataType=DataTypes.Bool, uid=None):
        super(VariableBase, self).__init__()
        # ui
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = TypeWidget(Colors.Bool, self)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.labelName = QLabel(self)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout.addWidget(self.labelName)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        # self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        # body
        self.varsListWidget = varsListWidget
        self.name = None
        self._value = value
        self.dataType = dataType
        self._uid = uid
        if self._uid is None:
            self._uid = uuid4()
        self.graph = graph
        self.setName(name)
        self.types = [v for v in inspect.getmembers(DataTypes) if v[0] not in ['__doc__', '__module__', 'Reference', 'Exec']]
        self.graph.vars[self.uid] = self

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value
        if self._uid in self.graph.vars:
            self.graph.vars.pop(self._uid)
            self.graph.vars[self._uid] = self

    @staticmethod
    def jsonTemplate():
        template = {
            'name': None,
            'uuid': None,
            'value': None,
            'type': None
        }
        return template

    def serialize(self):
        template = VariableBase.jsonTemplate()
        template['name'] = self.name
        template['uuid'] = str(self.uid)
        template['value'] = self.value
        template['type'] = self.dataType
        return template

    @staticmethod
    def deserialize(data, graph):
        var = graph.parent.variablesWidget.createVariable(uuid.UUID(data['uuid']))
        var.setName(data['name'])
        var.setDataType(data['type'])
        var.value = data['value']
        return var

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, data):
        self._value = data
        self.valueChanged.emit()

    ## Changes variable data type and updates [TypeWidget](@ref PyFlow.Core.Variable.TypeWidget) color
    # @bug in the end of this method we clear undo stack, but we should not. We do this because undo redo goes crazy
    def setDataType(self, dataType, _bJustSpawned=False):
        self.dataType = dataType
        self.widget.color = Pins.findPinClassByType(self.dataType).color()
        self.value = Pins.findPinClassByType(self.dataType).pinDataTypeHint()[1]
        self.widget.update()
        if _bJustSpawned:
            return
        self.dataTypeChanged.emit(self.dataType)
        self.graph.undoStack.clear()

    def mousePressEvent(self, event):
        QWidget.mousePressEvent(self, event)
        self.graph.tryFillPropertiesView(self)
        # self.onUpdatePropertyView(self.graph.parent.formLayout)

    def setName(self, name):
        self.labelName.setText(name)
        self.name = name
        self.nameChanged.emit(str(name))

    def onUpdatePropertyView(self, formLayout):
        # name
        le_name = QLineEdit(self.name)
        le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        formLayout.addRow("Name", le_name)

        # data type
        cbTypes = VarTypeComboBox(self)
        formLayout.addRow("Type", cbTypes)

        # current value
        def valSetter(x):
            self.value = x
        w = InputWidgets.getInputWidget(self.dataType, valSetter, Pins.getPinDefaultValueByType(self.dataType))
        if w:
            w.setWidgetValue(self.value)
            w.setObjectName(self.name)
            formLayout.addRow(self.name, w)

    # def retranslateUi(self, Form):
    #     Form.setWindowTitle(QApplication.translate("Form", "Form", None, QApplication.UnicodeUTF8))
    #     self.labelName.setText(QApplication.translate("Form", "var name", None, QApplication.UnicodeUTF8))
