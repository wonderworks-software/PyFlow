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
import weakref


class PinWidget(QWidget, PinWidget_ui.Ui_Form):
    """doc string for PinWidget"""
    def __init__(self, editor):
        super(PinWidget, self).__init__()
        self.setupUi(self)
        self.editor = weakref.ref(editor)
        self.lePinName.setText('pinName')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.items = [v for v in inspect.getmembers(DataTypes) if v[0] not in ['__doc__', '__module__', 'Reference']]
        self.cbType.clear()

        for i in self.items:
            self.cbType.addItem(i[0], i[1])

    @staticmethod
    def construct(name='pinName', hideLabel=False, dataType=DataTypes.Float, editor=None):
        w = PinWidget(editor)
        w.lePinName.setText(name)

        if hideLabel:
            w.cbHideLabel.setCheckState(QtCore.Qt.Checked)
        else:
            w.cbHideLabel.setCheckState(QtCore.Qt.Unchecked)

        w.cbType.setCurrentIndex(w.cbType.findData(dataType))
        return w

    def shouldHideLabel(self):
        return self.cbHideLabel.isChecked()

    def name(self):
        return self.lePinName.text()

    def dataType(self):
        return getattr(DataTypes, self.cbType.currentText())


class CodeEditor(QWidget, CodeEditor_ui.Ui_CodeEditorWidget):
    def __init__(self, node, uid):
        super(CodeEditor, self).__init__()
        self.setupUi(self)
        self.node = node
        self.uid = uid
        PythonSyntax.PythonHighlighter(self.plainTextEdit.document())
        option = QtGui.QTextOption()
        option.setFlags(option.Flags() | QtGui.QTextOption.ShowTabsAndSpaces)
        self.plainTextEdit.document().setDefaultTextOption(option)
        self.setFontSize(15)
        self.sbFontSize.valueChanged.connect(lambda: self.setFontSize(self.sbFontSize.value()))
        self.pbAddInput.clicked.connect(self.addDefaultInput)
        self.pbAddOutput.clicked.connect(self.addDefaultOutput)
        self.pbSave.clicked.connect(self.applyData)
        self.pbReset.clicked.connect(self.resetUiData)
        self.pbKillSelectedItems.clicked.connect(self.onKillSelectedPins)
        self.resetUiData()
        self.populate()

    def onKillSelectedPins(self):
        for i in self.lwInputs.selectedItems():
            r = self.lwInputs.row(i)
            item = self.lwInputs.takeItem(r)
            del item

        for o in self.lwOutputs.selectedItems():
            r = self.lwOutputs.row(o)
            item = self.lwOutputs.takeItem(r)
            del item

    def closeEvent(self, event):
        event.accept()
        self.node.graph().codeEditors[self.uid].deleteLater()

    def populate(self):
        '''
        populate ui from node
        '''
        for i in self.node.inputs:
            pw = PinWidget.construct(i.name, i.bLabelHidden, i.data_type, self)
            self.appendInput(pw)
        for o in self.node.outputs:
            pw = PinWidget.construct(o.name, o.bLabelHidden, o.data_type, self)
            self.appendOutput(pw)
        self.leLabel.setText(self.node.label().toPlainText())
        self.plainTextEdit.setPlainText(self.node.currentCode)

    def resetUiData(self):
        self.lwInputs.clear()
        self.lwOutputs.clear()
        self.plainTextEdit.setPlainText("def compute(self):\n\tprint('Hello')")

    def resetNode(self):
        self.node.bKillEditor = False
        edUid = self.node.editorUUID
        self.node = Node.recreate(self.node)
        self.node.editorUUID = edUid

    def applyData(self):
        # recreate node
        self.resetNode()

        # label
        lbText = self.leLabel.text()
        if not lbText == '':
            self.node.label().setPlainText(lbText)

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

        self.node.currentCode = code

    def appendInput(self, pw):
        item = QListWidgetItem(self.lwInputs)
        item.setSizeHint(QtCore.QSize(pw.sizeHint().width(), 80))
        self.lwInputs.addItem(item)
        self.lwInputs.setItemWidget(item, pw)
        del item

    def appendOutput(self, pw):
        item = QListWidgetItem(self.lwOutputs)
        item.setSizeHint(QtCore.QSize(pw.sizeHint().width(), 80))
        self.lwOutputs.addItem(item)
        self.lwOutputs.setItemWidget(item, pw)
        del item

    def addDefaultInput(self):
        w = PinWidget(self)
        self.appendInput(w)

    def addDefaultOutput(self):
        w = PinWidget(self)
        self.appendOutput(w)

    def setFontSize(self, size):
        f = self.plainTextEdit.font()
        size = abs(size)
        f.setPointSize(size)
        self.plainTextEdit.setTabStopWidth(size)
        self.plainTextEdit.setFont(f)
        option = self.plainTextEdit.document().defaultTextOption()
        option.setTabStop(size)
        self.plainTextEdit.document().setDefaultTextOption(option)
