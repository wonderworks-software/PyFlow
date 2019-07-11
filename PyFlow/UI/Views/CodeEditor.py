import weakref
from keyword import kwlist
import sys
try:
    # python 2 support
    import __builtin__ as builtins
except:
    import builtins
import inspect
from types import MethodType

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


import PyFlow.UI.Utils.PythonSyntax as PythonSyntax
from PyFlow.UI.Views import PinWidget_ui
from PyFlow.UI.Widgets import CodeEditor_ui
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.Core.Common import pinAffects
from PyFlow import (
    getAllPinClasses,
    getPinDefaultValueByType
)
from PyFlow.Core.PyCodeCompiler import Py3FunctionCompiler


_defaultWordList = kwlist + \
    ['setData(', 'getData()', 'currentData()', 'dataType',
     'setClean()', 'setDirty()'] + dir(builtins)


class WCompletionTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(WCompletionTextEdit, self).__init__(parent)
        self.setMinimumWidth(400)
        self.completer = QCompleter(_defaultWordList, self)
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
        tc.insertText(completion.replace(
            self.completer.completionPrefix(), ''))
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
        isShortcut = (event.modifiers(
        ) == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Space)
        if (not self.completer or not isShortcut):
            QPlainTextEdit.keyPressEvent(self, event)

        # ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (
            QtCore.Qt.ControlModifier, QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text() == '':
            # ctrl or shift key on it's own
            return

        # end of word
        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier)
                       and not ctrlOrShift)

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
        cr.setWidth(self.completer.popup().sizeHintForColumn(
            0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        # popup it up!
        self.completer.complete(cr)


class WPinWidget(QWidget, PinWidget_ui.Ui_Form):
    def __init__(self, editor):
        super(WPinWidget, self).__init__()
        self.setupUi(self)
        self.editor = weakref.ref(editor)
        self.lePinName.setText('pinName')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.items = [t.__name__ for t in getAllPinClasses()]
        self.cbType.clear()

        for i in self.items:
            self.cbType.addItem(i)

        self.cbType.setCurrentIndex(self.cbType.findText('AnyPin'))

    @staticmethod
    def construct(name='pinName', hideLabel=False, dataType='FloatPin', editor=None):
        w = WPinWidget(editor)
        w.lePinName.setText(name)

        if not hideLabel:
            w.cbHideLabel.setCheckState(QtCore.Qt.Checked)
        else:
            w.cbHideLabel.setCheckState(QtCore.Qt.Unchecked)

        w.cbType.setCurrentIndex(w.cbType.findText(dataType))
        return w

    def shouldHideLabel(self):
        return self.cbHideLabel.isChecked()

    def name(self):
        return self.lePinName.text()

    def dataType(self):
        return self.cbType.currentText()


class CodeEditor(QWidget, CodeEditor_ui.Ui_CodeEditorWidget):
    def __init__(self, graph, node, uid):
        super(CodeEditor, self).__init__()
        self.setupUi(self)
        self.graph = graph
        self.nodeUid = node.uid
        self.uid = uid

        # insert code editor
        self.plainTextEdit = WCompletionTextEdit(self.tabCode)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        PythonSyntax.PythonHighlighter(self.plainTextEdit.document())
        option = QtGui.QTextOption()
        # option.setFlags(option.Flags() | QtGui.QTextOption.ShowTabsAndSpaces)
        self.plainTextEdit.document().setDefaultTextOption(option)
        self.tabWidget.currentChanged.connect(self.OnCurrentTabChanged)
        self.setFontSize(10)

        self.sbFontSize.valueChanged.connect(
            lambda: self.setFontSize(self.sbFontSize.value()))
        self.pbAddInput.clicked.connect(self.addDefaultInput)
        self.pbAddOutput.clicked.connect(self.addDefaultOutput)
        self.pbSave.clicked.connect(self.applyData)
        self.pbKillSelectedItems.clicked.connect(self.onKillSelectedPins)
        self.resetUiData()
        self.populate()

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_S:
            self.applyData()

    def OnCurrentTabChanged(self, index):
        if index is 1:
            stringList = _defaultWordList + self.gatherPinNames()
            self.plainTextEdit.completer.model().setStringList(stringList)

    # slot for kill selected pins button
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

    # populte editor ui from node data
    def populate(self):
        node = self.graph.getNodes()[self.nodeUid]
        for i in node.inputs.values():
            pw = WPinWidget.construct(i.name, i.getLabel()().isVisible(), i.__class__.__name__, self)
            self.appendInput(pw)
        for o in node.outputs.values():
            pw = WPinWidget.construct(o.name, o.getLabel()().isVisible(), o.__class__.__name__, self)
            self.appendOutput(pw)
        self.leLabel.setText(node.label().toPlainText())
        code = ""
        for line in node.currentComputeCode:
            code += line
        self.plainTextEdit.setPlainText(code)

    # resets ui to defaults
    def resetUiData(self):
        self.lwInputs.clear()
        self.lwOutputs.clear()

    def resetNode(self):
        node = self.graph.getNodes()[self.nodeUid]
        for i in list(node.inputs.values()):
            i.kill()
        for o in list(node.outputs.values()):
            o.kill()

    def applyData(self):
        # reset node
        self.resetNode()
        node = self.graph.getNodes()[self.nodeUid]

        # label
        lbText = self.leLabel.text()
        if not lbText == '':
            node.label().setPlainText(lbText)

        # assign compute method
        code = self.plainTextEdit.toPlainText()
        # Py3FunctionCompiler works for python 2 as well
        foo = Py3FunctionCompiler('compute').compile(code)
        node.compute = MethodType(foo, node)
        node.currentComputeCode = code

        for index in range(self.lwOutputs.count()):
            w = self.lwOutputs.itemWidget(self.lwOutputs.item(index))
            if isinstance(w, WPinWidget):
                dataType = w.dataType()
                rawPin = node._rawNode.createOutputPin(w.name(), w.dataType(), getPinDefaultValueByType(dataType))
                uiPin = node._createUIPinWrapper(rawPin)
                w.lePinName.setText(uiPin.name)
                uiPin.getLabel()().setVisible(not w.shouldHideLabel())

        # recreate pins from editor data
        for index in range(self.lwInputs.count()):
            w = self.lwInputs.itemWidget(self.lwInputs.item(index))
            if isinstance(w, WPinWidget):
                dataType = w.dataType()
                compute = node.compute if dataType == "ExecPin" else None
                rawPin = node._rawNode.createInputPin(
                    w.name(), w.dataType(), getPinDefaultValueByType(dataType), compute)
                uiPin = node._createUIPinWrapper(rawPin)
                w.lePinName.setText(uiPin.name)
                uiPin.getLabel()().setVisible(not w.shouldHideLabel())

        node.autoAffectPins()

        # reset node shape
        node.updateNodeShape()

    def gatherPinNames(self):
        names = []
        for index in range(self.lwOutputs.count()):
            w = self.lwOutputs.itemWidget(self.lwOutputs.item(index))
            if isinstance(w, WPinWidget):
                name = w.lePinName.text()
                if name not in names:
                    names.append(name)
        for index in range(self.lwInputs.count()):
            w = self.lwInputs.itemWidget(self.lwInputs.item(index))
            if isinstance(w, WPinWidget):
                name = w.lePinName.text()
                if name not in names:
                    names.append(name)
        return names

    # puts created widget inside input list widget
    def appendInput(self, pw):
        item = QListWidgetItem(self.lwInputs)
        item.setSizeHint(QtCore.QSize(pw.sizeHint().width(), 80))
        self.lwInputs.addItem(item)
        self.lwInputs.setItemWidget(item, pw)
        del item

    # puts created widget inside output list widget
    def appendOutput(self, pw):
        item = QListWidgetItem(self.lwOutputs)
        item.setSizeHint(QtCore.QSize(pw.sizeHint().width(), 80))
        self.lwOutputs.addItem(item)
        self.lwOutputs.setItemWidget(item, pw)
        del item

    # add input pin slot
    def addDefaultInput(self):
        w = WPinWidget(self)
        self.appendInput(w)

    # add output pin slot
    def addDefaultOutput(self):
        w = WPinWidget(self)
        self.appendOutput(w)

    # changes text editor font size
    def setFontSize(self, size):
        f = self.plainTextEdit.font()
        size = abs(size)
        f.setPointSize(size)
        self.plainTextEdit.setTabStopWidth(size)
        self.plainTextEdit.setFont(f)
        option = self.plainTextEdit.document().defaultTextOption()
        option.setTabStop(size)
        self.plainTextEdit.document().setDefaultTextOption(option)
