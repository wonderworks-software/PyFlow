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
from types import MethodType
from Node import Node


class PinWidget(QWidget, PinWidget_ui.Ui_Form):
    """doc string for PinWidget"""
    def __init__(self):
        super(PinWidget, self).__init__()
        self.setupUi(self)
        self.lePinName.setText('pinName')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.items = [v for v in inspect.getmembers(DataTypes) if v[0] not in ['__doc__', '__module__', 'Reference']]
        self.cbType.clear()

        for i in self.items:
            self.cbType.addItem(i[0], i[1])

    @staticmethod
    def construct(name='pinName', hideLabel=False, dataType=DataTypes.Float):
        w = PinWidget()
        w.lePinName.setText(name)

        if hideLabel:
            w.cbHideLabel.setCheckState(QtCore.Qt.Checked)
        else:
            w.cbHideLabel.setCheckState(QtCore.Qt.Unchecked)

        w.cbType.setCurrentIndex(w.cbType.findData(dataType))

    def shouldHideLabel(self):
        return self.cbHideLabel.isChecked()

    def name(self):
        return self.lePinName.text()

    def dataType(self):
        return getattr(DataTypes, self.cbType.currentText())


class CodeEditor(QWidget, CodeEditor_ui.Ui_Form):
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
        self.pbReset.clicked.connect(self.resetUiData)
        self.resetUiData()

    def resetUiData(self):
        self.lwInputs.clear()
        self.lwOutputs.clear()
        self.plainTextEdit.setPlainText("def compute(self):\n    print('Hello')")

    def resetNode(self):
        self.node.bKillEditor = False
        edUid = self.node.editorUUID
        self.node = Node.recreate(self.node)
        self.node.editorUUID = edUid

    def applyData(self):
        # recreate node
        self.resetNode()

        # assign compute method
        code = self.plainTextEdit.toPlainText()
        code = code.replace('\t', '    ')
        exec(code)
        self.node.compute = MethodType(compute, self.node, Node)

        for index in range(self.lwOutputs.count()):
            w = self.lwOutputs.itemWidget(self.lwOutputs.item(index))
            if isinstance(w, PinWidget):
                self.node.add_output_port(w.name(), w.dataType(), None, w.shouldHideLabel())

        # recreate pins from editor data
        for index in range(self.lwInputs.count()):
            w = self.lwInputs.itemWidget(self.lwInputs.item(index))
            if isinstance(w, PinWidget):
                if w.dataType() == DataTypes.Exec:
                    self.node.add_input_port(w.name(), w.dataType(), self.node.compute, w.shouldHideLabel())
                else:
                    self.node.add_input_port(w.name(), w.dataType(), None, w.shouldHideLabel())

        for i in self.node.inputs:
            for o in self.node.outputs:
                portAffects(i, o)


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
