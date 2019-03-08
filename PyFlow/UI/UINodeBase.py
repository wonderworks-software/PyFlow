"""@file Node.py

Node is a base class for all ui nodes. This is actually a QGraphicsItem with all common stuff for nodes.

Also, it implements [initializeFromFunction](@ref PyFlow.Core.Node.initializeFromFunction) method which constructs node from given annotated function.
@sa FunctionLibrary.py
"""

import weakref

from Settings import *
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsObject
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QTextBrowser
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QGraphicsLinearLayout
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QTreeWidgetItem
from Qt.QtWidgets import QColorDialog
from Qt.QtWidgets import QMenu

from PyFlow.UI.UIPinBase import (
    UIPinBase,
    getUIPinInstance
)
from PyFlow.UI.InputWidgets import createInputWidget
from PyFlow.UI.NodePainter import NodePainter
from PyFlow.UI.IContextMenu import IContextMenu
from PyFlow.Core.NodeBase import NodeBase
from PyFlow.Core.Enums import ENone
from PyFlow.Core.AGraphCommon import *

from collections import OrderedDict
UI_NODES_FACTORIES = {}


class NodeName(QGraphicsTextItem):
    def __init__(self, parent, bUseTextureBg=True, color=Colors.NodeNameRectGreen):
        super(NodeName, self).__init__(parent)
        self.setParentItem(parent)
        self.bUseTextureBg = bUseTextureBg
        self.width = 50
        self.document().contentsChanged.connect(self.onDocContentsChanged)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.desc = parent._rawNode.description()
        self.descFontPen = QtGui.QPen(QtCore.Qt.gray, 0.5)
        self.defaultPen = QtGui.QPen(QtCore.Qt.white, 0.5)
        self.text_color = Colors.PinNameColor
        self.setDefaultTextColor(self.text_color)
        self.opt_font = QtGui.QFont('Consolas')
        self.opt_font_size = 8
        self.opt_font.setPointSize(self.opt_font_size)
        self.defaultHeight = self.opt_font_size * 2.5
        self.h = self.defaultHeight
        self.setFont(self.opt_font)
        self.descFont = QtGui.QFont(
            "Consolas", self.opt_font.pointSize() / 2.0, 2, True)
        self.setPos(0, -self.boundingRect().height() - 8)
        self.color = color
        self.clipRect = None
        self.roundCornerFactor = 1.0
        self.bg = QtGui.QImage(':/icons/resources/white.png')
        self.icon = None

    def onDocContentsChanged(self):
        self.width = QtGui.QFontMetricsF(
            self.font()).width(self.toPlainText()) + 5.0
        self.document().setTextWidth(self.width)

    @staticmethod
    def IsRenamable():
        return False

    def keyPressEvent(self, event):
        key = event.key()
        if (key == QtCore.Qt.Key_Return) or (key == QtCore.Qt.Key_Escape):
            self.setEnabled(False)
            self.setEnabled(True)
            return
        else:
            QGraphicsTextItem.keyPressEvent(self, event)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width + 5.0, self.h)

    def paint(self, painter, option, widget):
        if self.parentItem().bUseTextureBg:
            color = self.color

            parentRet = self.parentItem().childrenBoundingRect()
            if self.icon:
                painter.drawImage(QtCore.QRect(parentRet.width() - 9, 0, 8, 8), self.icon, QtCore.QRect(0, 0, self.icon.width(), self.icon.height()))
        else:
            parentRet = self.parentItem().childrenBoundingRect()
            if self.icon:
                painter.drawImage(QtCore.QRect(parentRet.width() - 12, 5, 8, 8), self.icon, QtCore.QRect(0, 0, self.icon.width(), self.icon.height()))
        # super(NodeName, self).paint(painter, option, widget)
        painter.setPen(self.defaultPen)
        font = painter.font()
        nameRectMargin = 2
        nameRect = QtCore.QRectF(self.boundingRect().topLeft() + QtCore.QPointF(nameRectMargin, nameRectMargin), QtCore.QPointF(self.parentItem().boundingRect().right() - 15,
                                 self.boundingRect().bottom() - font.pointSize() * 0.65))
        painter.drawText(nameRect, QtCore.Qt.AlignLeft, self.parentItem().displayName)
        packageRect = QtCore.QRectF(self.boundingRect().topLeft() + QtCore.QPointF(nameRectMargin, 0), QtCore.QPointF(self.parentItem().boundingRect().right(),
                                    self.boundingRect().bottom()))
        font = painter.font()
        font.setPointSize(font.pointSize() * 0.65)
        font.setItalic(True)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtCore.Qt.gray, 0.5))
        text = self.parentItem().packageName()
        # if self.parentItem()._rawNode.lib:
        #    text += "|{0}".format(self.parentItem()._rawNode.lib)
        painter.drawText(packageRect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, text)

    def focusInEvent(self, event):
        self.parentItem().graph().disableSortcuts()

    def focusOutEvent(self, event):
        self.parentItem().graph().enableSortcuts()
        # clear cursour
        cursor = QtGui.QTextCursor(self.document())
        cursor.clearSelection()
        self.setTextCursor(cursor)


class UINodeBase(QGraphicsObject):
    """
    Default node description
    """

    def __init__(self, raw_node, w=80, color=Colors.NodeBackgrounds, headColor=Colors.NodeNameRectGreen, bUseTextureBg=True):
        super(UINodeBase, self).__init__()
        self._rawNode = raw_node
        self._rawNode.setWrapper(self)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.opt_node_base_color = Colors.NodeBackgrounds
        self.opt_selected_pen_color = Colors.NodeSelectedPenColor
        self.opt_pen_selected_type = QtCore.Qt.SolidLine
        self._left_stretch = 0
        self.color = color
        self.headColor = headColor
        self.height_offset = 3
        self.nodeMainGWidget = QGraphicsWidget()
        self.nodeMainGWidget.setObjectName(
            '{0}MainLayout'.format(self._rawNode.__class__.__name__))
        self._w = 0
        self.h = 40
        self.bUseTextureBg = bUseTextureBg  # self.graph().styleSheetEditor.USETEXTUREBG
        if self.bUseTextureBg:
            self.sizes = [0, 0, self.w, self.h, 2, 2]
        else:
            self.sizes = [0, 0, self.w, self.h, 10, 10]
        self.w = w
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.custom_widget_data = {}
        # node name
        self.label = weakref.ref(
            NodeName(self, self.bUseTextureBg, self.headColor))
        self._displayName = self.name
        # set node layouts
        self.nodeMainGWidget.setParentItem(self)
        # main
        self.portsMainLayout = QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.portsMainLayout.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.portsMainLayout.setContentsMargins(0, 0, 0, 0)
        self.nodeMainGWidget.setLayout(self.portsMainLayout)
        self.nodeMainGWidget.setX(self.nodeMainGWidget.x())
        # inputs layout
        self.inputsLayout = QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.inputsLayout.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.inputsLayout.setContentsMargins(1, 1, 1, 1)
        self.portsMainLayout.addItem(self.inputsLayout)
        # outputs layout
        self.outputsLayout = QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.outputsLayout.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.outputsLayout.setContentsMargins(1, 1, 1, 1)
        self.portsMainLayout.addItem(self.outputsLayout)

        self.setZValue(1)

        self.icon = None
        self.UIPins = {}
        self.UIinputs = {}
        self.UIoutputs = {}
        self._menu = QMenu()
        # Resizing Options
        self.minWidth = 25
        self.minHeight = self.h
        self.initialRectWidth = 0.0
        self.initialRectHeight = 0.0
        self.expanded = True
        self.resizable = False
        self.bResize = False
        self.resizeDirection = (0, 0)
        self.lastMousePos = QtCore.QPointF()
        # Hiding/Moving By Group/collapse/By Pin
        self.nodesToMove = {}
        self.edgesToHide = []
        self.nodesNamesToMove = []
        self.pinsToMove = {}
        self._rect = self.childrenBoundingRect()

        # Core Nodes Support
        self.isTemp = False
        self.isCommentNode = False

    @property
    def graph(self):
        return self._rawNode.graph

    @graph.setter
    def graph(self, value):
        self._rawNode.graph = value

    @property
    def uid(self):
        return self._rawNode._uid

    @uid.setter
    def uid(self, value):
        self._rawNode.uid = value

    @property
    def name(self):
        return self._rawNode.name

    @property
    def displayName(self):
        return self._displayName

    @displayName.setter
    def displayName(self, value):
        self._displayName = value

    @property
    def pins(self):
        return self._rawNode.pins

    @property
    def inputs(self):
        return self._rawNode.inputs

    @inputs.setter
    def inputs(self, value):
        self._rawNode.inputs = value

    @property
    def outputs(self):
        return self._rawNode.outputs

    @outputs.setter
    def outputs(self, value):
        self._rawNode.outputs = value

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        self.sizes[2] = value

    def getName(self):
        return self._rawNode.getName()

    def setName(self, name):
        self._rawNode.setName(name)

    def getPinByName(self, name, pinsGroup=PinSelectionGroup.BothSides):
        return self._rawNode.getPinByName(name, pinsGroup)

    @staticmethod
    def removePinByName(node, name):
        pin = node.getPinByName(name)
        if pin:
            pin.kill()

    @staticmethod
    def recreate(node):
        templ = node.serialize()
        uid = node.uid
        node.kill()
        newNode = node.graph().createNode(templ)
        newNode.uid = uid
        return newNode

    @staticmethod
    def jsonTemplate():
        template = NodeBase.jsonTemplate()
        template['x'] = 0
        template['y'] = 0
        return template

    @staticmethod
    def deserialize(data, graph):
        node = graph.createNode(data)
        node.uid = uuid.UUID(data['uuid'])

        # set pins data
        for inpJson in data['inputs']:
            pin = node.getPinByName(inpJson['name'], PinSelectionGroup.Inputs)
            pin.uid = uuid.UUID(inpJson['uuid'])
            pin.setData(inpJson['value'])
            if inpJson['bDirty']:
                pin.setDirty()
            else:
                pin.setClean()

        for outJson in data['outputs']:
            pin = node.getPinByName(outJson['name'], PinSelectionGroup.Outputs)
            pin.uid = uuid.UUID(outJson['uuid'])
            pin.setData(outJson['value'])
            if outJson['bDirty']:
                pin.setDirty()
            else:
                pin.setClean()
        return node

    def serialize(self):
        template = self._rawNode.serialize()
        template['x'] = self.scenePos().x()
        template['y'] = self.scenePos().y()
        if self.resizable:
            template['meta']['resize'] = {
                'w': self._rect.right(), 'h': self._rect.bottom()}

        return template

    def postCreate(self, jsonTemplate=None):
        self._rawNode.postCreate(jsonTemplate)
        # create ui pin wrappers
        for uid, i in self.inputs.items():
            p = self._createUIPinWrapper(i)
            self.UIinputs[uid] = p

        for uid, o in self.outputs.items():
            p = self._createUIPinWrapper(o)
            self.UIoutputs[uid] = p

        self.updateNodeShape(label=jsonTemplate['meta']['label'])
        self._rect = self.childrenBoundingRect()
        if "resize" in jsonTemplate['meta']:
            self.resizable = True
            self._rect.setBottom(jsonTemplate['meta']['resize']['h'])
            self._rect.setRight(jsonTemplate['meta']['resize']['w'])
        self._displayName = self.name

    def isCallable(self):
        return self._rawNode.isCallable()

    def boundingRect(self):
        if self.childrenBoundingRect().height() > self._rect.height():
            self._rect.setHeight(self.childrenBoundingRect().height())
        if self.minWidth > self._rect.width():
            self._rect.setWidth(self.minWidth)

        return self._rect

    def category(self):
        return self._rawNode.category()

    def description(self):
        return self._rawNode.description()

    def packageName(self):
        return self._rawNode.packageName()

    def call(self, name):
        if pinName in [p.name for p in self.outputs.values() if p.dataType is 'ExecPin']:
            p = self.getPinByName(pinName)
            return p.call()

    def getData(self, pinName):
        if pinName in [p.name for p in self.inputs.values()]:
            p = self.getPinByName(pinName, PinSelectionGroup.Inputs)
            return p.getData()

    def setData(self, pinName, data):
        if pinName in [p.name for p in self.outputs.values()]:
            p = self.getPinByName(pinName, PinSelectionGroup.Outputs)
            p.setData(data)

    def getWidth(self):
        fontWidth = QtGui.QFontMetricsF(self.label().font()).width(
            self.displayName) + Spacings.kPinSpacing
        return fontWidth if fontWidth > 25 else 25

    def getPinsWidth(self):
        iwidth = 0
        owidth = 0
        pinwidth = 0
        pinwidth2 = 0
        for i in self.UIPins.values():
            if i.direction == PinDirection.Input:
                iwidth = max(iwidth,QtGui.QFontMetricsF(i._label().font()).width(i.displayName())) 
                pinwidth = max(pinwidth,i.width)  
            else:
                print i
                owidth = max(owidth,QtGui.QFontMetricsF(i._label().font()).width(i.displayName())) 
                pinwidth2 = max(pinwidth2,i.width)                                    
        return iwidth+owidth +pinwidth + pinwidth2 + Spacings.kPinOffset

    def updateWidth(self):
        print self.getPinsWidth()
        self.minWidth = max(self.getPinsWidth() , self.getWidth() + Spacings.kPinOffset)
        self.w = self.minWidth#,self.getWidth() + Spacings.kPinOffset)


    def updateNodeShape(self, label=None):
        for i in range(0, self.inputsLayout.count()):
            container = self.inputsLayout.itemAt(i)
            lyt = container.layout()
            if lyt:
                for j in range(0, lyt.count()):
                    lyt.setAlignment(lyt.itemAt(
                        j), QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        for i in range(0, self.outputsLayout.count()):
            container = self.outputsLayout.itemAt(i)
            lyt = container.layout()
            if lyt:
                for j in range(0, lyt.count()):
                    lyt.setAlignment(lyt.itemAt(
                        j), QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        if label is None:
            self.label().setPlainText(self._rawNode.__class__.__name__)
        else:
            self.label().setPlainText(label)

        self.updateWidth()
        self.nodeMainGWidget.setGeometry(QtCore.QRectF(
            0, 0, self.w, self.childrenBoundingRect().height()))        
        if self.isCallable():
            if 'flow' not in self.category().lower():
                if self.label().bUseTextureBg:
                    self.headColor = Colors.NodeNameRectBlue
                    self.label().color = Colors.NodeNameRectBlue
        self.setToolTip(self.description())
        self.update()

    def onChangeColor(self, label=False):
        res = QColorDialog.getColor(self.color, None, 'Node color setup')
        if res.isValid():
            res.setAlpha(80)
            self.color = res
            if label:
                self.label().color = res
                self.update()
                self.label().update()

    def itemChange(self, change, value):
        # if change == self.ItemPositionChange:
        #    # grid snapping
        #    value.setX(roundup(value.x() - self.graph().grid_size + self.graph().grid_size / 3.0, self.graph().grid_size))
        #    value.setY(roundup(value.y() - self.graph().grid_size + self.graph().grid_size / 3.0, self.graph().grid_size))
        #    value.setY(value.y() - 2)
        #    return value
        return QGraphicsItem.itemChange(self, change, value)

    def setPosition(self, x, y):
        self._rawNode.setPosition(x, y)
        self.setPos(QtCore.QPointF(x, y))

    def translate(self, x, y, moveChildren=False):
        if moveChildren:
            for n in self.nodesToMove:
                if not n.isSelected():
                    n.translate(x, y)
        super(UINodeBase, self).moveBy(x, y)

    def paint(self, painter, option, widget):
        NodePainter.default(self, painter, option, widget)

    def shouldResize(self, cursorPos):
        cursorPos = self.mapFromScene(cursorPos)
        margin = 4
        rect = self.boundingRect()
        pBottomRight = rect.bottomRight()
        pBottomLeft = rect.bottomLeft()
        bottomRightRect = QtCore.QRectF(
            pBottomRight.x() - margin, pBottomRight.y() - margin, margin, margin)
        bottomLeftRect = QtCore.QRectF(
            pBottomLeft.x(), pBottomLeft.y() - margin, 5, 5)
        result = {"resize": False, "direction": self.resizeDirection}
        if bottomRightRect.contains(cursorPos):
            result["resize"] = True
            result["direction"] = (1, -1)
        elif bottomLeftRect.contains(cursorPos):
            result["resize"] = True
            result["direction"] = (-1, -1)
        elif cursorPos.x() > (rect.width() - margin):
            result["resize"] = True
            result["direction"] = (1, 0)
        elif cursorPos.y() > (rect.bottom()-margin):
            result["resize"] = True
            result["direction"] = (0, -1)
        elif cursorPos.x() < (rect.x() + margin):
            result["resize"] = True
            result["direction"] = (-1, 0)
        return result

    def contextMenuEvent(self, event):
        self._menu.exec_(event.screenPos())

    def mousePressEvent(self, event):
        self.update()
        QGraphicsItem.mousePressEvent(self, event)
        self.mousePressPos = event.scenePos()
        self.origPos = self.pos()
        self.initPos = self.pos()
        self.initialRect = self.boundingRect()
        if self.expanded and self.resizable:
            resizeOpts = self.shouldResize(self.mapToScene(event.pos()))
            if resizeOpts["resize"]:
                self.resizeDirection = resizeOpts["direction"]
                self.initialRectWidth = self.initialRect.width()
                self.initialRectHeight = self.initialRect.height()
                self.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.bResize = True

    def mouseMoveEvent(self, event):
        QGraphicsItem.mouseMoveEvent(self, event)
        # resize
        if self.bResize:
            delta = event.scenePos() - self.mousePressPos
            if self.resizeDirection == (1, 0):
                # right edge resize
                newWidth = delta.x() + self.initialRectWidth
                if newWidth > self.minWidth:
                    self.label().width = newWidth
                    self._rect.setWidth(newWidth)
                    self.w = newWidth
                    self.nodeMainGWidget.setGeometry(QtCore.QRectF(
                        0, 0, newWidth, self.boundingRect().height()))
            elif self.resizeDirection == (-1, 0):
                # left edge resize
                posdelta = self.mapToScene(event.pos()) - self.origPos
                posdelta2 = self.mapToScene(event.pos()) - self.initPos
                newWidth = -posdelta2.x()+self.initialRectWidth
                if newWidth > self.minWidth:#(self.inputsLayout.geometry().width()+self.outputsLayout.geometry().width()) and newWidth > self.minWidth:
                    #if newWidth > (self.inputsLayout.geometry().width()+self.outputsLayout.geometry().width()):
                    self.translate(posdelta.x(), 0, False)
                    self.origPos = self.pos()
                    self.label().width = newWidth
                    self._rect.setWidth(newWidth)
                    self.w = newWidth
                    self.nodeMainGWidget.setGeometry(QtCore.QRectF(
                        0, 0, self.w, self.boundingRect().height()))
            elif self.resizeDirection == (0, -1):
                newHeight = delta.y() + self.initialRectHeight
                newHeight = max(newHeight, self.label().h + 20.0)
                if newHeight > self.minHeight:
                    # bottom edge resize
                    self._rect.setHeight(newHeight)
            elif self.resizeDirection == (1, -1):
                newWidth = delta.x() + self.initialRectWidth
                newHeight = delta.y() + self.initialRectHeight
                newHeight = max(newHeight, self.label().h + 20.0)
                if newWidth > self.minWidth:
                    self.label().width = newWidth
                    self._rect.setWidth(newWidth)
                    self.w = newWidth
                    self.nodeMainGWidget.setGeometry(QtCore.QRectF(
                        0, 0, self.w, self.boundingRect().height()))
                if newHeight > self.minHeight:
                    self._rect.setHeight(newHeight)
            elif self.resizeDirection == (-1, -1):
                posdelta2 = self.mapToScene(event.pos()) - self.initPos
                newWidth = -posdelta2.x()+self.initialRectWidth
                newHeight = delta.y() + self.initialRectHeight
                newHeight = max(newHeight, self.label().h + 20.0)
                posdelta = event.scenePos() - self.origPos
                if newWidth > self.minWidth:# and newWidth > self.minWidth:
                    self.translate(posdelta.x(), 0, False)
                    self.origPos = self.pos()
                    self.label().width = newWidth
                    self._rect.setWidth(newWidth)
                    self.w = newWidth
                    self.nodeMainGWidget.setGeometry(QtCore.QRectF(
                        0, 0, self.w, self.boundingRect().height()))
                if newHeight > self.minHeight:
                    self._rect.setHeight(newHeight)
            self.update()
            self.label().update()
        self.lastMousePos = event.pos()

    def mouseReleaseEvent(self, event):
        self.update()
        self.bResize = False
        QGraphicsItem.mouseReleaseEvent(self, event)

    def clone(self):
        templ = self.serialize()
        templ['name'] = self.graph().getUniqNodeName(self.name)
        templ['uuid'] = str(uuid.uuid4())
        for inp in templ['inputs']:
            inp['uuid'] = str(uuid.uuid4())
        for out in templ['outputs']:
            out['uuid'] = str(uuid.uuid4())
        new_node = self.graph().createNode(templ)
        return new_node

    def propertyView(self):
        return self.graph().parent.dockWidgetNodeView

    def onUpdatePropertyView(self, formLayout):
        # name
        le_name = QLineEdit(self.getName())
        le_name.setReadOnly(True)
        if self.label().IsRenamable():
            le_name.setReadOnly(False)
            le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        formLayout.addRow("Name", le_name)

        # uid
        leUid = QLineEdit(str(self.uid))
        leUid.setReadOnly(True)
        formLayout.addRow("Uuid", leUid)

        # type
        text = "{0}".format(self.packageName())
        if self._rawNode.lib:
            text += " | {0}".format(self._rawNode.lib)
        text += " | {0}".format(self._rawNode.__class__.__name__)
        leType = QLineEdit(text)
        leType.setReadOnly(True)
        formLayout.addRow("Type", leType)

        # pos
        le_pos = QLineEdit("{0} x {1}".format(self.pos().x(), self.pos().y()))
        formLayout.addRow("Pos", le_pos)

        # inputs
        if len([i for i in self.inputs.values()]) != 0:
            sep_inputs = QLabel()
            sep_inputs.setStyleSheet("background-color: black;")
            sep_inputs.setText("INPUTS")
            formLayout.addRow("", sep_inputs)

            for inp in self.inputs.values():
                dataSetter = inp.call if inp.dataType == 'ExecPin' else inp.setData
                w = createInputWidget(
                    inp.dataType, dataSetter, inp.defaultValue(), inp.getUserStruct())
                if w:
                    w.blockWidgetSignals(True)
                    w.setWidgetValue(inp.currentData())
                    w.blockWidgetSignals(False)
                    w.setObjectName(inp.getName())
                    formLayout.addRow(inp.name, w)
                    if inp.hasConnections():
                        w.setEnabled(False)

        # outputs
        if len([i for i in self.outputs.values()]) != 0:
            sep_outputs = QLabel()
            sep_outputs.setStyleSheet("background-color: black;")
            sep_outputs.setText("OUTPUTS")
            formLayout.addRow("", sep_outputs)
            for out in self.outputs.values():
                if out.dataType == 'ExecPin':
                    continue
                w = createInputWidget(
                    out.dataType, out.setData, out.defaultValue(), out.getUserStruct())
                if w:
                    w.blockWidgetSignals(True)
                    w.setWidgetValue(out.currentData())
                    w.blockWidgetSignals(False)
                    w.setObjectName(out.getName())
                    formLayout.addRow(out.name, w)
                    if out.hasConnections():
                        w.setEnabled(False)

        doc_lb = QLabel()
        doc_lb.setStyleSheet("background-color: black;")
        doc_lb.setText("Description")
        formLayout.addRow("", doc_lb)
        doc = QTextBrowser()
        doc.setOpenExternalLinks(True)
        doc.setHtml(self.description())
        formLayout.addRow("", doc)

    def propertyEditingFinished(self):
        le = QApplication.instance().focusWidget()
        if isinstance(le, QLineEdit):
            nodeName, attr = le.objectName().split('.')
            Pin = self.getPinByName(attr)
            Pin.setData(le.text())

    def getChainedNodes(self):
        nodes = []
        for pin in self.inputs.values():
            for edge in pin.edge_list:
                node = edge.source().topLevelItem()  # topLevelItem
                nodes.append(node)
                nodes += node.getChainedNodes()
        return nodes

    def kill(self):
        for i in list(self.inputs.values()) + list(self.outputs.values()):
            for edge in i.edge_list:
                edge.kill()
        self._rawNode.kill()
        self.scene().removeItem(self)
        del(self)

    def Tick(self, delta):
        self._rawNode.Tick(delta)

    def addContainer(self, portType, head=False):
        container = QGraphicsWidget()
        container.setObjectName('{0}PinContainerWidget'.format(self.name))
        container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        container.sizeHint(QtCore.Qt.MinimumSize, QtCore.QSizeF(50.0, 10.0))

        lyt = QGraphicsLinearLayout()
        lyt.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        lyt.setContentsMargins(1, 1, 1, 1)
        container.setLayout(lyt)
        if portType == PinDirection.Input:
            self.inputsLayout.addItem(container)
        else:
            self.outputsLayout.addItem(container)
        return container

    def _createUIPinWrapper(self, rawPin, index=-1):
        p = getUIPinInstance(self, rawPin)
        if rawPin.direction == PinDirection.Input:
            p.call = rawPin.call

        name = rawPin.name

        # TODO: do not use Proxy widget. Use QGraphicsTextItem instead
        connector_name = QGraphicsProxyWidget()
        connector_name.setObjectName('{0}PinConnector'.format(name))
        connector_name.setContentsMargins(0, 0, 0, 0)

        lblName = name

        lbl = QLabel(lblName)
        p.displayNameChanged.connect(lbl.setText)
        lbl.setContentsMargins(0, 0, 0, 0)
        lbl.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        font = QtGui.QFont('Consolas')
        color = Colors.PinNameColor
        font.setPointSize(6)
        lbl.setFont(font)
        style = 'color: rgb({0}, {1}, {2}, {3});'.format(
            color.red(),
            color.green(),
            color.blue(),
            color.alpha())
        lbl.setStyleSheet(style)
        connector_name.setWidget(lbl)
        if rawPin.direction == PinDirection.Input:
            container = self.addContainer(rawPin.direction)
            lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            container.layout().addItem(p)
            p.setLabel(connector_name)
            p._container = container
            container.layout().addItem(connector_name)

            self.inputsLayout.insertItem(index, container)
            container.adjustSize()
        elif rawPin.direction == PinDirection.Output:
            container = self.addContainer(rawPin.direction)
            lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            container.layout().addItem(connector_name)
            container.layout().addItem(p)
            p.setLabel(connector_name)
            p._container = container
            self.outputsLayout.insertItem(index, container)
            container.adjustSize()
        p.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.UIPins[rawPin.uid] = p
        self.graph().UIPins[rawPin.uid] = p
        return p


def REGISTER_UI_NODE_FACTORY(packageName, factory):
    if packageName not in UI_NODES_FACTORIES:
        UI_NODES_FACTORIES[packageName] = factory
        print("registering", packageName, "ui nodes")


def getUINodeInstance(raw_instance):
    packageName = raw_instance.packageName()
    instance = None
    if packageName in UI_NODES_FACTORIES:
        instance = UI_NODES_FACTORIES[packageName](raw_instance)
    assert(instance is not None)
    return instance
