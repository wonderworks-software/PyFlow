from nine import str
import random
from copy import deepcopy
import json
import uuid
import weakref
from collections import Counter
try:
    from inspect import getfullargspec as getargspec
except:
    from inspect import getargspec
from multipledispatch import dispatch

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
from Qt.QtWidgets import *

from PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Canvas.SelectionRect import SelectionRect
from PyFlow.UI.Canvas.UIConnection import UIConnection
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.UI.Canvas.UINodeBase import NodeActionButtonBase
from PyFlow.UI.Canvas.UIPinBase import UIPinBase, PinGroup
from PyFlow.UI.Views.NodeBox import NodesBox
from PyFlow.UI.Canvas.AutoPanController import AutoPanController
from PyFlow.UI.UIInterfaces import IPropertiesViewSupport
from PyFlow.Core.PinBase import PinBase
from PyFlow.Core.NodeBase import NodeBase
from PyFlow.Input import InputManager, InputAction, InputActionType
from PyFlow.UI.Views.VariablesWidget import (
    VARIABLE_TAG,
    VARIABLE_DATA_TAG
)

from PyFlow import getRawNodeInstance
from PyFlow.Core.Common import *

from PyFlow.Packages.PyFlowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyFlowBase.UI.UIRerouteNode import UIRerouteNode
from PyFlow.Packages.PyFlowBase.UI.UIRerouteNodeSmall import UIRerouteNodeSmall
from PyFlow.Packages.PyFlowBase import PACKAGE_NAME as PYFLOW_BASE_PACKAGE_NAME
from PyFlow.UI.Utils.stylesheet import editableStyleSheet


def getNodeInstance(jsonTemplate, canvas, parentGraph=None):
    nodeClassName = jsonTemplate['type']
    nodeName = jsonTemplate['name']
    packageName = jsonTemplate['package']
    if 'lib' in jsonTemplate:
        libName = jsonTemplate['lib']
    else:
        libName = None

    kwargs = {}

    # if get var or set var, construct additional keyword arguments
    if jsonTemplate['type'] in ('getVar', 'setVar'):
        kwargs['var'] = canvas.graphManager.findVariableByUid(uuid.UUID(jsonTemplate['varUid']))

    raw_instance = getRawNodeInstance(nodeClassName, packageName=packageName, libName=libName, **kwargs)
    assert(raw_instance.packageName == packageName)
    raw_instance.uid = uuid.UUID(jsonTemplate['uuid'])
    assert(raw_instance is not None), "Node {0} not found in package {1}".format(nodeClassName, packageName)
    instance = getUINodeInstance(raw_instance)
    canvas.addNode(instance, jsonTemplate, parentGraph=parentGraph)
    return instance


class SceneClass(QGraphicsScene):
    def __init__(self, parent):
        super(SceneClass, self).__init__(parent)
        self.setItemIndexMethod(self.NoIndex)
        # self.pressed_port = None
        self.selectionChanged.connect(self.OnSelectionChanged)
        self.tempnode = None
        self.hoverItems = []

    def shoutDown(self):
        self.selectionChanged.disconnect()

    def mousePressEvent(self, event):
        # do not clear selection when panning
        modifiers = event.modifiers()
        # or modifiers == QtCore.Qt.ShiftModifier:
        if event.button() == QtCore.Qt.RightButton:
            event.accept()
            return
        QGraphicsScene.mousePressEvent(self, event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
            mime = str(event.mimeData().text())
            jsonData = json.loads(mime)

            if VARIABLE_TAG in jsonData:
                return
            packageName = jsonData["package"]
            nodeType = jsonData["type"]
            libName = jsonData["lib"]
            name = nodeType

            nodeTemplate = NodeBase.jsonTemplate()
            nodeTemplate['package'] = packageName
            nodeTemplate['lib'] = libName
            nodeTemplate['type'] = nodeType
            nodeTemplate['name'] = name
            nodeTemplate['x'] = event.scenePos().x()
            nodeTemplate['y'] = event.scenePos().y()
            nodeTemplate['meta']['label'] = nodeType
            nodeTemplate['uuid'] = str(uuid.uuid4())
            try:
                self.tempnode.isTemp = False
                self.tempnode = None
            except Exception as e:
                pass
            self.tempnode = self.parent()._createNode(nodeTemplate)
            if self.tempnode:
                self.tempnode.isTemp = True
            self.hoverItems = []
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            if self.tempnode:
                self.tempnode.setPos(
                    (self.tempnode.w / -2) + event.scenePos().x(), event.scenePos().y())
                mouseRect = QtCore.QRect(QtCore.QPoint(event.scenePos().x() - 1, event.scenePos().y() - 1),
                                         QtCore.QPoint(event.scenePos().x() + 1, event.scenePos().y() + 1))
                hoverItems = self.items(mouseRect)
                for item in hoverItems:
                    if isinstance(item, UIConnection):
                        valid = False
                        for inp in self.tempnode.UIinputs.values():
                            if canConnectPins(item.source()._rawPin, inp._rawPin):
                                valid = True
                        for out in self.tempnode.UIoutputs.values():
                            if canConnectPins(out._rawPin, item.destination()._rawPin):
                                valid = True
                        if valid:
                            self.hoverItems.append(item)
                            item.drawThick()
                for item in self.hoverItems:
                    if item not in hoverItems:
                        self.hoverItems.remove(item)
                        if isinstance(item, UIConnection):
                            item.restoreThick()
                    else:
                        if isinstance(item, UIConnection):
                            item.drawThick()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        if self.tempnode:
            self.tempnode._rawNode.kill()
            self.tempnode = None
        event.accept()

    def OnSelectionChanged(self):
        pass

    def createVariableGetter(self):
        pass

    def dropEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()

        if event.mimeData().hasFormat('text/plain'):
            jsonData = json.loads(event.mimeData().text())

            # try load mime data text as json
            # in case if it is a variable
            # if no keyboard modifires create context menu with two actions
            # for creating getter or setter
            # if control - create getter, if alt - create setter
            if VARIABLE_TAG in jsonData:
                modifiers = event.modifiers()
                varData = jsonData[VARIABLE_DATA_TAG]
                nodeTemplate = NodeBase.jsonTemplate()
                nodeTemplate['name'] = varData['name']
                nodeTemplate['x'] = x
                nodeTemplate['y'] = y
                nodeTemplate['package'] = PYFLOW_BASE_PACKAGE_NAME
                if modifiers == QtCore.Qt.NoModifier:
                    nodeTemplate['type'] = 'getVar'
                    nodeTemplate['meta']['label'] = varData['name']
                    # node uid should be unique, different from var
                    nodeTemplate['uuid'] = str(uuid.uuid4())

                    nodeTemplate['varUid'] = varData['uuid']
                    m = QMenu()
                    getterAction = m.addAction('Get')

                    def varGetterCreator():
                        n = self.parent().createNode(nodeTemplate)
                        n.updateNodeShape()
                    getterAction.triggered.connect(varGetterCreator)

                    setNodeTemplate = dict(nodeTemplate)
                    setterAction = m.addAction('Set')
                    setNodeTemplate['type'] = 'setVar'
                    setterAction.triggered.connect(lambda: self.parent().createNode(setNodeTemplate))
                    m.exec_(QtGui.QCursor.pos(), None)
                if modifiers == QtCore.Qt.ControlModifier:
                    nodeTemplate['type'] = 'getVar'
                    # node uid should be unique, different from var
                    nodeTemplate['uuid'] = str(uuid.uuid4())
                    nodeTemplate['varUid'] = varData['uuid']
                    nodeTemplate['meta']['label'] = varData['name']
                    self.parent().createNode(nodeTemplate)
                    return
                if modifiers == QtCore.Qt.AltModifier:
                    nodeTemplate['type'] = 'setVar'
                    nodeTemplate['uuid'] = str(uuid.uuid4())
                    nodeTemplate['varUid'] = varData['uuid']
                    nodeTemplate['meta']['label'] = varData['name']
                    self.parent().createNode(nodeTemplate)
                    return
            else:
                packageName = jsonData["package"]
                nodeType = jsonData["type"]
                libName = jsonData['lib']
                name = nodeType
                dropItem = self.parent().nodeFromInstance(self.itemAt(event.scenePos(), QtGui.QTransform()))
                if not dropItem or (isinstance(dropItem, UINodeBase) and dropItem.isCommentNode or dropItem.isTemp) or isinstance(dropItem, UIPinBase) or isinstance(dropItem, UIConnection):
                    nodeTemplate = NodeBase.jsonTemplate()
                    nodeTemplate['package'] = packageName
                    nodeTemplate['lib'] = libName
                    nodeTemplate['type'] = nodeType
                    nodeTemplate['name'] = name
                    nodeTemplate['x'] = x
                    nodeTemplate['y'] = y
                    nodeTemplate['meta']['label'] = nodeType
                    nodeTemplate['uuid'] = str(uuid.uuid4())
                    if self.tempnode:
                        self.tempnode.updateOwningCommentNode()
                        self.tempnode.isTemp = False
                        self.tempnode.update()
                        node = self.tempnode
                        self.tempnode = None
                        for it in self.items(event.scenePos()):
                            if isinstance(it, UIPinBase):
                                dropItem = it
                                break
                            elif isinstance(it, UIConnection):
                                dropItem = it
                                break
                        EditorHistory().saveState("Create node {}".format(node.name))
                    else:
                        node = self.parent().createNode(nodeTemplate)

                    nodeInputs = node.namePinInputsMap
                    nodeOutputs = node.namePinOutputsMap

                    if isinstance(dropItem, UIPinBase):
                        node.setPos(x - node.boundingRect().width(), y)
                        for inp in nodeInputs.values():
                            if canConnectPins(dropItem._rawPin, inp._rawPin):
                                if dropItem.isExec():
                                    dropItem._rawPin.disconnectAll()
                                self.parent().connectPins(dropItem, inp)
                                node.setPos(x + node.boundingRect().width(), y)
                                break
                        for out in nodeOutputs.values():
                            if canConnectPins(out._rawPin, dropItem._rawPin):
                                self.parent().connectPins(out, dropItem)
                                node.setPos(x - node.boundingRect().width(), y)
                                break
                    if isinstance(dropItem, UIConnection):
                        for inp in nodeInputs.values():
                            if canConnectPins(dropItem.source()._rawPin, inp._rawPin):
                                if dropItem.source().isExec():
                                    dropItem.source()._rawPin.disconnectAll()
                                self.parent().connectPins(dropItem.source(), inp)
                                break
                        for out in nodeOutputs.values():
                            if canConnectPins(out._rawPin, dropItem.destination()._rawPin):
                                self.parent().connectPins(out, dropItem.destination())
                                break
        else:
            super(SceneClass, self).dropEvent(event)


class Canvas(QGraphicsView):
    _manipulationMode = CanvasManipulationMode.NONE

    _realTimeLineInvalidPen = Colors.Red
    _realTimeLineNormalPen = Colors.White
    _realTimeLineValidPen = Colors.Green

    _mouseWheelZoomRate = 0.0005

    requestFillProperties = QtCore.Signal(object)
    requestClearProperties = QtCore.Signal()

    # argument is a list of ui nodes
    requestShowSearchResults = QtCore.Signal(object)

    USETAB = True

    def __init__(self, graphManager, pyFlowInstance=None):
        super(Canvas, self).__init__()
        self.menu = QMenu()
        self.populateMenu()
        self.state = CanvasState.DEFAULT
        self.graphManager = graphManager
        self.graphManager.graphChanged.connect(self.onGraphChanged)
        self.pyFlowInstance = pyFlowInstance
        # connect with App class signals
        self.pyFlowInstance.newFileExecuted.connect(self.onNewFile)
        self.setScene(SceneClass(self))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pressed_item = None
        self.pressedPin = None
        self.released_item = None
        self.resizing = False
        self.hoverItems = []
        self.hoveredRerutes = []
        self.bPanMode = False
        self._isPanning = False
        self._mousePressed = False
        self._shadows = False
        self._panSpeed = 1.0
        self._minimum_scale = 0.2
        self._maximum_scale = 3.0

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # Antialias -- Change to Settings
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)
        ##
        self.setAcceptDrops(True)
        self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.scene().setSceneRect(QtCore.QRectF(0, 0, 10, 10))
        self.factor = 1

        self._current_file_name = 'Untitled'
        self.realTimeLine = QGraphicsPathItem(None, self.scene())
        self.realTimeLine.name = 'RealTimeLine'
        self.realTimeLineInvalidPen = QtGui.QPen(self._realTimeLineInvalidPen, 2.0, QtCore.Qt.SolidLine)
        self.realTimeLineNormalPen = QtGui.QPen(self._realTimeLineNormalPen, 2.0, QtCore.Qt.DashLine)
        self.realTimeLineValidPen = QtGui.QPen(self._realTimeLineValidPen, 2.0, QtCore.Qt.SolidLine)
        self.realTimeLine.setPen(self.realTimeLineNormalPen)
        self.mousePressPose = QtCore.QPointF(0, 0)
        self.mousePos = QtCore.QPointF(0, 0)
        self._lastMousePos = QtCore.QPointF(0, 0)
        self._right_button = False
        self._drawRealtimeLine = False
        self._update_items = False
        self._resize_group_mode = False
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.centerOn(QtCore.QPointF(self.sceneRect().width() /
                                     2, self.sceneRect().height() / 2))
        self.initialScrollBarsPos = QtGui.QVector2D(
            self.horizontalScrollBar().value(), self.verticalScrollBar().value())
        self._sortcuts_enabled = True
        self.current_rounded_pos = QtCore.QPointF(0.0, 0.0)
        self.autoPanController = AutoPanController()
        self._bRightBeforeShoutDown = False

        self.node_box = NodesBox(self)
        self.node_box.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.codeEditors = {}
        self._UIConnections = {}
        self.boundingRect = self.rect()
        if self.USETAB:
            self.installEventFilter(self)
        self.reconnectingWires = set()

    def getApp(self):
        return self.pyFlowInstance

    def onGraphChanged(self, newGraph):
        for node in self.nodes.values():
            bVisible = node._rawNode.graph() == newGraph
            node.setVisible(bVisible)
            for pin in node.UIPins.values():
                for connection in pin.uiConnectionList:
                    if bVisible:
                        if not connection.isUnderCollapsedComment():
                            connection.setVisible(bVisible)
                    else:
                        connection.setVisible(bVisible)

        self.validateCommentNodesOwnership(newGraph)
        for commentNode in newGraph.getNodesList():
            uiCommentNode = commentNode.getWrapper()
            if uiCommentNode.isCommentNode:
                if uiCommentNode.collapsed:
                    uiCommentNode.hideOwningNodes()
        self.validateConnections(newGraph)

        def nodeShapeUpdater():
            for node in self.nodes.values():
                node.updateNodeShape()
        QtCore.QTimer.singleShot(100, nodeShapeUpdater)

    def jumpToNode(self, uiNode):
        self.graphManager.selectGraph(uiNode.graph())
        self.clearSelection()
        uiNode.setSelected(True)
        self.frameSelectedNodes()

    @property
    def manipulationMode(self):
        return self._manipulationMode

    @manipulationMode.setter
    def manipulationMode(self, value):
        self._manipulationMode = value
        if value == CanvasManipulationMode.NONE:
            pass
        elif value == CanvasManipulationMode.SELECT:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        elif value == CanvasManipulationMode.PAN:
            self.viewport().setCursor(QtCore.Qt.OpenHandCursor)
        elif value == CanvasManipulationMode.MOVE:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        elif value == CanvasManipulationMode.ZOOM:
            self.viewport().setCursor(QtCore.Qt.SizeHorCursor)
        elif value == CanvasManipulationMode.COPY:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)

    def setSelectedNodesCollapsed(self, collapsed=True):
        for node in self.selectedNodes():
            node.collapsed = collapsed

    def collapseSelectedNodesToCompound(self):
        selectedNodes = self.selectedNodes()
        selectedNodesRect = self.getNodesRect(True, True)
        wires = list()
        for node in selectedNodes:
            for pin in node.UIPins.values():
                wires.extend(pin.uiConnectionList)

        inputPins = list()
        inputConectionList = dict()
        outputPins = list()
        outputConectionList = dict()
        for wire in wires:
            if wire.source().owningNode().isSelected() and not wire.destination().owningNode().isSelected():
                if wire.destination() not in outputPins:
                    outputPins.append(wire.destination())
                    outputConectionList[wire.destination()] = [[wire.source().owningNode().name, wire.source().name]]
                else:
                    outputConectionList[wire.destination()].append([wire.source().owningNode().name, wire.source().name])

            if not wire.source().owningNode().isSelected() and wire.destination().owningNode().isSelected():
                if wire.source() not in inputPins:
                    inputPins.append(wire.source())
                    inputConectionList[wire.source()] = [[wire.destination().owningNode().name, wire.destination().name]]
                else:
                    inputConectionList[wire.source()].append([wire.destination().owningNode().name, wire.destination().name])

        nodes = self.copyNodes(toClipBoard=False)
        for node in selectedNodes:
            node._rawNode.kill()

        compoundTemplate = NodeBase.jsonTemplate()
        compoundTemplate['package'] = 'PyFlowBase'
        compoundTemplate['type'] = 'compound'
        compoundTemplate['name'] = 'compound'
        compoundTemplate['uuid'] = str(uuid.uuid4())
        compoundTemplate['meta']['label'] = 'compound'
        compoundTemplate['x'] = selectedNodesRect.center().x()
        compoundTemplate['y'] = selectedNodesRect.center().y()
        uiCompoundNode = self._createNode(compoundTemplate)
        activeGraphName = self.graphManager.activeGraph().name

        uiCompoundNode.stepIn()
        self.pasteNodes(data=nodes, move=False)

        newInputPins = dict()
        newOutputPins = dict()

        if len(inputPins) > 0:
            graphInputsTemplate = NodeBase.jsonTemplate()
            graphInputsTemplate['package'] = 'PyFlowBase'
            graphInputsTemplate['type'] = 'graphInputs'
            graphInputsTemplate['name'] = 'graphInputs'
            graphInputsTemplate['uuid'] = str(uuid.uuid4())
            graphInputsTemplate['meta']['label'] = 'graphInputs'
            graphInputsTemplate['x'] = selectedNodesRect.left() - 100
            graphInputsTemplate['y'] = selectedNodesRect.center().y()
            graphInputs = self._createNode(graphInputsTemplate)

            for o in inputPins:
                newPinName = self.graphManager.getUniqName(o.owningNode().name)
                newPin = graphInputs.onAddOutPin(newPinName, o.dataType)
                newInputPins[o] = newPin
                for n in inputConectionList[o]:
                    node = self.findNode(n[0])
                    self.connectPinsInternal(newPin, node.getPinSG(n[1]))

        if len(outputPins) > 0:
            graphOutputsTemplate = NodeBase.jsonTemplate()
            graphOutputsTemplate['package'] = 'PyFlowBase'
            graphOutputsTemplate['type'] = 'graphOutputs'
            graphOutputsTemplate['name'] = 'graphOutputs'
            graphOutputsTemplate['uuid'] = str(uuid.uuid4())
            graphOutputsTemplate['meta']['label'] = 'graphOutputs'
            graphOutputsTemplate['x'] = selectedNodesRect.right() + 100
            graphOutputsTemplate['y'] = selectedNodesRect.center().y()
            graphOutputs = self._createNode(graphOutputsTemplate)

            for i in outputPins:
                newPinName = self.graphManager.getUniqName(i.owningNode().name)
                newPin = graphOutputs.onAddInPin(newPinName, i.dataType)
                newOutputPins[i] = newPin
                for n in outputConectionList[i]:
                    node = self.findNode(n[0])
                    self.connectPinsInternal(newPin, node.getPinSG(n[1]))

        def connectPins(compoundNode, inputs, outputs):
            for o in inputs:
                exposedPin = compoundNode.getPinSG(newInputPins[o].name)
                if exposedPin:
                    self.connectPinsInternal(exposedPin, o)

            for i in outputs:
                exposedPin = compoundNode.getPinSG(newOutputPins[i].name)
                if exposedPin:
                    self.connectPinsInternal(i, exposedPin)
            EditorHistory().saveState("Collapse to compound")

        QtCore.QTimer.singleShot(1, lambda: connectPins(uiCompoundNode, inputPins, outputPins))
        self.graphManager.selectGraphByName(activeGraphName)

    def populateMenu(self):
        self.actionCollapseSelectedNodes = self.menu.addAction("Collapse selected nodes")
        self.actionCollapseSelectedNodes.triggered.connect(lambda: self.setSelectedNodesCollapsed(True))
        self.menu.addAction(self.actionCollapseSelectedNodes)

        self.actionExpandSelectedNodes = self.menu.addAction("Expand selected nodes")
        self.actionExpandSelectedNodes.triggered.connect(lambda: self.setSelectedNodesCollapsed(False))
        self.menu.addAction(self.actionExpandSelectedNodes)

        self.actionCollapseSelectedNodesToCompound = self.menu.addAction("Collapse to compound")
        self.actionCollapseSelectedNodesToCompound.triggered.connect(self.collapseSelectedNodesToCompound)
        self.menu.addAction(self.actionCollapseSelectedNodesToCompound)

    def plot(self):
        self.graphManager.plot()

    def location(self):
        return self.graphManager.location()

    def __del__(self):
        # self.tick_timer.stop()
        pass

    def createVariable(self, dataType='AnyPin', accessLevel=AccessLevel.public, uid=None):
        return self.graphManager.activeGraph().createVariable(dataType=dataType, accessLevel=accessLevel, uid=uid)

    @property
    def nodes(self):
        """returns all ui nodes dict including compounds
        """
        result = {}
        for rawNode in self.graphManager.getAllNodes():
            uiNode = rawNode.getWrapper()
            if uiNode is None:
                print("{0} has not UI wrapper".format(rawNode.name))
            if rawNode.uid in result:
                rawNode.uid = uuid.uuid4()
            result[rawNode.uid] = uiNode
        return result

    @property
    def pins(self):
        """Returns UI pins dict {uuid: UIPinBase}
        """
        result = {}
        for node in self.graphManager.getAllNodes():
            for pin in node.pins:
                result[pin.uid] = pin.getWrapper()()
        return result

    @property
    def connections(self):
        return self._UIConnections

    def getAllNodes(self):
        """returns all ui nodes list
        """
        return list(self.nodes.values())

    def showNodeBox(self, dataType=None, pinDirection=None, pinStructure=PinStructure.Single):
        self.node_box.show()
        self.node_box.move(QtGui.QCursor.pos())
        self.node_box.treeWidget.refresh(dataType, '', pinDirection, pinStructure)
        self.node_box.lineEdit.blockSignals(True)
        self.node_box.lineEdit.setText("")
        self.node_box.lineEdit.blockSignals(False)
        if dataType is None:
            self.node_box.lineEdit.setFocus()

    def hideNodeBox(self):
        self.node_box.hide()
        self.node_box.lineEdit.clear()

    def shoutDown(self, *args, **kwargs):
        for ed in self.codeEditors.values():
            ed.deleteLater()
        self.scene().clear()
        self._UIConnections.clear()
        self.hideNodeBox()
        for node in self.nodes.values():
            node.shoutDown()

    def mouseDoubleClickEvent(self, event):
        QGraphicsView.mouseDoubleClickEvent(self, event)
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()

    def OnDoubleClick(self, pos):
        pass

    def Tick(self, deltaTime):
        if self.autoPanController.isActive():
            delta = self.autoPanController.getDelta() * -1
            self.pan(delta)

        for e in list(self.connections.values()):
            e.Tick()

    def isShortcutsEnabled(self):
        return self._sortcuts_enabled

    def disableSortcuts(self):
        self._sortcuts_enabled = False

    def enableSortcuts(self):
        self._sortcuts_enabled = True

    @dispatch(uuid.UUID)
    def findPin(self, uid):
        uiPin = None
        if uid in self.pins:
            return self.pins[uid]
        return uiPin

    @dispatch(str)
    def findPin(self, pinName):
        uiPin = None
        for pin in self.pins.values():
            if pinName == pin.getFullName():
                uiPin = pin
                break
        return uiPin

    def onNewFile(self, keepRoot=True):
        self.getApp().undoStack.clear()
        self.shoutDown()

    def getPinByFullName(self, full_name):
        node_name = full_name.split('.')[0]
        pinName = full_name.split('.')[1]
        node = self.findNode(node_name)
        if node:
            Pin = node.getPinSG(pinName)
            if Pin:
                return Pin

    def frameRect(self, nodesRect):
        if nodesRect is None:
            return
        windowRect = self.mapToScene(self.rect()).boundingRect()

        # pan to center of window
        delta = windowRect.center() - nodesRect.center()
        delta *= self.currentViewScale()
        self.pan(delta)

        # zoom to fit content
        ws = windowRect.size()
        nodesRect += QtCore.QMargins(0, 20, 150, 20)
        rs = nodesRect.size()
        widthRef = ws.width()
        heightRef = ws.height()
        sx = widthRef / nodesRect.width()
        sy = heightRef / nodesRect.height()
        scale = sx if sy > sx else sy
        self.zoom(scale)

        return scale

    def ensureNodesRectAlmostEqualWindowRect(self, tolerance=10.0):
        windowRect = self.mapToScene(self.rect()).boundingRect()
        nodesRect = self.getNodesRect()
        errorPoint = windowRect.topLeft() - nodesRect.topLeft()
        error = abs(errorPoint.x() + errorPoint.y())
        return error < tolerance

    def frameSelectedNodes(self):
        self.frameRect(self.getNodesRect(True))
        self.frameRect(self.getNodesRect(True))

    def frameAllNodes(self):
        rect = self.getNodesRect()
        if rect is not None:
            self.frameRect(rect)
            if not self.ensureNodesRectAlmostEqualWindowRect():
                self.frameRect(self.getNodesRect())

    def getNodesRect(self, selected=False, activeGraphOnly=True):
        rectangles = []
        if selected:
            for n in [n for n in self.getAllNodes() if n.isSelected()]:
                if activeGraphOnly:
                    if n._rawNode.graph() != self.graphManager.activeGraph():
                        continue
                n_rect = QtCore.QRectF(n.scenePos(), QtCore.QPointF(n.scenePos().x() + float(n.w), n.scenePos().y() + float(n.h)))
                rectangles.append([n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])
        else:
            for n in self.getAllNodes():
                if activeGraphOnly:
                    if n._rawNode.graph() != self.graphManager.activeGraph():
                        continue
                n_rect = QtCore.QRectF(n.scenePos(), QtCore.QPointF(n.scenePos().x() + float(n.w), n.scenePos().y() + float(n.h)))
                rectangles.append([n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])

        arr1 = [i[0] for i in rectangles]
        arr2 = [i[2] for i in rectangles]
        arr3 = [i[1] for i in rectangles]
        arr4 = [i[3] for i in rectangles]
        if any([len(arr1) == 0, len(arr2) == 0, len(arr3) == 0, len(arr4) == 0]):
            return None
        min_x = min(arr1)
        max_x = max(arr2)
        min_y = min(arr3)
        max_y = max(arr4)

        return QtCore.QRect(QtCore.QPoint(min_x, min_y), QtCore.QPoint(max_x, max_y))

    def selectedNodes(self):
        allNodes = self.getAllNodes()
        assert(None not in allNodes), "Bad nodes!"
        return [i for i in allNodes if i.isSelected()]

    def selectedConnections(self):
        return [i for i in self.connections.values() if i.isSelected()]

    def clearSelection(self):
        for node in self.selectedNodes():
            node.setSelected(False)

        for connection in self.selectedConnections():
            connection.setSelected(False)

    def killSelectedConnections(self):
        self.removeEdgeCmd(self.selectedConnections())

    def killSelectedNodes(self):
        selectedNodes = self.selectedNodes()
        if self.isShortcutsEnabled() and len(selectedNodes) > 0:
            for node in selectedNodes:
                node._rawNode.kill()
            self.requestClearProperties.emit()

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        currentInputAction = InputAction("temp", InputActionType.Keyboard, "temp", key=event.key(), modifiers=modifiers)

        if self.isShortcutsEnabled():
            if all([event.key() == QtCore.Qt.Key_C, modifiers == QtCore.Qt.NoModifier]):
                # create comment node
                rect = self.getNodesRect(True)
                if rect:
                    rect.setTop(rect.top() - 30)
                    rect.setLeft(rect.left() - 30)

                    rect.setRight(rect.right() + 100)
                    rect.setBottom(rect.bottom() + 30)

                nodeTemplate = NodeBase.jsonTemplate()
                nodeTemplate['package'] = "PyFlowBase"
                nodeTemplate['type'] = commentNode.__name__
                nodeTemplate['name'] = commentNode.__name__
                if rect:
                    nodeTemplate['x'] = rect.topLeft().x()
                    nodeTemplate['y'] = rect.topLeft().y()
                else:
                    nodeTemplate['x'] = self.mapToScene(self.mousePos).x()
                    nodeTemplate['y'] = self.mapToScene(self.mousePos).y()
                nodeTemplate['meta']['label'] = commentNode.__name__
                nodeTemplate['uuid'] = str(uuid.uuid4())

                instance = self.createNode(nodeTemplate)
                if rect:
                    instance._rect.setRight(rect.width())
                    instance._rect.setBottom(rect.height())
                instance.updateNodeShape()
                for node in self.selectedNodes():
                    node.updateOwningCommentNode()

            if currentInputAction in InputManager()["Canvas.AlignLeft"]:
                self.alignSelectedNodes(Direction.Left)
                return
            if currentInputAction in InputManager()["Canvas.AlignTop"]:
                self.alignSelectedNodes(Direction.Up)
                return
            if currentInputAction in InputManager()["Canvas.AlignRight"]:
                self.alignSelectedNodes(Direction.Right)
                return
            if currentInputAction in InputManager()["Canvas.AlignBottom"]:
                self.alignSelectedNodes(Direction.Down)
                return

            if currentInputAction in InputManager()["Canvas.Undo"]:
                    self.getApp().edHistory.undo()
            if currentInputAction in InputManager()["Canvas.Redo"]:
                    self.getApp().edHistory.redo()

            if currentInputAction in InputManager()["Canvas.FrameSelected"]:
                self.frameSelectedNodes()
            if currentInputAction in InputManager()["Canvas.FrameAll"]:
                self.frameAllNodes()

            if currentInputAction in InputManager()["Canvas.ZoomIn"]:
                self.zoomDelta(True)
            if currentInputAction in InputManager()["Canvas.ZoomOut"]:
                self.zoomDelta(False)
            if currentInputAction in InputManager()["Canvas.ResetScale"]:
                self.reset_scale()

            if currentInputAction in InputManager()["Canvas.KillSelected"]:
                self.killSelectedNodes()
                self.killSelectedConnections()
                EditorHistory().saveState("Kill selected")

            if currentInputAction in InputManager()["Canvas.CopyNodes"]:
                self.copyNodes()
            if currentInputAction in InputManager()["Canvas.CutNodes"]:
                self.cutNodes()
            if currentInputAction in InputManager()["Canvas.DuplicateNodes"]:
                self.duplicateNodes()
            if currentInputAction in InputManager()["Canvas.PasteNodes"]:
                self.pasteNodes()
                EditorHistory().saveState("Paste nodes")

        QGraphicsView.keyPressEvent(self, event)

    def duplicateNodes(self):
        copiedJson = self.copyNodes()
        self.pasteNodes(data=copiedJson)
        EditorHistory().saveState("Duplicate nodes")

    def makeSerializedNodesUnique(self, nodes, extra=[]):
        copiedNodes = deepcopy(nodes)
        # make names unique
        renameData = {}
        existingNames = self.graphManager.getAllNames() + extra
        for node in copiedNodes:
            newName = getUniqNameFromList(existingNames, node['name'])
            existingNames.append(newName)
            renameData[node['name']] = newName
            # rename old name in header data
            node["wrapper"]["headerHtml"] = node["wrapper"]["headerHtml"].replace(node['name'], newName)
            node['name'] = newName
            node['uuid'] = str(uuid.uuid4())
            for inp in node['inputs']:
                inp['fullName'] = '{0}_{1}'.format(node['name'], inp['name'])
                inp['uuid'] = str(uuid.uuid4())
            for out in node['outputs']:
                out['fullName'] = '{0}_{1}'.format(node['name'], out['name'])
                out['uuid'] = str(uuid.uuid4())

        # update connections
        for node in copiedNodes:
            for out in node['outputs']:
                for linkedToData in out['linkedTo']:
                    lhsNodeName = linkedToData["lhsNodeName"]
                    rhsNodeName = linkedToData["rhsNodeName"]
                    if lhsNodeName in renameData:
                        linkedToData["lhsNodeName"] = renameData[lhsNodeName]
                    if rhsNodeName in renameData:
                        linkedToData["rhsNodeName"] = renameData[rhsNodeName]
            for inp in node['inputs']:
                for linkedToData in inp['linkedTo']:
                    lhsNodeName = linkedToData["lhsNodeName"]
                    rhsNodeName = linkedToData["rhsNodeName"]
                    if lhsNodeName in renameData:
                        linkedToData["lhsNodeName"] = renameData[lhsNodeName]
                    if rhsNodeName in renameData:
                        linkedToData["rhsNodeName"] = renameData[rhsNodeName]

        for node in copiedNodes:
            if node['type'] == 'compound':
                node['graphData']['nodes'] = self.makeSerializedNodesUnique(node['graphData']['nodes'], extra=existingNames)
        return copiedNodes

    def cutNodes(self):
        self.copyNodes()
        self.killSelectedNodes()

    def copyNodes(self, toClipBoard=True):
        nodes = []
        selectedNodes = [i for i in self.nodes.values() if i.isSelected()]

        for node in selectedNodes:
            if node.isCommentNode and node.collapsed:
                selectedNodes.extend(node.owningNodes)

        if len(selectedNodes) == 0:
            return

        for n in selectedNodes:
            nodeJson = n.serialize()
            nodes.append(nodeJson)

        serializedNodeNames = [i["name"] for i in nodes]

        for nodeJson in nodes:
            for outJson in nodeJson["outputs"]:
                outJson["linkedTo"] = []
            for inpJson in nodeJson["inputs"]:
                for link in (inpJson["linkedTo"]):
                    if inpJson["dataType"] == "ExecPin":
                        if link["lhsNodeName"] not in serializedNodeNames:
                            inpJson["linkedTo"].remove(link)

        if len(nodes) > 0:
            copyJsonStr = json.dumps(nodes)
            if toClipBoard:
                QApplication.clipboard().clear()
                QApplication.clipboard().setText(copyJsonStr)
            return copyJsonStr

    def pasteNodes(self, move=True, data=None):
        if not data:
            nodes = None
            try:
                nodes = json.loads(QApplication.clipboard().text())
            except json.JSONDecodeError as err:
                return
        else:
            nodes = json.loads(data)

        existingNames = self.graphManager.getAllNames()
        nodes = self.makeSerializedNodesUnique(nodes, extra=existingNames)

        diff = QtCore.QPointF(self.mapToScene(self.mousePos)) - QtCore.QPointF(nodes[0]["x"], nodes[0]["y"])
        self.clearSelection()
        newNodes = {}

        nodesData = deepcopy(nodes)
        createdNodes = {}
        for node in nodesData:

            n = self._createNode(node)

            if n is None:
                continue
            createdNodes[n] = node

            if n is None:
                continue

            n.setSelected(True)
            if move:
                n.setPos(n.scenePos() + diff)

        for nodeJson in nodesData:
            for inpPinJson in nodeJson['inputs']:
                linkDatas = inpPinJson['linkedTo']
                for linkData in linkDatas:
                    try:
                        lhsNode = self.findNode(linkData["lhsNodeName"])
                        lhsNodePinId = linkData["outPinId"]
                        lhsPin = lhsNode.orderedOutputs[lhsNodePinId]

                        rhsNode = self.findNode(nodeJson["name"])
                        rhsNodePinId = linkData["inPinId"]
                        rhsPin = rhsNode.orderedInputs[rhsNodePinId]
                        connected = connectPins(lhsPin, rhsPin)
                        if connected:
                            self.createUIConnectionForConnectedPins(lhsPin.getWrapper()(), rhsPin.getWrapper()())
                    except Exception as e:
                        print(inpPinJson['fullName'], "not found")
                        continue

        # Hacks here!!
        # All nodes are copied. Nodes now do not know about under which comments they are
        # Expand all coped comments first
        for newNode, data in createdNodes.items():
            if newNode.isCommentNode:
                newNode.collapsed = False

        # Non comment nodes now can update owning comments
        for newNode, data in createdNodes.items():
            newNode.updateOwningCommentNode()

        # Restore comments collapsed state
        for newNode, data in createdNodes.items():
            if newNode.isCommentNode:
                newNode.collapsed = data["wrapper"]["collapsed"]

    @dispatch(str)
    def findNode(self, name):
        for node in self.nodes.values():
            if name == node.name:
                return node
        return None

    def alignSelectedNodes(self, direction):
        ls = [n for n in self.getAllNodes() if n.isSelected()]

        x_positions = [p.scenePos().x() for p in ls]
        y_positions = [p.scenePos().y() for p in ls]

        if direction == Direction.Left:
            if len(x_positions) == 0:
                return
            x = min(x_positions)
            for n in ls:
                p = n.scenePos()
                p.setX(x)
                n.setPos(p)

        if direction == Direction.Right:
            if len(x_positions) == 0:
                return
            x = max(x_positions)
            for n in ls:
                p = n.scenePos()
                p.setX(x)
                n.setPos(p)

        if direction == Direction.Up:
            if len(y_positions) == 0:
                return
            y = min(y_positions)
            for n in ls:
                p = n.scenePos()
                p.setY(y)
                n.setPos(p)

        if direction == Direction.Down:
            if len(y_positions) == 0:
                return
            y = max(y_positions)
            for n in ls:
                p = n.scenePos()
                p.setY(y)
                n.setPos(p)
        EditorHistory().saveState("Align nodes")

    def findGoodPlaceForNewNode(self):
        polygon = self.mapToScene(self.viewport().rect())
        ls = polygon.toList()
        point = QtCore.QPointF(
            (ls[1].x() - ls[0].x()) / 2, (ls[3].y() - ls[2].y()) / 2)
        point += ls[0]
        point.setY(point.y() + polygon.boundingRect().height() / 3)
        point += QtCore.QPointF(float(random.randint(50, 200)),
                                float(random.randint(50, 200)))
        return point

    def keyReleaseEvent(self, event):
        QGraphicsView.keyReleaseEvent(self, event)

    def nodeFromInstance(self, instance):
        if isinstance(instance, UINodeBase):
            return instance
        node = instance
        while (isinstance(node, QGraphicsItem) or isinstance(node, QGraphicsWidget) or isinstance(node, QGraphicsProxyWidget)) and node.parentItem():
            node = node.parentItem()
        if isinstance(node, UINodeBase):
            return node
        else:
            return None

    def getReruteNode(self, pos, connection=None):
        nodeClassName = "reroute"
        if connection and connection.drawSource._rawPin.isExec() and connection.drawDestination._rawPin.isExec():
            nodeClassName = "rerouteExecs"
        else:
            if self.pressedPin and self.pressedPin.isExec():
                nodeClassName = "rerouteExecs"
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate['package'] = "PyFlowBase"
        nodeTemplate['lib'] = None
        nodeTemplate['type'] = nodeClassName
        nodeTemplate['name'] = "reroute"
        nodeTemplate['x'] = self.mapToScene(pos).x()
        nodeTemplate['y'] = self.mapToScene(pos).y()
        nodeTemplate['uuid'] = str(uuid.uuid4())
        nodeTemplate['meta']['label'] = "reroute"
        reruteNode = self.createNode(nodeTemplate)
        reruteNode.translate(-reruteNode.boundingRect().center().x(), -5)
        return reruteNode

    def getInputNode(self):
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate['package'] = "PyFlowBase"
        nodeTemplate['lib'] = None
        nodeTemplate['type'] = "graphInputs"
        nodeTemplate['name'] = "graphInputs"
        nodeTemplate['x'] = self.boundingRect.left() + 50
        nodeTemplate['y'] = self.boundingRect.center().y() + 50
        nodeTemplate['uuid'] = str(uuid.uuid4())
        nodeTemplate['meta']['label'] = "Inputs"
        node = self.createNode(nodeTemplate)
        node.translate(-20, 0)
        return node

    def getOutputNode(self):
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate['package'] = "PyFlowBase"
        nodeTemplate['lib'] = None
        nodeTemplate['type'] = "graphOutputs"
        nodeTemplate['name'] = "graphOutputs"
        nodeTemplate['x'] = self.boundingRect.width() - 50
        nodeTemplate['y'] = self.boundingRect.center().y() + 50
        nodeTemplate['uuid'] = str(uuid.uuid4())
        nodeTemplate['meta']['label'] = "Outputs"
        node = self.createNode(nodeTemplate)
        node.translate(-20, 0)
        return node

    def validateConnections(self, graph):
        """Hides show if needed. Changes endpoints positions if needed
        """
        checked = set()
        for node in graph.getNodesList():
            uiNode = node.getWrapper()
            for pin in uiNode.UIPins.values():
                for connection in pin.uiConnectionList:
                    if connection in checked:
                        continue

                    # override src endpoint to comment left side if connected
                    # node is hidden and under collapsed comment
                    srcNode = connection.source().owningNode()
                    if srcNode.isUnderActiveGraph():
                        comment = srcNode.owningCommentNode
                        if comment is not None and comment.collapsed and not srcNode.isVisible():
                            connection.sourcePositionOverride = comment.getRightSideEdgesPoint

                    # override dst endpoint to comment right side if connected
                    # node is hidden and under collapsed comment
                    dstNode = connection.destination().owningNode()
                    if dstNode.isUnderActiveGraph():
                        comment = dstNode.owningCommentNode
                        if comment is not None and comment.collapsed and not dstNode.isVisible():
                            connection.destinationPositionOverride = comment.getLeftSideEdgesPoint

                    if connection.isUnderCollapsedComment():
                        connection.hide()
                    if not connection.source().owningNode().isUnderActiveGraph() or not connection.destination().owningNode().isUnderActiveGraph():
                        connection.hide()

                    checked.add(connection)

    def validateCommentNodesOwnership(self, graph, bExpandComments=True):
        state = self.state
        self.state = CanvasState.COMMENT_OWNERSHIP_VALIDATION
        comments = {}
        defaultNodes = set()
        # expand all comment nodes and reset owning nodes info
        for node in graph.getNodesList():
            uiNode = node.getWrapper()
            if uiNode.isUnderActiveGraph():
                if uiNode.isCommentNode:
                    comments[uiNode] = uiNode.collapsed
                    if not uiNode.collapsed:
                        if bExpandComments:
                            uiNode.collapsed = False
                        uiNode.owningNodes.clear()
                else:
                    defaultNodes.add(uiNode)

        # apply comment to comment membership
        for commentNode in comments:
            commentNode.updateOwningCommentNode()

        # apply node to comment membership
        for node in defaultNodes:
            node.updateOwningCommentNode()

        # restore comments collapse state
        for comment, wasCollapsed in comments.items():
            comment.collapsed = wasCollapsed
        self.state = state

    def mousePressEvent(self, event):
        self.pressed_item = self.itemAt(event.pos())
        node = self.nodeFromInstance(self.pressed_item)
        self.pressedPin = self.findPinNearPosition(event.pos())
        modifiers = event.modifiers()
        self.mousePressPose = event.pos()
        expandComments = False
        self.validateCommentNodesOwnership(self.graphManager.activeGraph(), expandComments)
        currentInputAction = InputAction("temp", "temp", InputActionType.Mouse, event.button(), modifiers=modifiers)
        if any([not self.pressed_item,
                isinstance(self.pressed_item, UIConnection) and modifiers != QtCore.Qt.AltModifier,
                isinstance(self.pressed_item, UINodeBase) and node.isCommentNode and not node.collapsed,
                isinstance(node, UINodeBase) and (node.resizable and node.shouldResize(self.mapToScene(event.pos()))["resize"])]):
            self.resizing = False
            if isinstance(node, UINodeBase) and (node.isCommentNode or node.resizable):
                super(Canvas, self).mousePressEvent(event)
                self.resizing = node.bResize
                node.setSelected(False)
            if not self.resizing:
                if isinstance(self.pressed_item, UIConnection) and modifiers == QtCore.Qt.NoModifier and event.button() == QtCore.Qt.LeftButton:
                    closestPin = self.findPinNearPosition(event.pos(), 20)
                    if closestPin is not None:
                        if closestPin.direction == PinDirection.Input:
                            self.pressed_item.destinationPositionOverride = lambda: self.mapToScene(self.mousePos)
                        elif closestPin.direction == PinDirection.Output:
                            self.pressed_item.sourcePositionOverride = lambda: self.mapToScene(self.mousePos)
                        self.reconnectingWires.add(self.pressed_item)
                elif event.button() == QtCore.Qt.LeftButton and modifiers in [QtCore.Qt.NoModifier, QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier, QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]:
                    self.manipulationMode = CanvasManipulationMode.SELECT
                    self._selectionRect = SelectionRect(graph=self, mouseDownPos=self.mapToScene(event.pos()), modifiers=modifiers)
                    self._selectionRect.selectFullyIntersectedItems = True
                    self._mouseDownSelection = [node for node in self.selectedNodes()]
                    self._mouseDownConnectionsSelection = [node for node in self.selectedConnections()]
                    if modifiers not in [QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier]:
                        self.clearSelection()
                else:
                    if hasattr(self, "_selectionRect") and self._selectionRect is not None:
                        self._selectionRect.destroy()
                        self._selectionRect = None
                LeftPaning = event.button() == QtCore.Qt.LeftButton and modifiers == QtCore.Qt.AltModifier
                if currentInputAction in InputManager()["Canvas.Pan"]:
                    self.manipulationMode = CanvasManipulationMode.PAN
                    self._lastPanPoint = self.mapToScene(event.pos())
                elif currentInputAction in InputManager()["Canvas.Zoom"]:
                    self.manipulationMode = CanvasManipulationMode.ZOOM
                    self._lastTransform = QtGui.QTransform(self.transform())
                    self._lastSceneRect = self.sceneRect()
                    self._lastSceneCenter = self._lastSceneRect.center()
                    self._lastScenePos = self.mapToScene(event.pos())
                    self._lastOffsetFromSceneCenter = self._lastScenePos - self._lastSceneCenter
            self.node_box.hide()
        else:
            if not isinstance(self.pressed_item, NodesBox) and self.node_box.isVisible():
                self.node_box.hide()
                self.node_box.lineEdit.clear()
            if isinstance(self.pressed_item, UIPinBase) and not type(self.pressed_item) is PinGroup:
                if event.button() == QtCore.Qt.LeftButton and modifiers == QtCore.Qt.NoModifier:
                    self.pressed_item.topLevelItem().setFlag(QGraphicsItem.ItemIsMovable, False)
                    self.pressed_item.topLevelItem().setFlag(QGraphicsItem.ItemIsSelectable, False)
                    self._drawRealtimeLine = True
                    self.autoPanController.start()
                elif event.button() == QtCore.Qt.LeftButton and modifiers == QtCore.Qt.ControlModifier:
                    for wire in self.pressed_item.uiConnectionList:
                        if self.pressed_item.direction == PinDirection.Input:
                            wire.destinationPositionOverride = lambda: self.mapToScene(self.mousePos)
                        elif self.pressed_item.direction == PinDirection.Output:
                            wire.sourcePositionOverride = lambda: self.mapToScene(self.mousePos)
                        self.reconnectingWires.add(wire)
                if currentInputAction in InputManager()["Canvas.DisconnectPin"]:
                    self.removeEdgeCmd(self.pressed_item.connections)
                    self._drawRealtimeLine = False
            else:
                if isinstance(self.pressed_item, UIConnection) and modifiers == QtCore.Qt.AltModifier:
                    reruteNode = self.getReruteNode(event.pos(), self.pressed_item)
                    self.clearSelection()
                    reruteNode.setSelected(True)
                    for inp in reruteNode.UIinputs.values():
                        if canConnectPins(self.pressed_item.source()._rawPin, inp._rawPin):
                            drawPin = self.pressed_item.drawSource
                            if self.pressed_item.source().isExec():
                                self.pressed_item.kill()
                            self.connectPins(self.pressed_item.source(), inp)
                            for conection in inp.connections:
                                conection.drawSource = drawPin
                            break
                    for out in reruteNode.UIoutputs.values():
                        drawPin = self.pressed_item.drawDestination
                        if canConnectPins(out._rawPin, self.pressed_item.destination()._rawPin):
                            self.connectPins(out, self.pressed_item.destination())
                            for conection in out.connections:
                                conection.drawDestination = drawPin
                            break
                    self.pressed_item = reruteNode
                    self.manipulationMode = CanvasManipulationMode.MOVE
                else:
                    if isinstance(self.pressed_item, UINodeBase) and node.isCommentNode:
                        if node.bResize:
                            return

                    if type(self.pressed_item) is PinGroup:
                        self.pressed_item.onClick()
                        return

                    if currentInputAction in InputManager()["Canvas.DragChainedNodes"]:
                        if node.isCommentNode:
                            self.manipulationMode = CanvasManipulationMode.PAN
                            return
                        if modifiers != QtCore.Qt.ShiftModifier:
                            self.clearSelection()
                        node.setSelected(True)
                        selectedNodes = self.selectedNodes()
                        if len(selectedNodes) > 0:
                            for snode in selectedNodes:
                                for n in node.getChainedNodes():
                                    n.setSelected(True)
                                snode.setSelected(True)
                    else:
                        if modifiers in [QtCore.Qt.NoModifier, QtCore.Qt.AltModifier]:
                            super(Canvas, self).mousePressEvent(event)
                        if modifiers == QtCore.Qt.ControlModifier and event.button() == QtCore.Qt.LeftButton:
                            node.setSelected(not node.isSelected())
                        if modifiers == QtCore.Qt.ShiftModifier:
                            node.setSelected(True)
                    if currentInputAction in InputManager()["Canvas.DragNodes"]:
                        self.manipulationMode = CanvasManipulationMode.MOVE
                        if self.pressed_item.objectName() == "MouseLocked":
                            super(Canvas, self).mousePressEvent(event)
                    if currentInputAction in InputManager()["Canvas.DragCopyNodes"]:
                        self.manipulationMode = CanvasManipulationMode.COPY

    def pan(self, delta):
        rect = self.sceneRect()
        scale = self.currentViewScale()
        x = -delta.x() / scale
        y = -delta.y() / scale
        rect.translate(x, y)
        self.setSceneRect(rect)
        self.update()

    def updateRerutes(self, event, showPins=False):
        tolerance = 9 * self.currentViewScale()
        mouseRect = QtCore.QRect(QtCore.QPoint(event.pos().x() - tolerance, event.pos().y() - tolerance),
                                 QtCore.QPoint(event.pos().x() + tolerance, event.pos().y() + tolerance))
        hoverItems = self.items(mouseRect)
        self.hoveredRerutes += [node for node in hoverItems if isinstance(node, UIRerouteNodeSmall)]
        for node in self.hoveredRerutes:
            if showPins:
                if node in hoverItems:
                    node.showPins()
                else:
                    node.hidePins()
                    self.hoveredRerutes.remove(node)
            else:
                node.hidePins()
                self.hoveredRerutes.remove(node)

    def mouseMoveEvent(self, event):
        self.mousePos = event.pos()
        mouseDelta = QtCore.QPointF(self.mousePos) - self._lastMousePos
        modifiers = event.modifiers()
        node = self.nodeFromInstance(self.itemAt(event.pos()))
        self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        if self.itemAt(event.pos()) and isinstance(node, UINodeBase) and node.resizable:
            resizeOpts = node.shouldResize(self.mapToScene(event.pos()))
            if resizeOpts["resize"] or node.bResize:
                if resizeOpts["direction"] in [(1, 0), (-1, 0)]:
                    self.viewport().setCursor(QtCore.Qt.SizeHorCursor)
                elif resizeOpts["direction"] in [(0, 1), (0, -1)]:
                    self.viewport().setCursor(QtCore.Qt.SizeVerCursor)
                elif resizeOpts["direction"] in [(1, 1), (-1, -1)]:
                    self.viewport().setCursor(QtCore.Qt.SizeFDiagCursor)
                elif resizeOpts["direction"] in [(-1, 1), (1, -1)]:
                    self.viewport().setCursor(QtCore.Qt.SizeBDiagCursor)

        if self._drawRealtimeLine:
            if isinstance(self.pressed_item, PinBase):
                if self.pressed_item.parentItem().isSelected():
                    self.pressed_item.parentItem().setSelected(False)
            if self.realTimeLine not in self.scene().items():
                self.scene().addItem(self.realTimeLine)

            self.updateRerutes(event, True)

            p1 = self.pressed_item.scenePos() + self.pressed_item.pinCenter()
            p2 = self.mapToScene(self.mousePos)

            mouseRect = QtCore.QRect(QtCore.QPoint(event.pos().x() - 5, event.pos().y() - 4),
                                     QtCore.QPoint(event.pos().x() + 5, event.pos().y() + 4))
            hoverItems = self.items(mouseRect)

            hoveredPins = [pin for pin in hoverItems if isinstance(pin, UIPinBase)]
            if len(hoveredPins) > 0:
                item = hoveredPins[0]
                if isinstance(item, UIPinBase) and isinstance(self.pressed_item, UIPinBase):
                    canBeConnected = canConnectPins(self.pressed_item._rawPin, item._rawPin)
                    self.realTimeLine.setPen(self.realTimeLineValidPen if canBeConnected else self.realTimeLineInvalidPen)
                    if canBeConnected:
                        p2 = item.scenePos() + item.pinCenter()
            else:
                self.realTimeLine.setPen(self.realTimeLineNormalPen)

            distance = p2.x() - p1.x()
            multiply = 3
            path = QtGui.QPainterPath()
            path.moveTo(p1)
            path.cubicTo(QtCore.QPoint(p1.x() + distance / multiply, p1.y()),
                         QtCore.QPoint(p2.x() - distance / 2, p2.y()), p2)
            self.realTimeLine.setPath(path)
            if modifiers == QtCore.Qt.AltModifier:
                self._drawRealtimeLine = False
                if self.realTimeLine in self.scene().items():
                    self.removeItemByName('RealTimeLine')
                reruteNode = self.getReruteNode(event.pos())
                self.clearSelection()
                reruteNode.setSelected(True)
                for inp in reruteNode.UIinputs.values():
                    if canConnectPins(self.pressed_item._rawPin, inp._rawPin):
                        self.connectPins(self.pressed_item, inp)
                        break
                for out in reruteNode.UIoutputs.values():
                    if canConnectPins(self.pressed_item._rawPin, out._rawPin):
                        self.connectPins(self.pressed_item, out)
                        break
                self.pressed_item = reruteNode
                self.manipulationMode = CanvasManipulationMode.MOVE
        if self.manipulationMode == CanvasManipulationMode.SELECT:
            dragPoint = self.mapToScene(event.pos())
            self._selectionRect.setDragPoint(dragPoint, modifiers)
            # This logic allows users to use ctrl and shift with rectangle
            # select to add / remove nodes.
            node = self.nodeFromInstance(self.pressed_item)
            if isinstance(self.pressed_item, UINodeBase) and node.isCommentNode:
                nodes = [node for node in self.getAllNodes() if not node.isCommentNode]
            else:
                nodes = self.getAllNodes()

            if modifiers == QtCore.Qt.ControlModifier:
                # handle nodes
                for node in nodes:
                    if node in self._mouseDownSelection:
                        if node.isSelected() and self._selectionRect.collidesWithItem(node):
                            node.setSelected(False)
                        elif not node.isSelected() and not self._selectionRect.collidesWithItem(node):
                            node.setSelected(True)
                    else:
                        if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                            node.setSelected(True)
                        elif node.isSelected() and not self._selectionRect.collidesWithItem(node):
                            if node not in self._mouseDownSelection:
                                node.setSelected(False)

                # handle connections
                for wire in self.connections.values():
                    if wire in self._mouseDownConnectionsSelection:
                        if wire.isSelected() and QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                            wire.setSelected(False)
                        elif not wire.isSelected() and not QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                            wire.setSelected(True)
                    else:
                        if not wire.isSelected() and QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                            wire.setSelected(True)
                        elif wire.isSelected() and not QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                            if wire not in self._mouseDownConnectionsSelection:
                                wire.setSelected(False)

            elif modifiers == QtCore.Qt.ShiftModifier:
                for node in nodes:
                    if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                        node.setSelected(True)
                    elif node.isSelected() and not self._selectionRect.collidesWithItem(node):
                        if node not in self._mouseDownSelection:
                            node.setSelected(False)

                for wire in self.connections.values():
                    if not wire.isSelected() and QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                        wire.setSelected(True)
                    elif wire.isSelected() and not QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                        if wire not in self._mouseDownConnectionsSelection:
                            wire.setSelected(False)

            elif modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier:
                for node in nodes:
                    if self._selectionRect.collidesWithItem(node):
                        node.setSelected(False)

                for wire in self.connections.values():
                    if QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                        wire.setSelected(False)
            else:
                self.clearSelection()
                for node in nodes:
                    # if node not in [self.inputsItem,self.outputsItem]:
                    if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                        node.setSelected(True)
                    elif node.isSelected() and not self._selectionRect.collidesWithItem(node):
                        node.setSelected(False)

                for wire in self.connections.values():
                    if not wire.isSelected() and QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                        wire.setSelected(True)
                    elif wire.isSelected() and not QtWidgets.QGraphicsWidget.collidesWithItem(self._selectionRect, wire):
                        wire.setSelected(False)
        elif self.manipulationMode == CanvasManipulationMode.MOVE:
            if self.pressed_item.objectName() == "MouseLocked":
                super(Canvas, self).mouseMoveEvent(event)
            else:
                newPos = self.mapToScene(event.pos())
                scaledDelta = mouseDelta / self.currentViewScale()

                selectedNodes = self.selectedNodes()
                # Apply the delta to each selected node
                for node in selectedNodes:
                    node.translate(scaledDelta.x(), scaledDelta.y())

            if (isinstance(node, UIRerouteNode) or isinstance(node, UIRerouteNodeSmall)) and modifiers == QtCore.Qt.AltModifier:
                mouseRect = QtCore.QRect(QtCore.QPoint(event.pos().x() - 1, event.pos().y() - 1),
                                         QtCore.QPoint(event.pos().x() + 1, event.pos().y() + 1))
                hoverItems = self.items(mouseRect)
                newOuts = []
                newIns = []
                for item in hoverItems:
                    if isinstance(item, UIConnection):
                        if list(node.UIinputs.values())[0].connections and list(node.UIoutputs.values())[0].connections:
                            if item.source() == list(node.UIinputs.values())[0].connections[0].source():
                                newOuts.append([item.destination(), item.drawDestination])
                            if item.destination() == list(node.UIoutputs.values())[0].connections[0].destination():
                                newIns.append([item.source(), item.drawSource])
                for out in newOuts:
                    self.connectPins(list(node.UIoutputs.values())[0], out[0])
                for inp in newIns:
                    self.connectPins(inp[0], list(node.UIinputs.values())[0])
        elif self.manipulationMode == CanvasManipulationMode.PAN:
            self.pan(mouseDelta)
        elif self.manipulationMode == CanvasManipulationMode.ZOOM:
            zoomFactor = 1.0
            if mouseDelta.x() > 0:
                zoomFactor = 1.0 + mouseDelta.x() / 100.0
            else:
                zoomFactor = 1.0 / (1.0 + abs(mouseDelta.x()) / 100.0)
            self.zoom(zoomFactor)
        elif self.manipulationMode == CanvasManipulationMode.COPY:
            delta = self.mousePos - self.mousePressPose 
            if delta.manhattanLength() > 15:
                self.manipulationMode = CanvasManipulationMode.MOVE
                selectedNodes = self.selectedNodes()
                copiedNodes = self.copyNodes(toClipBoard=False)
                self.pasteNodes(move=False, data=copiedNodes)
                scaledDelta = delta / self.currentViewScale()
                for node in self.selectedNodes():
                    node.translate(scaledDelta.x(), scaledDelta.y())
                EditorHistory().saveState("Drag copy nodes")
        else:
            super(Canvas, self).mouseMoveEvent(event)
        self.autoPanController.Tick(self.viewport().rect(), event.pos())
        self._lastMousePos = event.pos()

    def findPinNearPosition(self, scenePos, tolerance=3):
        tolerance = tolerance * self.currentViewScale()
        rect = QtCore.QRect(QtCore.QPoint(scenePos.x() - tolerance, scenePos.y() - tolerance),
                            QtCore.QPoint(scenePos.x() + tolerance, scenePos.y() + tolerance))
        items = self.items(rect)
        pins = [i for i in items if isinstance(i, UIPinBase) and type(i) is not PinGroup]
        if len(pins) > 0:
            return pins[0]
        return None

    def mouseReleaseEvent(self, event):
        super(Canvas, self).mouseReleaseEvent(event)

        modifiers = event.modifiers()

        self.autoPanController.stop()
        self.mouseReleasePos = event.pos()
        self.released_item = self.itemAt(event.pos())
        self.releasedPin = self.findPinNearPosition(event.pos())
        self._resize_group_mode = False
        self.viewport().setCursor(QtCore.Qt.ArrowCursor)

        if self.manipulationMode == CanvasManipulationMode.MOVE and len(self.selectedNodes()) > 0:
            EditorHistory().saveState("Move nodes")

        if len(self.reconnectingWires) > 0:
            if self.releasedPin is not None:
                for wire in self.reconnectingWires:
                    if wire.destinationPositionOverride is not None:
                        lhsPin = wire.source()
                        self.removeConnection(wire)
                        self.connectPinsInternal(lhsPin, self.releasedPin)
                        EditorHistory().saveState("Reconnect pins")
                    elif wire.sourcePositionOverride is not None:
                        rhsPin = wire.destination()
                        self.removeConnection(wire)
                        self.connectPinsInternal(self.releasedPin, rhsPin)
                        EditorHistory().saveState("Reconnect pins")
            else:
                for wire in self.reconnectingWires:
                    self.removeConnection(wire)
                EditorHistory().saveState("Tear off connection")

            for wire in self.reconnectingWires:
                wire.sourcePositionOverride = None
                wire.destinationPositionOverride = None
            self.reconnectingWires.clear()

        for n in self.getAllNodes():
            if not n.isCommentNode:
                n.setFlag(QGraphicsItem.ItemIsMovable)
                n.setFlag(QGraphicsItem.ItemIsSelectable)

        if self._drawRealtimeLine:
            self._drawRealtimeLine = False
            if self.realTimeLine in self.scene().items():
                self.removeItemByName('RealTimeLine')

        if self.manipulationMode == CanvasManipulationMode.SELECT:
            self._selectionRect.destroy()
            self._selectionRect = None

        if event.button() == QtCore.Qt.RightButton and modifiers == QtCore.Qt.NoModifier:
            # show nodebox only if drag is small and no items under cursor
            if self.pressed_item is None or (isinstance(self.pressed_item, UINodeBase) and self.nodeFromInstance(self.pressed_item).isCommentNode):
                if modifiers == QtCore.Qt.NoModifier:
                    dragDiff = self.mapToScene(self.mousePressPose) - self.mapToScene(event.pos())
                    if all([abs(i) < 0.4 for i in [dragDiff.x(), dragDiff.y()]]):
                        self.showNodeBox()
        elif event.button() == QtCore.Qt.RightButton and modifiers == QtCore.Qt.ControlModifier:
            self.menu.exec_(QtGui.QCursor.pos())
        elif event.button() == QtCore.Qt.LeftButton and self.releasedPin is None:
            if isinstance(self.pressed_item, UIPinBase) and not self.resizing and modifiers == QtCore.Qt.NoModifier:
                if not type(self.pressed_item) is PinGroup:
                    # suggest nodes that can be connected to pressed pin
                    self.showNodeBox(self.pressed_item.dataType, self.pressed_item.direction, self.pressed_item._rawPin.getCurrentStructure())
        self.manipulationMode = CanvasManipulationMode.NONE
        if not self.resizing:
            p_itm = self.pressedPin
            r_itm = self.releasedPin
            do_connect = True
            for i in [p_itm, r_itm]:
                if not i:
                    do_connect = False
                    break
                if not isinstance(i, UIPinBase):
                    do_connect = False
                    break
            if p_itm and r_itm:
                if p_itm.__class__.__name__ == UIPinBase.__name__ and r_itm.__class__.__name__ == UIPinBase.__name__:
                    if cycleCheck(p_itm, r_itm):
                        # print('cycles are not allowed')
                        do_connect = False

            if do_connect:
                if p_itm is not r_itm:
                    self.connectPins(p_itm, r_itm)

        # We don't want properties view go crazy
        # check if same node pressed and released left mouse button and not moved
        releasedNode = self.nodeFromInstance(self.released_item)
        pressedNode = self.nodeFromInstance(self.pressed_item)
        manhattanLengthTest = (self.mousePressPose - event.pos()).manhattanLength() <= 2
        if all([event.button() == QtCore.Qt.LeftButton, releasedNode is not None,
                pressedNode is not None, pressedNode == releasedNode, manhattanLengthTest]):

                # check if clicking on node action button
                if self.released_item is not None:
                    if isinstance(self.released_item.parentItem(), NodeActionButtonBase):
                        return

                self.tryFillPropertiesView(pressedNode)
        elif event.button() == QtCore.Qt.LeftButton:
            self.requestClearProperties.emit()
        self.resizing = False
        self.updateRerutes(event,False)
        self.validateCommentNodesOwnership(self.graphManager.activeGraph(), False)

    def removeItemByName(self, name):
        [self.scene().removeItem(i) for i in self.scene().items() if hasattr(i, 'name') and i.name == name]

    def tryFillPropertiesView(self, obj):
        if isinstance(obj, IPropertiesViewSupport):
            self.requestFillProperties.emit(obj.createPropertiesWidget)

    def wheelEvent(self, event):
        (xfo, invRes) = self.transform().inverted()
        topLeft = xfo.map(self.rect().topLeft())
        bottomRight = xfo.map(self.rect().bottomRight())
        center = (topLeft + bottomRight) * 0.5
        zoomFactor = 1.0 + event.delta() * self._mouseWheelZoomRate

        self.zoom(zoomFactor)

    def stepToCompound(self, compoundNode):
        self.graphManager.selectGraph(compoundNode)

    def drawBackground(self, painter, rect):
        super(Canvas, self).drawBackground(painter, rect)
        lod = self.getLodValueFromCurrentScale(3)
        self.boundingRect = rect

        polygon = self.mapToScene(self.viewport().rect())

        painter.fillRect(rect, QtGui.QBrush(editableStyleSheet().CanvasBgColor))

        left = int(rect.left()) - (int(rect.left()) % editableStyleSheet().GridSizeFine[0])
        top = int(rect.top()) - (int(rect.top()) % editableStyleSheet().GridSizeFine[0])

        if lod < 3:
            # Draw horizontal fine lines
            gridLines = []
            y = float(top)
            while y < float(rect.bottom()):
                gridLines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
                y += editableStyleSheet().GridSizeFine[0]
            painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColor, 1))
            painter.drawLines(gridLines)

            # Draw vertical fine lines
            gridLines = []
            x = float(left)
            while x < float(rect.right()):
                gridLines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
                x += editableStyleSheet().GridSizeFine[0]
            painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColor, 1))
            painter.drawLines(gridLines)

        # Draw thick grid
        left = int(rect.left()) - (int(rect.left()) % editableStyleSheet().GridSizeHuge[0])
        top = int(rect.top()) - (int(rect.top()) % editableStyleSheet().GridSizeHuge[0])

        # Draw vertical thick lines
        gridLines = []
        painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColorDarker, 1.5))
        x = left
        while x < rect.right():
            gridLines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
            x += editableStyleSheet().GridSizeHuge[0]
        painter.drawLines(gridLines)

        # Draw horizontal thick lines
        gridLines = []
        painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColorDarker, 1.5))
        y = top
        while y < rect.bottom():
            gridLines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
            y += editableStyleSheet().GridSizeHuge[0]
        painter.drawLines(gridLines)
        if editableStyleSheet().DrawNumbers[0] >= 1:
            # draw numbers
            scale = self.currentViewScale()
            f = painter.font()
            f.setPointSize(6 / min(scale, 1))
            f.setFamily("Consolas")
            painter.setFont(f)
            y = float(top)
            
            while y < float(rect.bottom()):
                y += editableStyleSheet().GridSizeFine[0]
                if abs(y) % 100 == 0 and y > rect.top() + 30:
                    painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColorDarker.lighter(300)))
                    painter.drawText(rect.left(), y - 1.0, str(y))

            x = float(left)
            while x < rect.right():
                x += editableStyleSheet().GridSizeHuge[0]
                if abs(x) % 100 == 0 and x > rect.left() + 30:
                    painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColorDarker.lighter(300)))
                    painter.drawText(x, rect.top() + painter.font().pointSize(), str(x))

    def _createNode(self, jsonTemplate):
        # Check if this node is variable get/set. Variables created in child graphs are not visible to parent ones
        # Stop any attempt to disrupt variable scope. Even if we accidentally forgot this check, GraphBase.addNode will fail
        if jsonTemplate['type'] in ['getVar', 'setVar']:
            var = self.graphManager.findVariableByUid(uuid.UUID(jsonTemplate['varUid']))
            variableLocation = var.location()
            graphLocation = self.graphManager.location()
            if len(variableLocation) > len(graphLocation):
                return None
            if len(variableLocation) == len(graphLocation):
                if Counter(variableLocation) != Counter(graphLocation):
                    return None

        nodeInstance = getNodeInstance(jsonTemplate, self)
        assert(nodeInstance is not None), "Node instance is not found!"
        nodeInstance.setPos(jsonTemplate["x"], jsonTemplate["y"])

        # set pins data
        for inpJson in jsonTemplate['inputs']:
            pin = nodeInstance.getPinSG(inpJson['name'], PinSelectionGroup.Inputs)
            if pin:
                pin.uid = uuid.UUID(inpJson['uuid'])
                try:
                    pin.setData(json.loads(inpJson['value'], cls=pin.jsonDecoderClass()))
                except:
                    pin.setData(pin.defaultValue())
                if inpJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        for outJson in jsonTemplate['outputs']:
            pin = nodeInstance.getPinSG(outJson['name'], PinSelectionGroup.Outputs)
            if pin:
                pin.uid = uuid.UUID(outJson['uuid'])
                try:
                    pin.setData(json.loads(outJson['value'], cls=pin.jsonDecoderClass()))
                except:
                    pin.setData(pin.defaultValue())
                if outJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        return nodeInstance

    def createNode(self, jsonTemplate, **kwargs):
        nodeInstance = self._createNode(jsonTemplate)
        EditorHistory().saveState("Create node {}".format(nodeInstance.name))
        return nodeInstance

    def createWrappersForGraph(self, rawGraph):
        # when raw graph was created, we need to create all ui wrappers for it
        uiNodesJsonData = {}
        for node in rawGraph.getNodesList():
            if node.getWrapper() is not None:
                continue
            uiNode = getUINodeInstance(node)
            uiNodeJsonTemplate = node.serialize()
            uiNodeJsonTemplate["wrapper"] = node.wrapperJsonData
            self.addNode(uiNode, uiNodeJsonTemplate, parentGraph=rawGraph)
            uiNode.updateNodeShape()
            uiNodesJsonData[uiNode] = uiNodeJsonTemplate

        # restore ui connections
        for rawNode in rawGraph.getNodesList():
            uiNode = rawNode.getWrapper()
            for outUiPin in uiNode.UIoutputs.values():
                for inputRawPin in getConnectedPins(outUiPin._rawPin):
                    inUiPin = inputRawPin.getWrapper()()
                    self.createUIConnectionForConnectedPins(outUiPin, inUiPin)

        for uiNode, data in uiNodesJsonData.items():
            if uiNode.isUnderActiveGraph():
                uiNode.show()
                if uiNode.isCommentNode:
                    uiNode.collapsed = False

        for uiNode, data in uiNodesJsonData.items():
            if uiNode.isUnderActiveGraph():
                if not uiNode.isCommentNode:
                    uiNode.updateOwningCommentNode()

        # comments should update collapsing info after everything was created
        for uiNode, data in uiNodesJsonData.items():
            if uiNode.isCommentNode:
                uiNode.collapsed = data["wrapper"]["collapsed"]
        self.validateCommentNodesOwnership(rawGraph)
        self.validateConnections(rawGraph)

    def addNode(self, uiNode, jsonTemplate, parentGraph=None):
        """Adds node to a graph

        :param uiNode: Raw node wrapper
        :type uiNode: :class:`~PyFlow.UI.Canvas.UINodeBase.UINodeBase`
        """

        uiNode.canvasRef = weakref.ref(self)
        self.scene().addItem(uiNode)

        assert(jsonTemplate is not None)

        if uiNode._rawNode.graph is None:
            # if added from node box
            self.graphManager.activeGraph().addNode(uiNode._rawNode, jsonTemplate)
        else:
            # When copy paste compound node. we are actually pasting a tree of graphs
            # So we need to put each node under correct graph
            assert(parentGraph is not None), "Parent graph is invalid"
            parentGraph.addNode(uiNode._rawNode, jsonTemplate)

        uiNode.postCreate(jsonTemplate)

    def createUIConnectionForConnectedPins(self, srcUiPin, dstUiPin):
        assert(srcUiPin is not None)
        assert(dstUiPin is not None)
        if srcUiPin.direction == PinDirection.Input:
            srcUiPin, dstUiPin = dstUiPin, srcUiPin
        uiConnection = UIConnection(srcUiPin, dstUiPin, self)
        self.scene().addItem(uiConnection)
        self.connections[uiConnection.uid] = uiConnection
        return uiConnection

    def connectPinsInternal(self, src, dst):
        result = connectPins(src._rawPin, dst._rawPin)
        if result:
            return self.createUIConnectionForConnectedPins(src, dst)
        return None

    def connectPins(self, src, dst):
        # Highest level connect pins function
        if src and dst:
            if canConnectPins(src._rawPin, dst._rawPin):
                wire = self.connectPinsInternal(src, dst)
                if wire is not None:
                    EditorHistory().saveState("Connect pins")

    def removeEdgeCmd(self, connections):
        for wire in list(connections):
            self.removeConnection(wire)

    def removeConnection(self, connection):
        src = connection.source()._rawPin
        dst = connection.destination()._rawPin
        # this will remove raw pins from affection lists
        # will call pinDisconnected for raw pins
        disconnectPins(src, dst)

        # call disconnection events for ui pins
        connection.source().pinDisconnected(connection.destination())
        connection.destination().pinDisconnected(connection.source())
        self.connections.pop(connection.uid)
        connection.source().uiConnectionList.remove(connection)
        connection.destination().uiConnectionList.remove(connection)
        connection.prepareGeometryChange()
        self.scene().removeItem(connection)

    def zoomDelta(self, direction):
        if direction:
            self.zoom(1 + 0.1)
        else:
            self.zoom(1 - 0.1)

    def reset_scale(self):
        self.resetMatrix()

    def viewMinimumScale(self):
        return self._minimum_scale

    def viewMaximumScale(self):
        return self._maximum_scale

    def currentViewScale(self):
        return self.transform().m22()

    def getLodValueFromScale(self, numLods=5, scale=1.0):
        lod = lerp(numLods, 1, GetRangePct(self.viewMinimumScale(), self.viewMaximumScale(), scale))
        return int(round(lod))

    def getLodValueFromCurrentScale(self, numLods=5):
        return self.getLodValueFromScale(numLods, self.currentViewScale())

    def zoom(self, scale_factor):
        self.factor = self.transform().m22()
        futureScale = self.factor * scale_factor
        if futureScale <= self._minimum_scale:
            scale_factor = (self._minimum_scale) / self.factor
        if futureScale >= self._maximum_scale:
            scale_factor = (self._maximum_scale - 0.1) / self.factor
        self.scale(scale_factor, scale_factor)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            self.showNodeBox()
        return False


class CanvasWidget(QWidget):
    """docstring for CanvasWidget."""
    def __init__(self, graphManager, pyFlowInstance, parent=None):
        super(CanvasWidget, self).__init__(parent)
        self.manager = graphManager
        self.pyFlowInstance = pyFlowInstance

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(1)
        self.mainLayout.setContentsMargins(1, 1, 1, 1)
        self.setContentsMargins(1, 1, 1, 1)
        self.mainLayout.setObjectName("canvasWidgetMainLayout")
        self.pathLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.pathLayout)
        self.compoundPropertiesWidget = QWidget()
        self.compoundPropertiesWidget.setContentsMargins(1, 1, 1, 1)
        self.compoundPropertiesWidget.setObjectName("compoundPropertiesWidget")
        self.compoundPropertiesLayout = QHBoxLayout(self.compoundPropertiesWidget)
        self.compoundPropertiesLayout.setSpacing(1)
        self.compoundPropertiesLayout.setContentsMargins(1, 1, 1, 1)
        self.mainLayout.addWidget(self.compoundPropertiesWidget)

        self.leCompoundName = QLineEdit()
        self.leCompoundName.setObjectName("leCompoundName")
        self.leCompoundCategory = QLineEdit()
        self.leCompoundCategory.setObjectName("leCompoundCategory")

        compoundNameLabel = QLabel("Name:")
        compoundNameLabel.setObjectName("compoundNameLabel")
        self.compoundPropertiesLayout.addWidget(compoundNameLabel)
        self.compoundPropertiesLayout.addWidget(self.leCompoundName)

        compoundCategoryLabel = QLabel("Category:")
        compoundCategoryLabel.setObjectName("compoundCategoryLabel")
        self.compoundPropertiesLayout.addWidget(compoundCategoryLabel)
        self.compoundPropertiesLayout.addWidget(self.leCompoundCategory)

        self.canvas = Canvas(graphManager, pyFlowInstance)
        self.mainLayout.addWidget(self.canvas)

        self.manager.graphChanged.connect(self.updateGraphTreeLocation)

        self.canvas.requestFillProperties.connect(self.pyFlowInstance.onRequestFillProperties)
        self.canvas.requestClearProperties.connect(self.pyFlowInstance.onRequestClearProperties)

        rxLettersAndNumbers = QtCore.QRegExp('^[a-zA-Z0-9]*$')
        nameValidator = QtGui.QRegExpValidator(rxLettersAndNumbers, self.leCompoundName)
        self.leCompoundName.setValidator(nameValidator)
        self.leCompoundName.returnPressed.connect(self.onActiveCompoundNameAccepted)

        rxLetters = QtCore.QRegExp('^[a-zA-Z]*$')
        categoryValidator = QtGui.QRegExpValidator(rxLetters, self.leCompoundCategory)
        self.leCompoundCategory.setValidator(categoryValidator)
        self.leCompoundCategory.returnPressed.connect(self.onActiveCompoundCategoryAccepted)

        self.updateGraphTreeLocation()

        self.pyFlowInstance.fileBeenLoaded.connect(self.onFileBeenLoaded)

    def shoutDown(self):
        self.canvas.shoutDown()

    def Tick(self, delta):
        self.canvas.Tick(delta)

    def onFileBeenLoaded(self):
        for graph in self.manager.getAllGraphs():
            self.canvas.createWrappersForGraph(graph)

    def updateGraphTreeLocation(self, *args, **kwargs):
        location = self.canvas.location()
        clearLayout(self.pathLayout)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.pathLayout.addItem(spacerItem)
        for folderName in location:
            index = self.pathLayout.count() - 1
            btn = QPushButton(folderName)

            def onClicked(checked, name=None):
                self.canvas.stepToCompound(name)

            btn.clicked.connect(lambda chk=False, name=folderName: onClicked(chk, name))
            self.pathLayout.insertWidget(index, btn)

        self.setCompoundPropertiesWidgetVisible(self.manager.activeGraph().depth() > 1)

    def setCompoundPropertiesWidgetVisible(self, bVisible):
        if bVisible:
            self.compoundPropertiesWidget.show()
            self.leCompoundName.setText(self.manager.activeGraph().name)
            self.leCompoundCategory.setText(self.manager.activeGraph().category)
        else:
            self.compoundPropertiesWidget.hide()

    def onActiveCompoundNameAccepted(self):
        newName = self.manager.getUniqName(self.leCompoundName.text())
        self.manager.activeGraph().name = newName
        self.leCompoundName.blockSignals(True)
        self.leCompoundName.setText(newName)
        self.leCompoundName.blockSignals(False)
        self.updateGraphTreeLocation()

    def onActiveCompoundCategoryAccepted(self):
        newCategoryName = self.leCompoundCategory.text()
        self.manager.activeGraph().category = newCategoryName
