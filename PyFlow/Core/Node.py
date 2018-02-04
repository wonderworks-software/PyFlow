from Settings import *
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QGraphicsLinearLayout
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QTreeWidgetItem
from AbstractGraph import *
from Pins import CreatePin
from types import MethodType
from InputWidgets import getInputWidget
from inspect import getargspec
from NodePainter import NodePainter


class NodeName(QGraphicsTextItem):
    def __init__(self, parent, bUseTextureBg=True, color=Colors.Green):
        super(NodeName, self).__init__(parent)
        self.setParentItem(parent)
        self.bUseTextureBg = bUseTextureBg
        self.width = 50
        self.document().contentsChanged.connect(self.onDocContentsChanged)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.desc = parent.description()
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


class Node(QGraphicsItem, NodeBase):
    """
    Default node description
    """
    def __init__(self, name, graph, w=80, color=Colors.NodeBackgrounds, spacings=Spacings, headColor=Colors.NodeNameRect, bUseTextureBg=True):
        QGraphicsItem.__init__(self)
        NodeBase.__init__(self, name, graph)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.opt_node_base_color = Colors.NodeBackgrounds
        self.opt_selected_pen_color = Colors.NodeSelectedPenColor
        self.opt_pen_selected_type = QtCore.Qt.SolidLine
        self._left_stretch = 0
        self.color = color
        self.height_offset = 3
        self.spacings = spacings
        self.nodeMainGWidget = QGraphicsWidget()
        self.nodeMainGWidget.setObjectName('{0}MainLayout'.format(name))
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
        if pinName in [p.name for p in self.outputs.values() if p.dataType is DataTypes.Exec]:
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
    def initializeFromFunction(foo, graph):
        meta = foo.__annotations__['meta']
        returnType = returnDefaultValue = None
        if foo.__annotations__['return'] is not None:
            returnType, returnDefaultValue = foo.__annotations__['return']
        nodeType = foo.__annotations__['nodeType']
        fooArgNames = getargspec(foo).args

        @staticmethod
        def description():
            return foo.__doc__

        @staticmethod
        def category():
            return meta['Category']

        @staticmethod
        def keywords():
            return meta['Keywords']

        def constructor(self, name, graph, **kwargs):
            Node.__init__(self, name, graph, **kwargs)

        nodeClass = type(foo.__name__, (Node,), {'__init__': constructor,
                                                 'category': category,
                                                 'keywords': keywords,
                                                 'description': description
                                                 })
        inst = nodeClass(graph.getUniqNodeName(foo.__name__), graph)

        if returnType is not None:
            p = inst.addOutputPin('out', returnType)
            p.setData(returnDefaultValue)
            p.setDefaultValue(returnDefaultValue)

        # this is array of 'references' outputs will be created for
        refs = []
        outExec = None

        # iterate over function arguments and create pins according to data types
        for index in range(len(fooArgNames)):
            dataType = foo.__annotations__[fooArgNames[index]]
            # tuple means this is reference pin with default value eg - (dataType, defaultValue)
            if isinstance(dataType, tuple):
                outRef = inst.addOutputPin(fooArgNames[index], dataType[0])
                outRef.setData(dataType[1])
                refs.append(outRef)
            else:
                inp = inst.addInputPin(fooArgNames[index], dataType)
                inp.setData(foo.__defaults__[index])
                inp.setDefaultValue(foo.__defaults__[index])

        # all inputs affects on all outputs
        for i in inst.inputs.values():
            for o in inst.outputs.values():
                pinAffects(i, o)

        # generate compute method from function
        def compute(self):
            # arguments will be taken from inputs
            kwargs = {}
            for i in self.inputs.values():
                if i.dataType is not DataTypes.Exec:
                    kwargs[i.name] = i.getData()
            for ref in refs:
                if ref.dataType is not DataTypes.Exec:
                    kwargs[ref.name] = ref
            result = foo(**kwargs)
            if returnType is not None:
                self.setData('out', result)
            if nodeType == NodeTypes.Callable:
                outExec.call()

        inst.compute = MethodType(compute, inst, Node)

        # create execs if callable
        if nodeType == NodeTypes.Callable:
            inst.addInputPin('inExec', DataTypes.Exec, inst.compute, True, index=0)
            outExec = inst.addOutputPin('outExec', DataTypes.Exec, inst.compute, True, index=0)
        return inst

    @staticmethod
    def deserialize(data, graph):
        node = graph.createNode(data)
        node.uid = uuid.UUID(data['uuid'])
        node.currentComputeCode = data['computeCode']

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
        self.setX(roundup(value.x() - self.graph().grid_size, self.graph().grid_size))
        self.setY(roundup(value.y() - self.graph().grid_size, self.graph().grid_size))

    def boundingRect(self):
        return self.childrenBoundingRect()

    def itemChange(self, change, value):
        if change == self.ItemPositionChange:
            # grid snapping
            value.setX(roundup(value.x() - self.graph().grid_size + self.graph().grid_size / 3.0, self.graph().grid_size))
            value.setY(roundup(value.y() - self.graph().grid_size + self.graph().grid_size / 3.0, self.graph().grid_size))
            value.setY(value.y() - 2)
            return value
        return QGraphicsItem.itemChange(self, change, value)

    @staticmethod
    def description():
        return "Default node description"

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    def postCreate(self, jsonTemplate=None):
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
        self.w = self.getWidth()
        self.nodeMainGWidget.setMaximumWidth(self.w + self.spacings.kPinOffset)
        self.nodeMainGWidget.setGeometry(QtCore.QRectF(0, 0, self.w + self.spacings.kPinOffset, self.childrenBoundingRect().height()))
        if self.isCallable():
            if 'flow' not in self.category().lower():
                if self.label().bUseTextureBg:
                    self.label().bg = QtGui.QImage(':/icons/resources/blue.png')
        else:
            if self.label().bUseTextureBg:
                self.label().bg = QtGui.QImage(':/icons/resources/green.png')
        self.label().setPlainText(self.__class__.__name__)
        self.setToolTip(self.description())

        NodeBase.postCreate(self, jsonTemplate)

    def getWidth(self):
        dPins = 0
        if len(self.outputs.values()) > 0:
            dPins = abs(self.outputs.values()[0].scenePos().x() - self.scenePos().x())
        fontWidth = QtGui.QFontMetricsF(self.label().font()).width(self.getName()) + self.spacings.kPinSpacing
        return max(dPins, fontWidth)

    @staticmethod
    def jsonTemplate():
        doc = '''# access pins like this\n\t# self.pinName.getData()\n\t# self.pinName.setData()'''
        doc += '''\n\t# self.getData(name) to get data from input pin by name'''
        doc += '''\n\t# self.setData(name, data) to set data to output pin by name\n'''

        template = {'type': None,
                    'x': None,
                    'y': None,
                    'name': None,
                    'uuid': None,
                    'computeCode': doc + "\nprint('Hello world')\n",
                    'inputs': [],
                    'outputs': [],
                    'meta': {'label': 'Node', 'var': {}}
                    }
        return template

    def serialize(self):
        template = Node.jsonTemplate()
        template['type'] = self.__class__.__name__
        template['name'] = self.name
        template['x'] = self.scenePos().x()
        template['y'] = self.scenePos().y()
        template['uuid'] = str(self.uid)
        template['computeCode'] = self.computeCode()
        template['inputs'] = [i.serialize() for i in self.inputs.values()]
        template['outputs'] = [o.serialize() for o in self.outputs.values()]
        template['meta']['label'] = self.label().toPlainText()
        return template

    def propertyView(self):
        return self.graph().parent.dockWidgetNodeView

    def Tick(self, delta):
        pass

    def setName(self, name):
        NodeBase.setName(self, name)

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

    def addInputPin(self, pinName, dataType, foo=None, hideLabel=False, bCreateInputWidget=True, index=-1):
        p = self._addPin(PinDirection.Input, dataType, foo, hideLabel, bCreateInputWidget, pinName, index=index)
        return p

    def addOutputPin(self, pinName, dataType, foo=None, hideLabel=False, bCreateInputWidget=True, index=-1):
        p = self._addPin(PinDirection.Output, dataType, foo, hideLabel, bCreateInputWidget, pinName, index=index)
        return p

    @staticmethod
    def category():
        return "Default"

    @staticmethod
    def keywords():
        return []

    def propertyEditingFinished(self):
        le = QApplication.instance().focusWidget()
        if isinstance(le, QLineEdit):
            nodeName, attr = le.objectName().split('.')
            Pin = self.getPinByName(attr)
            Pin.setData(le.text())

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
        if len([i for i in self.inputs.values() if not i.dataType == DataTypes.Exec]) != 0:
            sep_inputs = QLabel()
            sep_inputs.setStyleSheet("background-color: black;")
            sep_inputs.setText("INPUTS")
            formLayout.addRow("", sep_inputs)

            for inp in self.inputs.values():
                if inp.dataType == DataTypes.Exec:
                    continue
                w = getInputWidget(inp.dataType, inp.setData)
                if w:
                    w.setWidgetValue(inp.currentData())
                    w.setObjectName(inp.getName())
                    formLayout.addRow(inp.name, w)
                    if inp.hasConnections():
                        w.setEnabled(False)

        # outputs
        if len([i for i in self.outputs.values() if not i.dataType == DataTypes.Exec]) != 0:
            sep_outputs = QLabel()
            sep_outputs.setStyleSheet("background-color: black;")
            sep_outputs.setText("OUTPUTS")
            formLayout.addRow("", sep_outputs)
            for out in self.outputs.values():
                if out.dataType == DataTypes.Exec:
                    continue
                w = getInputWidget(out.dataType, out.setData)
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
        doc = QLabel(self.description())
        doc.setWordWrap(True)
        formLayout.addRow("", doc)

    def addContainer(self, portType, head=False):
        container = QGraphicsWidget()  # for set background color
        container.setObjectName('{0}PinContainerWidget'.format(self.name))
        container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        container.sizeHint(QtCore.Qt.MinimumSize, QtCore.QSizeF(50.0, 10.0))

        if self.graph().isDebug():
            container.setAutoFillBackground(True)
            container.setPalette(QtGui.QPalette(QtCore.Qt.gray))

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
        for i in self.inputs.values() + self.outputs.values():
            i.kill()

        if self.uid in self.graph().nodes:
            self.graph().nodes.pop(self.uid)
            self.graph().nodesPendingKill.append(self)

            self.scene().removeItem(self)
            del(self)

    def setPosition(self, x, y):
        NodeBase.setPosition(self, x, y)
        self.setPos(QtCore.QPointF(x, y))

    @staticmethod
    def removePinByName(node, name):
        pin = node.getPinByName(name)
        if pin:
            pin.kill()

    def _addPin(self, pinDirection, dataType, foo, hideLabel=False, bCreateInputWidget=True, name='', index=-1):
        # check if pins with this name already exists and get uniq name
        name = self.getUniqPinName(name)

        p = CreatePin(name, self, dataType, pinDirection)
        self.graph().pins[p.uid] = p

        if pinDirection == PinDirection.Input and foo is not None:
            p.call = foo

        connector_name = QGraphicsProxyWidget()
        connector_name.setObjectName('{0}PinConnector'.format(name))
        connector_name.setContentsMargins(0, 0, 0, 0)

        lblName = name
        if hideLabel:
            lblName = ''
            p.bLabelHidden = True

        lbl = QLabel(lblName)
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

            self.inputs[p.uid] = p
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
            self.outputs[p.uid] = p
            self.outputsLayout.insertItem(index, container)
            container.adjustSize()
        p.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # create member if created in runtime
        if not hasattr(self, name):
            setattr(self, name, p)
        return p
