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
    def __init__(self, color, parent=None):
        super(TypeWidget, self).__init__()
        self.color = color
        self.setMinimumWidth(24)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QColor.fromRgb(*self.color))
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(0, 0, 0, 0))
        painter.setPen(pen)
        rect = event.rect()
        rect.setHeight(10)
        rect.setWidth(15)
        rect.moveTop(3)
        painter.drawRoundedRect(rect, 5, 5)

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
        self._rawVariable.structure = PinStructure[name]
        self.variablesWidget.pyFlowInstance.onRequestFillProperties(self.createPropertiesWidget)
        EditorHistory().saveState("Change variable struct")

    def setDataType(self, dataType):
        self.dataType = dataType
        EditorHistory().saveState("Change variable data type")

    def createPropertiesWidget(self, propertiesWidget):
        baseCategory = CollapsibleFormWidget(headName="Base")
        # name
        le_name = QLineEdit(self._rawVariable.name)
        le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        baseCategory.addWidget("Name", le_name)

        # data type
        cbTypes = EnumComboBox([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin() if pin.__name__ != "AnyPin"])
        cbTypes.setCurrentIndex(cbTypes.findText(self.dataType))
        cbTypes.setEditable(False)
        cbTypes.changeCallback.connect(self.setDataType)
        propertiesWidget.addWidget(baseCategory)

        # structure type
        cbStructure = EnumComboBox([i.name for i in (PinStructure.Single, PinStructure.Array)])
        cbStructure.setEditable(False)
        cbStructure.setCurrentIndex(cbStructure.findText(self._rawVariable.structure.name))
        cbStructure.changeCallback.connect(self.onStructureChanged)
        propertiesWidget.addWidget(baseCategory)
        baseCategory.addWidget("Type", cbTypes)
        baseCategory.addWidget("Structure", cbStructure)

        valueCategory = CollapsibleFormWidget(headName="Value")

        # current value
        if self._rawVariable.structure == PinStructure.Single:
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
            EditorHistory().saveState("Change variable access level")
        cb.currentTextChanged.connect(accessLevelChanged)
        cb.setCurrentIndex(self._rawVariable.accessLevel)
        valueCategory.addWidget('Access level', cb)
        propertiesWidget.addWidget(valueCategory)

    def onFindRefsClicked(self):
        from PyFlow.App import PyFlow
        refs = [n.getWrapper() for n in self._rawVariable.findRefs()]
        app = PyFlow.instance()
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
