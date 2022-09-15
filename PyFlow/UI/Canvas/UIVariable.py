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

from PyFlow import getHashableDataTypes
from PyFlow.Core.Common import *
from PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.UI.UIInterfaces import IPropertiesViewSupport
from PyFlow.UI.Widgets.InputWidgets import createInputWidget
from PyFlow.UI.Widgets.PropertiesFramework import PropertiesWidget, CollapsibleFormWidget
from PyFlow import getPinDefaultValueByType
from PyFlow.UI.Widgets.EnumComboBox import EnumComboBox
from PyFlow import findPinClassByType
from PyFlow import getAllPinClasses


# Colored rounded rect
# color corresponds to pin data type color
class TypeWidget(QWidget):
    def __init__(self, keyColor, valueColor, parent=None):
        super(TypeWidget, self).__init__(parent=parent)
        self.keyColor = keyColor
        self.valueColor = valueColor
        self.setMinimumWidth(24)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)

        keyColor = QtGui.QColor.fromRgb(*findPinClassByType(self.parent().dataType).color())

        structure = self.parent()._rawVariable.structure
        if structure == StructureType.Single:
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            pen = QtGui.QPen()
            pen.setColor(QtGui.QColor(0, 0, 0, 0))
            painter.setPen(pen)
            rect = event.rect()
            rect.setHeight(10)
            rect.setWidth(15)
            rect.moveTop(3)
            painter.setBrush(keyColor)
            painter.drawRoundedRect(rect, 5, 5)

        if structure == StructureType.Array:
            gridSize = 3
            size = self.height()
            cellW = size / gridSize
            cellH = size / gridSize

            painter.setBrush(QtGui.QBrush(keyColor))
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 0.2))
            for row in range(gridSize):
                for column in range(gridSize):
                    x = row * cellW
                    y = column * cellH
                    painter.drawRect(x, y, cellW, cellH)

        if structure == StructureType.Dict:
            dictObject = self.parent()._rawVariable.value

            keyColor = QtGui.QColor.fromRgb(*findPinClassByType(dictObject.keyType).color())
            valueColor = QtGui.QColor.fromRgb(*findPinClassByType(dictObject.valueType).color())

            gridSize = 3
            size = self.height()
            cellW = size / gridSize
            cellH = size / gridSize

            painter.setBrush(QtGui.QBrush(keyColor))
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 0.2))
            for row in range(gridSize):
                painter.setBrush(keyColor)
                painter.drawRect(0, row * cellH, cellW, cellH)
                painter.setBrush(valueColor)
                painter.drawRect(cellW, row * cellH, cellW * 2, cellH)

        painter.end()


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
        self.labelName.setStyleSheet("background:transparent")
        self.labelName.setObjectName("labelName")
        self.horizontalLayout.addWidget(self.labelName)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        # find refs
        self.pbFindRefs = QPushButton("")
        self.pbFindRefs.setIcon(QtGui.QIcon(":/searching-magnifying-glass.png"))
        self.pbFindRefs.setObjectName("pbFindRefs")
        self.horizontalLayout.addWidget(self.pbFindRefs)
        self.pbFindRefs.clicked.connect(self.onFindRefsClicked)
        #  kill variable
        self.pbKill = QPushButton("")
        self.pbKill.setIcon(QtGui.QIcon(":/delete_icon.png"))
        self.pbKill.setObjectName("pbKill")
        self.horizontalLayout.addWidget(self.pbKill)
        self.pbKill.clicked.connect(self.onKillClicked)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.setName(self._rawVariable.name)
        self._rawVariable.setWrapper(self)

    def onStructureChanged(self, name):
        self._rawVariable.structure = StructureType[name]
        self.variablesWidget.pyFlowInstance.onRequestFillProperties(self.createPropertiesWidget)
        EditorHistory().saveState("Change variable struct", modify=True)
        self.widget.update()

    def setDataType(self, dataType):
        self.dataType = dataType
        self._rawVariable.dataType = dataType
        EditorHistory().saveState("Change variable data type", modify=True)

    def onDictKeyTypeChanged(self, newType):
        dictObject = self._rawVariable.value
        dictObject.keyType = newType
        self.widget.update()

    def onDictValueTypeChanged(self, newType):
        dictObject = self._rawVariable.value
        dictObject.valueType = newType
        self.widget.update()

    def createPropertiesWidget(self, propertiesWidget):
        baseCategory = CollapsibleFormWidget(headName="Base")
        # name
        le_name = QLineEdit(self._rawVariable.name)
        le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        baseCategory.addWidget("Name", le_name)

        # data type
        if self._rawVariable.structure == StructureType.Dict:
            dictObject = self._rawVariable.value
            keyTypeSelector = EnumComboBox(values=getHashableDataTypes())
            valueTypeSelector = EnumComboBox([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin() if pin.__name__ != "AnyPin"])

            keyTypeSelector.setEditable(False)
            valueTypeSelector.setEditable(False)

            keyTypeSelector.setCurrentIndex(keyTypeSelector.findText(dictObject.keyType))
            valueTypeSelector.setCurrentIndex(valueTypeSelector.findText(dictObject.valueType))

            keyTypeSelector.changeCallback.connect(self.onDictKeyTypeChanged)
            valueTypeSelector.changeCallback.connect(self.onDictValueTypeChanged)

            baseCategory.addWidget("Key type", keyTypeSelector)
            baseCategory.addWidget("Value type", valueTypeSelector)
        else:
            cbTypes = EnumComboBox([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin() if pin.__name__ != "AnyPin"])
            cbTypes.setCurrentIndex(cbTypes.findText(self.dataType))
            cbTypes.changeCallback.connect(self.setDataType)
            cbTypes.setEditable(False)
            baseCategory.addWidget("Type", cbTypes)
        propertiesWidget.addWidget(baseCategory)

        # structure type
        cbStructure = EnumComboBox([i.name for i in (StructureType.Single, StructureType.Array, StructureType.Dict)])
        cbStructure.setEditable(False)
        cbStructure.setCurrentIndex(cbStructure.findText(self._rawVariable.structure.name))
        cbStructure.changeCallback.connect(self.onStructureChanged)
        propertiesWidget.addWidget(baseCategory)
        baseCategory.addWidget("Structure", cbStructure)

        valueCategory = CollapsibleFormWidget(headName="Value")

        # current value
        if self._rawVariable.structure == StructureType.Single:
            if not type(self._rawVariable.value) in {list, set, dict, tuple}:
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
            EditorHistory().saveState("Change variable access level", modify=True)
        cb.currentTextChanged.connect(accessLevelChanged)
        cb.setCurrentIndex(self._rawVariable.accessLevel)
        valueCategory.addWidget('Access level', cb)
        propertiesWidget.addWidget(valueCategory)

    def onFindRefsClicked(self):
        from PyFlow.App import PyFlow
        refs = [n.getWrapper() for n in self._rawVariable.findRefs()]
        app = self.variablesWidget.pyFlowInstance
        if "Search results" not in [t.name() for t in app.getRegisteredTools()]:
            app.invokeDockToolByName("PyFlowBase", "Search results")
        self.variablesWidget.pyFlowInstance.getCanvas().requestShowSearchResults.emit(refs)

    def onKillClicked(self):
        # check refs and ask user what to do
        refs = self._rawVariable.findRefs()
        if len(refs) > 0:
            item, accepted = QInputDialog.getItem(None, 'Decide!', 'What to do with getters and setters in canvas?', ['kill', 'leave'], editable=False)
            if accepted:
                self.variablesWidget.killVar(self)
                if item == 'kill':
                    for i in refs:
                        i.kill()
                elif item == 'leave':
                    for i in refs:
                        i.var = None
        else:
            self.variablesWidget.killVar(self)

    @property
    def dataType(self):
        return self._rawVariable.dataType

    @ dataType.setter
    def dataType(self, value):
        self._rawVariable.dataType = value
        self.widget.color = findPinClassByType(self._rawVariable.dataType).color()
        self.widget.update()
        self.variablesWidget.onUpdatePropertyView(self)

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
        if self._rawVariable.uid in self.graph.getVars():
            self.graph.getVars().pop(self._rawVariable.uid)
            self.graph.getVars()[self._rawVariable.uid] = self._rawVariable

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
            template['value'] = json.dumps(self._rawVariable.value, cls=pinClass.jsonEncoderClass())

        template['type'] = self._rawVariable.dataType
        template['package'] = self._rawVariable.packageName
        template['accessLevel'] = self._rawVariable.accessLevel.value
        return template

    @staticmethod
    def deserialize(data, graph):
        pinClass = findPinClassByType(data['dataType'])

        varUid = uuid.UUID(data['uuid'])
        var = graph.getApp().variablesWidget.createVariable(
            dataType=data['dataType'], accessLevel=AccessLevel(data['accessLevel']), uid=varUid)
        var.setName(data['name'])
        var.setDataType(data['dataType'])

        if data['dataType'] == 'AnyPin':
            var.value = getPinDefaultValueByType('AnyPin')
        else:
            var.value = json.loads(data['value'], cls=pinClass.jsonDecoderClass())

        return var

    @property
    def value(self):
        return self._rawVariable.value

    @value.setter
    def value(self, data):
        self._rawVariable.value = data

    def mousePressEvent(self, event):
        super(UIVariable, self).mousePressEvent(event)
        self.variablesWidget.onUpdatePropertyView(self)

    def setName(self, name):
        self._rawVariable.name = name
        self.labelName.setText(self._rawVariable.name)
