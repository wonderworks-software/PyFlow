from Qt import QtWidgets
from Qt import QtCore,QtGui

from Qt.QtCore import QRegExp
from Qt.QtGui import QRegExpValidator, QValidator


class EditableLabel(QtWidgets.QGraphicsProxyWidget):
    nameChanged = QtCore.Signal(str)
    def __init__(self, name="",parent=None,node=None,graph=None):
        super(EditableLabel, self).__init__(parent)
        self.node=node
        self.graph = graph
        self.nameLabel = QtWidgets.QLabel(name)
        
        self.nameLabel.setContentsMargins(0, 0, 0, 0)
        self.nameLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)  
        self._font = QtGui.QFont('Consolas')
        self._font.setPointSize(6)
        self.nameLabel.setFont(self._font)
        self.setWidget(self.nameLabel)
        self.installEventFilter(self)
        self.prevName = name
        self.nameEdit = None
        self._isEditable = False
        self._beingEdited = False
        self.regex = QRegExp("^[A-Za-z0-9_-]+$")
               
    def font(self):
        return self._font

    def setName(self,text):
        self.nameLabel.setText(text)
        self.prevName = text
    def setText(self,text):
        self.nameLabel.setText(text)
        self.prevName = text
    def setColor(self,color):
        self.style = 'color: rgb({0}, {1}, {2}, {3});'.format(
            color.red(),
            color.green(),
            color.blue(),
            color.alpha())
        self.nameLabel.setStyleSheet(self.style)

    def start_edit_name(self):
        if self._isEditable:
            self._beingEdited = True
            self.graph._sortcuts_enabled = False
            self.nameEdit = QtWidgets.QLineEdit(self.nameLabel.text())
            self.__validator = QRegExpValidator(self.regex, self.nameEdit) 
            self.nameEdit.setValidator(self.__validator)
            self.nameEdit.setContentsMargins(0,-2, -5,-8)
            self.nameEdit.setAlignment(self.nameLabel.alignment())
            self.nameEdit.setText(self.nameLabel.text())
            self.nameEdit.setFont(self._font)
            self.nameEdit.setMaximumWidth(self.nameLabel.frameGeometry().width())
            #self.nameEdit.setMaximumHeight(self.nameLabel.frameGeometry().height())
            #self.nameEdit.setMaximumWidth( self.nameLabel.fontMetrics().boundingRect(self.nameLabel.text()).width()+3)
            style ="""
background-color: transparent;
border-style: transparent;
"""+self.style
        
            self.nameEdit.setStyleSheet(style)
            self.setWidget(self.nameEdit)
            self.nameEdit.returnPressed.connect(self.setOutFocus)
            self.nameLabel.hide()

    def setOutFocus(self):
        self.clearFocus()
  
    def restoreGraph(self):
        self.node.graph().enableSortcuts()
        if self._isEditable:
            if self.nameEdit:
                if self.nameEdit.text() != "":
                    self.prevName = self.nameEdit.text()   
                self.nameLabel.setText(self.prevName)
                self.setWidget(self.nameLabel)
                self.nameEdit.hide()
                self.nameLabel.show()
                self.graph._sortcuts_enabled = True
                self._beingEdited = False
                self.nameChanged.emit(self.prevName)

    def eventFilter(self, object, event):
        if self._isEditable:
            if event.type()== QtCore.QEvent.WindowDeactivate:
                self.restoreGraph()
            elif event.type()== QtCore.QEvent.FocusIn:
                self.node.graph().disableSortcuts()
            elif event.type()== QtCore.QEvent.FocusOut:
                self.restoreGraph()

        return super(EditableLabel,self).eventFilter(object, event)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ex = EditableLabel("test",None)
    ex.setStyle(QtWidgets.QStyleFactory.create("motif"))
    ex.show() 
    sys.exit(app.exec_())      
  