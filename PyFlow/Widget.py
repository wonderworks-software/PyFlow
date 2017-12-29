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
import math
import platform
import random
from Settings import Colors
from Settings import LineTypes
from Settings import get_line_type
from AbstractGraph import *
from Edge import Edge
from Pin import getPortColorByType, Pin
from Node import Node
from os import listdir, path, startfile
_file_folder = path.dirname(__file__)
nodes_path = _file_folder + '\\Nodes'
import Nodes
from GetVarNode import GetVarNode
from SetVarNode import SetVarNode
import FunctionLibraries
import Commands
from Variable import VariableBase
from time import ctime, clock
import OptionsWindow_ui
import rgba_color_picker_ui
import json
import re


class Direction:
    Left = 0
    Right = 1
    Up = 2
    Down = 3


def getMidPoint(args):
    return [sum(i) / len(i) for i in zip(*args)]


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


class PluginType:
    pNode = 0
    pCommand = 1


def _implementPlugin(name, console_out_foo, pluginType):
    CommandTemplate = """from Qt.QtWidgets import QUndoCommand


class {0}(QUndoCommand):

    def __init__(self):
        super({0}, self).__init__()

    def undo(self):
        pass

    def redo(self):
        pass
""".format(name)

    base_node_code = """from AbstractGraph import *
from Settings import *
from Node import Node


class {0}(Node, NodeBase):
    def __init__(self, name, graph):
        super({0}, self).__init__(name, graph, w=100, spacings=Spacings)
        self.inp0 = self.addInputPin('in0', DataTypes.Any)
        self.out0 = self.addOutputPin('out0', DataTypes.Any)
        portAffects(self.inp0, self.out0)

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'default description'

    def compute(self):

        str_data = self.inp0.getData()
        try:
            self.out0.setData(str_data.upper())
        except Exception as e:
            print(e)
""".format(name)

    if pluginType == PluginType.pNode:
        file_path = "{0}/{1}.py".format(Nodes.__path__[0], name)
        existing_nodes = [n.split(".")[0] for n in listdir(Nodes.__path__[0]) if n.endswith(".py") and "__init__" not in n]

        if name in existing_nodes:
            console_out_foo("[ERROR] Node {0} already exists".format(name))
            return

        # write to file. delete older if needed
        with open(file_path, "wb") as f:
            f.write(base_node_code)
        console_out_foo("[INFO] Node {0} been created.\nIn order to appear in node box, restart application.".format(name))
        startfile(file_path)

    else:
        file_path = "{0}/{1}.py".format(Commands.__path__[0], name)
        existing_commands = [c.split(".")[0] for c in listdir(Commands.__path__[0]) if c.endswith(".py") and "__init__" not in c]
        if name in existing_commands:
            console_out_foo("[ERROR] Command {0} already exists".format(name))
            return
        # write to file. delete older if needed
        with open(file_path, "wb") as f:
            f.write(CommandTemplate)
        console_out_foo("[INFO] Command {0} been created.\n Restart application.".format(name))
        startfile(file_path)


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


def parse(line):
    '''
    returns - {'cmd': command, 'flags': {-x1: 50, -x2: 100}}
    '''
    out = {}
    flag_sep = [m.start() for m in re.finditer(FLAG_SYMBOL, line)]
    if len(flag_sep) == 0:
        out["cmd"] = line
        return out
    out = {"flags": {}}
    cmd = line.split(" ")[0]
    out["cmd"] = cmd
    for i in xrange(len(flag_sep) - 1):
        newLine = line[flag_sep[i]:]
        newLineDashes = [m.start() for m in re.finditer(FLAG_SYMBOL, newLine)]
        flag = newLine[:newLineDashes[1] - 1].split(" ", 1)  # flag + value
        out["flags"][flag[0]] = flag[1]
    flag = line[flag_sep[-1]:].split(" ", 1)  # last flag + value
    out["flags"][flag[0]] = flag[1]
    return out


def getNodeInstance(module, class_name, nodeName, graph):
    # Check in Nodes module first
    mod = Nodes.getNode(class_name)
    if mod is not None:
        instance = mod(nodeName, graph)
        return instance

    # if not found - continue searching in FunctionLibraries
    foo = FunctionLibraries.findFunctionByName(class_name)
    if foo:
        instance = Node.initializeFromFunction(foo, graph)
        return instance
    return None


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
                self.amount = clamp(abs(rect.width() - pos.x()) * 0.3, 0.0, 25.0)
            if pos.y() < 0:
                self.autoPanDelta = QtGui.QVector2D(0.0, -self.amount)
                self.beenOutside = True
                self.amount = clamp(abs(pos.y()) * 0.3, 0.0, 25.0)
            if pos.y() > rect.height():
                self.autoPanDelta = QtGui.QVector2D(0.0, self.amount)
                self.beenOutside = True
                self.amount = clamp(abs(rect.height() - pos.y()) * 0.3, 0.0, 25.0)
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
        self.object_type = ObjectTypes.Scene
        self.setItemIndexMethod(self.NoIndex)
        self.pressed_port = None
        self.selectionChanged.connect(self.OnSelectionChanged)

    def shoutDown(self):
        self.selectionChanged.disconnect()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    # def clearSelection(self):
    #     for n in self.selectedItems():
    #         n.setSelected(False)

    def OnSelectionChanged(self):
        selectedNodesUids = self.parent().selectedNodes()
        cmdSelect = Commands.Select(selectedNodesUids, self.parent())
        self.parent().undoStack.push(cmdSelect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            tag, mimeText = event.mimeData().text().split('|')
            name = self.parent().getUniqNodeName(mimeText)
            dropItem = self.itemAt(event.scenePos())
            if not dropItem:
                nodeTemplate = Node.jsonTemplate()
                nodeTemplate['type'] = mimeText
                if tag == 'Var':
                    modifiers = event.modifiers()
                    if modifiers == QtCore.Qt.ControlModifier:
                        nodeTemplate['type'] = 'GetVarNode'
                        nodeTemplate['meta']['varuuid'] = mimeText
                        nodeTemplate['uuid'] = mimeText
                    if modifiers == QtCore.Qt.AltModifier:
                        nodeTemplate['type'] = 'SetVarNode'
                        nodeTemplate['meta']['varuuid'] = mimeText
                        nodeTemplate['uuid'] = mimeText
                    if modifiers == QtCore.Qt.NoModifier:
                        print('Getter pr setter')
                        return
                nodeTemplate['name'] = name
                nodeTemplate['x'] = event.scenePos().x()
                nodeTemplate['y'] = event.scenePos().y()
                nodeTemplate['meta']['label'] = mimeText
                nodeTemplate['uuid'] = None
                self.parent().createNode(nodeTemplate)
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
        self.categoryPaths = {}
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

    def insertNode(self, nodeCategoryPath, name, doc=None):
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
                    rootFolderItem.setText(0, folderName)
                    rootFolderItem.setBackground(folderId, QtGui.QColor(80, 85, 80))
                    self.categoryPaths[categoryPath] = rootFolderItem
            else:
                parentCategoryPath = categoryPath
                categoryPath += '|{}'.format(folderName)
                if categoryPath not in self.categoryPaths:
                    childCategoryItem = QTreeWidgetItem(self.categoryPaths[parentCategoryPath])
                    childCategoryItem.setText(0, folderName)
                    childCategoryItem.setBackground(0, QtGui.QColor(80, 85, 80))
                    self.categoryPaths[categoryPath] = childCategoryItem
        # create node under constructed folder
        nodeItem = QTreeWidgetItem(self.categoryPaths[categoryPath])
        nodeItem.setText(0, name)
        if doc:
            nodeItem.setToolTip(0, doc)

    def refresh(self, dataType=None, pattern=''):
        self.clear()
        self.categoryPaths = {}

        for libName in FunctionLibraries.libs():
            foos = FunctionLibraries.getLib(libName)
            for name, foo in foos:
                nodeCategoryPath = foo.__annotations__['meta']['Category']
                keywords = foo.__annotations__['meta']['Keywords']
                checkString = name + nodeCategoryPath + ''.join(keywords)
                if pattern in checkString.lower():
                    self.insertNode(nodeCategoryPath, name, foo.__doc__)

        for node_file_name in Nodes.getNodeNames():
            node_class = Nodes.getNode(node_file_name)
            nodeCategoryPath = node_class.category()

            checkString = node_file_name + nodeCategoryPath + ''.join(node_class.keywords())
            if pattern.lower() not in checkString.lower():
                continue

            self.insertNode(nodeCategoryPath, node_file_name, node_class.description())

    def keyPressEvent(self, event):
        super(NodeBoxTreeWidget, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        super(NodeBoxTreeWidget, self).mousePressEvent(event)
        item_clicked = self.currentItem()
        if not item_clicked:
            event.ignore()
            return
        pressed_text = item_clicked.text(0)

        if pressed_text in self.categoryPaths.keys():
            event.ignore()
            return
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        pressed_text = "Node|" + pressed_text
        mime_data.setText(pressed_text)
        drag.setMimeData(mime_data)
        drag.exec_()


class NodesBox(QWidget):
    """doc string for NodesBox"""
    def __init__(self, parent, graph=None):
        super(NodesBox, self).__init__(parent)
        self.graph = weakref.ref(graph)
        self.object_type = ObjectTypes.NodeBox
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
            self.treeWidget.setItemExpanded(self.treeWidget.categoryPaths[i], True)

    def leTextChanged(self):
        if self.lineEdit.text() == '':
            self.lineEdit.setPlaceholderText("enter node name..")
            self.treeWidget.refresh()
            return
        self.treeWidget.refresh(None, self.lineEdit.text())
        self.expandCategory()


class RubberRect(QGraphicsRectItem):
    def __init__(self, name):
        super(RubberRect, self).__init__()
        self.name = name
        self.setZValue(2)
        self.setPen(QtGui.QPen(Colors.RubberRect, 0.5, QtCore.Qt.SolidLine))
        self.setBrush(QtGui.QBrush(Colors.RubberRect))
        self.object_type = ObjectTypes.SelectionRect


class RGBAColorPicker(QWidget, rgba_color_picker_ui.Ui_rgba_color_picker_ui):
    def __init__(self, button):
        super(RGBAColorPicker, self).__init__()
        self.button = button
        self.setupUi(self)
        self.setButtonBackground(self.button.color)
        self.pb_color.color = self.button.color
        self.pb_color.clicked.connect(self.get_rgb)
        self.pb_apply.clicked.connect(self.apply)
        self.hs_alpha.valueChanged.connect(self.tweakAlpha)

    def setButtonBackground(self, color):
        self.pb_color.setStyleSheet("background-color: rgb({0}, {1}, {2}, {3});".format(
            color.red(),
            color.green(),
            color.blue(),
            color.alpha()
        ))

    def showEvent(self, event):
        self.setButtonBackground(self.button.color)
        self.hs_alpha.setValue(self.button.color.alpha())
        super(RGBAColorPicker, self).showEvent(event)

    def get_rgb(self):
        color = QtGui.QColorDialog.getColor()
        if color:
            self.pb_color.color = color
            color.setAlpha(self.hs_alpha.value())
            self.setButtonBackground(color)

    def tweakAlpha(self):
        self.pb_color.color.setAlpha(self.hs_alpha.value())
        self.setButtonBackground(self.pb_color.color)

    def apply(self):
        self.button.color = self.pb_color.color
        self.button.setStyleSheet("background-color: rgb({0}, {1}, {2}, {3});".format(
            self.pb_color.color.red(),
            self.pb_color.color.green(),
            self.pb_color.color.blue(),
            self.pb_color.color.alpha()
        ))
        self.close()


class OptionsClass(QMainWindow, OptionsWindow_ui.Ui_OptionsUI):
    def __init__(self):
        super(OptionsClass, self).__init__()
        self.setupUi(self)
        self.connectUi()
        self.populateUi()
        self.picker = None
        self.settings_path = path.dirname(__file__) + '\\config.ini'
        self.settings_class = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat, self)
        if not path.isfile(self.settings_path):
            self.write_default_config()
        self.pb_scene_bg_color.color = QtGui.QColor(self.settings_class.value('SCENE/Scene bg color'))
        self.setButtonBackground(self.pb_scene_bg_color, self.pb_scene_bg_color.color)
        self.pb_grid_color.color = QtGui.QColor(self.settings_class.value('SCENE/Grid color'))
        self.setButtonBackground(self.pb_grid_color, self.pb_grid_color.color)
        self.pb_edge_color.color = QtGui.QColor(self.settings_class.value('SCENE/Edge color'))
        self.setButtonBackground(self.pb_edge_color, self.pb_edge_color.color)
        self.pb_node_base_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes base color'))
        self.setButtonBackground(self.pb_node_base_color, self.pb_node_base_color.color)
        self.pb_node_selected_pen_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes selected pen color'))
        self.setButtonBackground(self.pb_node_selected_pen_color, self.pb_node_selected_pen_color.color)
        self.pb_node_label_bg_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes label bg color'))
        self.setButtonBackground(self.pb_node_label_bg_color, self.pb_node_label_bg_color.color)
        self.pb_node_label_font_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes label font color'))
        self.setButtonBackground(self.pb_node_label_font_color, self.pb_node_label_font_color.color)
        self.pb_lyt_a_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes lyt A color'))
        self.setButtonBackground(self.pb_lyt_a_color, self.pb_lyt_a_color.color)
        self.pb_lyt_b_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes lyt B color'))
        self.setButtonBackground(self.pb_lyt_b_color, self.pb_lyt_b_color.color)
        self.pb_port_color.color = QtGui.QColor(self.settings_class.value('NODES/Pin color'))
        self.setButtonBackground(self.pb_port_color, self.pb_port_color.color)
        self.pb_port_label_color.color = QtGui.QColor(self.settings_class.value('NODES/Pin label color'))
        self.setButtonBackground(self.pb_port_label_color, self.pb_port_label_color.color)
        self.pb_port_dirty_pen_color.color = QtGui.QColor(self.settings_class.value('NODES/Pin dirty color'))
        self.setButtonBackground(self.pb_port_dirty_pen_color, self.pb_port_dirty_pen_color.color)
        self.sb_node_label_font_size.setValue(int(self.settings_class.value('NODES/Nodes label font size')))
        self.fb_node_label_font.setCurrentFont(QtGui.QFont(self.settings_class.value('NODES/Nodes label font')))
        self.fb_port_label_font.setCurrentFont(QtGui.QFont(self.settings_class.value('NODES/Pin label font')))
        self.sb_port_font_size.setValue(int(self.settings_class.value('NODES/Pin label size')))
        self.sb_edge_thickness.setValue(float(self.settings_class.value('SCENE/Edge line thickness')))

        idx = self.cb_grid_lines_type.findText(str(self.settings_class.value('SCENE/Grid lines type')))
        self.cb_grid_lines_type.setCurrentIndex(idx)
        idx = self.cb_edge_pen_type.findText(str(self.settings_class.value('SCENE/Edge pen type')))
        self.cb_edge_pen_type.setCurrentIndex(idx)
        idx = self.cb_port_dirty_pen_type.findText(str(self.settings_class.value('NODES/Pin dirty type')))
        self.cb_port_dirty_pen_type.setCurrentIndex(idx)

    @staticmethod
    def setButtonBackground(button, color):
        button.setStyleSheet("background-color: rgb({0}, {1}, {2}, {3});".format(
            color.red(),
            color.green(),
            color.blue(),
            color.alpha()
        ))

    def setColor(self, button):
        self.picker = RGBAColorPicker(button)
        self.picker.move(self.geometry().topRight().x(), self.geometry().topRight().y())
        self.picker.show()

    def populateUi(self):
        line_types = [str(i) for i in dir(LineTypes) if i[0] == 'l']
        self.cb_port_dirty_pen_type.addItems(line_types)
        self.cb_grid_lines_type.addItems(line_types)
        self.cb_edge_pen_type.addItems(line_types)

    def connectUi(self):

        self.actionSave.triggered.connect(self.saveOptions)

        self.pb_scene_bg_color.clicked.connect(lambda: self.setColor(self.pb_scene_bg_color))
        self.pb_grid_color.clicked.connect(lambda: self.setColor(self.pb_grid_color))
        self.pb_edge_color.clicked.connect(lambda: self.setColor(self.pb_edge_color))
        self.pb_node_base_color.clicked.connect(lambda: self.setColor(self.pb_node_base_color))
        self.pb_node_label_font_color.clicked.connect(lambda: self.setColor(self.pb_node_label_font_color))

        self.pb_node_selected_pen_color.clicked.connect(lambda: self.setColor(self.pb_node_selected_pen_color))
        self.pb_node_label_bg_color.clicked.connect(lambda: self.setColor(self.pb_node_label_bg_color))
        self.pb_lyt_a_color.clicked.connect(lambda: self.setColor(self.pb_lyt_a_color))
        self.pb_lyt_b_color.clicked.connect(lambda: self.setColor(self.pb_lyt_b_color))
        self.pb_port_color.clicked.connect(lambda: self.setColor(self.pb_port_color))
        self.pb_port_label_color.clicked.connect(lambda: self.setColor(self.pb_port_label_color))
        self.pb_port_dirty_pen_color.clicked.connect(lambda: self.setColor(self.pb_port_dirty_pen_color))

    def saveOptions(self):

        print('save options', self.settings_path)
        self.writeConfig()
        self.close()
        try:
            if self.picker is not None:
                self.picker.close()
        except:
            pass

    def writeConfig(self):
        self.settings_class.beginGroup('NODES')
        self.settings_class.setValue('Nodes base color', self.pb_node_base_color.color)
        self.settings_class.setValue('Nodes selected pen color', self.pb_node_selected_pen_color.color)
        self.settings_class.setValue('Nodes label bg color', self.pb_node_label_bg_color.color)
        self.settings_class.setValue('Nodes label font', self.fb_node_label_font.currentFont())
        self.settings_class.setValue('Nodes label font color', self.pb_node_label_font_color.color)
        self.settings_class.setValue('Nodes label font size', self.sb_node_label_font_size.value())
        self.settings_class.setValue('Nodes lyt A color', self.pb_lyt_a_color.color)
        self.settings_class.setValue('Nodes lyt B color', self.pb_lyt_b_color.color)
        self.settings_class.setValue('Pin color', self.pb_port_color.color)
        self.settings_class.setValue('Pin dirty color', self.pb_port_dirty_pen_color.color)
        self.settings_class.setValue('Pin dirty type', self.cb_port_dirty_pen_type.currentText())
        self.settings_class.setValue('Pin label color', self.pb_port_label_color.color)
        self.settings_class.setValue('Pin label font', self.fb_port_label_font.currentFont())
        self.settings_class.setValue('Pin label size', self.sb_port_font_size.value())
        self.settings_class.endGroup()
        self.settings_class.beginGroup('SCENE')
        self.settings_class.setValue('Scene bg color', self.pb_scene_bg_color.color)
        self.settings_class.setValue('Grid color', self.pb_grid_color.color)
        self.settings_class.setValue('Grid lines type', self.cb_grid_lines_type.currentText())
        self.settings_class.setValue('Edge color', self.pb_edge_color.color)
        self.settings_class.setValue('Edge pen type', self.cb_edge_pen_type.currentText())
        self.settings_class.setValue('Edge line thickness', self.sb_edge_thickness.value())
        self.settings_class.endGroup()

    def write_default_config(self):
        print('create default config file')
        self.settings_class.beginGroup('NODES')
        self.settings_class.setValue('Nodes base color', Colors.NodeBackgrounds)
        self.pb_node_base_color.color = Colors.NodeBackgrounds
        self.settings_class.setValue('Nodes selected pen color', Colors.NodeSelectedPenColor)
        self.pb_node_selected_pen_color.color = Colors.NodeSelectedPenColor
        self.settings_class.setValue('Nodes selected pen type', LineTypes.lSolidLine)
        self.settings_class.setValue('Nodes label bg color', Colors.NodeNameRect)
        self.pb_node_label_bg_color.color = Colors.NodeNameRect
        self.settings_class.setValue('Nodes label font', QtGui.QFont('Consolas'))
        self.settings_class.setValue('Nodes label font color', Colors.White)
        self.settings_class.setValue('Nodes label font size', 6)
        self.settings_class.setValue('Nodes lyt A color', Colors.PortLinesA)
        self.pb_lyt_a_color.color = Colors.PortLinesA
        self.settings_class.setValue('Nodes lyt B color', Colors.PortLinesB)
        self.pb_lyt_b_color.color = Colors.PortLinesB
        self.settings_class.setValue('Pin color', Colors.Connectors)
        self.pb_port_color.color = Colors.Connectors
        self.settings_class.setValue('Pin dirty color', Colors.DirtyPen)
        self.pb_port_dirty_pen_color.color = Colors.DirtyPen
        self.settings_class.setValue('Pin dirty type', LineTypes.lDotLine)
        self.settings_class.setValue('Pin label color', Colors.PortNameColor)
        self.pb_port_label_color.color = Colors.PortNameColor
        self.settings_class.setValue('Pin label font', QtGui.QFont('Consolas'))
        self.settings_class.setValue('Pin label size', 5)
        self.settings_class.endGroup()
        self.settings_class.beginGroup('SCENE')
        self.settings_class.setValue('Scene bg color', Colors.SceneBackground)
        self.pb_scene_bg_color.color = Colors.SceneBackground
        self.settings_class.setValue('Grid color', Colors.GridColor)
        self.pb_grid_color.color = Colors.GridColor
        self.settings_class.setValue('Grid lines type', LineTypes.lDotLine)
        self.settings_class.setValue('Edge color', Colors.ConnectionLines)
        self.pb_edge_color.color = Colors.ConnectionLines
        self.settings_class.setValue('Edge pen type', LineTypes.lSolidLine)
        self.settings_class.setValue('Edge line thickness', 1.0)
        self.settings_class.endGroup()


class GraphWidget(QGraphicsView, Graph):

    def __init__(self, name, parent=None):
        super(GraphWidget, self).__init__()
        Graph.__init__(self, name)
        self.undoStack = QUndoStack(self)
        self.parent = parent
        self.parent.actionClear_history.triggered.connect(self.undoStack.clear)
        self.parent.listViewUndoStack.setStack(self.undoStack)
        self.menu = QMenu()
        self._lastClock = 0.0
        self.fps = 0
        self.setScene(SceneClass(self))
        self.options_widget = OptionsClass()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pressed_item = None
        self.released_item = None
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
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setAcceptDrops(True)
        self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.scene().setSceneRect(QtCore.QRect(0, 0, 10000, 10000))
        self._grid_spacing = 50
        self.factor = 1
        self.factor_diff = 0
        self.setWindowTitle(self.tr(name))
        self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)

        self._current_file_name = 'Untitled'
        self._file_name_label = QGraphicsTextItem()
        self._file_name_label.setZValue(5)
        self._file_name_label.setEnabled(False)
        self._file_name_label.setFlag(QGraphicsTextItem.ItemIgnoresTransformations)
        self._file_name_label.setDefaultTextColor(Colors.White)
        self._file_name_label.setPlainText(self._current_file_name)

        self.scene().addItem(self._file_name_label)
        self.rubber_rect = RubberRect('RubberRect')

        self.real_time_line = QGraphicsPathItem(None, self.scene())

        self.real_time_line.name = 'RealTimeLine'
        self.real_time_line.object_type = ObjectTypes.Connection
        self.real_time_line.setPen(QtGui.QPen(Colors.Green, 1.0, QtCore.Qt.DashLine))
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
        self.centerOn(QtCore.QPointF(self.sceneRect().width() / 2, self.sceneRect().height() / 2))
        self.initialScrollBarsPos = QtGui.QVector2D(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
        # self.registeredCommands = {}
        # self.registerCommands()
        self._sortcuts_enabled = True
        self.tick_timer = QtCore.QTimer()
        self.tick_timer.timeout.connect(self.mainLoop)
        self.tick_timer.start(20)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.grid_size = 10
        self.drawGrigSize = self.grid_size * 2
        self.current_rounded_pos = QtCore.QPointF(0.0, 0.0)
        self.autoPanController = AutoPanController()
        self._bRightBeforeShoutDown = False

        self.node_box = NodesBox(None, self)
        self.node_box.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.codeEditors = {}
        self.nodesMoveInfo = {}

    def showNodeBox(self, dataType=None):
        self.node_box.show()
        self.node_box.move(QtGui.QCursor.pos())
        self.node_box.treeWidget.refresh(dataType)
        self.node_box.lineEdit.clear()
        self.node_box.lineEdit.setFocus()

    def shoutDown(self):
        self.tick_timer.stop()
        self.tick_timer.timeout.disconnect()
        FunctionLibraries.shoutDown()
        self.scene().shoutDown()
        self.scene().clear()

    def moveScrollbar(self, delta):
        x = self.horizontalScrollBar().value() + delta.x()
        y = self.verticalScrollBar().value() + delta.y()
        self.horizontalScrollBar().setValue(x)
        self.verticalScrollBar().setValue(y)

    def setScrollbarsPositions(self, horizontal, vertical):
        try:
            self.horizontalScrollBar().setValue(horizontal)
            self.verticalScrollBar().setValue(vertical)
        except Exception as e:
            print(e)
            self.writeToConsole(e)

    def mouseDoubleClickEvent(self, event):
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()

    def OnDoubleClick(self, pos):
        if isinstance(self.pressed_item, Edge):
            # create knot
            pass

        if self.pressed_item and hasattr(self.pressed_item, "object_type"):
            if self.pressed_item.object_type == ObjectTypes.NodeName and self.pressed_item.IsRenamable():
                name, result = QInputDialog.getText(self, "New name dialog", "Enter new name:")
                if result:
                    self.pressed_item.parentItem().setName(name)
                    self.updatePropertyView(self.pressed_item.parentItem())

    def redrawNodes(self):
        for n in self.getNodes():
            n.updatePins()

    def __del__(self):
        self.tick_timer.stop()

    @staticmethod
    def playSoundWin(file_name):
        t = Thread(target=lambda: winsound.PlaySound(file_name, winsound.SND_FILENAME))
        t.start()

    def mainLoop(self):
        deltaTime = clock() - self._lastClock
        ds = (deltaTime * 1000.0)
        if ds > 0:
            self.fps = 1000.0 / ds
        if self.autoPanController.isActive():
            self.moveScrollbar(self.autoPanController.getDelta())
        for n in self.getNodes():
            n.Tick(deltaTime)

        self._lastClock = clock()

    def notify(self, message, duration):
        self.parent.statusBar.showMessage(message, duration)
        self.writeToConsole(message)

    def screenShot(self):
        name_filter = "Image (*.png)"
        fName = QFileDialog.getSaveFileName(filter=name_filter)
        if not fName[0] == '':
            self.writeToConsole("save screen to {0}".format(fName[0]))
            img = QtGui.QPixmap.grabWidget(self)
            img.save(fName[0], quality=100)

    def isShortcutsEnabled(self):
        return self._sortcuts_enabled

    def disableSortcuts(self):
        self._sortcuts_enabled = False

    def enableSortcuts(self):
        self._sortcuts_enabled = True

    def findPort(self, pinName):
        node = self.getNodeByName(pinName.split(".")[0])
        if node:
            attr = node.getPinByName(pinName.split(".")[1])
            return attr
        return None

    def getSettings(self):
        if path.isfile(self.options_widget.settings_path):
            settings = QtCore.QSettings(self.options_widget.settings_path, QtCore.QSettings.IniFormat)
            return settings

    def getGraphSaveData(self):
        data = {self.name: {'nodes': [], 'edges': [], 'variables': []}}
        # save nodes
        data[self.name]['nodes'] = [node.serialize() for node in self.getNodes()]
        # save edges
        data[self.name]['edges'] = [e.serialize() for e in self.edges.values()]
        # variables
        data[self.name]['variables'] = [v.serialize() for v in self.vars.values()]
        return data

    def save(self, save_as=False):
        if save_as:
            name_filter = "Graph files (*.json)"
            pth = QFileDialog.getSaveFileName(filter=name_filter)
            if not pth[0] == '':
                self._current_file_name = pth[0]
            else:
                self._current_file_name = "Untitled"
        else:
            if not path.isfile(self._current_file_name):
                name_filter = "Graph files (*.json)"
                pth = QFileDialog.getSaveFileName(filter=name_filter)
                if not pth[0] == '':
                    self._current_file_name = pth[0]
                else:
                    self._current_file_name = "Untitled"

        if self._current_file_name in ["", "Untitled"]:
            return

        if not self._current_file_name == '':
            with open(self._current_file_name, 'w') as f:
                json.dump(self.getGraphSaveData(), f)

            self._file_name_label.setPlainText(self._current_file_name)
            if self.parent:
                self.parent.console.append(str("// saved: '{0}'".format(self._current_file_name)))

    def save_as(self):
        self.save(True)

    def new_file(self):
        self._current_file_name = 'Untitled'
        self._file_name_label.setPlainText('Untitled')
        for node in self.getNodes():
            node.kill()
        self.vars.clear()
        self.parent.variablesWidget.listWidget.clear()
        self.undoStack.clear()

    def load(self):
        name_filter = "Graph files (*.json)"
        fpath = QFileDialog.getOpenFileName(filter=name_filter, dir="./Examples")
        if not fpath[0] == '':
            with open(fpath[0], 'r') as f:
                data = json.load(f)
                self.new_file()
                # vars
                for varJson in data[self.name]['variables']:
                    VariableBase.deserialize(varJson, self)
                # nodes
                for nodeJson in data[self.name]['nodes']:
                    Node.deserialize(nodeJson, self)
                # edges
                for edgeJson in data[self.name]['edges']:
                    Edge.deserialize(edgeJson, self)
                self._current_file_name = fpath[0]
                self._file_name_label.setPlainText(self._current_file_name)
                self.frame()
                self.undoStack.clear()

    def getPinByFullName(self, full_name):
        node_name = full_name.split('.')[0]
        pinName = full_name.split('.')[1]
        node = self.getNodeByName(node_name)
        if node:
            Pin = node.getPinByName(pinName)
            if Pin:
                return Pin

    def options(self):
        self.options_widget.show()

    def frame(self):
        nodes_rect = self.getNodesRect()
        if nodes_rect:
            self.centerOn(nodes_rect.center())

    def getNodesRect(self, selected=False):
        rectangles = []
        if selected:
            for n in [n for n in self.getNodes() if n.isSelected()]:
                n_rect = QtCore.QRectF(n.scenePos(),
                                       QtCore.QPointF(n.scenePos().x() + float(n.w),
                                                      n.scenePos().y() + float(n.h)))
                rectangles.append([n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])
        else:
            for n in self.getNodes():
                n_rect = QtCore.QRectF(n.scenePos(),
                                       QtCore.QPointF(n.scenePos().x() + float(n.w),
                                                      n.scenePos().y() + float(n.h)))
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
        return [i for i in self.getNodes() if i.isSelected()]

    def killSelectedNodes(self):
        cmdRemove = Commands.RemoveNodes(self.selectedNodes(), self)
        self.undoStack.push(cmdRemove)
        clearLayout(self.parent.formLayout)

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        if all([event.key() == QtCore.Qt.Key_N, modifiers == QtCore.Qt.ControlModifier]):
            self.new_file()
        if all([event.key() == QtCore.Qt.Key_Z, modifiers == QtCore.Qt.ControlModifier]):
            self.undoStack.undo()
        if all([event.key() == QtCore.Qt.Key_Y, modifiers == QtCore.Qt.ControlModifier]):
            self.undoStack.redo()
        if all([event.key() == QtCore.Qt.Key_Equal, modifiers == QtCore.Qt.ControlModifier]):
            self.zoomDelta(True)
        if all([event.key() == QtCore.Qt.Key_Minus, modifiers == QtCore.Qt.ControlModifier]):
            self.zoomDelta(False)
        if all([event.key() == QtCore.Qt.Key_R, modifiers == QtCore.Qt.ControlModifier]):
            self.reset_scale()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier]):
            self.save()
        if all([event.key() == QtCore.Qt.Key_O, modifiers == QtCore.Qt.ControlModifier]):
            self.load()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.save_as()
        if all([event.key() == QtCore.Qt.Key_F, modifiers == QtCore.Qt.ControlModifier]):
            self.frame()
        if all([event.key() == QtCore.Qt.Key_N, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            if self.parent:
                self.parent.toggle_node_box()
        if all([event.key() == QtCore.Qt.Key_M, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier]):
            self.parent.toggle_multithreaded()
        if all([event.key() == QtCore.Qt.Key_D, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier]):
            self.parent.toggle_debug()
        if all([event.key() == QtCore.Qt.Key_C, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.parent.toggle_console()
        if all([event.key() == QtCore.Qt.Key_P, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.parent.toggle_property_view()
        if event.key() == QtCore.Qt.Key_Delete:
            self.killSelectedNodes()
        if event.key() == QtCore.Qt.Key_P and modifiers == QtCore.Qt.NoModifier:
            print(self.getGraphSaveData())
        if all([event.key() == QtCore.Qt.Key_W, modifiers == QtCore.Qt.ControlModifier]):
            self.duplicateNodes()
        QGraphicsView.keyPressEvent(self, event)

    def duplicateNodes(self):
        selectedNodes = [i for i in self.getNodes() if i.isSelected()]

        if len(selectedNodes) > 0:
            diff = QtCore.QPointF(self.mapToScene(self.mousePos)) - selectedNodes[0].scenePos()

            for n in selectedNodes:
                new_node = n.clone()
                # n.setSelected(False)
                new_node.setSelected(True)
                new_node.setPos(new_node.scenePos() + diff)

    def alignSelectedNodes(self, direction):
        ls = [n for n in self.getNodes() if n.isSelected()]

        x_positions = [p.scenePos().x() for p in ls]
        y_positions = [p.scenePos().y() for p in ls]

        if direction == Direction.Left:
            if len(x_positions) == 0:
                return
            x = min(x_positions)
            for n in ls:
                n.setX(x)

        if direction == Direction.Right:
            if len(x_positions) == 0:
                return
            x = max(x_positions)
            for n in ls:
                n.setX(x)

        if direction == Direction.Up:
            if len(y_positions) == 0:
                return
            y = min(y_positions)
            for n in ls:
                n.setY(y)

        if direction == Direction.Down:
            if len(y_positions) == 0:
                return
            y = max(y_positions)
            for n in ls:
                n.setY(y)

    def findGoodPlaceForNewNode(self):
        polygon = self.mapToScene(self.viewport().rect())
        ls = polygon.toList()
        point = QtCore.QPointF((ls[1].x() - ls[0].x()) / 2, (ls[3].y() - ls[2].y()) / 2)
        point += ls[0]
        point.setY(point.y() + polygon.boundingRect().height() / 3)
        point += QtCore.QPointF(float(random.randint(50, 200)), float(random.randint(50, 200)))
        return point

    def keyReleaseEvent(self, event):
        QGraphicsView.keyReleaseEvent(self, event)

    def mousePressEvent(self, event):
        super(GraphWidget, self).mousePressEvent(event)
        self.pressed_item = self.itemAt(event.pos())
        self.mousePressPose = event.pos()
        if not isinstance(self.pressed_item, NodesBox) and self.node_box.isVisible():
            self.node_box.hide()

        modifiers = event.modifiers()

        if self.pressed_item and isinstance(self.pressed_item, QGraphicsItem):
            self.autoPanController.start()
            if isinstance(self.pressed_item, PinBase) and event.button() == QtCore.Qt.LeftButton:
                self.pressed_item.parent().setFlag(QGraphicsItem.ItemIsMovable, False)
                self.pressed_item.parent().setFlag(QGraphicsItem.ItemIsSelectable, False)
                self._draw_real_time_line = True
            else:
                self.pressed_item.setSelected(True)

        if not self.pressed_item:
            if event.button() == QtCore.Qt.LeftButton and modifiers == QtCore.Qt.NoModifier:
                self._is_rubber_band_selection = True
            if event.button() == QtCore.Qt.RightButton and modifiers == QtCore.Qt.NoModifier:
                self.bPanMode = True
            self.initialScrollBarsPos = QtGui.QVector2D(self.horizontalScrollBar().value(), self.verticalScrollBar().value())

        selectedNodes = self.selectedNodes()
        if len(selectedNodes) > 0 and isinstance(self.pressed_item, Node):
            self.nodesMoveInfo.clear()
            for n in self.getNodes():
                self.nodesMoveInfo[n.uid] = {'from': n.scenePos(), 'to': None}

    def pan(self, delta):
        delta *= self._scale * -1
        delta *= self._panSpeed
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())

    def mouseMoveEvent(self, event):
        super(GraphWidget, self).mouseMoveEvent(event)
        self.mousePos = event.pos()

        if self.bPanMode:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self._lastMousePos)
            self.pan(delta)

        if self._draw_real_time_line:
            if isinstance(self.pressed_item, Pin):
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
            path.cubicTo(QtCore.QPoint(p1.x() + distance / multiply, p1.y()), QtCore.QPoint(p2.x() - distance / 2, p2.y()), p2)
            self.real_time_line.setPath(path)

        if self._is_rubber_band_selection:
            mCurrentPose = self.mapToScene(self.mousePos)
            mPressPose = self.mapToScene(self.mousePressPose)
            if self.rubber_rect not in self.scene().items():
                self.scene().addItem(self.rubber_rect)
            if not self.rubber_rect.isVisible():
                self.rubber_rect.setVisible(True)
            r = QtCore.QRectF(mPressPose.x(),
                              mPressPose.y(),
                              mCurrentPose.x() - mPressPose.x(),
                              mCurrentPose.y() - mPressPose.y())
            self.rubber_rect.setRect(r.normalized())

        self.autoPanController.Tick(self.viewport().rect(), event.pos())

        self._lastMousePos = event.pos()

    def removeItemByName(self, name):
        [self.scene().removeItem(i) for i in self.scene().items() if hasattr(i, 'name') and i.name == name]

    def mouseReleaseEvent(self, event):
        super(GraphWidget, self).mouseReleaseEvent(event)

        self.autoPanController.stop()
        self.released_item = self.itemAt(event.pos())
        self.bPanMode = False
        self._resize_group_mode = False
        self.viewport().setCursor(QtCore.Qt.ArrowCursor)

        modifiers = event.modifiers()

        for n in self.getNodes():
            n.setFlag(QGraphicsItem.ItemIsMovable)
            n.setFlag(QGraphicsItem.ItemIsSelectable)

        if self._draw_real_time_line:
            self._draw_real_time_line = False
            if self.real_time_line in self.scene().items():
                self.removeItemByName('RealTimeLine')
        if self._is_rubber_band_selection:
            self._is_rubber_band_selection = False
            self.setDragMode(QGraphicsView.NoDrag)

            # hack. disable signals and call selectionChanged once with last selected item
            self.scene().blockSignals(True)
            items = [i for i in self.rubber_rect.collidingItems() if isinstance(i, Node)]
            for item in items[:-1]:
                item.setSelected(True)
            self.scene().blockSignals(False)
            if len(items) > 0:
                items[-1].setSelected(True)

            [i.setFlag(QGraphicsItem.ItemIsMovable) for i in self.getNodes() if i.isSelected()]
            self.removeItemByName(self.rubber_rect.name)
        if event.button() == QtCore.Qt.RightButton:
            # call context menu only if drag is small
            dragDiff = self.mapToScene(self.mousePressPose) - self.mapToScene(event.pos())
            if all([abs(i) < 0.1 for i in [dragDiff.x(), dragDiff.y()]]):
                if self.pressed_item is None:
                    self.showNodeBox()

            self._right_button = False
        p_itm = self.pressed_item
        r_itm = self.released_item
        do_connect = True
        for i in [p_itm, r_itm]:
            if not i:
                do_connect = False
                break
            if not hasattr(i, 'object_type'):
                do_connect = False
                break
            if not i.object_type == ObjectTypes.Pin:
                do_connect = False
                break
        if p_itm and r_itm:
            if isinstance(p_itm, Pin) and isinstance(r_itm, Pin):
                if cycle_check(p_itm, r_itm):
                    self.writeToConsole('cycles are not allowed')
                    do_connect = False

        if isinstance(r_itm, QGraphicsPathItem) and isinstance(p_itm, Pin):
            # node box tree pops up
            # with nodes taking supported data types of pressed Pin as input
            self.showNodeBox(p_itm.dataType)

        if do_connect:
            if p_itm is not r_itm:
                self.addEdge(p_itm, r_itm)

        for nodeUid in self.nodesMoveInfo:
            self.nodesMoveInfo[nodeUid]['to'] = self.nodes[nodeUid].scenePos()
        #  check if nodes moved
        bMoved = False
        for nodeUid, v in self.nodesMoveInfo.iteritems():
            if not v['from'] == v['to']:
                bMoved = True

        # pass copy of dict!
        if bMoved:
            cmdMove = Commands.Move(dict(self.nodesMoveInfo), self)
            self.undoStack.push(cmdMove)
            self.nodesMoveInfo.clear()

        selectedNodes = self.selectedNodes()
        if len(selectedNodes) != 0:
            self.tryFillPropertiesView(selectedNodes[0])
        else:
            self._clearPropertiesView()
        # selectedNodesUids = [n.uid for n in self.getNodes() if n.isSelected()]
        # if len(selectedNodesUids) > 0:
            # cmdSelect = Commands.Select(selectedNodesUids, self)
            # self.undoStack.push(cmdSelect)

    def tryFillPropertiesView(self, obj):
        '''
            toDO: obj should implement interface class
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
        self.zoom(math.pow(2.0, event.delta() / 240.0))

    def drawBackground(self, painter, rect):
        super(GraphWidget, self).drawBackground(painter, rect)

        polygon = self.mapToScene(self.viewport().rect())
        self._file_name_label.setPos(polygon[0])
        scene_rect = self.sceneRect()
        # Fill
        settings = self.getSettings()
        if settings:
            color = QtGui.QColor(settings.value('SCENE/Scene bg color'))
        else:
            color = self.kSceneBackground
        painter.fillRect(rect.intersect(scene_rect), QtGui.QBrush(color))

        left = int(scene_rect.left()) - (int(scene_rect.left()) % self.drawGrigSize)
        top = int(scene_rect.top()) - (int(scene_rect.top()) % self.drawGrigSize)

        # draw grid vertical lines
        scaleMult = 1.0
        for x in xrange(left, int(scene_rect.right()), self.drawGrigSize):
            if x % (self.drawGrigSize * 10.0) == 0.0:
                painter.setPen(QtGui.QPen(Colors.GridColorDarker, 1.0 / (self.factor * scaleMult), QtCore.Qt.SolidLine))
            else:
                painter.setPen(QtGui.QPen(Colors.GridColor, 0.5 / (self.factor * scaleMult), QtCore.Qt.SolidLine))
            painter.drawLine(x, scene_rect.top(), x, scene_rect.bottom())

        # draw grid horizontal lines
        for y in xrange(top, int(scene_rect.bottom()), self.drawGrigSize):
            if y % (self.drawGrigSize * 10.0) == 0.0:
                painter.setPen(QtGui.QPen(Colors.GridColorDarker, 1.0 / (self.factor * scaleMult), QtCore.Qt.SolidLine))
            else:
                painter.setPen(QtGui.QPen(Colors.GridColor, 0.5 / (self.factor * scaleMult), QtCore.Qt.SolidLine))
            painter.drawLine(scene_rect.left(), y, scene_rect.right(), y)

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
            self.parent.console.append(msg)

    def getVarByName(self, name):
        var = None
        for v in self.vars.values():
            if v.name == name:
                var = v
        return var

    def createVariableSetter(self, jsonTemplate):
        var = self.vars[uuid.UUID(jsonTemplate['meta']['varuuid'])]
        instance = SetVarNode(var.name, self, var)
        return instance

    def createVariableGetter(self, jsonTemplate):
        var = self.vars[uuid.UUID(jsonTemplate['meta']['varuuid'])]
        instance = GetVarNode(var.name, self, var)
        return instance

    def _createNode(self, jsonTemplate):
        nodeInstance = getNodeInstance(Nodes, jsonTemplate['type'], jsonTemplate['name'], self)

        # If not found, check variables
        if nodeInstance is None:
            if jsonTemplate['type'] == 'GetVarNode':
                nodeInstance = self.graph.createVariableGetter(jsonTemplate)
            if jsonTemplate['type'] == 'SetVarNode':
                nodeInstance = self.graph.createVariableSetter(jsonTemplate)

        # set pins data
        for inspJson in jsonTemplate['inputs']:
            pin = nodeInstance.getPinByName(inspJson['name'], PinSelectionGroup.Inputs)
            if pin:
                pin.uid = uuid.UUID(inspJson['uuid'])
                pin.setData(inspJson['value'])
                if inspJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        for outJson in jsonTemplate['outputs']:
            pin = nodeInstance.getPinByName(outJson['name'], PinSelectionGroup.Outputs)
            if pin:
                pin.uid = uuid.UUID(outJson['uuid'])
                pin.setData(outJson['value'])
                if outJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        if nodeInstance is None:
            raise ValueError("node class not found!")

        self.addNode(nodeInstance, jsonTemplate)
        return nodeInstance

    def createNode(self, jsonTemplate):
        cmd = Commands.CreateNode(self, jsonTemplate)
        self.undoStack.push(cmd)
        return cmd.nodeInstance

    def addNode(self, node, jsonTemplate=None):
        Graph.addNode(self, node, jsonTemplate)
        self.scene().addItem(node)

    def _addEdge(self, src, dst):
        result = Graph.addEdge(self, src, dst)
        if result:
            if src.type == PinTypes.Input:
                src, dst = dst, src
            edge = Edge(src, dst, self)
            src.edge_list.append(edge)
            dst.edge_list.append(edge)
            self.scene().addItem(edge)
            self.edges[edge.uid] = edge
            return edge

    def addEdge(self, src, dst):
        cmd = Commands.ConnectPin(self, src, dst)
        self.undoStack.push(cmd)

    def removeEdge(self, edge):
        Graph.removeEdge(self, edge)
        edge.source().update()
        edge.destination().update()
        self.edges.pop(edge.uid)
        edge.prepareGeometryChange()
        self.scene().removeItem(edge)

    def writeToConsole(self, data):
        if self.isDebug():
            self.parent.console.append(str(data))

    def plot(self):
        for k, v in self.nodes.iteritems():
            print(k, v.name)
        Graph.plot(self)
        self.parent.console.append('>>>>>>> {0} <<<<<<<\n{1}\n'.format(self.name, ctime()))
        if self.parent:
            for n in self.getNodes():
                self.parent.console.append(n.name)
                for i in n.inputs.values() + n.outputs.values():
                    self.parent.console.append('|--- {0} data - {1} affects on {2} affected by {3} DIRTY {4}, uid - {5}'.format(i.pinName(),
                                               i.currentData(),
                                               [p.pinName() for p in i.affects],
                                               [p.pinName() for p in i.affected_by],
                                               i.dirty,
                                               str(i.uid)))
            self.parent.console.append('Variables\n----------')
            for k, v in self.vars.iteritems():
                msg = '{0} - {1}, uid - {2}'.format(v.name, v.value, str(v.uid))
                print(msg)
                self.parent.console.append(msg)

    def zoomDelta(self, direction):
        current_factor = self.factor
        if direction:
            self.zoom(1 + 0.1)
        else:
            self.zoom(1 - 0.1)

    def reset_scale(self):
        self.resetMatrix()

    def zoom(self, scale_factor):

        self.factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        self.factor = round(self.factor, 1)
        if self.factor < (self.minimum_scale + 0.4):
            self.grid_size = 20
        else:
            self.grid_size = 10
        if self.factor < self.minimum_scale or self.factor > self.maximum_scale:
            return
        self.scale(scale_factor, scale_factor)
        self._scale *= scale_factor
