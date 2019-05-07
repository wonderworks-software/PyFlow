"""@file Variable.py

Variable related classes.
"""
import json

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QComboBox
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QSpacerItem
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QInputDialog

from PyFlow.Core.Common import *
from PyFlow.UI.UIInterfaces import IPropertiesViewSupport
from PyFlow.UI.Widgets.InputWidgets import createInputWidget
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Widgets.PropertiesFramework import PropertiesWidget, CollapsibleFormWidget
from PyFlow import getPinDefaultValueByType
from PyFlow import findPinClassByType
from PyFlow import getAllPinClasses


# Colored rounded rect
# color corresponds to pin data type color
class TypeWidget(QWidget):
    def __init__(self, color, parent=None):
        super(TypeWidget, self).__init__()
        self.color = color
        self.setMinimumWidth(24)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)

        painter.setBrush(QtGui.QColor.fromRgb(*self.color))
        rect = event.rect()
        rect.setHeight(10)
        rect.setWidth(20)
        rect.moveTop(12)
        painter.drawRoundedRect(rect, 5, 5)

        painter.end()


# Changes type of variable
class VarTypeComboBox(QComboBox):
    def __init__(self, var, parent=None):
        super(VarTypeComboBox, self).__init__(parent)
        self._bJustSpawned = True
        self.var = var
        self.types = [pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin()]
        for i in self.types:
            self.addItem(i)
        self.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.setCurrentIndex(self.findText(var.dataType))
        self._bJustSpawned = False

    def onCurrentIndexChanged(self, index):
        if self._bJustSpawned:
            val = self.var.value

        self.var.setDataType(self.itemText(index), self._bJustSpawned)

        if self._bJustSpawned:
            self.var.value = val


# Variable class
class UIVariable(QWidget, IPropertiesViewSupport):
    def __init__(self, rawVariable, variablesWidget, parent=None):
        super(UIVariable, self).__init__(parent)
        self._rawVariable = rawVariable
        self.variablesWidget = variablesWidget

        # ui
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = TypeWidget(findPinClassByType(self._rawVariable.dataType).color(), self)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.labelName = QLabel(self)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout.addWidget(self.labelName)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        # find refs
        self.pbFindRefs = QPushButton("")
        self.pbFindRefs.setIcon(QtGui.QIcon(RESOURCES_DIR + "/searching-magnifying-glass.png"))
        self.pbFindRefs.setObjectName("pbFindRefs")
        self.horizontalLayout.addWidget(self.pbFindRefs)
        self.pbFindRefs.clicked.connect(self.onFindRefsClicked)
        #  kill variable
        self.pbKill = QPushButton("")
        self.pbKill.setIcon(QtGui.QIcon(RESOURCES_DIR + "/delete_icon.png"))
        self.pbKill.setObjectName("pbKill")
        self.horizontalLayout.addWidget(self.pbKill)
        self.pbKill.clicked.connect(self.onKillClicked)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.setName(self._rawVariable.name)

    def createPropertiesWidget(self, propertiesWidget):
        baseCategory = CollapsibleFormWidget(headName="Base")
        # name
        le_name = QLineEdit(self._rawVariable.name)
        le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        baseCategory.addWidget("Name", le_name)

        # data type
        cbTypes = VarTypeComboBox(self)
        baseCategory.addWidget("Type", cbTypes)
        propertiesWidget.addWidget(baseCategory)

        valueCategory = CollapsibleFormWidget(headName="Value")

        # current value
        def valSetter(x):
            self._rawVariable.value = x
        w = createInputWidget(self._rawVariable.dataType, valSetter, getPinDefaultValueByType(self._rawVariable.dataType))
        if w:
            w.setWidgetValue(self._rawVariable.value)
            w.setObjectName(self._rawVariable.name)
            valueCategory.addWidget(self._rawVariable.name, w)

        # access level
        cb = QComboBox()
        cb.addItem('public', 0)
        cb.addItem('private', 1)
        cb.addItem('protected', 2)

        def accessLevelChanged(x):
            self._rawVariable.accessLevel = AccessLevel[x]
        cb.currentTextChanged.connect(accessLevelChanged)
        cb.setCurrentIndex(self._rawVariable.accessLevel)
        valueCategory.addWidget('Access level', cb)
        propertiesWidget.addWidget(valueCategory)

    def onFindRefsClicked(self):
        refs = self._rawVariable.findRefs()
        print(refs)

    def onKillClicked(self):
        # check refs and ask user what to do
        refs = self._rawVariable.findRefs()
        if len(refs) > 0:
            item, accepted = QInputDialog.getItem(None, 'Decide!', 'What to do with getters and setters in canvas?', ['kill', 'leave'], editable=False)
            if accepted:
                if item == 'kill':
                    self.variablesWidget.killVar(self)
                elif item == 'leave':
                    # mark node as invalid
                    # TODO: For future. Like in ue4, if variable is removed, it can be recreated from node (e.g. promote to variable)
                    print('leave')
        else:
            self.variablesWidget.killVar(self)

    @property
    def dataType(self):
        return self._rawVariable.dataType

    @ dataType.setter
    def dataType(self, value):
        self._rawVariable.dataType = value

    @property
    def packageName(self):
        return self._rawVariable.packageName

    @property
    def accessLevel(self):
        return self._rawVariable.accessLevel

    @accessLevel.setter
    def accessLevel(self, value):
        self._rawVariable.accessLevel = value

    @property
    def uid(self):
        return self._rawVariable.uid

    @uid.setter
    def uid(self, value):
        self._rawVariable.uid = value
        if self._rawVariable.uid in self.graph.vars:
            self.graph.vars.pop(self._rawVariable.uid)
            self.graph.vars[self._rawVariable.uid] = self._rawVariable

    @staticmethod
    def jsonTemplate():
        template = {
            'name': None,
            'uuid': None,
            'value': None,
            'type': None,
            'package': None,
            'accessLevel': None
        }
        return template

    def serialize(self):
        pinClass = findPinClassByType(self._rawVariable.dataType)

        template = UIVariable.jsonTemplate()
        template['name'] = self._rawVariable.name
        template['uuid'] = str(self._rawVariable.uid)

        if self._rawVariable.dataType == "AnyPin":
            # don't save any variables
            # value will be calculated for this type of variables
            template['value'] = None
        else:
            template['value'] = json.dumps(self._rawVariable.value, cls=pinClass.jsonEncoderClass(
            )) if not pinClass.isPrimitiveType() else self._rawVariable.value

        template['type'] = self._rawVariable.dataType
        template['package'] = self._rawVariable.packageName
        template['accessLevel'] = self._rawVariable.accessLevel.value
        return template

    @staticmethod
    def deserialize(data, graph):
        pinClass = findPinClassByType(data['dataType'])

        varUid = uuid.UUID(data['uuid'])
        # TODO: this is probably bad. Too long call chain
        var = graph.parent.variablesWidget.createVariable(
            dataType=data['dataType'], accessLevel=AccessLevel(data['accessLevel']), uid=varUid)
        var.setName(data['name'])
        var.setDataType(data['dataType'])

        if data['dataType'] == 'AnyPin':
            var.value = getPinDefaultValueByType('AnyPin')
        else:
            var.value = data['value'] if pinClass.isPrimitiveType() else json.loads(
                data['value'], cls=pinClass.jsonDecoderClass())

        return var

    @property
    def value(self):
        return self._rawVariable.value

    @value.setter
    def value(self, data):
        self._rawVariable.value = data

    # Changes variable data type and updates [TypeWidget](@ref PyFlow.Core.Variable.TypeWidget) color
    # @bug in the end of this method we clear undo stack, but we should not. We do this because undo redo goes crazy
    def setDataType(self, dataType, _bJustSpawned=False):
        self._rawVariable.dataType = dataType
        self.widget.color = findPinClassByType(self.dataType).color()
        self.widget.update()
        if _bJustSpawned:
            return
        self.variablesWidget.onUpdatePropertyView(self)

    def mousePressEvent(self, event):
        super(UIVariable, self).mousePressEvent(event)
        self.variablesWidget.onUpdatePropertyView(self)

    def setName(self, name):
        self._rawVariable.name = name
        self.labelName.setText(self._rawVariable.name)
