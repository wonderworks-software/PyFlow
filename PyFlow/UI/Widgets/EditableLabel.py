from Qt import QtWidgets
from Qt import QtCore,QtGui

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
            self.graph._sortcuts_enabled = False
            self.nameEdit = QtWidgets.QLineEdit(self.nameLabel.text())
            self.nameEdit.setContentsMargins(0, 0, 0, 0)
            self.nameEdit.setAlignment(self.nameLabel.alignment())
            #self.nameEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self.nameEdit.setText(self.nameLabel.text())
            self.nameEdit.setFont(self._font)
            self.nameEdit.setMaximumWidth( self.nameLabel.fontMetrics().boundingRect(self.nameLabel.text()).width()*1.5)
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
        self.clearFocus ()
  
    def restoreGraph(self):
        if self._isEditable:
            if self.nameEdit:
                if self.nameEdit.text() != "":
                    self.prevName = self.nameEdit.text()   
                self.nameLabel.setText(self.prevName)
                self.setWidget(self.nameLabel)
                self.nameEdit.hide()
                self.nameLabel.show()
                self.graph._sortcuts_enabled = True
                self.nameChanged.emit(self.prevName)

    def focusInEvent(self, event):
        self.node.graph().disableSortcuts()

    def eventFilter(self, object, event):
        if self._isEditable:
            if event.type()== QtCore.QEvent.WindowDeactivate:
                self.restoreGraph()
            elif event.type()== QtCore.QEvent.FocusOut:
                self.node.graph().enableSortcuts()
                self.restoreGraph()

        return super(EditableLabel,self).eventFilter(object, event)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ex = EditableLabel("test",None)
    ex.setStyle(QtWidgets.QStyleFactory.create("motif"))
    ex.show() 
    sys.exit(app.exec_())      
  