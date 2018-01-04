from Qt import QtGui
from Qt import QtCore
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QListWidgetItem
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QCompleter
from Qt.QtWidgets import QPlainTextEdit
import CodeEditor_ui
import PythonSyntax
import PinWidget_ui
from AbstractGraph import *
import inspect
from types import MethodType
from Node import Node
import weakref
from keyword import kwlist


class CompletionTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CompletionTextEdit, self).__init__(parent)
        self.setMinimumWidth(400)
        wordList = kwlist + ['setData(', 'getData()', 'currentData()', 'dataType', 'setClean()', 'setDirty()', 'setDirty()']
        self.completer = QCompleter(wordList, self)
        self.moveCursor(QtGui.QTextCursor.End)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.setFont(font)
        self.setCompleter(self.completer)

    def setCompleter(self, completer):
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion.replace(self.completer.completionPrefix(), ''))
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab):
                event.ignore()
                return

        # has ctrl-space been pressed??
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and
                      event.key() == QtCore.Qt.Key_Space)
        if (not self.completer or not isShortcut):
            QPlainTextEdit.keyPressEvent(self, event)

        # ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier, QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text() == '':
            # ctrl or shift key on it's own
            return

        # end of word
        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        if (not isShortcut and (hasModifier or event.text() == '' or len(completionPrefix) < 3 or event.text()[:-1] in eow)):
            self.completer.popup().hide()
            return

        if (completionPrefix != self.completer.completionPrefix()):
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        # popup it up!
        self.completer.complete(cr)


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
    def __init__(self, graph, node, uid):
        super(CodeEditor, self).__init__()
        self.setupUi(self)
        self.graph = graph
        self.nodeUid = node.uid
        self.uid = uid

        # insert code editor
        self.plainTextEdit = CompletionTextEdit(self.tabCode)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        PythonSyntax.PythonHighlighter(self.plainTextEdit.document())
        option = QtGui.QTextOption()
        option.setFlags(option.Flags() | QtGui.QTextOption.ShowTabsAndSpaces)
        self.plainTextEdit.document().setDefaultTextOption(option)
        self.setFontSize(10)

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
        try:
            ed = self.graph().codeEditors.pop(self.uid)
            ed.deleteLater()
        except:
            pass

    def populate(self):
        '''
        populate ui from node
        '''
        node = self.graph.nodes[self.nodeUid]
        for i in node.inputs.values():
            pw = PinWidget.construct(i.name, i.bLabelHidden, i.dataType, self)
            self.appendInput(pw)
        for o in node.outputs.values():
            pw = PinWidget.construct(o.name, o.bLabelHidden, o.dataType, self)
            self.appendOutput(pw)
        self.leLabel.setText(node.label().toPlainText())
        code = ""
        for line in node.currentComputeCode:
            code += line
        self.plainTextEdit.setPlainText(code)

    def resetUiData(self):
        self.lwInputs.clear()
        self.lwOutputs.clear()

    def resetNode(self):
        node = self.graph.nodes[self.nodeUid]
        for i in node.inputs.values():
            i.kill()
        for o in node.outputs.values():
            o.kill()
        node.inputs.clear()
        node.outputs.clear()

        for i in range(node.inputsLayout.count()):
            node.inputsLayout.removeAt(0)
        for i in range(node.outputsLayout.count()):
            node.outputsLayout.removeAt(0)

    @staticmethod
    def wrapCodeToFunction(fooName, code):
        foo = "def {}(self):".format(fooName)
        lines = [i for i in code.split('\n') if len(i) > 0]
        for line in lines:
            foo += '\n\t{}'.format(line)
        return foo

    def applyData(self):
        # reset node
        self.resetNode()
        node = self.graph.nodes[self.nodeUid]

        # label
        lbText = self.leLabel.text()
        if not lbText == '':
            node.label().setPlainText(lbText)
            node.name = lbText

        # assign compute method
        code = self.plainTextEdit.toPlainText()
        foo = CodeEditor.wrapCodeToFunction('compute', code)
        exec(foo)
        node.compute = MethodType(compute, node, Node)
        node.currentComputeCode = code

        for index in range(self.lwOutputs.count()):
            w = self.lwOutputs.itemWidget(self.lwOutputs.item(index))
            if isinstance(w, PinWidget):
                p = node.addOutputPin(w.name(), w.dataType(), None, w.shouldHideLabel())
                w.lePinName.setText(p.name)

        # recreate pins from editor data
        for index in range(self.lwInputs.count()):
            w = self.lwInputs.itemWidget(self.lwInputs.item(index))
            if isinstance(w, PinWidget):
                if w.dataType() == DataTypes.Exec:
                    p = node.addInputPin(w.name(), w.dataType(), node.compute, w.shouldHideLabel())
                    w.lePinName.setText(p.name)
                else:
                    p = node.addInputPin(w.name(), w.dataType(), None, w.shouldHideLabel())
                    w.lePinName.setText(p.name)

        for i in node.inputs.values():
            for o in node.outputs.values():
                pinAffects(i, o)

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