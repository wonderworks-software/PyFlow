"""@file CodeEditor.py

The code editor is a widget for [pythonNode](@ref PyFlow.Nodes.pythonNode.pythonNode)
To open it, create pythonNode first, then right click on it and click 'edit'. Code editor will pop up.
@image html codeEditorInput.jpg
The editor is divided into two parts.

**The first part** is a place where you will define and sort pins. To sort pins, simply drag

them as you would like them to be located on the node.

1. node name

2. create new input button. To the right there is a button for output pin creation also.

3. remove selected pins

4. pin widget. Here you can specify pin name and data type, as well as label visibility.

5. spin box to change editor font size

6. reset ui to defaults

7. apply to node. This button will populate node with data from code editor ui.

@image html codeEditorCode.jpg

**The second part** is actually the text editor. Here you can read/write pins data, import python modules and use them in calculationis.

When save button is pressed, function with code you wrote will be generated and used as node's compute method.

    Examples:
        # you can acess pins in two ways
        # like so
        >>> self.pinName.getData()
        >>> self.pinName.setData(value)
        # or like so
        >>> self.getData('pinName')
        >>> self.setData('pinName', value)

        # this code
        >>> import math
        >>> print(math.pi)
        # will be turned into the following
        >>> def compute(self):
        >>>     import math
        >>>     print(math.pi)
        # and then used inside the node


"""

import weakref
from keyword import kwlist
import __builtin__
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

from PyFlow.UI.Widgets import CodeEditor_ui
import PyFlow.UI.PythonSyntax as PythonSyntax
from PyFlow.UI.Widgets.UI import PinWidget_ui
from PyFlow.UI.Node import Node


_defaultWordList = kwlist + ['setData(', 'getData()', 'currentData()', 'dataType', 'setClean()', 'setDirty()'] + dir(__builtin__)


# TODO: Rewrite this


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
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Space)
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


class WPinWidget(QWidget, PinWidget_ui.Ui_Form):
    def __init__(self, editor):
        super(WPinWidget, self).__init__()
        self.setupUi(self)
        self.editor = weakref.ref(editor)
        self.lePinName.setText('pinName')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.items = [v for v in DataTypes if v not in ["Reference", 'EnumPin']]
        self.cbType.clear()

        for i in self.items:
            self.cbType.addItem(i.name, i.value)

    @staticmethod
    def construct(name='pinName', hideLabel=False, dataType='FloatPin', editor=None):
        w = WPinWidget(editor)
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


## @brief Used to write code into pythonNode
# @details See [Package description](@ref CodeEditor) for details
class WCodeEditor(QWidget, CodeEditor_ui.Ui_CodeEditorWidget):
    def __init__(self, graph, node, uid):
        super(WCodeEditor, self).__init__()
        self.setupUi(self)
        self.graph = graph
        self.nodeUid = node.uid
        self.uid = uid

        # insert code editor
        self.plainTextEdit = WCompletionTextEdit(self.tabCode)
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
        self.tabWidget.currentChanged.connect(self.OnCurrentTabChanged)
        self.setFontSize(10)

        self.sbFontSize.valueChanged.connect(lambda: self.setFontSize(self.sbFontSize.value()))
        self.pbAddInput.clicked.connect(self.addDefaultInput)
        self.pbAddOutput.clicked.connect(self.addDefaultOutput)
        self.pbSave.clicked.connect(self.applyData)
        self.pbReset.clicked.connect(self.resetUiData)
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

    ## slot for kill selected pins button
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

    ##  populte editor ui from node data
    def populate(self):
        node = self.graph.nodes[self.nodeUid]
        for i in node.inputs.values():
            pw = WPinWidget.construct(i.name, i.bLabelHidden, i.dataType, self)
            self.appendInput(pw)
        for o in node.outputs.values():
            pw = WPinWidget.construct(o.name, o.bLabelHidden, o.dataType, self)
            self.appendOutput(pw)
        self.leLabel.setText(node.label().toPlainText())
        code = ""
        for line in node.currentComputeCode:
            code += line
        self.plainTextEdit.setPlainText(code)

    ## resets ui to defaults
    def resetUiData(self):
        self.lwInputs.clear()
        self.lwOutputs.clear()

    ## @brief this method resets python node to its initial state
    # @details kills all inputs and outputs including all containers etc.
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
    ## this method wraps code into the function
    # @param fooName function name (string)
    # @param code python code (string)
    # @returns function object
    def wrapCodeToFunction(fooName, code):
        foo = "def {}(self):".format(fooName)
        lines = [i for i in code.split('\n') if len(i) > 0]
        for line in lines:
            foo += '\n\t{}'.format(line)
        return foo

    ## slot called when Save button is pressed
    # @sa CodeEditor
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
        foo = WCodeEditor.wrapCodeToFunction('compute', code)
        exec(foo)
        node.compute = MethodType(compute, node, Node)
        node.currentComputeCode = code

        for index in range(self.lwOutputs.count()):
            w = self.lwOutputs.itemWidget(self.lwOutputs.item(index))
            if isinstance(w, WPinWidget):
                p = node.addOutputPin(w.name(), w.dataType(), None, w.shouldHideLabel())
                w.lePinName.setText(p.name)

        # recreate pins from editor data
        for index in range(self.lwInputs.count()):
            w = self.lwInputs.itemWidget(self.lwInputs.item(index))
            if isinstance(w, WPinWidget):
                if w.dataType() == 'ExecPin':
                    p = node.addInputPin(w.name(), w.dataType(), node.compute, w.shouldHideLabel())
                    w.lePinName.setText(p.name)
                else:
                    p = node.addInputPin(w.name(), w.dataType(), None, w.shouldHideLabel())
                    w.lePinName.setText(p.name)

        for i in node.inputs.values():
            for o in node.outputs.values():
                pinAffects(i, o)

        # reset node shape
        node.updateNodeShape(lbText)

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

    ## puts created widget inside input list widget
    def appendInput(self, pw):
        item = QListWidgetItem(self.lwInputs)
        item.setSizeHint(QtCore.QSize(pw.sizeHint().width(), 80))
        self.lwInputs.addItem(item)
        self.lwInputs.setItemWidget(item, pw)
        del item

    ## puts created widget inside output list widget
    def appendOutput(self, pw):
        item = QListWidgetItem(self.lwOutputs)
        item.setSizeHint(QtCore.QSize(pw.sizeHint().width(), 80))
        self.lwOutputs.addItem(item)
        self.lwOutputs.setItemWidget(item, pw)
        del item

    ## add input pin slot
    def addDefaultInput(self):
        w = WPinWidget(self)
        self.appendInput(w)

    ## add output pin slot
    def addDefaultOutput(self):
        w = WPinWidget(self)
        self.appendOutput(w)

    ## changes text editor font size
    def setFontSize(self, size):
        f = self.plainTextEdit.font()
        size = abs(size)
        f.setPointSize(size)
        self.plainTextEdit.setTabStopWidth(size)
        self.plainTextEdit.setFont(f)
        option = self.plainTextEdit.document().defaultTextOption()
        option.setTabStop(size)
        self.plainTextEdit.document().setDefaultTextOption(option)
