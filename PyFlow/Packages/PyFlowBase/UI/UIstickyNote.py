from Qt import QtCore
from Qt import QtGui
import Qt
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Widgets.TextEditDialog import TextEditDialog
from PyFlow.UI.Widgets.QtSliders import pyf_ColorSlider
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from Qt.QtWidgets import QGraphicsTextItem,QGraphicsWidget,QGraphicsItem

class InputTextField(QGraphicsTextItem):
    def __init__(self,parent,*args,**Kwargs):
        super(InputTextField, self).__init__(*args,**Kwargs)
        self.setParentItem(parent)
        self.setObjectName("MouseLocked")
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setFlags(QGraphicsWidget.ItemSendsGeometryChanges | QGraphicsWidget.ItemIsMovable |
                                QGraphicsWidget.ItemIsFocusable | QGraphicsWidget.ItemIsSelectable )

    def focusInEvent(self, event):
        for node in self.parentItem().canvasRef().selectedNodes():
            if node != self.parentItem():
                node.setSelected(False)
        for connection in self.parentItem().canvasRef().selectedConnections():
            connection.setSelected(False)

        self.parentItem().setSelected(True)
        self.parentItem().canvasRef().disableSortcuts()
        super(InputTextField, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentItem().canvasRef().enableSortcuts()
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        super(InputTextField, self).focusOutEvent(event)

class UIstickyNote(UINodeBase):
    def __init__(self, raw_node):
        super(UIstickyNote, self).__init__(raw_node)
        self.color = QtGui.QColor(255, 255, 136)
        self.color.setAlpha(255)
        self.labelTextColor = QtGui.QColor(0,0,0,255)
        self.resizable = True
        self.editMessageAction = self._menu.addAction("Edit message")
        self.editMessageAction.setData(NodeActionButtonInfo(RESOURCES_DIR + "/rename.svg"))
        self.editMessageAction.triggered.connect(self.onChangeMessage)

        self.textInput = InputTextField(self,"Text Goes Here")
        self.textInput.setPos(QtCore.QPointF(5,self.nodeNameWidget.boundingRect().height()))
        self.textInput.document().contentsChanged.connect(self.updateSize)
        self.textWidget = QGraphicsWidget()
        self.textWidget.setGraphicsItem(self.textInput)
        self.nodeLayout.addItem(self.textWidget)        
        self.updateSize()

    def serializationHook(self):
        original = super(UIstickyNote, self).serializationHook()
        original["color"] = self.color.rgba()
        original["textColor"] = self.labelTextColor.rgba()
        original["currentText"] = self.textInput.toHtml()
        return original

    def postCreate(self, jsonTemplate=None):
        super(UIstickyNote, self).postCreate(jsonTemplate=jsonTemplate)
        if "color" in jsonTemplate["wrapper"]:
            self.color = QtGui.QColor.fromRgba(jsonTemplate["wrapper"]["color"])
        if "textColor" in jsonTemplate["wrapper"]:
            self.labelTextColor = QtGui.QColor.fromRgba(jsonTemplate["wrapper"]["textColor"])
        if "currentText" in jsonTemplate["wrapper"]:
            self.textInput.setHtml(jsonTemplate["wrapper"]["currentText"])

    def mouseDoubleClickEvent(self, event):
        self.textInput.setFocus()
        super(UIstickyNote, self).mouseDoubleClickEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            if value == False:
                self.textInput.clearFocus()
        return super(UIstickyNote, self).itemChange(change, value)

    def aboutToCollapse(self, futureCollapseState):
        if not futureCollapseState:
            self.textInput.show()
        else:
            self.textInput.hide()

    def onChangeMessage(self):
        dialog = TextEditDialog(self.nodeNameWidget.getFont(), self.labelTextColor)
        dialog.move(QtGui.QCursor.pos())
        dialog.setHtml(self.getHeaderHtml())
        dialog.exec_()
        try:
            html, accepted = dialog.getResult()
            if accepted:
                self.nodeNameWidget.setHtml(html)
                self.updateNodeShape()
        except Exception as e:
            print(e)
        self.setFocus()

    def paint(self, painter, option, widget):
        NodePainter.asCommentNode(self, painter, option, widget)
        self.updateSize()

    def mouseMoveEvent(self, event):
        super(UIstickyNote, self).mouseMoveEvent(event)
        self.updateSize()

    def updateSize(self):
        self.textInput.setTextWidth(self.boundingRect().width()-10)
        newHeight = self.textInput.boundingRect().height()+self.nodeNameWidget.boundingRect().height() + 5
        if self._rect.height() < newHeight:
            self._rect.setHeight(newHeight)
            try:
                self.updateNodeShape()
            except:
                pass
        self.minHeight = newHeight

    def updateColor(self,color):
        res = QtGui.QColor(color[0],color[1],color[2],color[3])
        if res.isValid():
            self.color = res
            self.update() 

    def updateTextColor(self,color):
        res = QtGui.QColor(color[0],color[1],color[2],color[3])
        if res.isValid():
            self.labelTextColor = res
            self.textInput.setDefaultTextColor(res)
            self.update() 

    def createInputWidgets ( self,propertiesWidget):
        inputsCategory = super(UIstickyNote, self).createInputWidgets(propertiesWidget)
        appearanceCategory = CollapsibleFormWidget(headName="Appearance")
        pb = pyf_ColorSlider(type="int",alpha=True,startColor=list(self.color.getRgbF()))
        pb.valueChanged.connect(self.updateColor)
        appearanceCategory.addWidget("Color", pb)
        pb = pyf_ColorSlider(type="int",alpha=True,startColor=list(self.labelTextColor.getRgbF()))
        pb.valueChanged.connect(self.updateTextColor)
        appearanceCategory.addWidget("TextColor", pb)        
        propertiesWidget.addWidget(appearanceCategory)