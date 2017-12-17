from Qt import QtGui
from Qt import QtCore
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QListWidgetItem
from Qt.QtWidgets import QSizePolicy
import CodeEditor_ui
import PythonSyntax
import PinWidget_ui
from AbstractGraph import *
import inspect


class PinWidget(QWidget, PinWidget_ui.Ui_Form):
    """doc string for PinWidget"""
    def __init__(self):
        super(PinWidget, self).__init__()
        self.setupUi(self)
        self.lePinName.setText('pinName')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.items = [v for v in inspect.getmembers(DataTypes) if v[0] not in ['__doc__', '__module__', 'Reference']]
        self.cbType.clear()
        self.cbType.addItems([i[0] for i in self.items])

    def name(self):
        return self.lePinName.text()

    def dataType(self):
        return getattr(DataTypes, self.cbType.currentText())


class CodeEditor(QWidget, CodeEditor_ui.Ui_Form):
    """
    add pin
    reomve pin
    change pin type
    restore editor from node
    update node on editor change data
    """
    def __init__(self, node):
        super(CodeEditor, self).__init__()
        self.setupUi(self)
        self.node = node
        PythonSyntax.PythonHighlighter(self.plainTextEdit.document())
        option = QtGui.QTextOption()
        option.setFlags(QtGui.QTextOption.ShowTabsAndSpaces)
        self.plainTextEdit.document().setDefaultTextOption(option)
        self.plainTextEdit.setTabStopWidth(15)
        self.sbFontSize.valueChanged.connect(lambda: self.setFontSize(self.sbFontSize.value()))
        self.pbAddInput.clicked.connect(self.addInput)
        self.pbAddOutput.clicked.connect(self.addOutput)
        self.pbSave.clicked.connect(self.applyData)
        self.plainTextEdit.setPlainText("def compute(self):\n    pass")

    def resetNode(self):
        for pinName in [i.name for i in self.node.inputs] + [o for o in self.node.outputs]:
            self.node.removePort(pinName)

    def applyData(self):
        self.resetNode()
        code = self.plainTextEdit.toPlainText()
        code = code.replace('\t', '    ')
        for index in range(self.lwInputs.count()):
            w = self.lwInputs.itemWidget(self.lwInputs.item(index))
            if isinstance(w, PinWidget):
                self.node.add_input_port(w.name(), w.dataType())

        for index in range(self.lwOutputs.count()):
            w = self.lwOutputs.itemWidget(self.lwOutputs.item(index))
            if isinstance(w, PinWidget):
                self.node.add_output_port(w.name(), w.dataType())

    def addInput(self):
        w = PinWidget()
        item = QListWidgetItem(self.lwInputs)
        item.setSizeHint(QtCore.QSize(w.sizeHint().width(), 40))
        self.lwInputs.addItem(item)
        self.lwInputs.setItemWidget(item, w)
        del item

    def addOutput(self):
        w = PinWidget()
        item = QListWidgetItem(self.lwOutputs)
        item.setSizeHint(QtCore.QSize(w.sizeHint().width(), 40))
        self.lwOutputs.addItem(item)
        self.lwOutputs.setItemWidget(item, w)
        del item

    def setFontSize(self, size):
        f = self.plainTextEdit.font()
        f.setPointSize(abs(size))
        self.plainTextEdit.setFont(f)
