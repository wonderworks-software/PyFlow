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
import nodes_res_rc
from uuid import uuid4
import inspect
from Pin import Pin
from Pin import getPortColorByType
from AbstractGraph import *


class TypeWidget(QWidget):
    """docstring for TypeWidget"""
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


class VarTypeComboBox(QComboBox):
    """docstring for VarTypeComboBox"""
    def __init__(self, var, parent=None):
        super(VarTypeComboBox, self).__init__(parent)
        self.var = var
        for i in self.var.types:
            self.addItem(i[0], i[1])
        self.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.setCurrentIndex(self.findData(var.dataType))

    def onCurrentIndexChanged(self, index):
        self.var.setDataType(self.itemData(index))


class VariableBase(QWidget):
    """docstring for VariableBase"""
    def __init__(self, name, value, graph, varsListWidget, dataType=DataTypes.Any):
        super(VariableBase, self).__init__()
        # ui
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = TypeWidget(getPortColorByType(dataType), self)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.labelName = QLabel(self)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout.addWidget(self.labelName)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        # body
        self.varsListWidget = varsListWidget
        self.name = None
        self.value = value
        self.dataType = dataType
        self.uid = uuid4()
        self.graph = graph
        self.setName(name)
        self.types = [v for v in inspect.getmembers(DataTypes) if v[0] not in ['__doc__', '__module__', 'Reference', 'Exec']]

    def setDataType(self, dataType):
        self.dataType = dataType
        self.value = PinBase.getDefaultDataValue(self.dataType)
        self.widget.color = getPortColorByType(dataType)
        self.widget.update()

    def mousePressEvent(self, event):
        QWidget.mousePressEvent(self, event)
        self.onUpdatePropertyView(self.graph.parent.formLayout)

    def setName(self, name):
        self.labelName.setText(name)
        self.name = name

    def onUpdatePropertyView(self, formLayout):
        clearLayout(formLayout)

        # name
        le_name = QLineEdit(self.name)
        le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        formLayout.addRow("Name", le_name)

        # data type
        cbTypes = VarTypeComboBox(self)
        formLayout.addRow("Type", cbTypes)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, QApplication.UnicodeUTF8))
        self.labelName.setText(QApplication.translate("Form", "var name", None, QApplication.UnicodeUTF8))