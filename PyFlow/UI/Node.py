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

from Pin import PinWidgetBase
from PyFlow.UI.InputWidgets import getInputWidget
from PyFlow.UI.NodePainter import NodePainter
from PyFlow.Core.Enums import ENone
from PyFlow.Core.AGraphCommon import *


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


class Node(QGraphicsItem):
    """
    Default node description
    """
    def __init__(self, raw_node, w=80, color=Colors.NodeBackgrounds, headColor=Colors.NodeNameRect, bUseTextureBg=True):
        super(Node, self).__init__()
        self._rawNode = raw_node
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

        self.inputs = {}
        self.outputs = {}

    @staticmethod
    def recreate(node):
        templ = node.serialize()
        uid = node.uid
        node.kill()
        newNode = node.graph().createNode(templ)
        newNode.uid = uid
        return newNode

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        self.sizes[2] = value

    def call(self, name):
        if pinName in [p.name for p in self.outputs.values() if p.dataType is 'ExecPin']:
            p = self._rawNode.getPinByName(pinName)
            return p.call()

    def getData(self, pinName):
        if pinName in [p.name for p in self.inputs.values()]:
            p = self._rawNode.getPinByName(pinName, PinSelectionGroup.Inputs)
            return p.getData()

    def setData(self, pinName, data):
        if pinName in [p.name for p in self.outputs.values()]:
            p = self._rawNode.getPinByName(pinName, PinSelectionGroup.Outputs)
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
        if self._rawNode._uid in self.graph().nodes:
            self.graph().nodes[value] = self.graph().nodes.pop(self._rawNode._uid)
            self._rawNode._uid = value

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

        if label is None:
            self.label().setPlainText(self.__class__.__name__)
        else:
            self.label().setPlainText(label)

        self.w = self.getWidth() + Spacings.kPinOffset
        self.nodeMainGWidget.setMaximumWidth(self.w)
        self.nodeMainGWidget.setGeometry(QtCore.QRectF(0, 0, self.w, self.childrenBoundingRect().height()))
        if self._rawNode.isCallable():
            if 'flow' not in self._rawNode.category().lower():
                if self.label().bUseTextureBg:
                    self.label().bg = QtGui.QImage(':/icons/resources/blue.png')
        else:
            if self.label().bUseTextureBg:
                self.label().bg = QtGui.QImage(':/icons/resources/green.png')
        self.setToolTip(self._rawNode.description())
        self.update()

    def postCreate(self, jsonTemplate=None):
        self._rawNode.postCreate(jsonTemplate)

        # create pins
        for i in self._rawNode.inputs.values():
            self.addInputPin(i)

        # create outputs
        for o in self._rawNode.outputs.values():
            self.addOutputPin(o)

        self.updateNodeShape(label=jsonTemplate['meta']['label'])

    def getWidth(self):
        fontWidth = QtGui.QFontMetricsF(self.label().font()).width(self.label().toPlainText()) + Spacings.kPinSpacing
        return fontWidth if fontWidth > 25 else 25

    @staticmethod
    def jsonTemplate():
        doc = '''# access pins like this\n\t# self.pinName.getData()\n\t# self.pinName.setData()'''
        doc += '''\n\t# self.getData(name) to get data from input pin by name'''
        doc += '''\n\t# self.setData(name, data) to set data to output pin by name\n'''

        template = {'package': None,
                    'type': None,
                    'x': None,
                    'y': None,
                    'name': None,
                    'uuid': None,
                    'inputs': [],
                    'outputs': [],
                    'meta': {'label': 'Node', 'var': {}}
                    }
        return template

    def serialize(self):
        template = Node.jsonTemplate()  # move this to raw node
        template['package'] = ""
        template['type'] = self._rawNode.__class__.__name__
        template['name'] = self.name
        template['x'] = self.scenePos().x()
        template['y'] = self.scenePos().y()
        template['uuid'] = str(self.uid)
        template['inputs'] = [i.serialize() for i in self.inputs.values()]
        template['outputs'] = [o.serialize() for o in self.outputs.values()]
        template['meta']['label'] = self.label().toPlainText()
        return template

    def propertyView(self):
        return self.graph().parent.dockWidgetNodeView

    def setName(self, name):
        self._rawNode.setName(self, name)

    @property
    def graph(self):
        return self._rawNode.graph

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
        # self.setCursor(QtCore.Qt.ClosedHandCursor)
        QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QGraphicsItem.mouseReleaseEvent(self, event)

    def addInputPin(self, rawPin, hideLabel=False, index=-1, foo=None):
        p = self._addPin(rawPin, PinDirection.Input, index=index)
        return p

    def addOutputPin(self, rawPin, hideLabel=False, index=-1, foo=None):
        p = self._addPin(rawPin, PinDirection.Output, index=index)
        return p

    @property
    def name(self):
        return self._rawNode.name

    def propertyEditingFinished(self):
        le = QApplication.instance().focusWidget()
        if isinstance(le, QLineEdit):
            nodeName, attr = le.objectName().split('.')
            Pin = self.getPinByName(attr)
            Pin.setData(le.text())

    def onUpdatePropertyView(self, formLayout):
        # name
        le_name = QLineEdit(self._rawNode.getName())
        le_name.setReadOnly(True)
        if self.label().IsRenamable():
            le_name.setReadOnly(False)
            le_name.returnPressed.connect(lambda: self._rawNode.setName(le_name.text()))
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
        if len([i for i in self._rawNode.inputs.values()]) != 0:
            sep_inputs = QLabel()
            sep_inputs.setStyleSheet("background-color: black;")
            sep_inputs.setText("INPUTS")
            formLayout.addRow("", sep_inputs)

            for inp in self._rawNode.inputs.values():
                dataSetter = inp.call if inp.dataType == 'ExecPin' else inp.setData
                w = getInputWidget(inp.dataType, dataSetter, inp.defaultValue(), inp.getUserStruct())
                if w:
                    w.setWidgetValue(inp.currentData())
                    w.setObjectName(inp.getName())
                    formLayout.addRow(inp.name, w)
                    if inp.hasConnections():
                        w.setEnabled(False)

        # outputs
        if len([i for i in self._rawNode.outputs.values()]) != 0:
            sep_outputs = QLabel()
            sep_outputs.setStyleSheet("background-color: black;")
            sep_outputs.setText("OUTPUTS")
            formLayout.addRow("", sep_outputs)
            for out in self._rawNode.outputs.values():
                if out.dataType == 'ExecPin':
                    continue
                w = getInputWidget(out.dataType, out.setData, out.defaultValue(), out.getUserStruct())
                if w:
                    w.setWidgetValue(out.currentData())
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
        doc.setHtml(self._rawNode.description())
        formLayout.addRow("", doc)

    def addContainer(self, portType, head=False):
        container = QGraphicsWidget()
        container.setObjectName('{0}PinContainerWidget'.format(self._rawNode.name))
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
        # disconnect edges
        for i in list(self._rawNode.inputs.values()) + list(self._rawNode.outputs.values()):
            i.kill()

        if self.uid in self.graph().nodes:
            self.graph().nodes.pop(self.uid)
            self.graph().nodesPendingKill.append(self)

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

    def _addPin(self, rawPin, pinDirection, hideLabel=False, index=-1, foo=None):
        # TODO: create wrapper for raw pin
        p = PinWidgetBase(self, rawPin)
        if pinDirection == PinDirection.Input:
            self.inputs[p.uid] = p
            p.call = rawPin.call
        if pinDirection == PinDirection.Output:
            self.outputs[p.uid] = p

        name = rawPin.name

        connector_name = QGraphicsProxyWidget()
        connector_name.setObjectName('{0}PinConnector'.format(name))
        connector_name.setContentsMargins(0, 0, 0, 0)

        lblName = name
        if hideLabel:
            lblName = ''
            p.bLabelHidden = True

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
        if pinDirection == PinDirection.Input:
            container = self.addContainer(pinDirection)
            if hideLabel:
                container.setMinimumWidth(15)
            lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            container.layout().addItem(p)
            p._container = container
            container.layout().addItem(connector_name)

            self._rawNode.inputs[rawPin.uid] = rawPin
            self.inputsLayout.insertItem(index, container)
            container.adjustSize()
        elif pinDirection == PinDirection.Output:
            container = self.addContainer(pinDirection)
            if hideLabel:
                container.setMinimumWidth(15)
            lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            container.layout().addItem(connector_name)
            container.layout().addItem(p)
            p._container = container
            self._rawNode.outputs[rawPin.uid] = rawPin
            self.outputsLayout.insertItem(index, container)
            container.adjustSize()
        p.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # create member if created in runtime
        if not hasattr(self, name):
            setattr(self, name, p)
        return p
