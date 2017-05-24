from PySide import QtCore
from PySide import QtGui
import math
import platform
import random
from Settings import Colors
from Settings import LineTypes
from Settings import get_line_type
from AbstractGraph import *
from Edge import Edge, RealTimeLine
from os import listdir, path, startfile
import sys
_file_folder = path.dirname(__file__)
_mod_folder = _file_folder.replace(_file_folder.rsplit('\\')[-1], '')
nodes_path = _mod_folder+'\\Nodes'
if nodes_path not in sys.path:
    sys.path.append(nodes_path)
import Nodes
import Commands
from time import ctime
import OptionsWindow_ui
import rgba_color_picker_ui
import json
import re
import winsound


def get_mid_point(args):

    return [sum(i)/len(i) for i in zip(*args)]


def get_nodes_file_names():

    return [i[:-3] for i in listdir(nodes_path) if i.endswith('.py') and '__init__' not in i]


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


def get_node(module, name, graph):

    if hasattr(module, name):
        try:
            mod = getattr(module, name)
            mod = mod(name, graph)
            return mod
        except Exception as e:
            print("ERROR node creation!!", e)
            return


class PluginType:
    pNode = 0
    pCommand = 1


def _implementPlugin(name, console_out_foo, pluginType, graph):
    base_command_code = """from AGraphPySide import Command


class {0}(Command.Command):

    def __init__(self, graph):
        super({0}, self).__init__(graph)

    def usage(self):

        return "[USAGE] usage string"

    def execute(self, line):
        commandLine = self.parse(line)
        try:
            self.graph.write_to_console(commandLine["-text"])
        except Exception as e:
            print(self.usage())
""".format(name)

    base_node_code = """from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode

DESC = '''node desc
'''

class {0}(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super({0}, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.inp0 = self.add_input_port('in0', AGPortDataTypes.tAny)
        self.out0 = self.add_output_port('out0', AGPortDataTypes.tAny)
        portAffects(self.inp0, self.out0)

    @staticmethod
    def get_category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        str_data = self.inp0.get_data()
        try:
            self.out0.set_data(str_data.upper(), False)
        except Exception as e:
            print(e)
""".format(name)

    if pluginType == PluginType.pNode:
        file_path = "{0}/{1}.py".format(Nodes.__path__[0], name)
        existing_nodes = [n.split(".")[0] for n in listdir(Nodes.__path__[0]) if n.endswith(".py") and "__init__" not in n]
        category_names = graph.node_box.tree_widget.categories.keys()
        if name in existing_nodes:
            console_out_foo("[ERROR] Node {0} already exists".format(name))
            return

        if name.lower() in [n.lower() for n in category_names]:
            console_out_foo("[ERROR] Category with this name ( {0} ) already exists. Please, choose another name".format(name))
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
            f.write(base_command_code)
        console_out_foo("[INFO] Command {0} been created.\n Restart application.".format(name))
        startfile(file_path)
    # sys.exit()


def import_by_name(module, name):

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
    for i in xrange(len(flag_sep)-1):
        newLine =  line[flag_sep[i]:]
        newLineDashes = [m.start() for m in re.finditer(FLAG_SYMBOL, newLine)]
        flag = newLine[:newLineDashes[1]-1].split(" ", 1) # flag + value
        out["flags"][flag[0]] = flag[1]
    flag = line[flag_sep[-1]:].split(" ", 1) # last flag + value
    out["flags"][flag[0]] = flag[1]
    return out


class SceneClass(QtGui.QGraphicsScene):
    def __init__(self, parent):
        super(SceneClass, self).__init__(parent)
        self.Type = 'SCENE'
        self.setItemIndexMethod(self.NoIndex)
        self.pressed_port = None
        self.selectionChanged.connect(self.OnSelectionChanged)

    def mouseDoubleClickEvent(self, event):
        self.parent().OnDoubleClick(event.scenePos())
        event.accept()

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

    def OnSelectionChanged(self):
        selected_nodes = []
        for n in self.parent().get_nodes():
            if n.isSelected():
                selected_nodes.append(n.name)
        if len(selected_nodes) == 0:
            self.parent().write_to_console("select {0}nl none".format(FLAG_SYMBOL))
            return
        cmd = "select {0}nl ".format(FLAG_SYMBOL)
        for n in selected_nodes:
            cmd += n
            cmd += " "
        self.parent().write_to_console(cmd[:-1])

    def dropEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            className = event.mimeData().text()
            name = self.parent().get_uniq_node_name(className)
            if className == "MakeArray":
                self.parent().executeCommand("createNode ~type MakeArray ~count {3} ~x {0} ~y {1} ~n {2}\n".format(event.scenePos().x(), event.scenePos().y(), name, 0))
            else:
                self.parent().executeCommand("createNode {4}type {0} {4}x {1} {4}y {2} {4}n {3}".format(className, event.scenePos().x(), event.scenePos().y(), name, FLAG_SYMBOL))
        else:
            super(SceneClass, self).dropEvent(event)


class NodesBoxListWidget(QtGui.QListWidget):
    def __init__(self, parent, events=True):
        super(NodesBoxListWidget, self).__init__(parent)
        self.parent_item = parent
        self._events = events
        style = "background-color: rgb(80, 80, 80);" +\
                "selection-background-color: rgb(150, 150, 150);" +\
                "selection-color: yellow;" +\
                "border-radius: 2px;" +\
                "font-size: 14px;" +\
                "border-color: black; border-style: outset; border-width: 1px;"
        self.setStyleSheet(style)
        self.setParent(parent)
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setObjectName("lw_nodes")
        self.setSortingEnabled(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def mousePressEvent(self, event):
        super(NodesBoxListWidget, self).mousePressEvent(event)
        pressed_text = self.selectedItems()[0].text()
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        mime_data.setText(pressed_text)
        drag.setMimeData(mime_data)
        drag.exec_()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            point = self.parent_item.graph.findGoodPlaceForNewNode()
            name = self.currentItem().text()
            self.parent_item.graph.create_node(name, point.x(), point.y(), name)
        if self._events:
            if event.key() == QtCore.Qt.Key_Escape:
                self.parent_item.close()
                self.clear()
        super(NodesBoxListWidget, self).keyPressEvent(event)


class NodeBoxLineEdit(QtGui.QLineEdit):
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
        self.setVisible(False)

    def keyPressEvent(self, event):
        if self._events:
            if event.key() == QtCore.Qt.Key_Escape:
                self.parent.close()
                self.parent.listWidget.clear()
        super(NodeBoxLineEdit, self).keyPressEvent(event)


class NodeBoxTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent):
        super(NodeBoxTreeWidget, self).__init__(parent)
        style = "background-color: rgb(80, 80, 80);" +\
                "selection-background-color: rgb(150, 150, 150);" +\
                "selection-color: yellow;" +\
                "border-radius: 2px;" +\
                "font-size: 14px;" +\
                "border-color: black; border-style: outset; border-width: 1px;"
        self.graph = parent
        self.setStyleSheet(style)
        self.setParent(parent)
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setObjectName("tree_nodes")
        self.setSortingEnabled(True)
        self.setDragEnabled(True)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.categories = {}
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def refresh(self):
        self.clear()
        for node_file_name in get_nodes_file_names():
            node_class = getattr(Nodes, node_file_name)
            category_name = node_class.get_category()
            if not category_name in self.categories:
                CatItem = QtGui.QTreeWidgetItem(self)
                CatItem.setText(0, category_name)
                self.categories[category_name] = CatItem
            NodeItem = QtGui.QTreeWidgetItem(self.categories[category_name])
            NodeItem.setText(0, node_file_name)

    def keyPressEvent(self, event):
        super(NodeBoxTreeWidget, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            point = self.graph.findGoodPlaceForNewNode()
            name = self.currentItem().text(0)
            self.graph.create_node(name, point.x(), point.y(), name)

    def mousePressEvent(self, event):
        super(NodeBoxTreeWidget, self).mousePressEvent(event)
        item_clicked = self.currentItem()
        if not item_clicked:
            event.ignore()
            return
        pressed_text = item_clicked.text(0)

        if pressed_text in self.categories.keys():
            event.ignore()
            return
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        mime_data.setText(pressed_text)
        drag.setMimeData(mime_data)
        drag.exec_()


class NodesBox(QtGui.QWidget):
    def __init__(self, graph):
        super(NodesBox, self).__init__()
        self.graph = graph
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)
        self.setObjectName("nodes_box_form")
        self.setWindowTitle('Node box - {0}'.format(self.graph.name))
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(160, 200)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.name = 'NODE_BOX'

        self.switch_button = QtGui.QPushButton("go to list mode")
        self.switch_button.clicked.connect(self.swap_appearance)

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.le_nodes = NodeBoxLineEdit(self)
        self.le_nodes.textChanged.connect(self.le_text_changed)
        self.verticalLayout.addWidget(self.switch_button)
        self.verticalLayout.addWidget(self.le_nodes)
        self.listWidget = NodesBoxListWidget(self)
        self.verticalLayout.addWidget(self.listWidget)
        self.listWidget.setVisible(False)
        self.setVisible(False)
        self.refresh_list('')
        self.tree_widget = NodeBoxTreeWidget(self.graph)
        self.verticalLayout.addWidget(self.tree_widget)
        self.tree_widget.refresh()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setStyleSheet("border:1 inset white")

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier]):
            self.swap_appearance()
        super(NodesBox, self).keyPressEvent(event)

    def swap_appearance(self):
        self.listWidget.setVisible(not self.listWidget.isVisible())
        self.tree_widget.setVisible(not self.tree_widget.isVisible())
        self.le_nodes.setVisible(not self.le_nodes.isVisible())
        if self.tree_widget.isVisible():
            self.switch_button.setText("go to list mode")
        else:
            self.switch_button.setText("go to category mode")

    def refresh_list(self, pattern):

        self.listWidget.clear()
        node_file_names = get_nodes_file_names()
        self.listWidget.addItems([i for i in node_file_names if pattern.lower() in i.lower()])
        item = self.listWidget.itemAt(0, 0)
        if item and not item.isSelected():
            item.setSelected(True)

    def get_nodes_file_names(self):
        return get_nodes_file_names()

    def set_visible(self):

        pos = self.graph.current_cursor_pose
        self.move(self.graph.mapFromScene(pos.toPoint()).x()+self.graph.pos().x(),
                  self.graph.mapFromScene(pos.toPoint()).y()+self.graph.pos().y()
                  )
        self.refresh_list('')
        self.show()

    def create_node(self):
        items = self.listWidget.selectedItems()
        if not len(items) == 0:
            name = items[0].text()
            node = get_node(Nodes, name, self.graph)
            print(node.name, 'created')
            self.graph.add_node(node, self.graph.current_cursor_pose.x(),
                                       self.graph.current_cursor_pose.y())
            if self.listWidget._events:
                self.close()
                self.listWidget.clear()

    def le_text_changed(self):
        if self.le_nodes.text() == '':
            self.le_nodes.setPlaceholderText("enter node name..")
            self.refresh_list('')
            return
        self.refresh_list(self.le_nodes.text())


class RubberRect(QtGui.QGraphicsRectItem, Colors):
    def __init__(self, name):
        super(RubberRect, self).__init__()
        self.name = name
        self.setZValue(2)
        self.setPen(QtGui.QPen(self.kRubberRect, 0.5, QtCore.Qt.SolidLine))
        self.setBrush(QtGui.QBrush(self.kRubberRect))


class CommentNodeName(QtGui.QGraphicsTextItem, Colors):
    def __init__(self, parent):
        super(CommentNodeName, self).__init__()
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.parent = parent
        self.setParentItem(parent)
        self.setPlainText('...')
        self.setDefaultTextColor(self.kWhite)
        self.setCursor(QtCore.Qt.IBeamCursor)

    def update_pos(self):

        self.setPos(self.parent.rect().topLeft())
        self.setY(self.parent.rect().topLeft().y() - self.boundingRect().height())

    def focusInEvent(self, event):
        self.parentItem().graph.disable_sortcuts()
        super(CommentNodeName, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentItem().graph.enable_sortcuts()
        self.update_pos()
        super(CommentNodeName, self).focusOutEvent(event)

    def paint(self, painter, option, widget):

        painter.fillRect(option.rect, QtGui.QColor(self.kCommentNodeNameBackground))
        super(CommentNodeName, self).paint(painter, option, widget)

 
class CommentNode(QtGui.QGraphicsRectItem, Colors):
    def __init__(self, graph):
        super(CommentNode, self).__init__()
        self.object_type = AGObjectTypes.tGrouper
        self.graph = graph
        self.nodes = []
        self.menu = QtGui.QMenu()
        self.setAcceptHoverEvents(True)
        self.action_delete = self.menu.addAction('delete')
        self.action_delete.triggered.connect(self.delete)
        self.action_fit = self.menu.addAction('fit contents')
        self.action_fit.triggered.connect(self.fit_content)
        # self.setFlag(self.ItemIsMovable)
        self._minimum_width = 150
        self._minimum_height = 150
        # self.setZValue(0.0)
        self.auto_fit_content = False
        self.setPen(QtGui.QPen(self.kCommentNodePen, 1, QtCore.Qt.SolidLine))
        self.setBrush(QtGui.QBrush(self.kCommentNodeBrush))
        self.label = CommentNodeName(self)
        self.count_label = QtGui.QGraphicsTextItem(parent=self)
        self.count_label.setDefaultTextColor(self.kWhite)
        self.count_label.setFont(QtGui.QFont("Courier New", 8))
        self.count_label.setPlainText(str(len(self.nodes)))
        self.resize_item = QtGui.QGraphicsPolygonItem(parent=self)
        self.resize_item.setCursor(QtCore.Qt.SizeFDiagCursor)
        self.resize_item.setFlag(self.ItemIsMovable, False)
        self.setFlag(self.ItemIsSelectable, False)
        self.resize_item.mark = 'resize_object'
        self.resize_item.setPolygon(QtGui.QPolygonF([QtCore.QPointF(0.0, 10.0),
                                                     QtCore.QPointF(10.0, 10.0),
                                                     QtCore.QPointF(10.0, 0.0),
                                                     QtCore.QPointF(0.0, 10.0)
                                                     ]))
        self.resize_item.setBrush(self.kCommentNodeResizer)
        self.set_bottom_right(QtCore.QPointF(self.minimum_width, self.minimum_height))

    @property
    def minimum_height(self):
        return self._minimum_height

    @minimum_height.getter
    def minimum_height(self):
        return abs(self._minimum_height)

    @minimum_height.setter
    def minimum_height(self, data):
        self._minimum_height = abs(data)

    @property
    def minimum_width(self):
        return self._minimum_width

    @minimum_width.getter
    def minimum_width(self):
        return abs(self._minimum_width)

    @minimum_width.setter
    def minimum_width(self, data):
        self._minimum_width = abs(data)

    def get_nodes_rect(self):
        rectangles = []
        for n in self.nodes:
            scene_pos = n.scenePos()
            n_rect = QtCore.QRectF(scene_pos, QtCore.QPointF(scene_pos.x()+float(n.w), scene_pos.y()+float(n.h)))
            rectangles.append([n_rect.topLeft().x(),
                               n_rect.topLeft().y(),
                               n_rect.bottomRight().x()+25,
                               n_rect.bottomRight().y()+25]
                              )
        min_x = min([i[0] for i in rectangles])
        max_x = max([i[2] for i in rectangles])
        min_y = min([i[1] for i in rectangles])
        max_y = max([i[3] for i in rectangles])

        return QtCore.QRectF(QtCore.QPointF(min_x, min_y), QtCore.QPointF(max_x, max_y))

    def set_bottom_right(self, point):

        r = QtCore.QRectF(self.rect().topLeft().x(),
                          self.rect().topLeft().y(),
                          point.x()-self.mapToScene(self.rect().topLeft()).x()+25,
                          point.y()-self.mapToScene(self.rect().topLeft()).y()+25
                          )
        self.setRect(r.normalized())
        self.update()

    def hoverEnterEvent(self, event):

        self.setBrush(self.brush().color().lighter(130))

    def hoverLeaveEvent(self, event):

        self.setBrush(self.kCommentNodeBrush)

    def update_count_label(self):

        self.count_label.setPlainText(str(len(self.nodes)))

    def update(self):

        self.label.update_pos()
        self.count_label.setPos(self.rect().topLeft()-QtCore.QPointF(self.count_label.boundingRect().width(), 0))
        self.resize_item.setPos(self.rect().bottomRight()-QtCore.QPointF(self.resize_item.boundingRect().width(),
                                                                         self.resize_item.boundingRect().height()))

    def has_nodes(self):

        return False if len(self.nodes) == 0 else True

    def fit_content(self):

        if self.has_nodes():
            nodes_rect = self.get_nodes_rect()
            nodes_bottom_right = nodes_rect.bottomRight()
            self.set_bottom_right(nodes_bottom_right)
            # self.setFlag(self.ItemIsMovable)

    def mousePressEvent(self, event):

        # for i in self.nodes+self.graph.nodes:
        #     i.setSelected(False)
        super(CommentNode, self).mousePressEvent(event)

    def unpack(self):

        for i in self.nodes:
            self.remove_node(i)
            i.setZValue(1)
        self.update_count_label()
        if not len(self.nodes) == 0:
            self.unpack()

    def delete(self, call_connection_functions=False):
        self.unpack()
        for i in self.scene().items():
            i.setSelected(False)
        for n in self.nodes:
            n.setSelected(True)
        self.graph.kill_selected_nodes(call_connection_functions)
        self.scene().removeItem(self)
        self.graph.groupers.remove(self)
        del self

    def contextMenuEvent(self, event):

        self.menu.exec_(event.screenPos())

    def add_from_iterable(self, iterable):
        for i in iterable:
            self.add_node(i)

    def remove_from_iterable(self, iterable):
        for i in iterable:
            self.remove_node(i)

    def set_label_from_html(self, html):
        self.label.setHtml(html)

    def add_node(self, node):
        if node.object_type == AGObjectTypes.tNode and node not in self.nodes:
            if not node.parentItem():
                node.setZValue(self.zValue()+0.5)
                node.setParentItem(self)
                node.setPos(node.pos()-self.scenePos())
                self.nodes.append(node)
                self.update_count_label()

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            node.setParentItem(self.parentItem())
            node.setPos(self.mapToScene(node.pos()))
            self.update_count_label()


class RGBAColorPicker(QtGui.QWidget, rgba_color_picker_ui.Ui_rgba_color_picker_ui):
    def __init__(self, button):
        super(RGBAColorPicker, self).__init__()
        self.button = button
        self.setupUi(self)
        self.set_button_background(self.button.color)
        self.pb_color.color = self.button.color
        self.pb_color.clicked.connect(self.get_rgb)
        self.pb_apply.clicked.connect(self.apply)
        self.hs_alpha.valueChanged.connect(self.tweak_alpha)

    def set_button_background(self, color):
        self.pb_color.setStyleSheet("background-color: rgb({0}, {1}, {2}, {3});".format(
            color.red(),
            color.green(),
            color.blue(),
            color.alpha()
        ))

    def showEvent(self, event):
        self.set_button_background(self.button.color)
        self.hs_alpha.setValue(self.button.color.alpha())
        super(RGBAColorPicker, self).showEvent(event)

    def get_rgb(self):
        color = QtGui.QColorDialog.getColor()
        if color:
            self.pb_color.color = color
            color.setAlpha(self.hs_alpha.value())
            self.set_button_background(color)

    def tweak_alpha(self):
        self.pb_color.color.setAlpha(self.hs_alpha.value())
        self.set_button_background(self.pb_color.color)

    def apply(self):
        self.button.color = self.pb_color.color
        self.button.setStyleSheet("background-color: rgb({0}, {1}, {2}, {3});".format(
            self.pb_color.color.red(),
            self.pb_color.color.green(),
            self.pb_color.color.blue(),
            self.pb_color.color.alpha()
        ))
        self.close()


class OptionsClass(QtGui.QMainWindow, OptionsWindow_ui.Ui_OptionsUI):
    def __init__(self):
        super(OptionsClass, self).__init__()
        self.setupUi(self)
        self.connect_ui()
        self.populate_ui()
        self.picker = None
        self.settings_path = path.dirname(__file__)+'\\config.ini'
        self.settings_class = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat, self)
        if not path.isfile(self.settings_path):
            self.write_default_config()
        self.pb_scene_bg_color.color = QtGui.QColor(self.settings_class.value('SCENE/Scene bg color'))
        self.set_button_background(self.pb_scene_bg_color, self.pb_scene_bg_color.color)
        self.pb_grid_color.color = QtGui.QColor(self.settings_class.value('SCENE/Grid color'))
        self.set_button_background(self.pb_grid_color, self.pb_grid_color.color)
        self.pb_edge_color.color = QtGui.QColor(self.settings_class.value('SCENE/Edge color'))
        self.set_button_background(self.pb_edge_color, self.pb_edge_color.color)
        self.pb_node_base_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes base color'))
        self.set_button_background(self.pb_node_base_color, self.pb_node_base_color.color)
        self.pb_node_selected_pen_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes selected pen color'))
        self.set_button_background(self.pb_node_selected_pen_color, self.pb_node_selected_pen_color.color)
        self.pb_node_label_bg_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes label bg color'))
        self.set_button_background(self.pb_node_label_bg_color, self.pb_node_label_bg_color.color)
        self.pb_node_label_font_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes label font color'))
        self.set_button_background(self.pb_node_label_font_color, self.pb_node_label_font_color.color)
        self.pb_lyt_a_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes lyt A color'))
        self.set_button_background(self.pb_lyt_a_color, self.pb_lyt_a_color.color)
        self.pb_lyt_b_color.color = QtGui.QColor(self.settings_class.value('NODES/Nodes lyt B color'))
        self.set_button_background(self.pb_lyt_b_color, self.pb_lyt_b_color.color)
        self.pb_port_color.color = QtGui.QColor(self.settings_class.value('NODES/Port color'))
        self.set_button_background(self.pb_port_color, self.pb_port_color.color)
        self.pb_port_label_color.color = QtGui.QColor(self.settings_class.value('NODES/Port label color'))
        self.set_button_background(self.pb_port_label_color, self.pb_port_label_color.color)
        self.pb_port_dirty_pen_color.color = QtGui.QColor(self.settings_class.value('NODES/Port dirty color'))
        self.set_button_background(self.pb_port_dirty_pen_color, self.pb_port_dirty_pen_color.color)
        self.sb_node_label_font_size.setValue(int(self.settings_class.value('NODES/Nodes label font size')))
        self.fb_node_label_font.setCurrentFont(QtGui.QFont(self.settings_class.value('NODES/Nodes label font')))
        self.fb_port_label_font.setCurrentFont(QtGui.QFont(self.settings_class.value('NODES/Port label font')))
        self.sb_port_font_size.setValue(int(self.settings_class.value('NODES/Port label size')))
        self.sb_edge_thickness.setValue(float(self.settings_class.value('SCENE/Edge line thickness')))

        idx = self.cb_grid_lines_type.findText(str(self.settings_class.value('SCENE/Grid lines type')))
        self.cb_grid_lines_type.setCurrentIndex(idx)
        idx = self.cb_edge_pen_type.findText(str(self.settings_class.value('SCENE/Edge pen type')))
        self.cb_edge_pen_type.setCurrentIndex(idx)
        idx = self.cb_port_dirty_pen_type.findText(str(self.settings_class.value('NODES/Port dirty type')))
        self.cb_port_dirty_pen_type.setCurrentIndex(idx)

    @staticmethod
    def set_button_background(button, color):
        button.setStyleSheet("background-color: rgb({0}, {1}, {2}, {3});".format(
            color.red(),
            color.green(),
            color.blue(),
            color.alpha()
        ))

    def set_color(self, button):
        self.picker = RGBAColorPicker(button)
        self.picker.move(self.geometry().topRight().x(), self.geometry().topRight().y())
        self.picker.show()

    def populate_ui(self):
        line_types = [str(i) for i in dir(LineTypes) if i[0] == 'l']
        self.cb_port_dirty_pen_type.addItems(line_types)
        self.cb_grid_lines_type.addItems(line_types)
        self.cb_edge_pen_type.addItems(line_types)

    def connect_ui(self):

        self.actionSave.triggered.connect(self.save_options)

        self.pb_scene_bg_color.clicked.connect(lambda: self.set_color(self.pb_scene_bg_color))
        self.pb_grid_color.clicked.connect(lambda: self.set_color(self.pb_grid_color))
        self.pb_edge_color.clicked.connect(lambda: self.set_color(self.pb_edge_color))
        self.pb_node_base_color.clicked.connect(lambda: self.set_color(self.pb_node_base_color))
        self.pb_node_label_font_color.clicked.connect(lambda: self.set_color(self.pb_node_label_font_color))

        self.pb_node_selected_pen_color.clicked.connect(lambda: self.set_color(self.pb_node_selected_pen_color))
        self.pb_node_label_bg_color.clicked.connect(lambda: self.set_color(self.pb_node_label_bg_color))
        self.pb_lyt_a_color.clicked.connect(lambda: self.set_color(self.pb_lyt_a_color))
        self.pb_lyt_b_color.clicked.connect(lambda: self.set_color(self.pb_lyt_b_color))
        self.pb_port_color.clicked.connect(lambda: self.set_color(self.pb_port_color))
        self.pb_port_label_color.clicked.connect(lambda: self.set_color(self.pb_port_label_color))
        self.pb_port_dirty_pen_color.clicked.connect(lambda: self.set_color(self.pb_port_dirty_pen_color))

    def save_options(self):

        print('save options', self.settings_path)
        self.write_config()
        self.close()
        try:
            self.picker.close()
        except:
            pass

    def write_config(self):
        self.settings_class.beginGroup('NODES')
        self.settings_class.setValue('Nodes base color', self.pb_node_base_color.color)
        self.settings_class.setValue('Nodes selected pen color', self.pb_node_selected_pen_color.color)
        self.settings_class.setValue('Nodes label bg color', self.pb_node_label_bg_color.color)
        self.settings_class.setValue('Nodes label font', self.fb_node_label_font.currentFont())
        self.settings_class.setValue('Nodes label font color', self.pb_node_label_font_color.color)
        self.settings_class.setValue('Nodes label font size', self.sb_node_label_font_size.value())
        self.settings_class.setValue('Nodes lyt A color', self.pb_lyt_a_color.color)
        self.settings_class.setValue('Nodes lyt B color', self.pb_lyt_b_color.color)
        self.settings_class.setValue('Port color', self.pb_port_color.color)
        self.settings_class.setValue('Port dirty color', self.pb_port_dirty_pen_color.color)
        self.settings_class.setValue('Port dirty type', self.cb_port_dirty_pen_type.currentText())
        self.settings_class.setValue('Port label color', self.pb_port_label_color.color)
        self.settings_class.setValue('Port label font', self.fb_port_label_font.currentFont())
        self.settings_class.setValue('Port label size', self.sb_port_font_size.value())
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
        self.settings_class.setValue('Nodes base color', Colors.kNodeBackgrounds)
        self.pb_node_base_color.color = Colors.kNodeBackgrounds
        self.settings_class.setValue('Nodes selected pen color', Colors.kNodeSelectedPenColor)
        self.pb_node_selected_pen_color.color = Colors.kNodeSelectedPenColor
        self.settings_class.setValue('Nodes selected pen type', LineTypes.lDotLine)
        self.settings_class.setValue('Nodes label bg color', Colors.kNodeNameRect)
        self.pb_node_label_bg_color.color = Colors.kNodeNameRect
        self.settings_class.setValue('Nodes label font', QtGui.QFont('Arial'))
        self.settings_class.setValue('Nodes label font color', Colors.kWhite)
        self.settings_class.setValue('Nodes label font size', 8)
        self.settings_class.setValue('Nodes lyt A color', Colors.kPortLinesA)
        self.pb_lyt_a_color.color = Colors.kPortLinesA
        self.settings_class.setValue('Nodes lyt B color', Colors.kPortLinesB)
        self.pb_lyt_b_color.color = Colors.kPortLinesB
        self.settings_class.setValue('Port color', Colors.kConnectors)
        self.pb_port_color.color = Colors.kConnectors
        self.settings_class.setValue('Port dirty color', Colors.kDirtyPen)
        self.pb_port_dirty_pen_color.color = Colors.kDirtyPen
        self.settings_class.setValue('Port dirty type', LineTypes.lDotLine)
        self.settings_class.setValue('Port label color', Colors.kPortNameColor)
        self.pb_port_label_color.color = Colors.kPortNameColor
        self.settings_class.setValue('Port label font', QtGui.QFont('Arial'))
        self.settings_class.setValue('Port label size', 8)
        self.settings_class.endGroup()
        self.settings_class.beginGroup('SCENE')
        self.settings_class.setValue('Scene bg color', Colors.kSceneBackground)
        self.pb_scene_bg_color.color = Colors.kSceneBackground
        self.settings_class.setValue('Grid color', Colors.kGridColor)
        self.pb_grid_color.color = Colors.kGridColor
        self.settings_class.setValue('Grid lines type', LineTypes.lDotLine)
        self.settings_class.setValue('Edge color', Colors.kConnectionLines)
        self.pb_edge_color.color = Colors.kConnectionLines
        self.settings_class.setValue('Edge pen type', LineTypes.lSolidLine)
        self.settings_class.setValue('Edge line thickness', 1.0)
        self.settings_class.endGroup()


class GraphWidget(QtGui.QGraphicsView, Colors, AGraph):

    def __init__(self, name, parent=None):
        super(GraphWidget, self).__init__()
        AGraph.__init__(self, name)
        self.parent = parent
        self.menu = QtGui.QMenu(self)
        self.node_box = NodesBox(self)
        self.scene_widget = SceneClass(self)
        self.add_actions()
        self.options_widget = OptionsClass()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pressed_item = None
        self.released_item = None
        self.groupers = []
        self.reroutes = []
        self._isPanning = False
        self._mousePressed = False
        self._shadows = False
        self.scale(1.5, 1.5)
        self.minimum_scale = 0.5
        self.maximum_scale = 3
        self.setViewportUpdateMode(self.FullViewportUpdate)
        self.setScene(self.scene_widget)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setAcceptDrops(True)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.scene_widget.setSceneRect(QtCore.QRect(0, 0, 10000, 10000))
        self._grid_spacing = 50
        self.factor = 1
        self.factor_diff = 0
        self.scale(self.factor, self.factor)
        self.setWindowTitle(self.tr(name))

        self._current_file_name = 'Untitled'
        self._file_name_label = QtGui.QGraphicsTextItem()
        self._file_name_label.setZValue(5)
        self._file_name_label.setEnabled(False)
        self._file_name_label.setFlag(QtGui.QGraphicsTextItem.ItemIgnoresTransformations)
        self._file_name_label.setDefaultTextColor(self.kWhite)
        self._file_name_label.setPlainText(self._current_file_name)
        self.scene_widget.addItem(self._file_name_label)
        self.rubber_rect = RubberRect('RubberRect')

        self.real_time_line = QtGui.QGraphicsPathItem(None, self.scene())
        self.real_time_line.name = 'RealTimeLine'
        self.real_time_line.object_type = AGObjectTypes.tConnectionLine
        self.real_time_line.setPen(QtGui.QPen(self.kGreen, 1.0, QtCore.Qt.DashLine))
        self.cursor_pressed_pos = QtCore.QPoint(0, 0)
        self.current_cursor_pose = QtCore.QPoint(0, 0)
        self._right_button = False
        self._is_rubber_band_selection = False
        self._draw_real_time_line = False
        self._update_items = False
        self._resize_group_mode = False
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().maximum()/2)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum()/2)
        self._tick_functions = []
        self.registeredCommands = {}
        self.registerCommands()
        self._sortcuts_enabled = True
        self.tick_timer = QtCore.QTimer() # this timer executes all functions in '_tick_functions'
        self.tick_timer.timeout.connect(self._tick_executor)
        self.tick_timer.start(50)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.grid_size = 10
        self.current_rounded_pos = QtCore.QPointF(0.0, 0.0)

        if (path.isfile(_mod_folder+'resources/sounds/startup.wav') and platform.system() == "Windows"):
            GraphWidget.play_sound_win(_mod_folder+'resources/sounds/startup.wav')

    def set_scrollbars_positions(self, horizontal, vertical):
        try:
            self.horizontalScrollBar().setValue(horizontal)
            self.verticalScrollBar().setValue(vertical)
        except Exception as e:
            print(e)
            self.write_to_console(e, True)

    def OnDoubleClick(self, pos):
        if self.pressed_item:
            if isinstance(self.pressed_item, Edge):
                # store neighbors
                src = self.pressed_item.source_pos_object
                dst = self.pressed_item.destination_pos_object
                # create rerout node
                node = self.create_node("Reroute", pos.x(), pos.y() - 5.0, "Reroute")
                # kill pressed edge
                self.pressed_item.kill()
                # reconnect neighbors
                self.add_edge(src, node.inp0)
                self.add_edge(node.out0, dst)


    def redraw_nodes(self):
        for n in self.nodes:
            n.update_ports()

    def __del__(self):
        self.tick_timer.stop()

    @staticmethod
    def play_sound_win(file_name):
        t = Thread(target=lambda: winsound.PlaySound(file_name, winsound.SND_FILENAME))
        t.start()

    def _tick_executor(self):
        for foo in self._tick_functions:
            foo()

    def notify(self, message, duration):
        self.parent.statusBar.showMessage(message, duration)
        self.write_to_console(message)

    def registerCommands(self):

        for d in listdir(Commands.__path__[0]):
            if d.endswith(".py") and "__init__" not in d:
                cmd = import_by_name(Commands, d.split(".")[0])
                if cmd:
                    cmd = cmd(self)
                    self.registeredCommands[cmd.__class__.__name__] = cmd
                else:
                    print "command not imported", d.split(".")[0]

    def screen_shot(self):

        name_filter = "Image (*.png)"
        fName = QtGui.QFileDialog.getSaveFileName(filter=name_filter)
        if not fName[0] == '':
            self.write_to_console("save screen to {0}".format(fName[0]))
            img = QtGui.QPixmap.grabWidget(self)
            img.save(fName[0], quality = 100)

    def is_sortcuts_enabled(self):
        return self._sortcuts_enabled

    def disable_sortcuts(self):
        self._sortcuts_enabled = False

    def enable_sortcuts(self):
        self._sortcuts_enabled = True

    def get_nodes(self):

        ls = []
        for i in self.scene_widget.items():
            if hasattr(i, 'object_type'):
                if i.object_type == AGObjectTypes.tNode:
                    if i.isVisible():
                        ls.append(i)
        return ls

    def findPort(self, port_name):
        node = self.get_node_by_name(port_name.split(".")[0])
        if node:
            attr = node.get_port_by_name(port_name.split(".")[1])
            return attr
        return None

    def get_settings(self):
        if path.isfile(self.options_widget.settings_path):
            settings = QtCore.QSettings(self.options_widget.settings_path, QtCore.QSettings.IniFormat)
            return settings

    def add_actions(self):
        save_action = QtGui.QAction(self)
        save_action.setText('Save')
        if path.isfile(_mod_folder+'resources/save_icon.png'):
            save_action.setIcon(QtGui.QIcon(_mod_folder+'resources/save_icon.png'))
        else:
            save_action.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton))
        save_action.triggered.connect(self.save)

        load_action = QtGui.QAction(self)
        load_action.setText('Load')
        if path.isfile(_mod_folder+'resources/folder_open_icon.png'):
            load_action.setIcon(QtGui.QIcon(_mod_folder+'resources/folder_open_icon.png'))
        else:
            load_action.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton))
        load_action.triggered.connect(self.load)

        save_as_action = QtGui.QAction(self)
        save_as_action.setText('Save as')
        if path.isfile(_mod_folder+'resources/save_as_icon.png'):
            save_as_action.setIcon(QtGui.QIcon(_mod_folder+'resources/save_as_icon.png'))
        else:
            save_as_action.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton))
        save_as_action.triggered.connect(lambda: self.save(True))

        options_action = QtGui.QAction(self)
        options_action.setText('Options')
        if path.isfile(_mod_folder+'resources/colors_icon.png'):
            options_action.setIcon(QtGui.QIcon(_mod_folder+'resources/colors_icon.png'))
        else:
            options_action.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton))
        options_action.triggered.connect(self.options)

        new_file_action = QtGui.QAction(self)
        new_file_action.setText('New')
        if path.isfile(_mod_folder+'resources/new_file_icon.png'):
            new_file_action.setIcon(QtGui.QIcon(_mod_folder+'resources/new_file_icon.png'))
        else:
            new_file_action.setIcon(self.style().standardIcon(QtGui.QStyle.SP_FileDialogNewFolder))
        new_file_action.triggered.connect(self.new_file)

        node_box_action = QtGui.QAction(self)
        node_box_action.setText('Node box')
        if path.isfile(_mod_folder+'resources/node_box_icon.png'):
            node_box_action.setIcon(QtGui.QIcon(_mod_folder+'resources/node_box_icon.png'))
        else:
            node_box_action.setIcon(self.style().standardIcon(QtGui.QStyle.SP_FileDialogNewFolder))
        node_box_action.triggered.connect(self.node_box.set_visible)

        separator = QtGui.QAction(self)
        separator.setSeparator(True)

        self.menu.addAction(new_file_action)
        self.menu.addAction(load_action)
        self.menu.addAction(save_action)
        self.menu.addAction(save_as_action)
        self.menu.addAction(separator)
        self.menu.addAction(options_action)
        self.menu.addAction(node_box_action)

    def save(self, save_as=False):

        if save_as:
            name_filter = "Graph files (*.graph)"
            pth = QtGui.QFileDialog.getSaveFileName(filter=name_filter)
            if not pth[0] == '':
                self._current_file_name = pth[0]
            else:
                self._current_file_name = "Untitled"
        else:
            if not path.isfile(self._current_file_name):
                name_filter = "Graph files (*.graph)"
                pth = QtGui.QFileDialog.getSaveFileName(filter=name_filter)
                if not pth[0] == '':
                    self._current_file_name = pth[0]
                else:
                    self._current_file_name = "Untitled"

        if self._current_file_name in ["", "Untitled"]:
            return

        graph = "SAVE GRAPH SCRIPT\n"   #  add some scene info. version, user, date, etc.
        # slider positions
        graph += "setHorizontalScrollBar ~h {0}\n".format(self.horizontalScrollBar().value())
        graph += "setVerticalScrollBar ~v {0}\n".format(self.verticalScrollBar().value())
        # tools visibility
        graph += "setNodeBoxVisible ~v {0}\n".format(int(self.parent.dockWidgetNodeBox.isVisible()))
        graph += "setConsoleVisible ~v {0}\n".format(int(self.parent.dockWidgetConsole.isVisible()))
        graph += "setPropertiesVisible ~v {0}\n".format(int(self.parent.dockWidgetNodeView.isVisible()))
        graph += "enableShadows ~state {0}\n".format(int(self._shadows))
        # create all nodes and set attributes
        for n in self.get_nodes():
            # process nodes with customized behavior
            line = n.save_command()
            graph += line
            for inp in n.inputs:
                line = "setAttr {2}an {0} {2}v {1}\n".format(inp.port_name(), inp.current_data(), FLAG_SYMBOL)
                graph += line
            for out in n.outputs:
                line = "setAttr {2}an {0} {2}v {1}\n".format(out.port_name(), out.current_data(), FLAG_SYMBOL)
                graph += line
            # connect all attributes
        for e in self.edges:
            port_names = e.__str__().split(" >>> ")
            line = "connectAttr {2}src {0} {2}dst {1}\n".format(port_names[0], port_names[1], FLAG_SYMBOL)
            graph += line

            # comment nodes
        for c in self.groupers:
            nodes = ""
            for n in c.nodes:
                nodes += "{0} ".format(n.name)
            line = "comment {2}mode names {2}text {0} {2}nl {1}\n".format(c.label.toHtml().replace("\n", ""), nodes, FLAG_SYMBOL)
            graph += line
        self.write_to_console(graph)

        if not self._current_file_name == '':
            with open(self._current_file_name, 'wb') as f:
                f.write(graph)
            self._file_name_label.setPlainText(self._current_file_name)
            if self.parent:
                self.parent.console.append(str("// saved: '{0}'".format(self._current_file_name)))

    def save_as(self):

        self.save(True)

    def new_file(self):

        self._current_file_name = 'Untitled'
        self._file_name_label.setPlainText('Untitled')
        for n in self.nodes:
            n.kill(False)
        for g in self.groupers:
            g.delete()
        if len(self.nodes) > 0:
            self.new_file()

    def load(self):

        name_filter = "Graph files (*.graph)"
        fpath = QtGui.QFileDialog.getOpenFileName(filter=name_filter, dir="./Examples")
        if not fpath[0] == '':
            with open(fpath[0], 'r') as f:
                data = f.readlines()
            self.new_file()
            for l in data[1:]:
                cmd = l.replace("\n", "")
                self.executeCommand(cmd)
        self._current_file_name = fpath[0]
        self._file_name_label.setPlainText(self._current_file_name)

    def get_port_by_full_name(self, full_name):

        node_name = full_name.split('.')[0]
        port_name = full_name.split('.')[1]
        node = self.get_node_by_name(node_name)
        if node:
            port = node.get_port_by_name(port_name)
            if port:
                return port

    def options(self):

        print 'show options'
        self.options_widget.show()

    def contextMenuEvent(self, event):

        if not self.pressed_item:
            self.menu.exec_(event.globalPos())
        super(GraphWidget, self).contextMenuEvent(event)

    def set_shadows_enabled(self, state):

        for n in self.nodes:
            n.set_shadows_enabled(state)
        self._shadows = state

    def frame(self):

        polygon = self.mapToScene(self.viewport().rect())
        rect = QtCore.QRectF(polygon[0], polygon[2])
        mid_points = []
        for n in self.nodes:
            n_rect = QtCore.QRectF(n.scenePos(),
                                   QtCore.QPointF(n.scenePos().x()+float(n.w),
                                                  n.scenePos().y()+float(n.h)))
            mid_points.append(((n_rect.center().x()), n_rect.center().y()))
        mp = get_mid_point(mid_points)
        if len(mp) == 0:
            return
        nodes_rect = self.get_nodes_rect()
        if not rect.contains(nodes_rect):
            by_x = mp[0]/self.sceneRect().width()
            by_y = mp[1]/self.sceneRect().height()
            self.horizontalScrollBar().setValue(float(self.horizontalScrollBar().maximum()*by_x))
            self.verticalScrollBar().setValue(float(self.verticalScrollBar().maximum()*by_y))

    def get_nodes_rect(self, selected=False):

        rectangles = []
        if selected:
            for n in [n for n in self.nodes if n.isSelected()]:
                n_rect = QtCore.QRectF(n.scenePos(),
                                       QtCore.QPointF(n.scenePos().x()+float(n.w),
                                                      n.scenePos().y()+float(n.h)))
                rectangles.append([n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])
        else:
            for n in self.nodes:
                n_rect = QtCore.QRectF(n.scenePos(),
                                       QtCore.QPointF(n.scenePos().x()+float(n.w),
                                                      n.scenePos().y()+float(n.h)))
                rectangles.append([n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])
        min_x = min([i[0] for i in rectangles])
        max_x = max([i[2] for i in rectangles])
        min_y = min([i[1] for i in rectangles])
        max_y = max([i[3] for i in rectangles])

        return QtCore.QRect(QtCore.QPoint(min_x, min_y), QtCore.QPoint(max_x, max_y))

    def selected_nodes(self):
        return [i for i in self.nodes if i.isSelected()]

    def kill_selected_nodes(self, call_connection_functions=False):

        selected = self.selected_nodes()
        for i in self.nodes:
            if i.isSelected() and i in self.nodes and i in self.scene().items():
                i.kill(call_connection_functions)
        if not len(selected) == 0:
            self.kill_selected_nodes(call_connection_functions)

        clearLayout(self.parent.PropertiesformLayout)

    def keyPressEvent(self, event):

        if not self.is_sortcuts_enabled():
            QtGui.QGraphicsView.keyPressEvent(self, event)
            return

        modifiers = event.modifiers()
        if all([event.key() == QtCore.Qt.Key_N, modifiers == QtCore.Qt.ControlModifier]):
            self.new_file()
        if all([event.key() == QtCore.Qt.Key_Equal, modifiers == QtCore.Qt.ControlModifier]):
            self.scale_step(True, 1.1)
        if all([event.key() == QtCore.Qt.Key_Minus, modifiers == QtCore.Qt.ControlModifier]):
            self.scale_step(False, 0.9)
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
        if all([event.key() == QtCore.Qt.Key_C, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier | QtCore.Qt.AltModifier]):
            self.commentSelectedNodes()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier | QtCore.Qt.AltModifier]):
            self.set_shadows_enabled(not self._shadows)
        if all([event.key() == QtCore.Qt.Key_M, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier]):
            self.parent.toggle_multithreaded()
        if all([event.key() == QtCore.Qt.Key_A, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.align_selected_nodes(True)
        if all([event.key() == QtCore.Qt.Key_Q, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.align_selected_nodes(False)
        if all([event.key() == QtCore.Qt.Key_D, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier]):
            self.parent.toggle_debug()
        if all([event.key() == QtCore.Qt.Key_C, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.parent.toggle_console()
        if all([event.key() == QtCore.Qt.Key_P, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.parent.toggle_property_view()
        if event.key() == QtCore.Qt.Key_Delete:
            self.kill_selected_nodes(False)
        if self.node_box.listWidget._events:
            if event.key() == QtCore.Qt.Key_Tab:
                self.node_box.set_visible()
        if all([event.key() == QtCore.Qt.Key_W, modifiers == QtCore.Qt.ControlModifier]):
            self.duplicate_node()
        QtGui.QGraphicsView.keyPressEvent(self, event)

    def duplicate_node(self):
        new_nodes = []
        for n in [i for i in self.nodes if i.isSelected()]:
            new_nodes.append(n.clone())
            n.setSelected(False)
        for n in new_nodes:
            n.setSelected(True)


    def align_selected_nodes(self, direction):
        scene_poses = []
        relative_poses = []
        scene_nodes_selected = [n for n in self.nodes if n.isSelected() and not isinstance(n.parentItem(), CommentNode)]
        commented_nodes = [n for n in self.nodes if n.isSelected() and isinstance(n.parentItem(), CommentNode)]

        x_min = min(([p.scenePos().x() for p in scene_nodes_selected]))
        y_min = min(([p.scenePos().y() for p in scene_nodes_selected]))

        for n in scene_nodes_selected:
            if direction:
                n.setX(x_min)
            else:
                n.setY(y_min)



    def findGoodPlaceForNewNode(self):
        polygon = self.mapToScene(self.viewport().rect())
        ls = polygon.toList()
        point = QtCore.QPointF((ls[1].x() - ls[0].x())/2, (ls[3].y() - ls[2].y())/2)
        point += ls[0]
        point.setY(point.y()+polygon.boundingRect().height()/3)
        point += QtCore.QPointF(float(random.randint(50, 200)), float(random.randint(50, 200)))
        return point


    def keyReleaseEvent(self, event):

        QtGui.QGraphicsView.keyReleaseEvent(self, event)

    def mousePressEvent(self, event):

        modifiers = event.modifiers()
        self.pressed_item = self.itemAt(event.pos())
        if self.pressed_item and hasattr(self.pressed_item, 'mark'):
            self._resize_group_mode = True
            self.pressed_item.parentItem().setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        if not self.pressed_item:
            self.node_box.close()
            self.node_box.le_nodes.clear()
        if self.pressed_item:
            if hasattr(self.pressed_item, 'object_type') and not hasattr(self.pressed_item, 'non_selectable'):
                if self.pressed_item.object_type == AGObjectTypes.tPort:
                    self.pressed_item.parent.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
            else:
                self.pressed_item.setSelected(True)
        self.cursor_pressed_pos = self.mapToScene(event.pos())
        if self.pressed_item and event.button() == QtCore.Qt.LeftButton:
            if hasattr(self.pressed_item, 'object_type'):
                if self.pressed_item.object_type == AGObjectTypes.tPort:
                    self.pressed_item.parent.setSelected(False)
                    self._draw_real_time_line = True
        if event.button() == QtCore.Qt.RightButton:
            self._right_button = True
        if all([event.button() == QtCore.Qt.LeftButton, modifiers == QtCore.Qt.AltModifier]):
            self.setDragMode(self.ScrollHandDrag)
        if all([event.button() == QtCore.Qt.LeftButton,
                modifiers == QtCore.Qt.NoModifier or modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            if not self.pressed_item or hasattr(self.pressed_item, 'non_selectable'):
                self._is_rubber_band_selection = True
        super(GraphWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.current_cursor_pose = self.mapToScene(event.pos())

        if self._resize_group_mode:
            grp = self.pressed_item.parentItem()
            self.viewport().setCursor(QtCore.Qt.SizeFDiagCursor)
            x = max([self.current_cursor_pose.x()-grp.pos().x(),
                     grp.rect().topLeft().x()+grp.minimum_width])
            y = max([self.current_cursor_pose.y()-grp.pos().y(),
                     grp.rect().topLeft().y()+grp.minimum_height])

            r = QtCore.QRectF(grp.rect().topLeft(), QtCore.QPointF(x, y))
            grp.setRect(r.normalized())
            grp.resize_item.setPos(grp.rect().bottomRight()-QtCore.QPointF(grp.resize_item.boundingRect().width(),
                                                                           grp.resize_item.boundingRect().height()))

        if self._draw_real_time_line:
            if self.pressed_item.parent.isSelected():
                self.pressed_item.parent.setSelected(False)
            if self.real_time_line not in self.scene().items():
                self.scene().addItem(self.real_time_line)

            p1 = self.pressed_item.scenePos() + QtCore.QPointF(self.pressed_item.boundingRect().width()/2, self.pressed_item.boundingRect().height()/2)
            p2 = self.current_cursor_pose

            distance = p2.x() - p1.x()
            multiply = 3
            path = QtGui.QPainterPath()
            path.moveTo(p1)
            path.cubicTo(QtCore.QPoint(p1.x()+distance/multiply, p1.y()), QtCore.QPoint(p2.x()-distance/2, p2.y()), p2)
            self.real_time_line.setPath(path)

        if self._is_rubber_band_selection:
            if self.rubber_rect not in self.scene().items():
                self.scene().addItem(self.rubber_rect)
            if not self.rubber_rect.isVisible():
                self.rubber_rect.setVisible(True)
            r = QtCore.QRectF(self.cursor_pressed_pos.x(),
                              self.cursor_pressed_pos.y(),
                              self.current_cursor_pose.x()-self.cursor_pressed_pos.x(),
                              self.current_cursor_pose.y()-self.cursor_pressed_pos.y())
            self.rubber_rect.setRect(r.normalized())
        super(GraphWidget, self).mouseMoveEvent(event)

    def createComment(self, x1, y1, x2, y2, name):

        grp = CommentNode(self)
        self.groupers.append(grp)
        self.scene_widget.addItem(grp)
        grp.setPos(QtCore.QPoint(int(x1), int(y1)))
        grp.set_bottom_right(QtCore.QPoint(int(x2), int(y2)))
        grp.label.setHtml(name)
        # grp.label.setPlainText(name)

    def commentSelectedNodes(self, comment = "enter comment"):
        selected_nodes = []
        for n in self.get_nodes():
            if n.isSelected():
                selected_nodes.append(n.name)
        if len(selected_nodes) == 0:
            self.createComment(self.current_cursor_pose.x(), self.current_cursor_pose.y(), self.current_cursor_pose.x()+250, self.current_cursor_pose.y()+100, comment)
            return

        r = self.get_nodes_rect(True)
        grp = CommentNode(self)
        grp.label.setHtml(comment)
        # grp.label.setPlainText(comment)
        self.groupers.append(grp)
        grp.setRect(r.x() - (r.topLeft().x()+50),
                    r.y() - (r.topLeft().y()+50),
                    r.width() + 150,
                    r.height() + 150)
        grp.update()
        grp.setPos(r.topLeft())
        self.scene_widget.addItem(grp)
        selected_nodes = []
        for n in self.get_nodes():
            if n.isSelected():
                if n in self.nodes and not n.parentItem():
                    n.setSelected(False)
                    grp.add_node(n)
                    selected_nodes.append(n.name)
        grp.fit_content()
        # print console command
        cmd = "comment"
        for i in selected_nodes:
            cmd += " " + i
        self.write_to_console(cmd)

    def remove_item_by_name(self, name):

        [self.scene_widget.removeItem(i) for i in self.scene().items() if hasattr(i, 'name') and i.name == name]

    def mouseReleaseEvent(self, event):

        self.released_item = self.itemAt(event.pos())
        self.setDragMode(self.NoDrag)
        self._resize_group_mode = False
        self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        modifiers = event.modifiers()
        if self.released_item and not hasattr(self.released_item, 'non_selectable'):
            if isinstance(self.released_item, CommentNode):
                # self.released_item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
                pass
        else:
            if self.pressed_item and not hasattr(self.pressed_item, 'non_selectable'):
                parent = self.pressed_item.parentItem()
                # if parent and hasattr(parent, 'object_type'):
                #     if parent.object_type == AGObjectTypes.tGrouper:
                #         parent.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

        for n in self.nodes:
            n.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

        if event.button() == QtCore.Qt.RightButton:
            self._right_button = False
        if self._draw_real_time_line:
            self._draw_real_time_line = False
            if self.real_time_line in self.scene().items():
                self.remove_item_by_name('RealTimeLine')
        if self._is_rubber_band_selection:
            self._is_rubber_band_selection = False
            [i.setSelected(True) for i in self.rubber_rect.collidingItems()]
            self.remove_item_by_name(self.rubber_rect.name)
        if event.button() == QtCore.Qt.RightButton:
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
            if not i.object_type == AGObjectTypes.tPort:
                do_connect = False
                break
        if p_itm and r_itm:
            if hasattr(p_itm, 'object_type') and hasattr(r_itm, 'object_type'):
                if all([p_itm.object_type == AGObjectTypes.tPort, r_itm.object_type == AGObjectTypes.tPort]):
                    if cycle_check(p_itm, r_itm):
                        self.write_to_console('cycles are not allowed')
                        do_connect = False

        if do_connect:
            self.add_edge(p_itm, r_itm)
        selected_nodes = self.selected_nodes()
        if len(selected_nodes) != 0:
            self.update_property_view(selected_nodes[0])
        else:
            clearLayout(self.parent.PropertiesformLayout)

        super(GraphWidget, self).mouseReleaseEvent(event)

    def update_property_view(self, node):
        root = self.parent.dockWidgetNodeView
        layout = self.parent.PropertiesformLayout
        root.owned_node = node
        clearLayout(layout)

        # label
        le_name = QtGui.QLineEdit(node.get_name())
        le_name.returnPressed.connect(lambda: node.set_name(le_name.text()))
        layout.addRow("Name", le_name)

        # pos
        le_pos = QtGui.QLineEdit("{0} x {1}".format(node.pos().x(), node.pos().y()))
        layout.addRow("Pos", le_pos)

        # inputs
        if len(node.inputs) != 0:
            sep_inputs = QtGui.QLabel()
            sep_inputs.setStyleSheet("background-color: black;")
            sep_inputs.setText("INPUTS")
            layout.addRow("", sep_inputs)

            def tmp(le):
                print(le.text())

            for inp in node.inputs:
                le = QtGui.QLineEdit(str(inp.current_data()))
                layout.addRow(inp.name, le)
                le.setReadOnly(True)

        # outputs
        if len(node.outputs) != 0:
            sep_outputs = QtGui.QLabel()
            sep_outputs.setStyleSheet("background-color: black;")
            sep_outputs.setText("OUTPUTS")
            layout.addRow("", sep_outputs)
            for out in node.outputs:
                le = QtGui.QLineEdit(str(out.current_data()))
                le.setReadOnly(True)
                layout.addRow(out.name, le)

        doc_lb = QtGui.QLabel()
        doc_lb.setStyleSheet("background-color: black;")
        doc_lb.setText("Description")
        layout.addRow("", doc_lb)
        doc = QtGui.QLabel(node.description())
        doc.setWordWrap(True)
        layout.addRow("", doc)

    def wheelEvent(self, event):

        self.scale_view(math.pow(2.0, event.delta() / 240.0))

    def drawBackground(self, painter, rect):
        super(GraphWidget, self).drawBackground(painter, rect)

        polygon = self.mapToScene(self.viewport().rect())
        self._file_name_label.setPos(polygon[0])
        scene_rect = self.sceneRect()
        # Fill
        settings = self.get_settings()
        if settings:
            color = QtGui.QColor(settings.value('SCENE/Scene bg color'))
        else:
            color = self.kSceneBackground
        painter.fillRect(rect.intersect(scene_rect), QtGui.QBrush(color))

        left = int(scene_rect.left()) - (int(scene_rect.left()) % self.grid_size)
        top = int(scene_rect.top()) - (int(scene_rect.top()) % self.grid_size)

        painter.setPen(QtGui.QPen(self.kGridColor, 0.5, QtCore.Qt.SolidLine))

        # draw grid vertical lines
        for x in xrange(left, int(scene_rect.right()), self.grid_size): 
            painter.drawLine(x, scene_rect.top(), x, scene_rect.bottom())

        # draw grid horizontal lines
        for y in xrange(top, int(scene_rect.bottom()), self.grid_size):
            painter.drawLine(scene_rect.left(), y, scene_rect.right(), y)

        painter.setPen(QtGui.QPen(self.kGridColorDarker, 1.0, QtCore.Qt.SolidLine))

        # draw grid vertical lines
        for x in xrange(left, int(scene_rect.right()), self.grid_size*10):
            painter.drawLine(x, scene_rect.top(), x, scene_rect.bottom())

        # draw grid horizontal lines
        for y in xrange(top, int(scene_rect.bottom()), self.grid_size*10):
            painter.drawLine(scene_rect.left(), y, scene_rect.right(), y)

    def console_help(self):

        msg = """///// AVAILABLE NODES LIST /////\n\n"""

        for f in listdir(path.dirname(Nodes.__file__)):
            if f.endswith(".py") and "init" not in f:
                msg += "{0}\n".format(f.split(".")[0])

        msg += "\n"

        msg += """///// AVAILABLE COMMANDS /////\n"""
        msg += "\t<<< Builtin >>>\n"
        for c in self.parent.consoleInput.builtinCommands:
            msg += (c+"\n")
        msg += "\t<<< Plugins >>>\n"
        for c in self.registeredCommands:
            msg += (c+" - {0}\n".format(self.registeredCommands[c].usage()))

        if self.parent:
            self.parent.console.append(msg)

    def create_node(self, className, x, y, name):

        node_class = get_node(Nodes, className, self)
        node_class.set_name(name)
        self.add_node(node_class, x, y)
        return node_class

    def executeCommand(self, command):

        commandLine = parse(command)

        # execute custom command
        if not commandLine["cmd"] in self.parent.consoleInput.builtinCommands:

            cmdObject = None
            try:
                cmdObject = self.registeredCommands[commandLine['cmd']]
            except:
                self.parent.console.append("[ERROR] command '{0}' not found".format(commandLine['cmd']))
                return

            try:
                args = command.split(" ", 1)
                if len(args) == 1:
                    args = None
                else:
                    args = args[1]
                self.parent.console.append(command)
                cmdObject.execute(args)
            except:
                self.parent.console.append(cmdObject.usage())
                return
            return

        # execute builtins

        if commandLine['cmd'] == "renameNode":
            self.parent.console.append(command)
            try:
                node = self.get_node_by_name(commandLine["flags"]["{0}name".format(FLAG_SYMBOL)])
                if node:
                    newName = self.get_uniq_node_name(commandLine["flags"]["{0}newName".format(FLAG_SYMBOL)])
                    node.set_name(newName)
                return
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE] renameNode {0}name str {0}newName str".format(FLAG_SYMBOL))
            return

        if commandLine['cmd'] == "plot":
            self.parent.console.append(command)
            self.plot()
            return

        if commandLine['cmd'] == "load":
            self.parent.console.append(command)
            self.load()
            return

        if commandLine['cmd'] == "save":
            self.parent.console.append(command)
            self.save()
            return

        if commandLine['cmd'] == "setScrollbars":
            try:
                self.parent.console.append(command)
                h = commandLine['flags']['~h']
                v = commandLine['flags']['~v']
                self.set_scrollbars_positions(int(h), int(v))
            except Exception as e:
                print(e)
                self.write_to_console(e, True)
                self.write_to_console("[USAGE] setScrollbars ~h int ~v int")
                return

        if commandLine['cmd'] == "setHorizontalScrollBar":
            try:
                self.parent.console.append(command)
                h = commandLine['flags']['~h']
                self.set_scrollbars_positions(int(h), self.verticalScrollBar().value())
            except Exception as e:
                print(e)
                self.write_to_console(e, True)
                self.write_to_console("[USAGE] setHorizontalScrollBar ~h int")
                return

        if commandLine['cmd'] == "setVerticalScrollBar":
            try:
                self.parent.console.append(command)
                v = commandLine['flags']['~v']
                self.set_scrollbars_positions(self.horizontalScrollBar().value(), int(v))
            except Exception as e:
                print(e)
                self.write_to_console(e, True)
                self.write_to_console("[USAGE] setVerticalScrollBar ~v int")
                return

        if commandLine['cmd'] == "setConsoleVisible":
            try:
                self.parent.console.append(command)
                v = commandLine['flags']['~v']
                if int(v) == 1:
                    self.parent.dockWidgetConsole.show()
                else:
                    self.parent.dockWidgetConsole.hide()
            except Exception as e:
                print(e)
                self.write_to_console(e, True)
                self.write_to_console("[USAGE] setConsoleVisible ~v int")
                return

        if commandLine['cmd'] == "setNodeBoxVisible":
            try:
                self.parent.console.append(command)
                v = commandLine['flags']['~v']
                if int(v) == 1:
                    self.parent.dockWidgetNodeBox.show()
                else:
                    self.parent.dockWidgetNodeBox.hide()
            except Exception as e:
                print(e)
                self.write_to_console(e, True)
                self.write_to_console("[USAGE] setNodeBoxVisible ~v int")
                return

        if commandLine['cmd'] == "setPropertiesVisible":
            try:
                self.parent.console.append(command)
                v = commandLine['flags']['~v']
                if int(v) == 1:
                    self.parent.dockWidgetNodeView.show()
                else:
                    self.parent.dockWidgetNodeView.hide()
            except Exception as e:
                print(e)
                self.write_to_console(e, True)
                self.write_to_console("[USAGE] setPropertiesVisible ~v int")
                return

        if commandLine['cmd'] == "createNode":
            try:
                self.parent.console.append(command)
                if commandLine['flags']['~type'] == "MakeArray":
                    mArrayMod = getattr(Nodes, "MakeArray")
                    node_class = mArrayMod(commandLine["flags"]["~n"], self, int(commandLine["flags"]["~count"]))
                    node_class.set_name("MakeArray")
                    self.add_node(node_class, float(commandLine["flags"]["~x"]), float(commandLine["flags"]["~y"]))
                else:
                    self.create_node(commandLine['flags']['~type'], float(commandLine['flags']['~x']), float(commandLine['flags']['~y']), commandLine['flags']['~n'])
                return
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE] createNode {0}type className {0}x float {0}y float {0}n str".format(FLAG_SYMBOL))

        if commandLine['cmd'] == "comment":
            try:
                if commandLine['flags']["{0}mode".format(FLAG_SYMBOL)] == "selected":
                    self.commentSelectedNodes(comment = commandLine['flags']["{0}text".format(FLAG_SYMBOL)])
                if commandLine['flags']["{0}mode".format(FLAG_SYMBOL)] == "empty":
                    try:
                        self.parent.console.append(command)
                        self.createComment(commandLine['flags']["{0}x1".format(FLAG_SYMBOL)], commandLine['flags']["{0}y1".format(FLAG_SYMBOL)], commandLine['flags']["{0}x2".format(FLAG_SYMBOL)], commandLine['flags']["{0}y2".format(FLAG_SYMBOL)], commandLine['flags']["{0}text".format(FLAG_SYMBOL)])
                        return
                    except Exception, e:
                        self.parent.console.append("[ERROR] {0}".format(e))
                    return
                if commandLine['flags']["{0}mode".format(FLAG_SYMBOL)] == "names":
                    for n in self.get_nodes():
                        n.setSelected(False)
                    for i in commandLine["flags"]["{0}nl".format(FLAG_SYMBOL)].split(" "):
                        node = self.get_node_by_name(i)
                        if node:
                            node.setSelected(True)
                    self.commentSelectedNodes(comment = commandLine["flags"]["{0}text".format(FLAG_SYMBOL)])
                    return
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE]>>>\ncomment {0}mode selected {0}text str\ncomment {0}mode names {0}text str {0}nl name1 name2 ...\ncomment {0}mode empty {0}x1 float {0}y1 float {0}x2 float {0}y2 float {0}text str".format(FLAG_SYMBOL))

        if commandLine["cmd"] == "pluginWizard":
            try:
                mode = commandLine["flags"]["{0}mode".format(FLAG_SYMBOL)]
                if mode == "implementNode":
                    _implementPlugin(str(commandLine["flags"]["{0}n".format(FLAG_SYMBOL)]), self.parent.console.append, PluginType.pNode, self)
                if mode == "implementCommand":
                    _implementPlugin(str(commandLine["flags"]["{0}n".format(FLAG_SYMBOL)]), self.parent.console.append, PluginType.pCommand, self)
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE]>>>pluginWizard {0}mode [implementNode|implementCommand] {0}n name".format(FLAG_SYMBOL))

        if commandLine["cmd"] == "killNode":
            try:
                nodeNames = commandLine["flags"]["{0}nl".format(FLAG_SYMBOL)].split(" ")
                for n in nodeNames:
                    node = self.get_node_by_name(n)
                    if node:
                        node.kill()
                    else:
                        self.parent.console.append("[WARNING] node {0} not found".format(n))
                self.parent.console.append(command)
                return
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE] killNode {0}nl nodeName1 nodeName2 ...".format(FLAG_SYMBOL))

        if commandLine["cmd"] == "setAttr":
            try:
                nodeName = commandLine["flags"]["{0}an".format(FLAG_SYMBOL)].split('.')[0]
                attrName = commandLine["flags"]["{0}an".format(FLAG_SYMBOL)].split('.')[1]
                node = self.get_node_by_name(nodeName)
                if node:
                    attr = node.get_port_by_name(attrName)
                    if attr:
                        attr.set_data(commandLine["flags"]["{0}v".format(FLAG_SYMBOL)])
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE] setAttr {0}an nodeName.attrName {0}v value".format(FLAG_SYMBOL))

        if commandLine["cmd"] == "connectAttr":
            try:
                # find ports
                nodeSrcName = commandLine["flags"]["{0}src".format(FLAG_SYMBOL)].split('.')[0]
                portSrcName = commandLine["flags"]["{0}src".format(FLAG_SYMBOL)].split('.')[1]
                nodeDstName = commandLine["flags"]["{0}dst".format(FLAG_SYMBOL)].split('.')[0]
                portDstName = commandLine["flags"]["{0}dst".format(FLAG_SYMBOL)].split('.')[1]

                nodeSrc = self.get_node_by_name(nodeSrcName)
                nodeDst = self.get_node_by_name(nodeDstName)
                if nodeSrc and nodeDst:
                    src = nodeSrc.get_port_by_name(portSrcName)
                    dst = nodeDst.get_port_by_name(portDstName)
                    if src and dst:
                        self.add_edge(src, dst)
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE] connectAttr {0}src nodeName.srcAttrName {0}dst nodeName.dstAttrName".format(FLAG_SYMBOL))

        if commandLine["cmd"] == "disconnectAttr":
            try:
                nodeName = commandLine["flags"]["{0}an".format(FLAG_SYMBOL)].split('.')[0]
                attrName = commandLine["flags"]["{0}an".format(FLAG_SYMBOL)].split('.')[1]
                node = self.get_node_by_name(nodeName)
                if node:
                    attr = node.get_port_by_name(attrName)
                    if attr:
                        attr.disconnect_all()
                        self.parent.console.append(command)
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE] disconnectAttr {0}an nodeName.attrname".format(FLAG_SYMBOL))

        if commandLine["cmd"] == "select":
            try:
                if commandLine["flags"]["{0}nl".format(FLAG_SYMBOL)] == "none":
                    for n in self.get_nodes():
                        n.setSelected(False)
                    self.parent.console.append(command)
                else:
                    for i in commandLine["flags"]["{0}nl".format(FLAG_SYMBOL)].split(" "):
                        node = self.get_node_by_name(i)
                        if node:
                            node.setSelected(True)
                    self.parent.console.append(command)
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE]\nselect {0}nl nodeName1 nodeName2 ...\n'select {0}nl none' - to deselect all".format(FLAG_SYMBOL))

        if commandLine["cmd"] == "move":
            try:
                node = self.get_node_by_name(commandLine["flags"]["{0}n".format(FLAG_SYMBOL)])
                if node:
                    node.set_pos(float(commandLine["flags"]["{0}x".format(FLAG_SYMBOL)]), float(commandLine["flags"]["{0}y".format(FLAG_SYMBOL)]))
                    self.parent.console.append(command)
                else:
                    self.parent.console.append("[WARNING] node {0} not found".format(commandLine["flags"]["{0}n".format(FLAG_SYMBOL)]))
            except Exception, e:
                self.parent.console.append("[ERROR] {0}".format(e))
                self.parent.console.append("[USAGE] move {0}n nodeName {0}x float {0}y float".format(FLAG_SYMBOL))

        if commandLine["cmd"] == "help":
            self.parent.console.append(command)
            self.console_help()

    def add_node(self, node, x, y):

        AGraph.add_node(self, node, x, y)
        if node:
            node.label.setPlainText(node.name)
            self.scene_widget.addItem(node)
            node.set_shadows_enabled(self._shadows)
            node.post_create()
        else:
            print '[add_node()] error node creation'

    def add_edge(self, src, dst):

        result = AGraph.add_edge(self, src, dst)
        if result:
            if src.type == AGPortTypes.kInput:
                src, dst = dst, src
            edge = Edge(src, dst, self)
            src.edge_list.append(edge)
            dst.edge_list.append(edge)
            self.scene_widget.addItem(edge)
            self.edges.append(edge)
            self.write_to_console("connectAttr ~src {0} ~dst {1}".format(src.port_name(), dst.port_name()))
            return edge

    def remove_edge(self, edge, call_connection_functions=True):

        AGraph.remove_edge(self, edge, call_connection_functions)
        self.edges.remove(edge)
        edge.prepareGeometryChange()
        self.scene_widget.removeItem(edge)



    def write_to_console(self, data, force=False):
        if not force:
            if not self.is_debug():
                return
        else:
            if self.parent:
                self.parent.console.append(str(data))

    def plot(self):
        AGraph.plot(self)
        self.parent.console.append('>>>>>>> {0} <<<<<<<\n{1}\n'.format(self.name, ctime()))
        if self.parent:
            for n in self.nodes:
                self.parent.console.append(n.name)
                for i in n.inputs+n.outputs:
                    self.parent.console.append('|--- {0} data - {1} affects on {2} affected by {3} DIRTY {4}'.format(i.port_name(),
                                          i.current_data(),
                                          [p.port_name() for p in i.affects],
                                          [p.port_name() for p in i.affected_by],
                                          i.dirty))

    def scale_step(self, direction, step_size):
        current_factor = self.factor

        if direction:
            self.factor += (step_size-1)
            self.factor_diff += self.factor-current_factor
            # if self.factor_diff >= self.maximum_scale:
            #     self.factor_diff = self.maximum_scale-0.01
            #     return
            self.scale(step_size, step_size)
        else:
            self.factor -= (1-step_size)
            self.factor_diff += self.factor-current_factor
            # if self.factor_diff <= self.minimum_scale:
            #     self.factor_diff = self.minimum_scale+0.01
            #     return
            self.scale(step_size, step_size)

    def reset_scale(self):
        self.resetMatrix()

    def scale_view(self, scale_factor):

        self.factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if self.factor < self.minimum_scale or self.factor > self.maximum_scale:
            return
        self.scale(scale_factor, scale_factor)
