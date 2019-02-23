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
from Qt.QtWidgets import QMenu

from PyFlow.UI.UIPinBase import UIPinBase
from PyFlow.UI.InputWidgets import createInputWidget
from PyFlow.UI.NodePainter import NodePainter
from PyFlow.UI.IContextMenu import IContextMenu
from PyFlow.Core.Enums import ENone
from PyFlow.Core.AGraphCommon import *


UI_NODES_FACTORIES = {}


class NodeName(QGraphicsTextItem):
    def __init__(self, parent, bUseTextureBg=True, color=Colors.Green):
        super(NodeName, self).__init__(parent)
        self.setParentItem(parent)
        self.bUseTextureBg = bUseTextureBg
        self.width = 50
        self.document().contentsChanged.connect(self.onDocContentsChanged)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.desc = parent._rawNode.description()
        self.descFontPen = QtGui.QPen(QtCore.Qt.gray, 0.5)
        self.defaultHeight = 30
        self.h = self.defaultHeight
        self.text_color = Colors.PinNameColor
        self.setDefaultTextColor(self.text_color)
        self.opt_font = QtGui.QFont('Consolas')
        self.opt_font_size = 8
        self.opt_font.setPointSize(self.opt_font_size)
        self.setFont(self.opt_font)
        self.descFont = QtGui.QFont("Consolas", self.opt_font.pointSize() / 2.0, 2, True)
        self.setPos(0, -self.boundingRect().height() - 8)
        self.color = color
        self.clipRect = None
        self.roundCornerFactor = 1.0
        self.bg = QtGui.QImage(':/icons/resources/white.png')
        self.icon = None

    def onDocContentsChanged(self):
        self.width = QtGui.QFontMetricsF(self.font()).width(self.toPlainText()) + 5.0

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
        r = QtCore.QRectF(option.rect)
        r.setWidth(self.parentItem().childrenBoundingRect().width() - 0.25)
        r.setX(0.25)
        r.setY(0.25)
        b = QtGui.QLinearGradient(0, 0, 0, r.height())
        b.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
        b.setColorAt(0.25, self.color)
        b.setColorAt(1, self.color)
        painter.setPen(QtCore.Qt.NoPen)
        if self.bUseTextureBg:
            b = QtGui.QBrush(self.bg)
            b.setStyle(QtCore.Qt.TexturePattern)
            painter.setBrush(b)
        else:
            painter.setBrush(self.color)
            b.setStyle(QtCore.Qt.SolidPattern)
        painter.drawRoundedRect(r, self.roundCornerFactor, self.roundCornerFactor)
        parentRet = self.parentItem().childrenBoundingRect()
        if self.icon:
            painter.drawImage(QtCore.QRect(parentRet.width() - 9, 0, 8, 8), self.icon, QtCore.QRect(0, 0, self.icon.width(), self.icon.height()))

        super(NodeName, self).paint(painter, option, widget)

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
    def __init__(self, raw_node, w=80, color=Colors.NodeBackgrounds, headColor=Colors.NodeNameRect, bUseTextureBg=True):
        super(UINodeBase, self).__init__()
        self._rawNode = raw_node
        self._rawNode.setWrapper(self)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.opt_node_base_color = Colors.NodeBackgrounds
        self.opt_selected_pen_color = Colors.NodeSelectedPenColor
        self.opt_pen_selected_type = QtCore.Qt.SolidLine
        self._left_stretch = 0
        self.color = color
        self.height_offset = 3
        self.nodeMainGWidget = QGraphicsWidget()
        self.nodeMainGWidget.setObjectName('{0}MainLayout'.format(self._rawNode.__class__.__name__))
        self._w = 0
        self.h = 40
        self.sizes = [0, 0, self.w, self.h, 1, 1]
        self.w = w
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.custom_widget_data = {}
        # node name
        self.label = weakref.ref(NodeName(self, bUseTextureBg, headColor))
        # set node layouts
        self.nodeMainGWidget.setParentItem(self)
        # main
        self.portsMainLayout = QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.portsMainLayout.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.portsMainLayout.setContentsMargins(1, 1, 1, 1)
        self.nodeMainGWidget.setLayout(self.portsMainLayout)
        self.nodeMainGWidget.setX(self.nodeMainGWidget.x())
        # inputs layout
        self.inputsLayout = QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.inputsLayout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.inputsLayout.setContentsMargins(1, 1, 1, 1)
        self.portsMainLayout.addItem(self.inputsLayout)
        # outputs layout
        self.outputsLayout = QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.outputsLayout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.outputsLayout.setContentsMargins(1, 1, 1, 1)
        self.portsMainLayout.addItem(self.outputsLayout)

        self.setZValue(1)
        self.setCursor(QtCore.Qt.OpenHandCursor)

        self.tweakPosition()
        self.icon = None
        self.UIPins = {}
        self._menu = QMenu()

    def contextMenuEvent(self, event):
        self._menu.exec_(event.screenPos())

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

    @staticmethod
    def recreate(node):
        templ = node.serialize()
        uid = node.uid
        node.kill()
        newNode = node.graph().createNode(templ)
        newNode.uid = uid
        return newNode

    def getPinByName(self, name, pinsGroup=PinSelectionGroup.BothSides):
        return self._rawNode.getPinByName(name, pinsGroup)

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        self.sizes[2] = value

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

    def isCallable(self):
        return self._rawNode.isCallable()

    def tweakPosition(self):
        value = self.scenePos()
        self.setX(roundup(value.x() - GRID_SIZE, GRID_SIZE))
        self.setY(roundup(value.y() - GRID_SIZE, GRID_SIZE))

    def boundingRect(self):
        return self.childrenBoundingRect()

    def itemChange(self, change, value):
        if change == self.ItemPositionChange:
            # grid snapping
            value.setX(roundup(value.x() - GRID_SIZE + GRID_SIZE / 3.0, GRID_SIZE))
            value.setY(roundup(value.y() - GRID_SIZE + GRID_SIZE / 3.0, GRID_SIZE))
            value.setY(value.y() - 2)
            return value
        return QGraphicsItem.itemChange(self, change, value)

    @property
    def uid(self):
        return self._rawNode._uid

    @uid.setter
    def uid(self, value):
        self._rawNode.uid = value

    def category(self):
        return self._rawNode.category()

    def updateNodeShape(self, label=None):
        for i in range(0, self.inputsLayout.count()):
            container = self.inputsLayout.itemAt(i)
            lyt = container.layout()
            if lyt:
                for j in range(0, lyt.count()):
                    lyt.setAlignment(lyt.itemAt(j), QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        for i in range(0, self.outputsLayout.count()):
            container = self.outputsLayout.itemAt(i)
            lyt = container.layout()
            if lyt:
                for j in range(0, lyt.count()):
                    lyt.setAlignment(lyt.itemAt(j), QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        self.label().setPlainText(self._rawNode.__class__.__name__)

        self.w = self.getWidth() + Spacings.kPinOffset
        self.nodeMainGWidget.setMaximumWidth(self.w)
        self.nodeMainGWidget.setGeometry(QtCore.QRectF(0, 0, self.w, self.childrenBoundingRect().height()))
        if self.isCallable():
            if 'flow' not in self.category().lower():
                if self.label().bUseTextureBg:
                    self.label().bg = QtGui.QImage(':/icons/resources/blue.png')
        else:
            if self.label().bUseTextureBg:
                self.label().bg = QtGui.QImage(':/icons/resources/green.png')
        self.setToolTip(self.description())
        self.update()

    def description(self):
        return self._rawNode.description()

    def postCreate(self, jsonTemplate=None):
        self._rawNode.postCreate(jsonTemplate)

        # create ui pin wrappers
        for uid, i in self.inputs.items():
            self._createUIPinWrapper(i)

        for uid, o in self.outputs.items():
            self._createUIPinWrapper(o)

        self.updateNodeShape(label=jsonTemplate['meta']['label'])

    def getWidth(self):
        fontWidth = QtGui.QFontMetricsF(self.label().font()).width(self.label().toPlainText()) + Spacings.kPinSpacing
        return fontWidth if fontWidth > 25 else 25

    def jsonTemplate(self):
        template = NodeBase.jsonTemplate()
        template['x'] = 0
        template['y'] = 0
        return template

    def packageName(self):
        return self._rawNode.packageName()

    def serialize(self):
        template = self._rawNode.serialize()
        template['x'] = self.scenePos().x()
        template['y'] = self.scenePos().y()
        return template

    def propertyView(self):
        return self.graph().parent.dockWidgetNodeView

    def setName(self, name):
        self._rawNode.setName(self, name)

    @property
    def graph(self):
        return self._rawNode.graph

    @graph.setter
    def graph(self, value):
        self._rawNode.graph = value

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

    def paint(self, painter, option, widget):
        NodePainter.default(self, painter, option, widget)

    def mousePressEvent(self, event):
        self.update()
        QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QGraphicsItem.mouseReleaseEvent(self, event)

    @property
    def name(self):
        return self._rawNode.name

    def propertyEditingFinished(self):
        le = QApplication.instance().focusWidget()
        if isinstance(le, QLineEdit):
            nodeName, attr = le.objectName().split('.')
            Pin = self.getPinByName(attr)
            Pin.setData(le.text())

    def getName(self):
        return self._rawNode.getName()

    def setName(self, name):
        self._rawNode.setName(name)

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
        leType = QLineEdit(self.__class__.__name__)
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
                # TODO: iterate over registered factories and create pin
                w = createInputWidget(inp.dataType, dataSetter, inp.defaultValue(), inp.getUserStruct())
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
                # TODO: iterate over registered factories and create pin
                w = createInputWidget(out.dataType, out.setData, out.defaultValue(), out.getUserStruct())
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

    def kill(self):
        for i in list(self.inputs.values()) + list(self.outputs.values()):
            for edge in i.edge_list:
                edge.kill()
        self._rawNode.kill()
        self.scene().removeItem(self)
        del(self)

    def Tick(self, delta):
        self._rawNode.Tick(delta)

    def setPosition(self, x, y):
        self._rawNode.setPosition(x, y)
        self.setPos(QtCore.QPointF(x, y))

    @staticmethod
    def removePinByName(node, name):
        pin = node.getPinByName(name)
        if pin:
            pin.kill()

    def _createUIPinWrapper(self, rawPin, index=-1):
        p = UIPinBase(self, rawPin)
        if rawPin.direction == PinDirection.Input:
            p.call = rawPin.call

        name = rawPin.name

        connector_name = QGraphicsProxyWidget()
        connector_name.setObjectName('{0}PinConnector'.format(name))
        connector_name.setContentsMargins(0, 0, 0, 0)

        lblName = name

        lbl = QLabel(lblName)
        p.nameChanged.connect(lbl.setText)
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
            p._container = container
            container.layout().addItem(connector_name)

            self.inputsLayout.insertItem(index, container)
            container.adjustSize()
        elif rawPin.direction == PinDirection.Output:
            container = self.addContainer(rawPin.direction)
            lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            container.layout().addItem(connector_name)
            container.layout().addItem(p)
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
