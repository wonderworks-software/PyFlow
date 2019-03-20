import math
import platform
import random
from os import listdir, path
from time import ctime
import json
import re
import uuid
import weakref
try:
    from inspect import getfullargspec as getargspec
except:
    from inspect import getargspec

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsScene
from Qt.QtWidgets import QAbstractItemView
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QFileDialog
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QFrame
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QScrollArea
from Qt.QtWidgets import QRubberBand
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QAction
from Qt.QtWidgets import QTreeWidget, QTreeWidgetItem
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QMainWindow
from Qt.QtWidgets import QVBoxLayout
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsRectItem
from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsPathItem
from Qt.QtWidgets import QGraphicsView
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QUndoStack
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QPushButton

from Settings import Colors
from SelectionRect import SelectionRect
from PyFlow.UI.UIConnection import UIConnection
from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.UINodeBase import NodeName
from PyFlow.UI.UINodeBase import getUINodeInstance
from PyFlow.UI.Widgets.EditableLabel import EditableLabel
from PyFlow.Commands.CreateNode import CreateNode as cmdCreateNode
from PyFlow.Commands.RemoveNodes import RemoveNodes as cmdRemoveNodes
from PyFlow.Commands.ConnectPin import ConnectPin as cmdConnectPin
from PyFlow.Commands.RemoveEdges import RemoveEdges as cmdRemoveEdges
from PyFlow.UI.UIPinBase import UIPinBase
from PyFlow.Core.GraphBase import GraphBase
from PyFlow.Core.PinBase import PinBase
from PyFlow.Core.NodeBase import NodeBase
from PyFlow.UI.UIVariable import UIVariable
from PyFlow.UI.VariablesWidget import (
    VARIABLE_TAG,
    VARIABLE_DATA_TAG
)

from PyFlow import (
    getRawNodeInstance,
    GET_PACKAGES
)
from PyFlow.Core.Common import *

from PyFlow.Packages.PyflowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyflowBase.UI.UIcommentNode import UIcommentNode
from PyFlow.Packages.PyflowBase.UI.UIRerouteNode import UIRerouteNode
from PyFlow.Packages.PyflowBase import PACKAGE_NAME as PYFLOW_BASE_PACKAGE_NAME


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


def importByName(module, name):

    if hasattr(module, name):
        try:
            mod = getattr(module, name)
            return mod
        except Exception as e:
            print(e)
            return
    else:
        print("error", name)


def getNodeInstance(jsonTemplate, graph):
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
        kwargs['var'] = graph.vars[uuid.UUID(jsonTemplate['meta']['var']['uuid'])]

    raw_instance = getRawNodeInstance(nodeClassName, packageName, libName, **kwargs)
    raw_instance.uid = uuid.UUID(jsonTemplate['uuid'])
    assert(raw_instance is not None), "Node {0} not found in package {1}".format(
        nodeClassName, packageName)
    instance = getUINodeInstance(raw_instance)
    graph.addNode(instance)
    return instance


class AutoPanController(object):
    def __init__(self, amount=10.0):
        super(AutoPanController, self).__init__()
        self.bAllow = False
        self.amount = amount
        self.autoPanDelta = QtGui.QVector2D(0.0, 0.0)
        self.beenOutside = False

    def Tick(self, rect, pos):
        if self.bAllow:
            if pos.x() < 0:
                self.autoPanDelta = QtGui.QVector2D(-self.amount, 0.0)
                self.beenOutside = True
                self.amount = clamp(abs(pos.x()) * 0.3, 0.0, 25.0)
            if pos.x() > rect.width():
                self.autoPanDelta = QtGui.QVector2D(self.amount, 0.0)
                self.beenOutside = True
                self.amount = clamp(
                    abs(rect.width() - pos.x()) * 0.3, 0.0, 25.0)
            if pos.y() < 0:
                self.autoPanDelta = QtGui.QVector2D(0.0, -self.amount)
                self.beenOutside = True
                self.amount = clamp(abs(pos.y()) * 0.3, 0.0, 25.0)
            if pos.y() > rect.height():
                self.autoPanDelta = QtGui.QVector2D(0.0, self.amount)
                self.beenOutside = True
                self.amount = clamp(
                    abs(rect.height() - pos.y()) * 0.3, 0.0, 25.0)
            if self.beenOutside and rect.contains(pos):
                self.reset()

    def getAmount(self):
        return self.amount

    def getDelta(self):
        return self.autoPanDelta

    def setAmount(self, amount):
        self.amount = amount

    def start(self):
        self.bAllow = True

    def isActive(self):
        return self.bAllow

    def stop(self):
        self.bAllow = False
        self.reset()

    def reset(self):
        self.beenOutside = False
        self.autoPanDelta = QtGui.QVector2D(0.0, 0.0)


class SceneClass(QGraphicsScene):
    def __init__(self, parent):
        super(SceneClass, self).__init__(parent)
        self.setItemIndexMethod(self.NoIndex)
        # self.pressed_port = None
        self.selectionChanged.connect(self.OnSelectionChanged)
        # self.tempnode = None
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

            # packageName = jsonData["package"]
            # nodeType = jsonData["type"]
            # libName = jsonData["lib"]
            # name = self.parent().getUniqNodeName(nodeType)

            # nodeTemplate = NodeBase.jsonTemplate()
            # nodeTemplate['package'] = packageName
            # nodeTemplate['lib'] = libName
            # nodeTemplate['type'] = nodeType
            # nodeTemplate['name'] = name
            # nodeTemplate['x'] = event.scenePos().x()
            # nodeTemplate['y'] = event.scenePos().y()
            # nodeTemplate['meta']['label'] = nodeType
            # nodeTemplate['uuid'] = None

            # try:
            #     self.tempnode.kill()
            #     self.tempnode.scene().removeItem(self.tempnode)
            # except Exception as e:
            #     pass
            # self.tempnode = getNodeInstance(nodeTemplate, self.parent())

            # self.tempnode.update()
            # self.tempnode.postCreate(nodeTemplate)
            # self.tempnode.isTemp = True
            # self.hoverItems = []
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            # if self.tempnode:
            #     self.tempnode.setPosition((self.tempnode.w / -2) + event.scenePos().x(), event.scenePos().y())
            #     mouseRect = QtCore.QRect(QtCore.QPoint(event.scenePos().x() - 1, event.scenePos().y() - 1),
            #                              QtCore.QPoint(event.scenePos().x() + 1, event.scenePos().y() + 1))
            #     hoverItems = self.items(mouseRect)
            #     for item in hoverItems:
            #         if isinstance(item, UIConnection):
            #             valid = False
            #             for inp in self.tempnode.inputs.values():
            #                 if self.parent().canConnectPins(item.source(), inp):
            #                     valid = True
            #             for out in self.tempnode.outputs.values():
            #                 if self.parent().canConnectPins(out, item.destination()):
            #                     valid = True
            #             if valid:
            #                 self.hoverItems.append(item)
            #                 item.drawThick()
            #         elif isinstance(item, UIRerouteNode):
            #             self.hoverItems.append(item)
            #             item.showPins()
            #     for item in self.hoverItems:
            #         if item not in hoverItems:
            #             self.hoverItems.remove(item)
            #             if isinstance(item, UIConnection):
            #                 item.restoreThick()
            #             elif isinstance(item, UIRerouteNode):
            #                 item.hidePins()

            # self.itemAt(event.pos()).drawThink()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # if self.tempnode:
        #     self.removeItem(self.tempnode)
        event.accept()

    def OnSelectionChanged(self):
        # selectedNodesUids = self.parent().selectedNodes()
        # cmdSelect = Commands.Select(selectedNodesUids, self.parent())
        # self.parent().undoStack.push(cmdSelect)
        pass

    def createVariableGetter(self):
        pass

    def dropEvent(self, event):
        # if self.tempnode:
        #     x = self.tempnode.scenePos().x()
        #     y = self.tempnode.scenePos().y()
        #     try:
        #         self.tempnode.kill()
        #     except:
        #         pass
        # else:
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

                    nodeTemplate['meta']['var']['uuid'] = varData['uuid']
                    m = QMenu()
                    getterAction = m.addAction('Get')

                    def varGetterCreator():
                        n = self.parent().createNode(nodeTemplate)
                        n.updateNodeShape(label=n.var.name)
                    getterAction.triggered.connect(varGetterCreator)

                    setNodeTemplate = dict(nodeTemplate)
                    setterAction = m.addAction('Set')
                    setNodeTemplate['type'] = 'setVar'
                    setterAction.triggered.connect(
                        lambda: self.parent().createNode(setNodeTemplate))
                    m.exec_(QtGui.QCursor.pos(), None)
                if modifiers == QtCore.Qt.ControlModifier:
                    nodeTemplate['type'] = 'getVar'
                    # node uid should be unique, different from var
                    nodeTemplate['uuid'] = str(uuid.uuid4())
                    nodeTemplate['meta']['var']['uuid'] = varData['uuid']
                    nodeTemplate['meta']['label'] = varData['name']
                    self.parent().createNode(nodeTemplate)
                    return
                if modifiers == QtCore.Qt.AltModifier:
                    nodeTemplate['type'] = 'setVar'
                    nodeTemplate['uuid'] = varData['uuid']
                    nodeTemplate['meta']['var']['uuid'] = varData['uuid']
                    nodeTemplate['meta']['label'] = varData['name']
                    self.parent().createNode(nodeTemplate)
                    return

            else:
                packageName = jsonData["package"]
                nodeType = jsonData["type"]
                libName = jsonData['lib']
                name = self.parent().getUniqNodeName(nodeType)
                dropItem = self.itemAt(event.scenePos(), QtGui.QTransform())
                if not dropItem or (isinstance(dropItem, UINodeBase) and dropItem.isCommentNode) or isinstance(dropItem, UIPinBase) or isinstance(dropItem, UIConnection):
                    nodeTemplate = NodeBase.jsonTemplate()
                    nodeTemplate['package'] = packageName
                    nodeTemplate['lib'] = libName
                    nodeTemplate['type'] = nodeType
                    nodeTemplate['name'] = name
                    nodeTemplate['x'] = x
                    nodeTemplate['y'] = y
                    nodeTemplate['meta']['label'] = nodeType
                    nodeTemplate['uuid'] = str(uuid.uuid4())

                    node = self.parent().createNode(nodeTemplate)

                    nodeInputs = node.inputs
                    nodeOutputs = node.outputs
                    if isinstance(dropItem, UIPinBase):
                        node.setPos(x - node.boundingRect().width(), y)
                        for inp in nodeInputs.values():
                            if self.parent().canConnectPins(dropItem, inp):
                                if dropItem.dataType == 'ExecPin':
                                    dropItem.disconnectAll()
                                self.parent().connectPins(dropItem, inp)
                                node.setPos(x + node.boundingRect().width(), y)
                                break
                        for out in nodeOutputs.values():
                            if self.parent().canConnectPins(out, dropItem):
                                self.parent().connectPins(out, dropItem)
                                node.setPos(x - node.boundingRect().width(), y)
                                break
                    if isinstance(dropItem, UIConnection):
                        for inp in nodeInputs.values():
                            if self.parent().canConnectPins(dropItem.source(), inp):
                                if dropItem.source().dataType == 'ExecPin':
                                    dropItem.source().disconnectAll()
                                self.parent().connectPins(dropItem.source(), inp)
                                break
                        for out in nodeOutputs.values():
                            if self.parent().canConnectPins(out, dropItem.destination()):
                                self.parent().connectPins(out, dropItem.destination())
                                break
        else:
            super(SceneClass, self).dropEvent(event)


class NodeBoxLineEdit(QLineEdit):
    def __init__(self, parent, events=True):
        super(NodeBoxLineEdit, self).__init__(parent)
        self.setParent(parent)
        self._events = events
        self.parent = parent
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English,
                                      QtCore.QLocale.UnitedStates))
        self.setObjectName("le_nodes")
        style = "background-color: rgb(80, 80, 80);" +\
                "border-radius: 2px;" +\
                "font-size: 14px;" +\
                "border-color: black; border-style: outset; border-width: 1px;"
        self.setStyleSheet(style)
        self.setPlaceholderText("enter node name..")


class NodeBoxTreeWidget(QTreeWidget):
    def __init__(self, parent):
        super(NodeBoxTreeWidget, self).__init__(parent)
        style = "background-color: rgb(40, 40, 40);" +\
                "selection-background-color: rgb(50, 50, 50);" +\
                "border-radius: 2px;" +\
                "font-size: 14px;" +\
                "border-color: black; border-style: outset; border-width: 1px;"
        self.setStyleSheet(style)
        self.setParent(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Sunken)
        self.setObjectName("tree_nodes")
        self.setSortingEnabled(True)
        self.setDragEnabled(True)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setAnimated(True)
        self.categoryPaths = {}

    def _isCategoryExists(self, category_name, categories):
        bFound = False
        if category_name in categories:
            return True
        if not bFound:
            for c in categories:
                sepCatNames = c.split('|')
                if len(sepCatNames) == 1:
                    if category_name == c:
                        return True
                else:
                    for i in range(0, len(sepCatNames)):
                        c = '|'.join(sepCatNames)
                        if category_name == c:
                            return True
                        sepCatNames.pop()
        return False

    def insertNode(self, nodeCategoryPath, name, doc=None, libName=None):
        nodePath = nodeCategoryPath.split('|')
        categoryPath = ''
        # walk from tree top to bottom, creating folders if needed
        # also writing all paths in dict to avoid duplications
        for folderId in range(0, len(nodePath)):
            folderName = nodePath[folderId]
            if folderId == 0:
                categoryPath = folderName
                if categoryPath not in self.categoryPaths:
                    rootFolderItem = QTreeWidgetItem(self)
                    rootFolderItem.bCategory = True
                    rootFolderItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    rootFolderItem.setText(0, folderName)
                    rootFolderItem.setBackground(
                        folderId, QtGui.QColor(80, 85, 80))
                    self.categoryPaths[categoryPath] = rootFolderItem
            else:
                parentCategoryPath = categoryPath
                categoryPath += '|{}'.format(folderName)
                if categoryPath not in self.categoryPaths:
                    childCategoryItem = QTreeWidgetItem(
                        self.categoryPaths[parentCategoryPath])
                    childCategoryItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    childCategoryItem.bCategory = True
                    childCategoryItem.setText(0, folderName)
                    childCategoryItem.setBackground(
                        0, QtGui.QColor(80, 85, 80))
                    self.categoryPaths[categoryPath] = childCategoryItem
        # create node under constructed folder
        nodeItem = QTreeWidgetItem(self.categoryPaths[categoryPath])
        nodeItem.bCategory = False
        nodeItem.setText(0, name)
        nodeItem.libName = libName
        if doc:
            nodeItem.setToolTip(0, doc)

    def refresh(self, dataType=None, pattern='', pinType=None):
        self.clear()
        self.categoryPaths = {}

        for package_name, package in GET_PACKAGES().items():
            # annotated functions
            for libName, lib in package.GetFunctionLibraries().items():
                foos = lib.getFunctions()
                for name, foo in foos.items():
                    foo = foo
                    libName = foo.__annotations__["lib"]
                    fooArgNames = getargspec(foo).args
                    fooInpTypes = []
                    fooOutTypes = []
                    if foo.__annotations__['nodeType'] == NodeTypes.Callable:
                        fooInpTypes.append('ExecPin')
                        fooOutTypes.append('ExecPin')

                    # consider return type if not None
                    if foo.__annotations__['return'] is not None:
                        fooOutTypes.append(foo.__annotations__['return'][0])

                    for index in range(len(fooArgNames)):
                        dType = foo.__annotations__[fooArgNames[index]]
                        # if tuple - this means ref pin type (output) + default value
                        # eg: (3, True) - bool with True default val
                        if isinstance(dType, tuple):
                            fooOutTypes.append(dType[0])
                        else:
                            fooInpTypes.append(dType)

                    nodeCategoryPath = "{0}|{1}".format(
                        package_name, foo.__annotations__['meta']['Category'])
                    keywords = foo.__annotations__['meta']['Keywords']
                    checkString = name + nodeCategoryPath + ''.join(keywords)
                    if pattern.lower() in checkString.lower():
                        # create all nodes items if clicked on canvas
                        if dataType is None:
                            self.insertNode(nodeCategoryPath,
                                            name, foo.__doc__, libName)
                        else:
                            if pinType == PinDirection.Output:
                                if dataType in fooInpTypes:
                                    self.insertNode(
                                        nodeCategoryPath, name, foo.__doc__, libName)
                            else:
                                if dataType in fooOutTypes:
                                    self.insertNode(
                                        nodeCategoryPath, name, foo.__doc__, libName)

            # class based nodes
            for node_class in package.GetNodeClasses().values():
                if node_class.__name__ in ('setVar', 'getVar'):
                    continue

                nodeCategoryPath = "{0}|{1}".format(
                    package_name, node_class.category())

                checkString = node_class.__name__ + \
                    nodeCategoryPath + ''.join(node_class.keywords())
                if pattern.lower() not in checkString.lower():
                    continue
                if dataType is None:
                    self.insertNode(
                        nodeCategoryPath, node_class.__name__, node_class.description())
                else:
                    # if pressed pin is output pin
                    # filter by nodes input types
                    if pinType == PinDirection.Output:
                        if dataType in node_class.pinTypeHints()['inputs']:
                            self.insertNode(
                                nodeCategoryPath, node_class.__name__, node_class.description())
                    else:
                        # if pressed pin is input pin
                        # filter by nodes output types
                        if dataType in node_class.pinTypeHints()['outputs']:
                            self.insertNode(
                                nodeCategoryPath, node_class.__name__, node_class.description())
            # expand all categories
            if dataType is not None:
                for categoryItem in self.categoryPaths.values():
                    categoryItem.setExpanded(True)

    def keyPressEvent(self, event):
        super(NodeBoxTreeWidget, self).keyPressEvent(event)
        key = event.key()
        if key == QtCore.Qt.Key_Return:
            item_clicked = self.currentItem()
            if not item_clicked:
                event.ignore()
                return
            # check if clicked item is a category
            if item_clicked.bCategory:
                event.ignore()
                return
            # find top level parent
            rootItem = item_clicked
            while not rootItem.parent() is None:
                rootItem = rootItem.parent()
            packageName = rootItem.text(0)
            pressed_text = item_clicked.text(0)
            libName = item_clicked.libName
            if pressed_text in self.categoryPaths.keys():
                event.ignore()
                return

            nodeClassName = self.currentItem().text(0)
            name = self.parent().graph().getUniqNodeName(nodeClassName)
            pos = self.parent().graph().mapToScene(self.parent().graph().mouseReleasePos)
            nodeTemplate = NodeBase.jsonTemplate()
            nodeTemplate['package'] = packageName
            nodeTemplate['lib'] = libName
            nodeTemplate['type'] = pressed_text
            nodeTemplate['name'] = name
            nodeTemplate['x'] = pos.x()
            nodeTemplate['y'] = pos.y()
            nodeTemplate['meta']['label'] = nodeClassName
            nodeTemplate['uuid'] = None

            self.parent().graph().createNode(nodeTemplate)

    def mousePressEvent(self, event):
        super(NodeBoxTreeWidget, self).mousePressEvent(event)
        item_clicked = self.currentItem()
        if not item_clicked:
            event.ignore()
            return
        # check if clicked item is a category
        if item_clicked.bCategory:
            event.ignore()
            return
        # find top level parent
        rootItem = item_clicked
        while not rootItem.parent() is None:
            rootItem = rootItem.parent()
        packageName = rootItem.text(0)
        pressed_text = item_clicked.text(0)
        libName = item_clicked.libName

        if pressed_text in self.categoryPaths.keys():
            event.ignore()
            return
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        jsonTemplate = NodeBase.jsonTemplate()
        jsonTemplate['package'] = packageName
        jsonTemplate['lib'] = libName
        jsonTemplate['type'] = pressed_text
        jsonTemplate['name'] = pressed_text

        pressed_text = json.dumps(jsonTemplate)
        mime_data.setText(pressed_text)
        drag.setMimeData(mime_data)
        drag.exec_()


class NodesBox(QWidget):
    """doc string for NodesBox"""

    def __init__(self, parent, graph=None):
        super(NodesBox, self).__init__(parent)
        self.graph = weakref.ref(graph)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.lineEdit = NodeBoxLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.treeWidget = NodeBoxTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)
        self.lineEdit.textChanged.connect(self.leTextChanged)
        self.treeWidget.refresh()

    def sizeHint(self):
        return QtCore.QSize(400, 250)

    def expandCategory(self):
        for i in self.treeWidget.categoryPaths:
            self.treeWidget.setItemExpanded(
                self.treeWidget.categoryPaths[i], True)

    def leTextChanged(self):
        if self.lineEdit.text() == '':
            self.lineEdit.setPlaceholderText("enter node name..")
            self.treeWidget.refresh()
            return
        self.treeWidget.refresh(None, self.lineEdit.text())
        self.expandCategory()


MANIP_MODE_NONE = 0
MANIP_MODE_SELECT = 1
MANIP_MODE_PAN = 2
MANIP_MODE_MOVE = 3
MANIP_MODE_ZOOM = 4
MANIP_MODE_COPY = 5

buttonStyle = """
QPushButton{color : rgba(255,255,255,255);
    background-color: rgba(150,150,150,150);
    border-width: 0px;
    border-color: transparent;
    border-style: solid;
    font-size: 10px;
    font-weight: bold;}
QPushButton:hover{
    color: rgba(255, 211, 25, 255);
}
QPushButton:pressed{
    color: rgba(255, 160, 47, 255)
}
"""


class GraphWidgetUI(QGraphicsView):
    _manipulationMode = MANIP_MODE_NONE

    _backgroundColor = Colors.SceneBackground  # QtGui.QColor(50, 50, 50)
    _gridPenS = Colors.GridColor
    _gridPenL = Colors.GridColorDarker
    _gridSizeFine = 10
    _gridSizeCourse = 100

    _mouseWheelZoomRate = 0.0005
    outPinCreated = QtCore.Signal(object)
    outPinDeleted = QtCore.Signal(object)
    inPinCreated = QtCore.Signal(object)
    inPinDeleted = QtCore.Signal(object)

    def __init__(self, parent=None, graphBase=None, parentGraph=None, parentNode=None):
        super(GraphWidgetUI, self).__init__()
        assert(isinstance(graphBase, GraphBase))
        self._graphBase = graphBase
        self._parentGraph = parentGraph
        self._parentNode = parentNode
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.undoStack = QUndoStack(self)
        self.parent = parent
        self.parent.actionClear_history.triggered.connect(self.undoStack.clear)
        self.parent.listViewUndoStack.setStack(self.undoStack)
        self.menu = QMenu()
        self.setScene(SceneClass(self))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pressed_item = None
        self.released_item = None
        self.resizing = False
        self.hoverItems = []
        self.bPanMode = False
        self.groupers = []
        self._isPanning = False
        self._mousePressed = False
        self._shadows = False
        self._scale = 1.0
        self._panSpeed = 1.0
        self.minimum_scale = 0.5
        self.maximum_scale = 2.0
        self.setViewportUpdateMode(self.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        # Antialias -- Change to styleSheetEditor
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)
        ##
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setAcceptDrops(True)
        self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.scene().setSceneRect(QtCore.QRectF(0, 0, 10, 10))
        self._grid_spacing = 50
        self.factor = 1
        self.factor_diff = 0
        self.setWindowTitle(self._graphBase.name)

        self._current_file_name = 'Untitled'
        self._file_name_label = QGraphicsTextItem()
        self._file_name_label.setZValue(5)
        self._file_name_label.setEnabled(False)
        self._file_name_label.setFlag(
            QGraphicsTextItem.ItemIgnoresTransformations)
        self._file_name_label.setDefaultTextColor(Colors.White)
        self._file_name_label.setPlainText(self._current_file_name)
        self.scene().addItem(self._file_name_label)
        if self._parentGraph:
            graph = self
            graphName = []
            graphName.append(graph._parentNode.name)
            self.GoUpButtonProxy = QGraphicsProxyWidget()
            self.GoUpButton = QPushButton("Go Up")
            self.GoUpButtonProxy.setWidget(self.GoUpButton)
            self.GoUpButton.setStyleSheet(buttonStyle)
            self.GoUpButton.clicked.connect(self.goUp)
            self.GoUpButtonProxy.setFlag(
                QGraphicsTextItem.ItemIgnoresTransformations)
            self.scene().addItem(self.GoUpButtonProxy)
            graph = graph._parentGraph
            while graph._parentGraph:
                graphName.append(graph._parentNode.name)
                graph = graph._parentGraph
            graphName.append("root")
            graphName = graphName[::-1]
            graphName = " | ".join(graphName)
            self._file_name_label.setPlainText(graphName)
        self.real_time_line = QGraphicsPathItem(None, self.scene())
        self.real_time_line.name = 'RealTimeLine'
        self.real_time_line.setPen(QtGui.QPen(
            Colors.Green, 1.0, QtCore.Qt.DashLine))
        self.mousePressPose = QtCore.QPointF(0, 0)
        self.mousePos = QtCore.QPointF(0, 0)
        self._lastMousePos = QtCore.QPointF(0, 0)
        self._right_button = False
        self._is_rubber_band_selection = False
        self._draw_real_time_line = False
        self._update_items = False
        self._resize_group_mode = False
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.centerOn(QtCore.QPointF(self.sceneRect().width() /
                                     2, self.sceneRect().height() / 2))
        self.initialScrollBarsPos = QtGui.QVector2D(
            self.horizontalScrollBar().value(), self.verticalScrollBar().value())
        self._sortcuts_enabled = True
        self.grid_size = 10
        self.drawGrigSize = self.grid_size * 2
        self.current_rounded_pos = QtCore.QPointF(0.0, 0.0)
        self.autoPanController = AutoPanController()
        self._bRightBeforeShoutDown = False

        self.node_box = NodesBox(None, self)
        self.node_box.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.codeEditors = {}
        self._UIConnections = {}
        self.boundingRect = self.rect()
        self._storedVars = []
        self.installEventFilter(self)

    def __del__(self):
        # self.tick_timer.stop()
        pass

    def createVariable(self, dataType='AnyPin', accessLevel=AccessLevel.public, uid=None):
        return self._graphBase.createVariable(dataType=dataType, accessLevel=accessLevel, uid=uid)

    @property
    def vars(self):
        return self._graphBase.vars

    @property
    def name(self):
        return self._graphBase.name

    @property
    def nodes(self):
        result = {}
        for rawNode in self._graphBase.getNodes():
            result[rawNode.uid] = rawNode.getWrapper()()
        return result

    @property
    def pins(self):
        """Returns UI pins dict {uuid: UIPinBase}
        """
        result = {}
        for rawPin in self._graphBase.pins.values():
            result[rawPin.uid] = rawPin.getWrapper()()
        return result

    @property
    def connections(self):
        return self._UIConnections

    def getNodes(self):
        return list(self.nodes.values())

    def getUniqNodeName(self, name):
        return self._graphBase.getUniqNodeName(name)

    def getUniqNodeDisplayName(self, name):
        nodes_names = [n.displayName for n in self.nodes.values()]
        if name not in nodes_names:
            return name
        idx = 0
        tmp = name
        while tmp in nodes_names:
            idx += 1
            tmp = name + str(idx)
        return name + str(idx)

    def showNodeBox(self, dataType=None, pinType=None):
        self.node_box.show()
        self.node_box.move(QtGui.QCursor.pos())
        self.node_box.treeWidget.refresh(dataType, '', pinType)
        self.node_box.lineEdit.setText("")
        if dataType is None:
            self.node_box.lineEdit.setFocus()

    def goUp(self):
        if self._parentGraph:
            self.parent.currentGraph = self._parentGraph
            self._parentGraph.show()
            self.hide()
            self.parent.variablesWidget.setGraph(self._parentGraph)

    def shoutDown(self):
        for ed in self.codeEditors.values():
            ed.deleteLater()
        nodes = list(self.getNodes())
        for node in nodes:
            node.kill()
        self.scene().shoutDown()
        self.scene().clear()
        self.node_box.hide()
        self.node_box.lineEdit.clear()

    def moveScrollbar(self, delta):
        # delta = self.mapToScene(event.pos()) - self._lastPanPoint
        rect = self.sceneRect()
        rect.translate(delta.x(), delta.y())
        self.setSceneRect(rect)

    def mouseDoubleClickEvent(self, event):
        QGraphicsView.mouseDoubleClickEvent(self, event)
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()

    def OnDoubleClick(self, pos):
        if self.pressed_item and isinstance(self.pressed_item, NodeName):
            if self.pressed_item.IsRenamable():
                name, result = QInputDialog.getText(
                    self, "New name dialog", "Enter new name:")
                if result:
                    self.pressed_item.parentItem().setName(name)
                    self.updatePropertyView(self.pressed_item.parentItem())
        elif self.pressed_item and isinstance(self.pressed_item, EditableLabel):
            if self.pressed_item._isEditable:
                self.pressed_item.start_edit_name()

    def Tick(self, deltaTime):
        if self.autoPanController.isActive():
            self.moveScrollbar(self.autoPanController.getDelta())
        for n in self.getNodes():
            n.Tick(deltaTime)
        for e in list(self.connections.values()):
            e.Tick()

    def notify(self, message, duration):
        self.parent.statusBar.showMessage(message, duration)
        print(message)

    def screenShot(self):
        name_filter = "Image (*.png)"
        fName = QFileDialog.getSaveFileName(filter=name_filter)
        if not fName[0] == '':
            print("save screen to {0}".format(fName[0]))
            img = QtGui.QPixmap.grab(self)
            img.save(fName[0], quality=100)

    def isShortcutsEnabled(self):
        return self._sortcuts_enabled

    def disableSortcuts(self):
        self._sortcuts_enabled = False

    def enableSortcuts(self):
        self._sortcuts_enabled = True

    def findPinByUID(self, uid):
        uiPin = None
        if uid in self.pins:
            return self.pins[uid]
        return uiPin

    def findPinByName(self, pinName):
        uiPin = None
        for pin in self.pins.values():
            if pinName == pin.getName():
                uiPin = pin
                break
        return uiPin

    def getGraphSaveData(self):
        data = {self.name: {'nodes': [], 'connections': [], 'vars': []}}
        # save nodes
        data[self.name]['nodes'] = [node.serialize() for node in self.getNodes(
        ) if not node.isCommentNode] + [node.serialize() for node in self.getNodes() if node.isCommentNode]
        # save connections
        data[self.name]['connections'] = [e.serialize() for e in self.connections.values()]
        # variables
        data[self.name]['vars'] = [v.serialize() for v in self.vars.values()]
        return data

    def save(self, save_as=False):
        if save_as:
            name_filter = "Graph files (*.json)"
            savepath = QFileDialog.getSaveFileName(filter=name_filter)
            if type(savepath) in [tuple, list]:
                pth = savepath[0]
            else:
                pth = savepath
            if not pth == '':
                self._current_file_name = pth
            else:
                self._current_file_name = "Untitled"
        else:
            if not path.isfile(self._current_file_name):
                name_filter = "Graph files (*.json)"
                savepath = QFileDialog.getSaveFileName(filter=name_filter)
                if type(savepath) in [tuple, list]:
                    pth = savepath[0]
                else:
                    pth = savepath
                if not pth == '':
                    self._current_file_name = pth
                else:
                    self._current_file_name = "Untitled"

        if self._current_file_name in ["", "Untitled"]:
            return

        if not self._current_file_name == '':
            with open(self._current_file_name, 'w') as f:
                graphData = self.getGraphSaveData()
                json.dump(graphData, f, indent=4)

            self._file_name_label.setPlainText(self._current_file_name)
            print(str("// saved: '{0}'".format(self._current_file_name)))

    def save_as(self):
        self.save(True)

    def new_file(self):
        self._current_file_name = 'Untitled'
        self._file_name_label.setPlainText('Untitled')
        nodes = list(self.getNodes())
        for node in nodes:
            node.kill()
        self.parent.variablesWidget.killAll()
        self.undoStack.clear()
        self._clearPropertiesView()

    def load(self):
        name_filter = "Graph files (*.json)"
        savepath = QFileDialog.getOpenFileName(filter=name_filter)
        if type(savepath) in [tuple, list]:
            fpath = savepath[0]
        else:
            fpath = savepath
        if not fpath == '':
            with open(fpath, 'r') as f:
                data = json.load(f)
                self.loadFromData(data, fpath)

    def loadFromData(self, data, fpath=""):
        self.new_file()
        # vars
        for varJson in data[self.name]['vars']:
            UIVariable.deserialize(varJson, self)
        # nodes
        for nodeJson in data[self.name]['nodes']:
            try:
                UINodeBase.deserialize(nodeJson, self)
            except Exception as e:
                print(nodeJson)
                print(e)
        # connections
        for edgeJson in data[self.name]['connections']:
            UIConnection.deserialize(edgeJson, self)
        self._current_file_name = fpath
        self._file_name_label.setPlainText(self._current_file_name)
        self.frameAllNodes()
        self.undoStack.clear()
        for node in self.getNodes():
            if node.isCommentNode:
                if not node.expanded:
                    node.expanded = True
                    node.updateChildren(node.nodesToMove.keys())
                    node.toogleCollapsed()
        self._clearPropertiesView()

    def getPinByFullName(self, full_name):
        node_name = full_name.split('.')[0]
        pinName = full_name.split('.')[1]
        node = self.getNodeByName(node_name)
        if node:
            Pin = node.getPinByName(pinName)
            if Pin:
                return Pin

    def frameRect(self, nodesRect):
        if nodesRect is None:
            return
        windowRect = self.rect()

        scaleX = float(windowRect.width()) / float(nodesRect.width())
        scaleY = float(windowRect.height()) / float(nodesRect.height())
        if scaleY > scaleX:
            scale = scaleX
        else:
            scale = scaleY

        if scale < 1.0:
            self.setTransform(QtGui.QTransform.fromScale(scale, scale))
        else:
            self.setTransform(QtGui.QTransform())

        sceneRect = self.sceneRect()
        pan = sceneRect.center() - nodesRect.center()
        sceneRect.translate(-pan.x(), -pan.y())
        self.setSceneRect(sceneRect)
        # Update the main panel when reframing.
        self.update()

    def frameSelectedNodes(self):
        self.frameRect(self.getNodesRect(True))

    def frameAllNodes(self):
        self.frameRect(self.getNodesRect())

    def getNodesRect(self, selected=False):
        rectangles = []
        if selected:
            for n in [n for n in self.getNodes() if n.isSelected()]:
                n_rect = QtCore.QRectF(n.scenePos(),
                                       QtCore.QPointF(n.scenePos().x() + float(n.w),
                                                      n.scenePos().y() + float(n.h)))
                rectangles.append(
                    [n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])
        else:
            for n in self.getNodes():
                n_rect = QtCore.QRectF(n.scenePos(),
                                       QtCore.QPointF(n.scenePos().x() + float(n.w),
                                                      n.scenePos().y() + float(n.h)))
                rectangles.append(
                    [n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])

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
        return [i for i in self.getNodes() if i.isSelected()]

    def clearSelection(self):
        for node in self.selectedNodes():
            node.setSelected(False)

    def killSelectedNodes(self):
        selectedNodes = self.selectedNodes()
        if self.isShortcutsEnabled() and len(selectedNodes) > 0:
            cmdRemove = cmdRemoveNodes(selectedNodes, self)
            self.undoStack.push(cmdRemove)
            clearLayout(self.parent.formLayout)

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        if self.isShortcutsEnabled():
            if all([event.key() == QtCore.Qt.Key_C, modifiers == QtCore.Qt.NoModifier]):
                # create comment node
                rect = UIcommentNode.getNodesRect(self.selectedNodes())
                if rect:
                    rect.setTop(rect.top() - 20)
                    rect.setLeft(rect.left() - 20)

                    rect.setRight(rect.right() + 20)
                    rect.setBottom(rect.bottom() + 20)

                nodeTemplate = NodeBase.jsonTemplate()
                nodeTemplate['package'] = "PyflowBase"
                nodeTemplate['type'] = commentNode.__name__
                nodeTemplate['name'] = self.getUniqNodeName(commentNode.__name__)
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
                    instance.label().width = rect.width()
                    instance.label().adjustSizes()

            if all([event.key() == QtCore.Qt.Key_Left, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
                self.alignSelectedNodes(Direction.Left)
                return
            if all([event.key() == QtCore.Qt.Key_Up, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
                self.alignSelectedNodes(Direction.Up)
                return
            if all([event.key() == QtCore.Qt.Key_Right, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
                self.alignSelectedNodes(Direction.Right)
                return
            if all([event.key() == QtCore.Qt.Key_Down, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
                self.alignSelectedNodes(Direction.Down)
                return

            if all([event.key() == QtCore.Qt.Key_Z, modifiers == QtCore.Qt.ControlModifier]):
                    self.undoStack.undo()
            if all([event.key() == QtCore.Qt.Key_Y, modifiers == QtCore.Qt.ControlModifier]):
                    self.undoStack.redo()

            if all([event.key() == QtCore.Qt.Key_N, modifiers == QtCore.Qt.ControlModifier]):
                self.new_file()
            if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier]):
                self.save()
            if all([event.key() == QtCore.Qt.Key_O, modifiers == QtCore.Qt.ControlModifier]):
                self.load()
            if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
                self.save_as()

            if all([event.key() == QtCore.Qt.Key_F, modifiers == QtCore.Qt.NoModifier]):
                self.frameSelectedNodes()
            if all([event.key() == QtCore.Qt.Key_H, modifiers == QtCore.Qt.NoModifier]):
                self.frameAllNodes()

            if all([event.key() == QtCore.Qt.Key_Equal, modifiers == QtCore.Qt.ControlModifier]):
                self.zoomDelta(True)
            if all([event.key() == QtCore.Qt.Key_Minus, modifiers == QtCore.Qt.ControlModifier]):
                self.zoomDelta(False)
            if all([event.key() == QtCore.Qt.Key_R, modifiers == QtCore.Qt.ControlModifier]):
                self.reset_scale()

            # if all([event.key() == QtCore.Qt.Key_N, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            #    if self.parent:
            #        self.parent.toggle_node_box()
            # if all([event.key() == QtCore.Qt.Key_M, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier]):
            #    self.parent.toggle_multithreaded()
            # if all([event.key() == QtCore.Qt.Key_D, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier]):
            #    self.parent.toggle_debug()

            if all([event.key() == QtCore.Qt.Key_P, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
                self.parent.togglePropertyView()

            if event.key() == QtCore.Qt.Key_Delete:
                self.killSelectedNodes()

            if all([event.key() == QtCore.Qt.Key_D, modifiers == QtCore.Qt.ControlModifier]):
                self.duplicateNodes()
            if all([event.key() == QtCore.Qt.Key_C, modifiers == QtCore.Qt.ControlModifier]):
                self.copyNodes()
            if all([event.key() == QtCore.Qt.Key_V, modifiers == QtCore.Qt.ControlModifier]):
                self.pasteNodes()

        QGraphicsView.keyPressEvent(self, event)

    def duplicateNodes(self):
        selectedNodes = [i for i in self.getNodes() if i.isSelected()]

        if len(selectedNodes) > 0:
            diff = QtCore.QPointF(self.mapToScene(
                self.mousePos)) - selectedNodes[0].scenePos()
            newNodes = []
            oldNodes = []
            connections = []
            for n in selectedNodes:
                new_node = n.clone()
                assert(new_node is not None)
                n.setSelected(False)
                new_node.setSelected(True)
                new_node.setPos(new_node.scenePos() + diff)
                newNodes.append(new_node)
                oldNodes.append(n)
                for i in n.inputs.values() + n.outputs.values():
                    connections += i.connections
            for e in connections:
                if e.source().UiNode in oldNodes and e.destination().UiNode in oldNodes:
                    nsrc = newNodes[oldNodes.index(
                        e.source().UiNode)].getPinByName(e.source().name)
                    ndst = newNodes[oldNodes.index(e.destination().UiNode)].getPinByName(
                        e.destination().name)
                    self.connectPins(nsrc, ndst)
                elif e.source().UiNode not in oldNodes and e.source().dataType != "ExecPin":
                    nsrc = e.source()
                    ndst = newNodes[oldNodes.index(e.destination().UiNode)].getPinByName(
                        e.destination().name)
                    self.connectPins(nsrc, ndst)

    def copyNodes(self, toClipboard=True):
        nodes = []
        oldNodes = []
        selectedNodes = [i for i in self.getNodes() if i.isSelected()]
        connections = []
        for n in selectedNodes:
            oldNodes.append(n)
            nodes.append(n.serialize())
            for i in list(n.inputs.values()) + list(n.outputs.values()):
                connections += i.connections
        fullEdges = []
        for e in connections:
            if e.source().owningNode() in oldNodes and e.destination().owningNode() in oldNodes:
                fullEdges.append({"full": True, "sourcenode": e.source().owningNode().name, "sourcePin": e.source(
                ).name, "destinationNode": e.destination().owningNode().name, "destinationPin": e.destination().name})
            elif e.source().owningNode() not in oldNodes and e.source().dataType != "ExecPin":
                fullEdges.append({"full": False, "sourcenode": e.source().owningNode().name, "sourcePin": e.source(
                ).name, "destinationNode": e.destination().owningNode().name, "destinationPin": e.destination().name})
        if len(nodes) > 0:
            ret = {"nodes": nodes, "connections": fullEdges}
            n = json.dumps(ret)
            if toClipboard:
                QApplication.clipboard().clear()
                QApplication.clipboard().setText(n)
            else:
                return n

    def pasteNodes(self, move=True, data=None):
        if not data:
            nodes = json.loads(QApplication.clipboard().text())
        else:
            nodes = json.loads(data)
        if "nodes" not in nodes or "connections" not in nodes:
            return

        diff = QtCore.QPointF(self.mapToScene(
            self.mousePos)) - QtCore.QPointF(nodes["nodes"][0]["x"], nodes["nodes"][0]["y"])
        self.clearSelection()
        newNodes = {}

        for node in nodes["nodes"]:
            oldName = node["name"]
            node["name"] = self.getUniqNodeName(node["name"])
            node['uuid'] = str(uuid.uuid4())
            for inp in node['inputs']:
                inp['uuid'] = str(uuid.uuid4())
            for out in node['outputs']:
                out['uuid'] = str(uuid.uuid4())

            n = self.createNode(node)
            newNodes[oldName] = n
            n.setSelected(True)
            if move:
                n.setPos(n.scenePos() + diff)
        for connection in nodes["connections"]:
            if connection["full"]:
                nsrc = newNodes[connection["sourcenode"]
                                ].getPinByName(connection["sourcePin"])
                ndst = newNodes[connection["destinationNode"]
                                ].getPinByName(connection["destinationPin"])
                self.connectPins(nsrc, ndst)
            else:
                nsrc = self.getNodeByName(connection["sourcenode"])
                if nsrc is not None:
                    nsrc = nsrc.getPinByName(connection["sourcePin"])
                    if nsrc is not None:
                        ndst = newNodes[connection["destinationNode"]
                                        ].getPinByName(connection["destinationPin"])
                        self.connectPins(nsrc, ndst)

    def alignSelectedNodes(self, direction):
        ls = [n for n in self.getNodes() if n.isSelected()]

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
        while (isinstance(node, QGraphicsItem) or isinstance(node, QGraphicsWidget) or isinstance(node, QGraphicsProxyWidget))and node.parentItem() is not None:
            node = node.parentItem()
        return node

    def getReruteNode(self, pos):
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate['package'] = "PyflowBase"
        nodeTemplate['lib'] = None
        nodeTemplate['type'] = "reroute"
        nodeTemplate['name'] = "reroute"
        nodeTemplate['x'] = self.mapToScene(pos).x()
        nodeTemplate['y'] = self.mapToScene(pos).y()
        nodeTemplate['uuid'] = str(uuid.uuid4())
        nodeTemplate['meta']['label'] = "reroute"
        reruteNode = self.createNode(nodeTemplate)
        reruteNode.color = self.pressed_item.color
        reruteNode.translate(-reruteNode.boundingRect().center().x(), -5)
        return reruteNode

    def getInputNode(self):
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate['package'] = "PyflowBase"
        nodeTemplate['lib'] = None
        nodeTemplate['type'] = "graphInputs"
        nodeTemplate['name'] = self.getUniqNodeName("graphInputs")
        nodeTemplate['x'] = self.boundingRect.left() + 50
        nodeTemplate['y'] = self.boundingRect.center().y() + 50
        nodeTemplate['uuid'] = str(uuid.uuid4())
        nodeTemplate['meta']['label'] = "Inputs"
        node = self.createNode(nodeTemplate)
        node.translate(-20, 0)
        return node

    def getOutputNode(self):
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate['package'] = "PyflowBase"
        nodeTemplate['lib'] = None
        nodeTemplate['type'] = "graphOutputs"
        nodeTemplate['name'] = self.getUniqNodeName("graphOutputs")
        nodeTemplate['x'] = self.boundingRect.width() - 50
        nodeTemplate['y'] = self.boundingRect.center().y() + 50
        nodeTemplate['uuid'] = str(uuid.uuid4())
        nodeTemplate['meta']['label'] = "Outputs"
        node = self.createNode(nodeTemplate)
        node.translate(-20, 0)
        return node

    def mousePressEvent(self, event):
        if self.pressed_item and isinstance(self.pressed_item, EditableLabel):
            if self.pressed_item != self.itemAt(event.pos()):
                self.pressed_item.setOutFocus()
        self.pressed_item = self.itemAt(event.pos())
        modifiers = event.modifiers()
        self.mousePressPose = event.pos()
        node = self.nodeFromInstance(self.pressed_item)
        if any([not self.pressed_item, isinstance(self.pressed_item, UIConnection) and modifiers != QtCore.Qt.AltModifier, isinstance(self.pressed_item, UINodeBase) and node.isCommentNode, isinstance(node, UINodeBase) and (node.resizable and node.shouldResize(self.mapToScene(event.pos()))["resize"])]):
            self.resizing = False
            if isinstance(node, UINodeBase) and (node.isCommentNode or node.resizable):
                super(GraphWidgetUI, self).mousePressEvent(event)
                self.resizing = node.bResize
                node.setSelected(False)
            if not self.resizing:
                if event.button() == QtCore.Qt.LeftButton and modifiers in [QtCore.Qt.NoModifier, QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier, QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]:
                    self._manipulationMode = MANIP_MODE_SELECT
                    self._selectionRect = SelectionRect(
                        graph=self, mouseDownPos=self.mapToScene(event.pos()), modifiers=modifiers)
                    self._mouseDownSelection = [
                        node for node in self.selectedNodes()]
                    if modifiers not in [QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier]:
                        self.clearSelection()
                        # super(GraphWidgetUI, self).mousePressEvent(event)
                else:
                    if hasattr(self, "_selectionRect") and self._selectionRect is not None:
                        self._selectionRect.destroy()
                        self._selectionRect = None
                LeftPaning = event.button() == QtCore.Qt.LeftButton and modifiers == QtCore.Qt.AltModifier
                if event.button() == QtCore.Qt.MiddleButton or LeftPaning:
                    self.viewport().setCursor(QtCore.Qt.OpenHandCursor)
                    self._manipulationMode = MANIP_MODE_PAN
                    self._lastPanPoint = self.mapToScene(event.pos())
                elif event.button() == QtCore.Qt.RightButton:
                    self.viewport().setCursor(QtCore.Qt.SizeHorCursor)
                    self._manipulationMode = MANIP_MODE_ZOOM
                    self._lastMousePos = event.pos()
                    self._lastTransform = QtGui.QTransform(self.transform())
                    self._lastSceneRect = self.sceneRect()
                    self._lastSceneCenter = self._lastSceneRect.center()
                    self._lastScenePos = self.mapToScene(event.pos())
                    self._lastOffsetFromSceneCenter = self._lastScenePos - self._lastSceneCenter
            # elif modifiers not in  [QtCore.Qt.ShiftModifier,QtCore.Qt.ControlModifier]:
            #    super(GraphWidgetUI, self).mousePressEvent(event)
            self.node_box.hide()

        elif not isinstance(self.pressed_item, EditableLabel) or (isinstance(self.pressed_item, EditableLabel) and not self.pressed_item._beingEdited):
            # else:
            if not isinstance(self.pressed_item, NodesBox) and self.node_box.isVisible():
                self.node_box.hide()
                self.node_box.lineEdit.clear()
            if isinstance(self.pressed_item, QGraphicsItem):
                if isinstance(self.pressed_item, UIPinBase):
                    if event.button() == QtCore.Qt.LeftButton:
                        self.pressed_item.topLevelItem().setFlag(QGraphicsItem.ItemIsMovable, False)
                        self.pressed_item.topLevelItem().setFlag(QGraphicsItem.ItemIsSelectable, False)
                        self._draw_real_time_line = True
                    if modifiers == QtCore.Qt.AltModifier:
                        self.removeEdgeCmd(self.pressed_item.connections)
                        self._draw_real_time_line = False
                else:
                    # super(GraphWidgetUI, self).mousePressEvent(event)
                    if isinstance(self.pressed_item, UIConnection) and modifiers == QtCore.Qt.AltModifier:
                        reruteNode = self.getReruteNode(event.pos())
                        self.clearSelection()
                        reruteNode.setSelected(True)
                        for inp in reruteNode.inputs.values():
                            if self.canConnectPins(self.pressed_item.source(), inp):
                                if self.pressed_item.source().dataType == 'ExecPin':
                                    self.pressed_item.source().disconnectAll()
                                self.connectPins(self.pressed_item.source(), inp)
                                break
                        for out in reruteNode.outputs.values():
                            if self.canConnectPins(out, self.pressed_item.destination()):
                                self.connectPins(out, self.pressed_item.destination())
                                break
                        self.pressed_item = reruteNode
                        self._manipulationMode = MANIP_MODE_MOVE
                        self._lastDragPoint = self.mapToScene(event.pos())
                    else:
                        if isinstance(self.pressed_item, UINodeBase) and node.isCommentNode:
                            if node.bResize:
                                return
                        if event.button() == QtCore.Qt.MidButton:
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
                                super(GraphWidgetUI, self).mousePressEvent(event)
                            if modifiers == QtCore.Qt.ControlModifier:
                                node.setSelected(not node.isSelected())
                            if modifiers == QtCore.Qt.ShiftModifier:
                                node.setSelected(True)
                        self.autoPanController.start()
                        if all([(event.button() == QtCore.Qt.MidButton or event.button() == QtCore.Qt.LeftButton), modifiers == QtCore.Qt.NoModifier]):
                            self._manipulationMode = MANIP_MODE_MOVE
                            self._lastDragPoint = self.mapToScene(event.pos())
                        elif all([(event.button() == QtCore.Qt.MidButton or event.button() == QtCore.Qt.LeftButton), modifiers == QtCore.Qt.AltModifier]):
                            self._manipulationMode = MANIP_MODE_MOVE
                            self._lastDragPoint = self.mapToScene(event.pos())
                            selectedNodes = self.selectedNodes()
                            newNodes = []
                            copiedNodes = self.copyNodes(toClipboard=False)
                            self.pasteNodes(move=False, data=copiedNodes)

        else:
            super(GraphWidgetUI, self).mousePressEvent(event)

    def pan(self, delta):
        rect = self.sceneRect()
        rect.translate(-delta.x(), -delta.y())
        self.setSceneRect(rect)
        # delta *= self._scale * -1
        # delta *= self._panSpeed
        # self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
        # self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())

    def mouseMoveEvent(self, event):
        self.mousePos = event.pos()
        modifiers = event.modifiers()
        node = self.nodeFromInstance(self.itemAt(event.pos()))
        if self.itemAt(event.pos()) and isinstance(node, UINodeBase) and node.resizable:
            resizeOpts = node.shouldResize(self.mapToScene(event.pos()))
            if resizeOpts["resize"] or node.bResize:
                if resizeOpts["direction"] == (1, -1):
                    self.viewport().setCursor(QtCore.Qt.SizeFDiagCursor)
                elif resizeOpts["direction"] in [(1, 0), (-1, 0)]:
                    self.viewport().setCursor(QtCore.Qt.SizeHorCursor)
                elif resizeOpts["direction"] == (0, -1):
                    self.viewport().setCursor(QtCore.Qt.SizeVerCursor)
                elif resizeOpts["direction"] == (-1, -1):
                    self.viewport().setCursor(QtCore.Qt.SizeBDiagCursor)

        if self._draw_real_time_line:
            if isinstance(self.pressed_item, PinBase):
                if self.pressed_item.parentItem().isSelected():
                    self.pressed_item.parentItem().setSelected(False)
            if self.real_time_line not in self.scene().items():
                self.scene().addItem(self.real_time_line)

            p1 = self.pressed_item.scenePos() + self.pressed_item.boundingRect().center()
            p2 = self.mapToScene(self.mousePos)

            distance = p2.x() - p1.x()
            multiply = 3
            path = QtGui.QPainterPath()
            path.moveTo(p1)
            path.cubicTo(QtCore.QPoint(p1.x() + distance / multiply, p1.y()),
                         QtCore.QPoint(p2.x() - distance / 2, p2.y()), p2)
            self.real_time_line.setPath(path)
            mouseRect = QtCore.QRect(QtCore.QPoint(event.pos().x() - 2, event.pos().y() - 2),
                                     QtCore.QPoint(event.pos().x() + 2, event.pos().y() + 2))
            hoverItems = self.items(mouseRect)
            for item in hoverItems:
                if isinstance(item, UIRerouteNode):
                    self.hoverItems.append(item)
                    item.showPins()
            for item in self.hoverItems:
                if item not in hoverItems:
                    self.hoverItems.remove(item)
                    if isinstance(item, UIRerouteNode):
                        item.hidePins()
            if modifiers == QtCore.Qt.AltModifier:
                self._draw_real_time_line = False
                if self.real_time_line in self.scene().items():
                    self.removeItemByName('RealTimeLine')
                reruteNode = self.getReruteNode(event.pos())
                self.clearSelection()
                reruteNode.setSelected(True)
                for inp in reruteNode.inputs.values():
                    if self.canConnectPins(self.pressed_item, inp):
                        self.connectPins(self.pressed_item, inp)
                        break
                for out in reruteNode.outputs.values():
                    if self.canConnectPins(self.pressed_item, out):
                        self.connectPins(self.pressed_item, out)
                        break
                self.pressed_item = reruteNode
                self._manipulationMode = MANIP_MODE_MOVE
                self._lastDragPoint = self.mapToScene(event.pos())
        # if not isinstance(self.pressed_item,EditableLabel):
        if self._manipulationMode == MANIP_MODE_SELECT:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
            dragPoint = self.mapToScene(event.pos())
            self._selectionRect.setDragPoint(dragPoint, modifiers)
            # This logic allows users to use ctrl and shift with rectangle
            # select to add / remove nodes.
            node = self.nodeFromInstance(self.pressed_item)
            if isinstance(self.pressed_item, UINodeBase) and node.isCommentNode:
                nodes = [node for node in self.getNodes()
                         if not node.isCommentNode]
            else:
                nodes = self.getNodes()
            if modifiers == QtCore.Qt.ControlModifier:
                for node in nodes:
                    # if node not in [self.inputsItem,self.outputsItem]:
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

            elif modifiers == QtCore.Qt.ShiftModifier:
                for node in nodes:
                    # if node not in [self.inputsItem,self.outputsItem]:
                    if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                        node.setSelected(True)
                    elif node.isSelected() and not self._selectionRect.collidesWithItem(node):
                        if node not in self._mouseDownSelection:
                            node.setSelected(False)

            elif modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier:
                for node in nodes:
                    # if node not in [self.inputsItem,self.outputsItem]:
                    if self._selectionRect.collidesWithItem(node):
                        node.setSelected(False)
            else:
                self.clearSelection()
                for node in nodes:
                    # if node not in [self.inputsItem,self.outputsItem]:
                    if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                        node.setSelected(True)
                    elif node.isSelected() and not self._selectionRect.collidesWithItem(node):
                        node.setSelected(False)

        elif self._manipulationMode == MANIP_MODE_MOVE:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
            newPos = self.mapToScene(event.pos())
            delta = newPos - self._lastDragPoint
            self._lastDragPoint = self.mapToScene(event.pos())
            selectedNodes = self.selectedNodes()
            # Apply the delta to each selected node
            for node in selectedNodes:
                # if node not in [self.inputsItem,self.outputsItem]:
                node.translate(delta.x(), delta.y())
            if isinstance(node, UIRerouteNode) and modifiers == QtCore.Qt.AltModifier:
                mouseRect = QtCore.QRect(QtCore.QPoint(event.pos().x() - 1, event.pos().y() - 1),
                                         QtCore.QPoint(event.pos().x() + 1, event.pos().y() + 1))
                hoverItems = self.items(mouseRect)
                newOuts = []
                newIns = []
                for item in hoverItems:
                    if isinstance(item, UIConnection):
                        if list(node.inputs.values())[0].connections and list(node.outputs.values())[0].connections:
                            if item.source() == list(node.inputs.values())[0].connections[0].source():
                                newOuts.append(item.destination())
                            if item.destination() == list(node.outputs.values())[0].connections[0].destination():
                                newIns.append(item.source())
                for out in newOuts:
                    self.connectPins(list(node.outputs.values())[0], out)
                for inp in newIns:
                    self.connectPins(inp, list(node.inputs.values())[0])

        elif self._manipulationMode == MANIP_MODE_PAN:
            self.viewport().setCursor(QtCore.Qt.OpenHandCursor)
            delta = self.mapToScene(event.pos()) - self._lastPanPoint
            rect = self.sceneRect()
            rect.translate(-delta.x(), -delta.y())
            self.setSceneRect(rect)
            self._lastPanPoint = self.mapToScene(event.pos())

        elif self._manipulationMode == MANIP_MODE_ZOOM:
            self.viewport().setCursor(QtCore.Qt.SizeHorCursor)
            # How much
            delta = event.pos() - self._lastMousePos
            # self._lastMousePos = event.pos()
            zoomFactor = 1.0
            if delta.x() > 0:
                zoomFactor = 1.0 + delta.x() / 100.0
            else:
                zoomFactor = 1.0 / (1.0 + abs(delta.x()) / 100.0)

            # Limit zoom to 3x
            if self._lastTransform.m22() * zoomFactor >= 2.0:
                return

            # Reset to when we mouse pressed
            self.setSceneRect(self._lastSceneRect)
            self.setTransform(self._lastTransform)

            # Center scene around mouse down
            rect = self.sceneRect()
            rect.translate(self._lastOffsetFromSceneCenter)
            self.setSceneRect(rect)

            # Zoom in (QGraphicsView auto-centers!)
            self.scale(zoomFactor, zoomFactor)

            newSceneCenter = self.sceneRect().center()
            newScenePos = self.mapToScene(self._lastMousePos)
            newOffsetFromSceneCenter = newScenePos - newSceneCenter

            # Put mouse down back where is was on screen
            rect = self.sceneRect()
            rect.translate(-1 * newOffsetFromSceneCenter)
            self.setSceneRect(rect)

            # Call udpate to redraw background
            self.update()

        else:
            super(GraphWidgetUI, self).mouseMoveEvent(event)
        # else:
        #    super(GraphWidgetUI, self).mouseMoveEvent(event)
        self.autoPanController.Tick(self.viewport().rect(), event.pos())

    def mouseReleaseEvent(self, event):
        super(GraphWidgetUI, self).mouseReleaseEvent(event)

        self.autoPanController.stop()
        self.mouseReleasePos = event.pos()
        self.released_item = self.itemAt(event.pos())
        self._resize_group_mode = False
        self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        for n in self.getNodes():
            if not n.isCommentNode:
                n.setFlag(QGraphicsItem.ItemIsMovable)
                n.setFlag(QGraphicsItem.ItemIsSelectable)

        if self._draw_real_time_line:
            self._draw_real_time_line = False
            if self.real_time_line in self.scene().items():
                self.removeItemByName('RealTimeLine')

        if self._manipulationMode == MANIP_MODE_SELECT:
            self._selectionRect.destroy()
            self._selectionRect = None

        if event.button() == QtCore.Qt.RightButton:
            # show nodebox only if drag is small and no items under cursor
            if self.pressed_item is None or (isinstance(self.pressed_item, UINodeBase) and self.nodeFromInstance(self.pressed_item).isCommentNode):
                dragDiff = self.mapToScene(
                    self.mousePressPose) - self.mapToScene(event.pos())
                if all([abs(i) < 0.4 for i in [dragDiff.x(), dragDiff.y()]]):
                    self.showNodeBox()
        elif event.button() == QtCore.Qt.LeftButton and not isinstance(self.released_item, UIPinBase):
            if isinstance(self.pressed_item, UIPinBase) and not self.resizing:
                # node box tree pops up
                # with nodes taking supported data types of pressed Pin as input
                self.showNodeBox(self.pressed_item.dataType,
                                 self.pressed_item.direction)
        self._manipulationMode = MANIP_MODE_NONE
        if not self.resizing:
            p_itm = self.pressed_item
            r_itm = self.released_item
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
                    if cycle_check(p_itm, r_itm):
                        print('cycles are not allowed')
                        do_connect = False

            if do_connect:
                if p_itm is not r_itm:
                    self.connectPins(p_itm, r_itm)

        selectedNodes = self.selectedNodes()
        if len(selectedNodes) != 0 and event.button() == QtCore.Qt.LeftButton:
            self.tryFillPropertiesView(selectedNodes[0])
        elif event.button() == QtCore.Qt.LeftButton:
            self._clearPropertiesView()
        self.resizing = False

    def removeItemByName(self, name):
        [self.scene().removeItem(i) for i in self.scene().items()
         if hasattr(i, 'name') and i.name == name]

    def tryFillPropertiesView(self, obj):
        '''
            TODO: obj should implement interface class
            with onUpdatePropertyView method
        '''
        if hasattr(obj, 'onUpdatePropertyView'):
            self._clearPropertiesView()
            obj.onUpdatePropertyView(self.parent.formLayout)

    def _clearPropertiesView(self):
        clearLayout(self.parent.formLayout)

    def propertyEditingFinished(self):
        le = QApplication.instance().focusWidget()
        if isinstance(le, QLineEdit):
            nodeName, attr = le.objectName().split('.')
            node = self.getNodeByName(nodeName)
            Pin = node.getPinByName(attr)
            Pin.setData(le.text())

    def wheelEvent(self, event):
        (xfo, invRes) = self.transform().inverted()
        topLeft = xfo.map(self.rect().topLeft())
        bottomRight = xfo.map(self.rect().bottomRight())
        center = (topLeft + bottomRight) * 0.5
        zoomFactor = 1.0 + event.delta() * self._mouseWheelZoomRate

        transform = self.transform()

        # Limit zoom to 3x
        if transform.m22() * zoomFactor >= 2.0:
            return

        self.scale(zoomFactor, zoomFactor)

        # Call udpate to redraw background
        self.update()

    def drawBackground(self, painter, rect):

        super(GraphWidgetUI, self).drawBackground(painter, rect)
        self.boundingRect = rect

        polygon = self.mapToScene(self.viewport().rect())
        self._file_name_label.setPos(polygon[0])

        if self._parentGraph:
            self.GoUpButtonProxy.setPos(polygon[0].x(), polygon[0].y())
            self._file_name_label.moveBy(self.GoUpButton.width(), 0)
        # self.inputsItem.setPos(self.mapToScene(self.viewport().rect().x(),self.viewport().rect().y()+50) )
        # self.inputsItem.setPos(self.boundingRect.topLeft().x(),self.boundingRect.topLeft().y()+50)
        # self.inputsItem.update()
        # self.outputsItem.setPos(self.boundingRect.topRight().x()-self.outputsItem.boundingRect().width(),self.boundingRect.topRight().y()+50)
        # self.outputsItem.update()

        color = self._backgroundColor
        painter.fillRect(rect, QtGui.QBrush(color))

        left = int(rect.left()) - (int(rect.left()) % self._gridSizeFine)
        top = int(rect.top()) - (int(rect.top()) % self._gridSizeFine)

        # Draw horizontal fine lines
        gridLines = []
        painter.setPen(QtGui.QPen(self._gridPenS, 1))
        y = float(top)
        while y < float(rect.bottom()):
            gridLines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
            y += self._gridSizeFine
        painter.drawLines(gridLines)

        # Draw vertical fine lines
        gridLines = []
        painter.setPen(QtGui.QPen(self._gridPenS, 1))
        x = float(left)
        while x < float(rect.right()):
            gridLines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
            x += self._gridSizeFine
        painter.drawLines(gridLines)

        # Draw thick grid
        left = int(rect.left()) - (int(rect.left()) % self._gridSizeCourse)
        top = int(rect.top()) - (int(rect.top()) % self._gridSizeCourse)

        # Draw vertical thick lines
        gridLines = []
        painter.setPen(QtGui.QPen(self._gridPenL, 1.5))
        x = left
        while x < rect.right():
            gridLines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
            x += self._gridSizeCourse
        painter.drawLines(gridLines)

        # Draw horizontal thick lines
        gridLines = []
        painter.setPen(QtGui.QPen(self._gridPenL, 1.5))
        y = top
        while y < rect.bottom():
            gridLines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
            y += self._gridSizeCourse
        painter.drawLines(gridLines)

    def consoleHelp(self):
        msg = """///// AVAILABLE NODES LIST /////\n\n"""

        for f in listdir(path.dirname(Nodes.__file__)):
            if f.endswith(".py") and "init" not in f:
                msg += "{0}\n".format(f.split(".")[0])

        msg += "\n"

        msg += """///// AVAILABLE COMMANDS /////\n"""
        msg += "\t<<< Builtin >>>\n"
        for c in self.parent.consoleInput.builtinCommands:
            msg += (c + "\n")
        msg += "\t<<< Plugins >>>\n"
        for c in self.registeredCommands:
            msg += (c + " - {0}\n".format(self.registeredCommands[c].usage()))

        if self.parent:
            print(msg)

    def _createNode(self, jsonTemplate):
        nodeInstance = getNodeInstance(jsonTemplate, self)
        assert(nodeInstance is not None), "Node instance is not found!"
        nodeInstance.setPosition(jsonTemplate["x"], jsonTemplate["y"])

        # set pins data
        for inpJson in jsonTemplate['inputs']:
            pin = nodeInstance.getPinByName(
                inpJson['name'], PinSelectionGroup.Inputs)
            if pin:
                pin.uid = uuid.UUID(inpJson['uuid'])
                pin.setData(inpJson['value'])
                if inpJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        for outJson in jsonTemplate['outputs']:
            pin = nodeInstance.getPinByName(
                outJson['name'], PinSelectionGroup.Outputs)
            if pin:
                pin.uid = uuid.UUID(outJson['uuid'])
                pin.setData(outJson['value'])
                if outJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        nodeInstance.postCreate(jsonTemplate)
        return nodeInstance

    def createNode(self, jsonTemplate, **kwags):
        cmd = cmdCreateNode(self, jsonTemplate, **kwags)
        self.undoStack.push(cmd)
        return cmd.nodeInstance

    def addNode(self, node):
        """Adds node to a graph

        Arguments:
            node UINodeBase -- raw node wrapper
        """
        self._graphBase.addNode(node._rawNode)
        node.graph = weakref.ref(self)
        self.scene().addItem(node)

    def connectPinsInternal(self, src, dst):
        # reconnection may occur in raw connections
        # need to know it and remove invalid ui connections
        result = self._graphBase.connectPins(src._rawPin, dst._rawPin)
        if result:
            if src.direction == PinDirection.Input:
                src, dst = dst, src
            uiConnection = UIConnection(src, dst, self)
            self.scene().addItem(uiConnection)
            self.connections[uiConnection.uid] = uiConnection
            return uiConnection
        return None

    def canConnectPins(self, src, dst):
        return self._graphBase.canConnectPins(src, dst)

    def connectPins(self, src, dst):
        if self.canConnectPins(src, dst):
            cmd = cmdConnectPin(self, src, dst)
            self.undoStack.push(cmd)

    def removeEdgeCmd(self, connections):
        self.undoStack.push(cmdRemoveEdges(self, [e.serialize() for e in connections]))

    def removeConnection(self, connection):
        src = connection.source()._rawPin
        dst = connection.destination()._rawPin
        # this will remove raw pins from affection lists
        # will call pinDisconnected for raw pins
        disconnectPins(src, dst)

        # call disconnection events for ui pins
        connection.source().pinDisconnected(connection.destination())
        connection.destination().pinDisconnected(connection.source())
        connection.source().update()
        connection.destination().update()
        self.connections.pop(connection.uid)
        connection.source().uiConnectionList.remove(connection)
        connection.destination().uiConnectionList.remove(connection)
        connection.prepareGeometryChange()
        self.scene().removeItem(connection)

    def count(self):
        return self._graphBase.count()

    def getVars(self):
        return self._graphBase.getVars()

    def getUniqVarName(self, name):
        return self._graphBase.getUniqVarName(name)

    def getNodeByName(self, name):
        return self._graphBase.getNodeByName(name)

    def getNodesByClassName(self, className):
        return [node._wrapper() for node in self._graphBase.getNodesByClassName(className)]

    def isDebug(self):
        return self._graphBase.isDebug()

    def getNextLayerNodes(node, direction=PinDirection.Input):
        return self._GraphBase.getNextLayerNodes(node, direction)

    def getEvaluationOrder(self, node):
        return self._graphBase.getEvaluationOrder(node)

    def plot(self):
        self._graphBase.plot()

    def zoomDelta(self, direction):
        current_factor = self.factor
        if direction:
            self.zoom(1 + 0.1)
        else:
            self.zoom(1 - 0.1)

    def reset_scale(self):
        self.resetMatrix()

    def zoom(self, scale_factor):

        self.factor = self.matrix().scale(scale_factor, scale_factor).mapRect(
            QtCore.QRectF(0, 0, 1, 1)).width()
        self.factor = round(self.factor, 1)
        if self.factor < (self.minimum_scale + 0.4):
            self.grid_size = 20
        else:
            self.grid_size = 10
        if self.factor < self.minimum_scale or self.factor > self.maximum_scale:
            return
        self.scale(scale_factor, scale_factor)
        self._scale *= scale_factor

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            self.showNodeBox()
        return False
