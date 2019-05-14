"""@file Node.py

Node is a base class for all ui nodes. This is actually a QGraphicsItem with all common stuff for nodes.

Also, it implements [initializeFromFunction](@ref PyFlow.Core.Node.initializeFromFunction) method which constructs node from given annotated function.
@sa FunctionLibrary.py
"""

import weakref
from multipledispatch import dispatch
from nine import str

from Qt import QtCore
from Qt import QtGui
from Qt import QtSvg
from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsPixmapItem
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsObject
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QTextBrowser
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QGraphicsLinearLayout
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QColorDialog
from Qt.QtWidgets import QMenu

from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Canvas.UIPinBase import (
    UIPinBase,
    getUIPinInstance,
    UIGroupPinBase
)
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Widgets.InputWidgets import createInputWidget
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Widgets.EditableLabel import EditableLabel
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget, PropertiesWidget
from PyFlow.UI.UIInterfaces import IPropertiesViewSupport
from PyFlow.UI.Canvas.NodeActionButton import NodeActionButtonBase
from PyFlow.UI import RESOURCES_DIR
from PyFlow.Core.NodeBase import NodeBase
from PyFlow.Core.Common import *

from collections import OrderedDict

UI_NODES_FACTORIES = {}


class CollapseNodeActionButton(NodeActionButtonBase):
    """docstring for CollapseNodeActionButton."""
    def __init__(self, svgFilePath, action, uiNode):
        super(CollapseNodeActionButton, self).__init__(svgFilePath, action, uiNode)
        self.svgIcon.setElementId("Collapse")

    def mousePressEvent(self, event):
        super(CollapseNodeActionButton, self).mousePressEvent(event)
        if self.parentItem().collapsed:
            self.svgIcon.setElementId("Expand")
        else:
            self.svgIcon.setElementId("Collapse")


class NodeName(QGraphicsWidget):
    """docstring for NodeName"""
    def __init__(self, parent=None):
        super(NodeName, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self.setGraphicsItem(self)
        self.hovered = False
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def IsRenamable(self):
        return False

    def hoverEnterEvent(self, event):
        super(NodeName, self).hoverEnterEvent(event)
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        super(NodeName, self).hoverLeaveEvent(event)
        self.hovered = False
        self.update()

    def sizeHint(self, which, constraint):
        nameFont = self.parentItem().nodeNameFont
        typeFont = self.parentItem().nodeTypeFont

        nameTextWidth = QtGui.QFontMetrics(nameFont).width(self.parentItem().displayName) + NodeDefaults().CONTENT_MARGINS * 2
        nameTextHeight = QtGui.QFontMetrics(nameFont).height()

        typeTextWidth = QtGui.QFontMetrics(nameFont).width(self.parentItem().displayName) + NodeDefaults().CONTENT_MARGINS * 2
        typeTextHeight = QtGui.QFontMetrics(typeFont).height()

        return QtCore.QSizeF(max(nameTextWidth, typeTextWidth), nameTextHeight + typeTextHeight)

    def setGeometry(self, rect):
        self.prepareGeometryChange()
        super(QGraphicsWidget, self).setGeometry(rect)
        self.setPos(rect.topLeft())

    def paint(self, painter, option, widget):
        lod = self.parentItem().canvasRef().getLodValueFromCurrentScale(3)
        frame = QtCore.QRectF(QtCore.QPointF(0, 0), self.geometry().size())

        if lod < 3:
            nodeName = self.parentItem().name
            nodeType = self.parentItem()._rawNode.__class__.__name__
            nodeResizable = self.parentItem().resizable
            painter.setFont(self.parentItem().nodeNameFont)
            painter.setPen(QtGui.QPen(self.parentItem().labelTextColor, 0.7))
            width = QtGui.QFontMetrics(painter.font()).width(nodeName)
            height = QtGui.QFontMetrics(painter.font()).height()
            yCenter = (frame.height() / 2) + (height / 2.5)
            x = PinDefaults().PIN_SIZE / 2

            painter.drawText(x, yCenter - height / 2, nodeName)
            painter.setFont(self.parentItem().nodeTypeFont)
            painter.setPen(QtGui.QPen(self.parentItem().typeTextColor, 0.5))
            height = QtGui.QFontMetrics(painter.font()).height()
            painter.drawText(x, yCenter + height / 3, nodeType)


class UINodeBase(QGraphicsWidget, IPropertiesViewSupport):
    """
    Default node description
    """
    # Event called when node name changes
    displayNameChanged = QtCore.Signal(str)

    def __init__(self, raw_node, w=80, color=Colors.NodeBackgrounds, headColorOverride=None):
        super(UINodeBase, self).__init__()
        self.setFlag(QGraphicsWidget.ItemIsMovable)
        self.setFlag(QGraphicsWidget.ItemIsFocusable)
        self.setFlag(QGraphicsWidget.ItemIsSelectable)
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAcceptHoverEvents(True)
        self._rawNode = raw_node
        self._rawNode.setWrapper(self)
        self._rawNode.killed.connect(self.kill)
        self._rawNode.tick.connect(self.Tick)

        self.custom_widget_data = {}
        # node name
        self._displayName = self.name

        # GUI Layout
        self.opt_node_base_color = Colors.NodeBackgrounds
        self.opt_selected_pen_color = Colors.NodeSelectedPenColor
        self.opt_pen_selected_type = QtCore.Qt.SolidLine
        self._collapsed = False
        self._left_stretch = 0
        self.color = color
        self.drawlabel = True
        self.headColorOverride = headColorOverride
        self.headColor = headColorOverride
        self.height_offset = 3
        self._w = 0
        self.h = 25
        self.minWidth = 25
        self.minHeight = self.h
        self._labelTextColor = QtCore.Qt.white
        self._typeTextColor = QtCore.Qt.white

        self.drawLayoutsDebug = False
        self.nodeLayout = QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.nodeLayout.setContentsMargins(NodeDefaults().CONTENT_MARGINS,
                                           NodeDefaults().CONTENT_MARGINS,
                                           NodeDefaults().CONTENT_MARGINS,
                                           NodeDefaults().CONTENT_MARGINS)
        self.nodeLayout.setSpacing(NodeDefaults().LAYOUTS_SPACING)
        self.nodeNameFont = QtGui.QFont("Consolas")
        self.nodeNameFont.setPointSize(6)

        self.nodeTypeFont = QtGui.QFont("Consolas")
        self.nodeTypeFont.setPointSize(4)
        self.nodeTypeFont.setItalic(True)

        self.headerLayout = QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.nodeLayout.addItem(self.headerLayout)
        self.nodeNameWidget = NodeName(self)
        self.headerLayout.addItem(self.nodeNameWidget)
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout.setSpacing(3)

        self.nameActionsSpacer = QGraphicsWidget()
        self.nameActionsSpacer.setObjectName("nameActionsSpacer")
        self.nameActionsSpacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.headerLayout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.headerLayout.addItem(self.nameActionsSpacer)
        self.headerLayout.setMaximumHeight(self.labelHeight)

        self.pinsLayout = QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.pinsLayout.setContentsMargins(0, 0, 0, 0)
        self.pinsLayout.setSpacing(NodeDefaults().LAYOUTS_SPACING)
        self.nodeLayout.addItem(self.pinsLayout)
        self.nodeLayout.setStretchFactor(self.pinsLayout, 2)
        self.inputsLayout = QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.inputsLayout.setContentsMargins(0, 0, 0, 0)
        self.inputsLayout.setSpacing(NodeDefaults().LAYOUTS_SPACING)
        self.outputsLayout = QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.outputsLayout.setContentsMargins(0, 0, 0, 0)
        self.outputsLayout.setSpacing(NodeDefaults().LAYOUTS_SPACING)
        self.pinsLayout.addItem(self.inputsLayout)
        self.pinLayoutSpacer = QGraphicsWidget()
        self.pinLayoutSpacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pinLayoutSpacer.setObjectName("pinLayoutSpacer")
        self.pinsLayout.addItem(self.pinLayoutSpacer)
        self.pinsLayout.addItem(self.outputsLayout)
        self.setLayout(self.nodeLayout)
        self.svgIcon = QtSvg.QGraphicsSvgItem(self)
        self.svgIcon.setPos(-6, -6)

        self._image = None
        self.canvasRef = None
        self._menu = QMenu()

        # Resizing Options
        self.initialRectWidth = self.minWidth
        self.initialRectHeight = self.minHeight
        self.expanded = True
        self.resizable = False
        self.bResize = False
        self.resizeDirection = (0, 0)
        self.resizeStripsSize = 2
        self.resizeStrips = [0, 0, 0, 0, 0]  # Left, Top, Right, Bottom, BottomRight

        self.lastMousePos = QtCore.QPointF()

        # Hiding/Moving By Group/collapse/By Pin
        self.edgesToHide = []
        self.nodesNamesToMove = []
        self.pinsToMove = {}
        self._rect = QtCore.QRectF(0, 0, self.minWidth, self.minHeight)

        # Group pins
        self.inputGroupPins = {}
        self.outputGroupPins = {}

        # Action buttons
        self._actionButtons = set()

        # Core nodes support
        self.isTemp = False
        self.isCommentNode = False

        # collapse action
        self.actionToggleCollapse = self._menu.addAction("ToggleCollapse")
        self.actionToggleCollapse.setToolTip("Toggles node's body collapsed or not")
        self.actionToggleCollapse.triggered.connect(self.toggleCollapsed)
        self.actionToggleCollapse.setData(NodeActionButtonInfo(RESOURCES_DIR + "/nodeCollapse.svg", CollapseNodeActionButton))

    def toggleCollapsed(self):
        self.collapsed = not self.collapsed

    def aboutToCollapse(self, futureCollapseState):
        """Called before collapsing or expanding."""
        pass

    @property
    def collapsed(self):
        return self._collapsed

    @collapsed.setter
    def collapsed(self, bCollapsed):
        if bCollapsed != self._collapsed:
            self._collapsed = bCollapsed
            self.aboutToCollapse(self._collapsed)
            for i in range(0, self.inputsLayout.count()):
                inp = self.inputsLayout.itemAt(i)
                inp.setVisible(not bCollapsed)
            for o in range(0, self.outputsLayout.count()):
                out = self.outputsLayout.itemAt(o)
                out.setVisible(not bCollapsed)
            self.pinLayoutSpacer.setVisible(not bCollapsed)
            self.updateNodeShape()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.svgIcon.renderer().load(value)
        elementName = QtCore.QFileInfo(value).baseName()
        self.svgIcon.setElementId(elementName)
        # self.svgIcon.setPos(self.geometry().topRight())

    def getImageDrawRect(self):
        topRight = self.boundingRect().topRight()
        topRight.setY(-12)
        topRight.setX(self.boundingRect().width() - 12)
        r = self.boundingRect()
        r.setWidth(24)
        r.setHeight(24)
        r.translate(topRight)
        return r

    @property
    def typeTextColor(self):
        return self._typeTextColor

    @typeTextColor.setter
    def typeTextColor(self, value):
        self._typeTextColor = value

    @property
    def labelTextColor(self):
        return self._labelTextColor

    @labelTextColor.setter
    def labelTextColor(self, value):
        self._labelTextColor = value

    def __repr__(self):
        graphName = self._rawNode.graph().name if self._rawNode.graph is not None else str(None)
        return "<class[{0}]; name[{1}]; graph[{2}]>".format(self.__class__.__name__, self.getName(), graphName)

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(self.getNodeWidth(), self.getNodeHeight())

    def setGeometry(self, rect):
        self.prepareGeometryChange()
        super(QGraphicsWidget, self).setGeometry(rect)
        self.setPos(rect.topLeft())

    @property
    def uid(self):
        return self._rawNode._uid

    @uid.setter
    def uid(self, value):
        self._rawNode._uid = value

    @property
    def name(self):
        return self._rawNode.name

    @name.setter
    def name(self, value):
        self._rawNode.setName(value)

    @property
    def displayName(self):
        return self._displayName

    @displayName.setter
    def displayName(self, value):
        self._displayName = value
        self.displayNameChanged.emit(self._displayName)
        self.updateNodeShape()

    @property
    def pins(self):
        return self._rawNode.pins

    @property
    def UIPins(self):
        result = OrderedDict()
        for rawPin in self._rawNode.pins:
            uiPinRef = rawPin.getWrapper()
            if uiPinRef is not None:
                result[rawPin.uid] = uiPinRef()
        return result

    @property
    def UIinputs(self):
        result = OrderedDict()
        for rawPin in self._rawNode.pins:
            if rawPin.direction == PinDirection.Input:
                result[rawPin.uid] = rawPin.getWrapper()()
        return result

    @property
    def UIoutputs(self):
        result = OrderedDict()
        for rawPin in self._rawNode.pins:
            if rawPin.direction == PinDirection.Output:
                result[rawPin.uid] = rawPin.getWrapper()()
        return result

    @property
    def namePinOutputsMap(self):
        result = OrderedDict()
        for rawPin in self._rawNode.pins:
            if rawPin.direction == PinDirection.Output:
                result[rawPin.name] = rawPin.getWrapper()()
        return result

    @property
    def namePinInputsMap(self):
        result = OrderedDict()
        for rawPin in self._rawNode.pins:
            if rawPin.direction == PinDirection.Input:
                result[rawPin.name] = rawPin.getWrapper()()
        return result

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value

    def getName(self):
        return self._rawNode.getName()

    def isRenamable(self):
        return False

    def setName(self, name):
        self._rawNode.setName(name)

    def getPin(self, name, pinsGroup=PinSelectionGroup.BothSides):
        pin = self._rawNode.getPin(str(name), pinsGroup)
        if pin is not None:
            if pin.getWrapper() is not None:
                return pin.getWrapper()()
        return None

    @staticmethod
    def removePinByName(node, name):
        pin = node.getPin(name)
        if pin:
            pin.kill()

    @staticmethod
    def recreate(node):
        templ = node.serialize()
        uid = node.uid
        node.kill()
        newNode = node.canvas.createNode(templ)
        newNode.uid = uid
        return newNode

    @property
    def isCompoundNode(self):
        return self._rawNode.isCompoundNode

    # TODO: add this to ui node interface
    def serializationHook(self):
        # this will be called by raw node
        # to gather ui specific info
        template = {}
        if self.resizable:
            template['resize'] = {'w': self._rect.right(), 'h': self._rect.bottom()}
        template['displayName'] = self.displayName
        template['collapsed'] = self.collapsed
        return template

    def serialize(self):
        return self._rawNode.serialize()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self._rawNode.setPosition(value.x(), value.y())
        return super(UINodeBase, self).itemChange(change, value)

    def autoAffectPins(self):
        self._rawNode.autoAffectPins()

    def postCreate(self, jsonTemplate=None):
        # create ui pin wrappers
        for i in self._rawNode.getOrderedPins():
            self._createUIPinWrapper(i)

        self.updateNodeShape()
        self.setPos(self._rawNode.x, self._rawNode.y)

        if self.canvasRef().graphManager.activeGraph() != self._rawNode.graph():
            self.hide()

        if not self.drawlabel:
            self.nodeNameWidget.hide()

        if self.headColorOverride is None:
            if self.isCallable():
                self.headColor = NodeDefaults().CALLABLE_NODE_HEAD_COLOR
            else:
                self.headColor = NodeDefaults().PURE_NODE_HEAD_COLOR
        else:
            self.headColor = self.headColorOverride

        self.createActionButtons()

        if jsonTemplate is not None:
            if "collapsed" in jsonTemplate["wrapper"]:
                self.collapsed = jsonTemplate["wrapper"]["collapsed"]

        self.setToolTip(self.description())
        if self.resizable:
            w = self.getNodeWidth()
            h = self.getNodeHeight()
            if jsonTemplate is not None:
                if "resize" in jsonTemplate["wrapper"]:
                    w = jsonTemplate["wrapper"]["resize"]["w"]
                    h = jsonTemplate["wrapper"]["resize"]["h"]
            self._rect.setWidth(w)
            self._rect.setHeight(h)
            self.updateNodeShape()

    def createActionButtons(self):
        # NOTE: actions with action button class specified will be added next to node name
        for action in self._menu.actions():
            actionData = action.data()
            if isinstance(actionData, NodeActionButtonInfo):
                actionButtonClass = actionData.actionButtonClass()
                svgFilePath = actionData.filePath()
                if actionButtonClass is None:
                    actionButtonClass = NodeActionButtonBase
                self.headerLayout.addItem(actionButtonClass(svgFilePath, action, self))
                action.setVisible(False)

    def isCallable(self):
        return self._rawNode.isCallable()

    def category(self):
        return self._rawNode.category()

    def description(self):
        return self._rawNode.description()

    @property
    def packageName(self):
        return self._rawNode.packageName

    def getData(self, pinName):
        if pinName in [p.name for p in self.inputs.values()]:
            p = self.getPin(pinName, PinSelectionGroup.Inputs)
            return p.getData()

    def setData(self, pinName, data):
        if pinName in [p.name for p in self.outputs.values()]:
            p = self.getPin(pinName, PinSelectionGroup.Outputs)
            p.setData(data)

    @property
    def labelHeight(self):
        return self.nodeNameWidget.sizeHint(None, None).height()

    @property
    def labelWidth(self):
        headerWidth = QtGui.QFontMetrics(self.nodeNameFont).width(self.displayName) + NodeDefaults().CONTENT_MARGINS * 2

        # actions width. 10 is svg icon size, probably need to move this value to some preferences
        numActions = len(self._actionButtons)
        headerWidth += numActions * 10
        headerWidth += numActions * self.headerLayout.spacing()
        if self.collapsed and not self.resizable:
            headerWidth += self.nameActionsSpacer.boundingRect().width()
        headerWidth += self.headerLayout.spacing() + NodeDefaults().CONTENT_MARGINS * 2
        return headerWidth

    def getNodeWidth(self):
        width = self.getPinsWidth() + self.pinsLayout.spacing() * 2
        if self.resizable:
            width = max(self._rect.width(), width)
        width = max(width, self.labelWidth)
        return width

    def getNodeHeight(self):
        h = self.nodeNameWidget.sizeHint(None, None).height()
        h += self.nodeLayout.spacing()
        try:
            numInputs = len(self.UIinputs)
            numOutputs = len(self.UIoutputs)
            pins = self.UIinputs.values() if numInputs > numOutputs else self.UIoutputs.values()
            h += NodeDefaults().CONTENT_MARGINS * 2

            for pin in pins:
                if pin.isVisible():
                    h += pin.sizeHint(None, None).height() + NodeDefaults().LAYOUTS_SPACING
        except:
            pass

        if h < self.minHeight:
            h = self.minHeight

        if self.resizable:
            h = max(self._rect.height(), h)

        if self.collapsed:
            h = self.minHeight

        return h

    def getPinsWidth(self):
        iwidth = 0
        owidth = 0
        pinwidth = 0
        pinwidth2 = 0
        for i in self.UIPins.values():
            if i.direction == PinDirection.Input:
                iwidth = max(iwidth, i.sizeHint(None, None).width())
                # pinwidth = max(pinwidth, i.width)
            else:
                owidth = max(owidth, i.sizeHint(None, None).width())
                # pinwidth2 = max(pinwidth2, i.width)
        return iwidth + owidth + pinwidth + pinwidth2 + Spacings.kPinOffset

    def invalidateNodeLayouts(self):
        self.inputsLayout.invalidate()
        self.outputsLayout.invalidate()
        self.pinsLayout.invalidate()
        self.headerLayout.invalidate()
        self.nodeLayout.invalidate()

    def updateNodeShape(self):
        self.prepareGeometryChange()
        self.invalidateNodeLayouts()
        self.updateGeometry()
        self.update()
        self.canvasRef().update()

    def onChangeColor(self, label=False):
        res = QColorDialog.getColor(self.color, None, 'Node color setup')
        if res.isValid():
            res.setAlpha(80)
            self.color = res
            if label:
                # self.label().color = res
                self.update()
                # self.label().update()

    def getCollidingNodes(self):
        collidingItems = self.collidingItems()
        collidingNodes = set()
        for item in collidingItems:
            node = item.topLevelItem()
            if node is not self and isinstance(node, UINodeBase):
                collidingNodes.add(node)
        return collidingNodes

    def translate(self, x, y):
        super(UINodeBase, self).moveBy(x, y)

    def paint(self, painter, option, widget):
        NodePainter.default(self, painter, option, widget)
        if self.drawLayoutsDebug:
            painter.drawRect(self.headerLayout.geometry())
            painter.drawRect(self.nodeLayout.geometry())
            painter.drawRect(self.inputsLayout.geometry())
            painter.drawRect(self.outputsLayout.geometry())

    def shouldResize(self, cursorPos):
        result = {"resize": False, "direction": self.resizeDirection}
        if self.resizeStrips[0] == 1:
            result["resize"] = True
            result["direction"] = (-1, 0)
        if self.resizeStrips[1] == 1:
            result["resize"] = True
            result["direction"] = (0, -1)
        if self.resizeStrips[2] == 1:
            result["resize"] = True
            result["direction"] = (1, 0)
        elif self.resizeStrips[3] == 1:
            result["resize"] = True
            result["direction"] = (0, 1)
        elif self.resizeStrips[4] == 1:
            result["resize"] = True
            result["direction"] = (1, 1)
        return result

    def contextMenuEvent(self, event):
        self._menu.exec_(event.screenPos())

    def mousePressEvent(self, event):
        self.update()
        super(UINodeBase, self).mousePressEvent(event)
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
        super(UINodeBase, self).mouseMoveEvent(event)
        # resize
        if self.bResize:
            delta = event.scenePos() - self.mousePressPos
            if self.resizeDirection == (1, 0):
                # right connection resize
                newWidth = delta.x() + self.initialRectWidth
                if newWidth > self.minWidth:
                    self._rect.setWidth(newWidth)
                    self.w = newWidth
                    self.updateNodeShape()
            elif self.resizeDirection == (0, 1):
                newHeight = delta.y() + self.initialRectHeight
                if newHeight > self.minHeight:
                    self._rect.setHeight(newHeight)
                    self.updateNodeShape()
            elif self.resizeDirection == (-1, 0):
                # left connection resize
                posdelta = self.mapToScene(event.pos()) - self.origPos
                posdelta2 = self.mapToScene(event.pos()) - self.initPos
                newWidth = -posdelta2.x() + self.initialRectWidth
                if newWidth > self.minWidth:
                    self.translate(posdelta.x(), 0)
                    self.origPos = self.pos()
                    self._rect.setWidth(newWidth)
                    self.updateNodeShape()
            elif self.resizeDirection == (1, 1):
                newWidth = delta.x() + self.initialRectWidth
                newHeight = delta.y() + self.initialRectHeight
                if newWidth > self.minWidth:
                    self._rect.setWidth(newWidth)
                    self.w = newWidth
                    self.updateNodeShape()
                if newHeight > self.minHeight:
                    self._rect.setHeight(newHeight)
                    self.updateNodeShape()
            self.update()
        self.lastMousePos = event.pos()

    def mouseReleaseEvent(self, event):
        self.bResize = False
        self.update()
        super(UINodeBase, self).mouseReleaseEvent(event)

    def clone(self):
        templ = self.serialize()
        templ['name'] = self.name
        templ['uuid'] = str(uuid.uuid4())
        for inp in templ['inputs']:
            inp['uuid'] = str(uuid.uuid4())
        for out in templ['outputs']:
            out['uuid'] = str(uuid.uuid4())
        new_node = self.canvasRef().createNode(templ)
        return new_node

    def call(self, name):
        self._rawNode.call(name)

    def createPropertiesWidget(self, propertiesWidget):
        baseCategory = CollapsibleFormWidget(headName="Base")

        le_name = QLineEdit(self.getName())
        le_name.setReadOnly(True)
        # if self.label().IsRenamable():
        #     le_name.setReadOnly(False)
        #     le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        baseCategory.addWidget("Name", le_name)

        leUid = QLineEdit(str(self._rawNode.graph().name))
        leUid.setReadOnly(True)
        baseCategory.addWidget("Owning graph", leUid)

        text = "{0}".format(self.packageName)
        if self._rawNode.lib:
            text += " | {0}".format(self._rawNode.lib)
        text += " | {0}".format(self._rawNode.__class__.__name__)
        leType = QLineEdit(text)
        leType.setReadOnly(True)
        baseCategory.addWidget("Type", leType)

        propertiesWidget.addWidget(baseCategory)

        # inputs
        if len([i for i in self.UIinputs.values()]) != 0:
            inputsCategory = CollapsibleFormWidget(headName="Inputs")
            sortedInputs = sorted(self.UIinputs.values(), key=lambda x: x.name)
            for inp in sortedInputs:
                if inp.isList():
                    # TODO: create list input widget
                    continue
                dataSetter = inp.call if inp.isExec() else inp.setData
                w = createInputWidget(inp.dataType, dataSetter, inp.defaultValue())
                if w:
                    inp.dataBeenSet.connect(w.setWidgetValueNoSignals)
                    w.blockWidgetSignals(True)
                    w.setWidgetValue(inp.currentData())
                    w.blockWidgetSignals(False)
                    w.setObjectName(inp.getName())
                    inputsCategory.addWidget(inp.name, w)
                    if inp.hasConnections():
                        w.setEnabled(False)
            propertiesWidget.addWidget(inputsCategory)

        Info = CollapsibleFormWidget(headName="Info", collapsed=True)
        doc = QTextBrowser()
        doc.setOpenExternalLinks(True)
        doc.setHtml(self.description())
        Info.addWidget(widget=doc)
        propertiesWidget.addWidget(Info)

    def getChainedNodes(self):
        nodes = []
        for pin in self.UIinputs.values():
            for connection in pin.connections:
                node = connection.source().topLevelItem()  # topLevelItem
                nodes.append(node)
                nodes += node.getChainedNodes()
        return nodes

    def kill(self, *args, **kwargs):
        self.scene().removeItem(self)
        del(self)

    def collidesWithCommentNode(self):
        nodes = self.getCollidingNodes()
        result = None
        for n in nodes:
            if n.isCommentNode:
                result = n
                break
        return result

    def handleVisibility(self):
        if self._rawNode.graph() != self.canvasRef().graphManager.activeGraph():
            # if current graph != node's graph - hide node and connections
            self.hide()
            for uiPin in self.UIPins.values():
                for connection in uiPin.uiConnectionList:
                    connection.hide()
        else:
            # if current graph == node's graph - show it only if its not under collapsed comment node
            collidedCommentNode = self.collidesWithCommentNode()
            if collidedCommentNode is None:
                self.show()
                for uiPin in self.UIPins.values():
                    for connection in uiPin.uiConnectionList:
                        connection.show()
            else:
                if collidedCommentNode.collapsed:
                    self.hide()
                else:
                    self.show()

    def hoverLeaveEvent(self, event):
        self.resizeStrips = [0, 0, 0, 0, 0]
        self.update()

    def hoverMoveEvent(self, event):
        if self.resizable and not self.collapsed:
            height = self.geometry().height()
            width = self.geometry().width()
            rf = NodeDefaults().CORNERS_ROUND_FACTOR

            leftStrip = QtCore.QRectF(0, rf, self.resizeStripsSize, height - rf * 2)
            topStrip = QtCore.QRectF(rf, 0, width - rf * 2, self.resizeStripsSize)
            rightStrip = QtCore.QRectF(width - self.resizeStripsSize, rf, self.resizeStripsSize, height - rf * 2)
            bottomStrip = QtCore.QRectF(rf, height - self.resizeStripsSize, width - rf * 2, self.resizeStripsSize)
            bottomRightStrip = QtCore.QRectF(width - rf, height - rf, rf, rf)

            # detect where on the node
            self.resizeStrips[0] = 1 if leftStrip.contains(event.pos()) else 0
            self.resizeStrips[1] = 1 if topStrip.contains(event.pos()) else 0
            self.resizeStrips[2] = 1 if rightStrip.contains(event.pos()) else 0
            self.resizeStrips[3] = 1 if bottomStrip.contains(event.pos()) else 0
            self.resizeStrips[4] = 1 if bottomRightStrip.contains(event.pos()) else 0
            self.update()

    def Tick(self, delta, *args, **kwargs):
        # NOTE: Do not call wrapped raw node Tick method here!
        # this ui node tick called from underlined raw node's emitted signal
        # do here only UI stuff
        # self.handleVisibility()
        pass

    def addGroupContainer(self, portType, groupName="group"):
        container = QGraphicsWidget()
        container.setObjectName('{0}PinGroupContainerWidget'.format(self.name))
        lyt = QGraphicsLinearLayout()
        lyt.setOrientation(QtCore.Qt.Vertical)
        lyt.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        lyt.setContentsMargins(1, 1, 1, 1)
        container.group_name = EditableLabel(name=groupName, node=self, canvas=self.canvasRef())
        font = QtGui.QFont('Consolas')
        font.setBold(True)
        font.setPointSize(500)
        container.group_name._font = font
        container.group_name.nameLabel.setFont(font)
        container.group_name.nameLabel.update()
        container.group_name.setObjectName(
            '{0}_GroupConnector'.format(container.group_name))
        container.group_name.setContentsMargins(0, 0, 0, 0)
        container.group_name.setColor(Colors.AbsoluteBlack)
        grpCon = self.addContainer()
        container.groupIcon = UIGroupPinBase(container)
        lyt.addItem(grpCon)
        container.setLayout(lyt)
        if portType == PinDirection.Input:
            container.group_name.nameLabel.setAlignment(
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            grpCon.layout().addItem(container.groupIcon)
            grpCon.layout().addItem(container.group_name)
        else:
            container.group_name.nameLabel.setAlignment(
                QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            grpCon.layout().addItem(container.group_name)
            grpCon.layout().addItem(container.groupIcon)
        return container

    def addContainer(self):
        container = QGraphicsWidget()
        container.setObjectName('{0}PinContainerWidget'.format(self.name))
        container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        container.sizeHint(QtCore.Qt.MinimumSize, QtCore.QSizeF(50.0, 10.0))
        lyt = QGraphicsLinearLayout()
        lyt.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        lyt.setContentsMargins(1, 1, 1, 1)
        container.setLayout(lyt)
        return container

    def _createUIPinWrapper(self, rawPin, index=-1, group=None, linkedPin=None):
        wrapper = rawPin.getWrapper()
        if wrapper is not None:
            return wrapper()

        p = getUIPinInstance(self, rawPin)
        p.call = rawPin.call

        name = rawPin.name
        lblName = name
        if rawPin.direction == PinDirection.Input:
            self.inputsLayout.addItem(p)
            self.inputsLayout.setAlignment(p, QtCore.Qt.AlignLeft)

        elif rawPin.direction == PinDirection.Output:
            self.outputsLayout.addItem(p)
            self.outputsLayout.setAlignment(p, QtCore.Qt.AlignRight)

        p.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.update()
        # self.nodeMainGWidget.update()
        self.updateNodeShape()
        p.syncDynamic()
        p.syncRenamable()
        if self.collapsed:
            p.hide()
        return p

    def collapsePinGroup(self, container):
        for i in range(1, container.layout().count()):
            item = container.layout().itemAt(i)
            pin = item.layout().itemAt(0) if isinstance(
                item.layout().itemAt(0), UIPinBase) else item.layout().itemAt(1)
            if pin.hasConnections:
                if pin.direction == PinDirection.Input:
                    for ege in pin.connections:
                        ege.drawDestination = container.layout().itemAt(0).layout().itemAt(0)
                if pin.direction == PinDirection.Output:
                    for ege in pin.connections:
                        ege.drawSource = container.layout().itemAt(0).layout().itemAt(1)
            item.hide()

    def expandPinGroup(self, container):
        for i in range(1, container.layout().count()):
            item = container.layout().itemAt(i)
            pin = item.layout().itemAt(0) if isinstance(
                item.layout().itemAt(0), UIPinBase) else item.layout().itemAt(1)
            if pin.hasConnections:
                if pin.direction == PinDirection.Input:
                    for ege in pin.connections:
                        ege.drawDestination = pin
                if pin.direction == PinDirection.Output:
                    for ege in pin.connections:
                        ege.drawSource = pin
            item.show()


def REGISTER_UI_NODE_FACTORY(packageName, factory):
    if packageName not in UI_NODES_FACTORIES:
        UI_NODES_FACTORIES[packageName] = factory
        print("registering", packageName, "ui nodes")


def getUINodeInstance(raw_instance):
    packageName = raw_instance.packageName
    instance = None
    if packageName in UI_NODES_FACTORIES:
        instance = UI_NODES_FACTORIES[packageName](raw_instance)
    assert(instance is not None)
    return instance
