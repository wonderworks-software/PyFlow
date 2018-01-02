import weakref
from Qt import QtCore
from Qt import QtGui
import ArrayInputWidget_ui
from Qt.QtWidgets import QDoubleSpinBox
from Qt.QtWidgets import QSpinBox
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QListWidgetItem
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QGraphicsProxyWidget
from AGraphCommon import DataTypes
from AGraphCommon import push
import Variable


class VarInputWidgetBase(object):
    """doc string for VarInputWidgetBase"""

    def __init__(self, var, **kwds):
        super(VarInputWidgetBase, self).__init__(**kwds)
        if not isinstance(var, Variable.VariableBase):
            raise TypeError("[ERROR] VariableBase expected, got {0}".format(type(var)))
        self.var = weakref.ref(var)
        self.varDataUpdated(self.var().value)

    def kill(self):
        pass

    def postCreate(self, data):
        pass

    def widgetValueUpdated(self, value):
        # update var
        self.var().value = value

    def varDataUpdated(self, data):
        # update widget
        pass


class FloatInputWidget(VarInputWidgetBase, QDoubleSpinBox):
    """doc string for FloatInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(FloatInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(-2147483648.01, 2147483647.01)
        self.setSingleStep(0.01)
        self.setMaximumWidth(70)
        self.setDecimals(20)
        self.valueChanged.connect(self.widgetValueUpdated)

    def varDataUpdated(self, data):
        self.setValue(float(data))


class IntInputWidget(VarInputWidgetBase, QSpinBox):
    """doc string for IntInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(IntInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setRange(-2147483648, 2147483647)
        self.setMaximumWidth(70)
        self.valueChanged.connect(self.widgetValueUpdated)

    def varDataUpdated(self, data):
        self.setValue(int(data))


class StringInputWidget(VarInputWidgetBase, QLineEdit):
    """doc string for StringInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(StringInputWidget, self).__init__(**kwds)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.textChanged.connect(self.widgetValueUpdated)
        self.setMaximumWidth(70)

    def varDataUpdated(self, data):
        self.setText(str(data))


class BoolInputWidget(VarInputWidgetBase, QCheckBox):
    """doc string for BoolInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(BoolInputWidget, self).__init__(**kwds)
        self.stateChanged.connect(self.widgetValueUpdated)

    def varDataUpdated(self, data):
        if bool(data):
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)


class ArrayInputWidget(VarInputWidgetBase, QCheckBox):
    """doc string for BoolInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(BoolInputWidget, self).__init__(**kwds)
        self.stateChanged.connect(self.widgetValueUpdated)

    def varDataUpdated(self, data):
        if bool(data):
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)


class _ArrayIniputWidget(QWidget):
    """docstring for _ArrayIniputWidget"""
    def __init__(self, data, parent=None):
        super(_ArrayIniputWidget, self).__init__(parent)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QLineEdit(self, data)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QPushButton(self)
        self.pushButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText('x')
        self.horizontalLayout.addWidget(self.pushButton)


class ArrayInputWidget(VarInputWidgetBase, QWidget, ArrayInputWidget_ui.Ui_Form):
    """docstring for ArrayInputWidget"""
    def __init__(self, parent=None, **kwds):
        super(ArrayInputWidget, self).__init__(**kwds)
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.onAddElement(None, True))
        self.index = 0
        self.data = {}

    def setElementData(self, index, data):
        self.var().value[index] = data

    def onAddElement(self, data=None, bAddToVarList=True):
        arrInputWidget = _ArrayIniputWidget(data)
        index = self.index
        arrInputWidget.lineEdit.editingFinished.connect(lambda: self.setElementData(index, arrInputWidget.lineEdit.text()))
        self.data[self.index] = arrInputWidget
        arrInputWidget.label.setText(str(self.index))
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(arrInputWidget.sizeHint().width(), 40))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, arrInputWidget)
        del item
        if bAddToVarList:
            self.var().value.append(data)
        self.index += 1
        return arrInputWidget

    def postCreate(self, data):
        # populate widget from var data
        for index in range(len(data)):
            arrInputWidget = _ArrayIniputWidget(data[index])
            arrInputWidget.lineEdit.editingFinished.connect(lambda: self.setElementData(index, arrInputWidget.lineEdit.text()))
            arrInputWidget.label.setText(str(index))
            arrInputWidget.lineEdit.setText(str(self.var().value[index]))
            item = QListWidgetItem(self.listWidget)
            item.setSizeHint(QtCore.QSize(arrInputWidget.sizeHint().width(), 40))
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, arrInputWidget)
            del item


def getVarWidget(var):
    '''
    fabric method
    '''
    if not isinstance(var, Variable.VariableBase):
        raise TypeError("[ERROR] VariableBase expected, got {0}".format(type(var)))
    if var.dataType == DataTypes.Float:
        return FloatInputWidget(var=var)
    if var.dataType == DataTypes.Int:
        return IntInputWidget(var=var)
    if var.dataType == DataTypes.String:
        return StringInputWidget(var=var)
    if var.dataType == DataTypes.Bool:
        return BoolInputWidget(var=var)
    if var.dataType == DataTypes.Array:
        return ArrayInputWidget(var=var)
    if var.dataType == DataTypes.Any:
        return StringInputWidget(var=var)
    return None
