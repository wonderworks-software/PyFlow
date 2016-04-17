from PySide import QtCore
from PySide import QtGui
import math
from Settings import Colors
from Settings import LineTypes
from Settings import get_line_type
from AbstractGraph import *
from Edge import Edge
from os import listdir, path
import sys
_file_folder = path.dirname(__file__)
_mod_folder = _file_folder.replace(_file_folder.rsplit('\\')[-1], '')
nodes_path = _mod_folder+'\\Nodes'
if nodes_path not in sys.path:
    sys.path.append(nodes_path)
import Nodes
from time import ctime
import OptionsWindow_ui
import rgba_color_picker_ui
import json


def get_mid_point(args):

    return [sum(i)/len(i) for i in zip(*args)]


class SceneClass(QtGui.QGraphicsScene):
    def __init__(self, parent):
        super(SceneClass, self).__init__(parent)
        self.Type = 'SCENE'
        self.setItemIndexMethod(self.NoIndex)
        self.pressed_port = None

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

    def dropEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            node_name = event.mimeData().text()
            node = self.parent().node_box.get_node(Nodes, node_name)
            self.parent().add_node(node, event.scenePos().x(), event.scenePos().y())
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
            self.parent_item.create_node()
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

    def keyPressEvent(self, event):
        if self._events:
            if event.key() == QtCore.Qt.Key_Escape:
                self.parent.close()
                self.parent.listWidget.clear()
        super(NodeBoxLineEdit, self).keyPressEvent(event)


class NodesBox(QtGui.QWidget):
    def __init__(self, graph):
        super(NodesBox, self).__init__()
        self.graph = graph
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)
        self.setObjectName("nodes_box_form")
        self.setWindowTitle('Node box - {0}'.format(self.graph.name))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(160, 200)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.name = 'NODE_BOX'
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.le_nodes = NodeBoxLineEdit(self)
        self.le_nodes.textChanged.connect(self.le_text_changed)
        self.verticalLayout.addWidget(self.le_nodes)
        self.listWidget = NodesBoxListWidget(self)
        self.verticalLayout.addWidget(self.listWidget)
        self.setVisible(False)
        self.refresh_list('')

    def get_node(self, module, name):

        if hasattr(module, name):
            try:
                mod = getattr(module, name)
                mod = mod(name, self.graph)
                return mod
            except Exception, e:
                print "ERROR node creation!!", e
                return

    def refresh_list(self, pattern):

        self.listWidget.clear()
        words = [i[:-3] for i in listdir(_mod_folder+'\\Nodes') if i.endswith('.py') and '__init__' not in i]
        self.listWidget.addItems([i for i in words if pattern.lower() in i.lower()])
        item = self.listWidget.itemAt(0, 0)
        if item and not item.isSelected():
            item.setSelected(True)

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
            node = self.get_node(Nodes, name)
            print node.name, 'created'
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
        self.setZValue(1)
        self.setPen(QtGui.QPen(self.kRubberRect, 0.5, QtCore.Qt.SolidLine))
        self.setBrush(QtGui.QBrush(self.kRubberRect))


class GroupObjectName(QtGui.QGraphicsTextItem, Colors):
    def __init__(self, parent):
        super(GroupObjectName, self).__init__()
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.parent = parent
        self.setParentItem(parent)
        self.setPlainText('enter comment')
        self.setDefaultTextColor(self.kWhite)
        self.setCursor(QtCore.Qt.IBeamCursor)

    def update_pos(self):

        self.setPos(self.parent.rect().topLeft())
        self.setY(self.parent.rect().topLeft().y() - self.boundingRect().height())

    def focusOutEvent(self, event):

        self.update_pos()
        super(GroupObjectName, self).focusOutEvent(event)

    def paint(self, painter, option, widget):

        painter.fillRect(option.rect, QtGui.QColor(self.kGroupObjectNameBackground))
        super(GroupObjectName, self).paint(painter, option, widget)


class GroupObject(QtGui.QGraphicsRectItem, Colors):
    def __init__(self, graph):
        super(GroupObject, self).__init__()
        self.object_type = AGObjectTypes.tGrouper
        self.graph = graph
        self.nodes = []
        self.menu = QtGui.QMenu()
        self.setAcceptHoverEvents(True)
        self.action_delete = self.menu.addAction('delete')
        self.action_delete.triggered.connect(self.delete)
        self.action_fit = self.menu.addAction('fit contents')
        self.action_fit.triggered.connect(self.fit_content)
        self.setFlag(self.ItemIsMovable)
        self._minimum_width = 50
        self._minimum_height = 50
        self.setZValue(2)
        self.auto_fit_content = False
        self.setPen(QtGui.QPen(self.kGroupObjectPen, 1, QtCore.Qt.SolidLine))
        self.setBrush(QtGui.QBrush(self.kGroupObjectBrush))
        self.label = GroupObjectName(self)
        self.count_label = QtGui.QGraphicsTextItem(parent=self)
        self.count_label.setDefaultTextColor(self.kWhite)
        self.count_label.setFont(QtGui.QFont("Courier New", 8))
        self.count_label.setPlainText(str(len(self.nodes)))
        self.resize_item = QtGui.QGraphicsPolygonItem(parent=self)
        self.resize_item.setCursor(QtCore.Qt.SizeFDiagCursor)
        self.resize_item.setFlag(self.ItemIsMovable, False)
        self.resize_item.mark = 'resize_object'
        self.resize_item.setPolygon(QtGui.QPolygonF([QtCore.QPointF(0.0, 10.0),
                                                     QtCore.QPointF(10.0, 10.0),
                                                     QtCore.QPointF(10.0, 0.0),
                                                     QtCore.QPointF(0.0, 10.0)
                                                     ]))
        self.resize_item.setBrush(self.kGroupObjectResizer)
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
            n_rect = QtCore.QRectF(scene_pos,
                                   QtCore.QPointF(scene_pos.x()+float(n.w),
                                                  scene_pos.y()+float(n.h)
                                                  )
                                   )
            rectangles.append([n_rect.topLeft().x(),
                               n_rect.topLeft().y(),
                               n_rect.bottomRight().x(),
                               n_rect.bottomRight().y()]
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

        self.setBrush(self.kGroupObjectBrush)

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
            self.setFlag(self.ItemIsMovable)

    def get_rect(self):

        print self.rect()

    def mousePressEvent(self, event):

        for i in self.nodes+self.graph.nodes:
            i.setSelected(False)
        super(GroupObject, self).mousePressEvent(event)

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

        print 'save options', self.settings_path
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
        self._isPanning = False
        self._mousePressed = False
        self._shadows = False
        self.scale(1.5, 1.5)
        self.minimum_scale = 0.2
        self.maximum_scale = 5
        self.setViewportUpdateMode(self.FullViewportUpdate)
        self.setScene(self.scene_widget)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setAcceptDrops(True)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.scene_widget.setSceneRect(QtCore.QRect(0, 0, 10000, 10000))
        self._grid_spacing = 50
        # self.draw_grid()
        self.factor = 1
        self.scale(self.factor, self.factor)
        self.setWindowTitle(self.tr(name))

        self._current_file_name = ['Untitled']
        self._file_name_label = QtGui.QGraphicsTextItem()
        self._file_name_label.setZValue(5)
        self._file_name_label.setEnabled(False)
        self._file_name_label.setFlag(QtGui.QGraphicsTextItem.ItemIgnoresTransformations)
        self._file_name_label.setDefaultTextColor(self.kWhite)
        self._file_name_label.setPlainText(self._current_file_name[0])
        self.scene_widget.addItem(self._file_name_label)
        self.rubber_rect = RubberRect('RubberRect')

        self.real_time_line = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.real_time_line.name = 'RealTimeLine'
        self.real_time_line.object_type = AGObjectTypes.tConnectionLine
        self.real_time_line.setPen(QtGui.QPen(self.kWhite,
                                              0.5,
                                              QtCore.Qt.DotLine))
        self.cursor_pressed_pos = QtCore.QPoint(0, 0)
        self.current_cursor_pose = QtCore.QPoint(0, 0)
        self._right_button = False
        self._is_rubber_band_selection = False
        self._draw_real_time_line = False
        self._update_items = False
        self._resize_group_mode = False
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().maximum()/2)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum()/2)

    def get_nodes(self):

        ls = []
        for i in self.scene_widget.items():
            if hasattr(i, 'object_type'):
                if i.object_type == AGObjectTypes.tNode:
                    ls.append(i)
        return ls

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
        if path.isfile(_mod_folder+'resources/options_icon.png'):
            options_action.setIcon(QtGui.QIcon(_mod_folder+'resources/options_icon.png'))
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
                self._current_file_name = pth
        else:
            if not path.isfile(self._current_file_name[0]):
                name_filter = "Graph files (*.graph)"
                self._current_file_name = QtGui.QFileDialog.getSaveFileName(filter=name_filter)

        data = {'edges': [], 'nodes': [], 'groupers': [], 'request_nodes': {}}
        for g in self.groupers:
            data['groupers'].append(
                    {
                        'x': g.scenePos().x(),
                        'y': g.scenePos().y(),
                        'brX': g.rect().width(),
                        'brY': g.rect().height(),
                        'nodes': [i.name for i in g.nodes],
                        'comment': g.label.toPlainText()
                    }
                )
        for n in self.nodes:
            if n.__class__.__name__ == "RequestNode":
                data['request_nodes'][n.name] = {'delta_time': n.spin_box.value(), 'eval_state': n.cb.isChecked()}
            data['nodes'].append(
                {'x': n.pos().x(),
                 'y': n.pos().y(),
                 'node_type': n.__class__.__name__,
                 'ports_data': None,
                 'name': n.name
                }
            )

            ports_data = {'inputs': {}, 'outputs': {}}
            for p in n.inputs:
                ports_data['inputs'][p.name] = p.current_data()
            for p in n.outputs:
                ports_data['outputs'][p.name] = p.current_data()
            for x in data['nodes']:
                if x['name'] == n.name:
                    x['ports_data'] = ports_data
        
        for e in self.edges:
            data['edges'].append({'From': e.source_port_name(), 'To': e.destination_port_name()})

        if not self._current_file_name[0] == '':
            with open(self._current_file_name[0], 'wb') as f:
                json.dump(data, f)
            self._file_name_label.setPlainText(self._current_file_name[0])
            print 'saved', self._current_file_name[0]

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
        fpath = QtGui.QFileDialog.getOpenFileName(filter=name_filter)
        if not fpath[0] == '':
            with open(fpath[0], 'r') as f:
                data = json.load(f)
            self.new_file()
            #create nodes
            for i in data['nodes']:
                node = self.node_box.get_node(Nodes, i['node_type'])
                self.add_node(node, i['x'], i['y'])
                node.set_name(i['name'])
                for p in node.inputs:
                    if p.name in i['ports_data']['inputs']:
                        p.set_data(i['ports_data']['inputs'][p.name])
                for p in node.outputs:
                    if p.name in i['ports_data']['outputs']:
                        p.set_data(i['ports_data']['outputs'][p.name])
                # restore request nodes data
                if node.__class__.__name__ == "RequestNode":
                    if node.name in data['request_nodes']:
                        node.spin_box.setValue(data['request_nodes'][node.name]['delta_time'])
                        state = QtCore.Qt.Unchecked
                        if bool(data['request_nodes'][node.name]['eval_state']) == True:
                            state = QtCore.Qt.Checked
                        node.cb.setCheckState(state)
                    else:
                        print data['request_nodes'][node.name]

            # create edges
            for e in data['edges']:
                src = self.get_port_by_full_name(e['From'])
                dst = self.get_port_by_full_name(e['To'])
                if src and dst:
                    self.add_edge(src, dst)

            #create groupers
            for g in data['groupers']:
                grouper = GroupObject(self)
                grouper.label.setPlainText(g['comment'])
                self.scene_widget.addItem(grouper)
                self.groupers.append(grouper)
                grouper.setPos(QtCore.QPointF(g['x'], g['y']))
                grouper.setRect(grouper.rect().x(), grouper.rect().y(), g['brX'], g['brY'])
                grouper.update()
                for n in g['nodes']:
                    node = self.get_node_by_name(n)
                    grouper.add_node(node)
                    node.setPos(node.pos()+grouper.scenePos())
            self._current_file_name = fpath
            self._file_name_label.setPlainText(fpath[0])

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

        return QtCore.QRectF(QtCore.QPointF(min_x, min_y), QtCore.QPointF(max_x, max_y))

    def kill_selected_nodes(self, call_connection_functions=False):

        selected = [i for i in self.nodes if i.isSelected()]
        for i in self.nodes:
            if i.isSelected() and i in self.nodes and i in self.scene().items():
                i.kill(call_connection_functions)
        if not len(selected) == 0:
            self.kill_selected_nodes(call_connection_functions)

    def keyPressEvent(self, event):

        modifiers = event.modifiers()
        if all([event.key() == QtCore.Qt.Key_N, modifiers == QtCore.Qt.ControlModifier]):
            self.new_file()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier]):
            self.save()
        if all([event.key() == QtCore.Qt.Key_O, modifiers == QtCore.Qt.ControlModifier]):
            self.load()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.save_as()
        if event.key() == QtCore.Qt.Key_F:
            self.frame()
        if event.key() == QtCore.Qt.Key_Delete:
            self.kill_selected_nodes(False)
        if self.node_box.listWidget._events:
            if event.key() == QtCore.Qt.Key_Tab:
                self.node_box.set_visible()
        QtGui.QGraphicsView.keyPressEvent(self, event)

    def keyReleaseEvent(self, event):
        QtGui.QGraphicsView.keyReleaseEvent(self, event)

    def mousePressEvent(self,  event):

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
            self.real_time_line.setLine(self.cursor_pressed_pos.x(),
                                        self.cursor_pressed_pos.y(),
                                        self.current_cursor_pose.x(),
                                        self.current_cursor_pose.y())
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

    def remove_item_by_name(self, name):

        [self.scene_widget.removeItem(i) for i in self.scene().items() if hasattr(i, 'name') and i.name == name]

    def mouseReleaseEvent(self, event):

        self.released_item = self.itemAt(event.pos())
        self.setDragMode(self.NoDrag)
        self._resize_group_mode = False
        self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        modifiers = event.modifiers()
        if self.released_item and not hasattr(self.released_item, 'non_selectable'):
            if isinstance(self.released_item, GroupObject):
                self.released_item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        else:
            if self.pressed_item and not hasattr(self.pressed_item, 'non_selectable'):
                parent = self.pressed_item.parentItem()
                if parent and hasattr(parent, 'object_type'):
                    if parent.object_type == AGObjectTypes.tGrouper:
                        parent.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
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
        if all([event.button() == QtCore.Qt.LeftButton,
                modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            grp = GroupObject(self)
            self.groupers.append(grp)
            grp.setRect(self.rubber_rect.rect().x()-self.cursor_pressed_pos.x(),
                        self.rubber_rect.rect().y()-self.cursor_pressed_pos.y(),
                        self.rubber_rect.rect().width(),
                        self.rubber_rect.rect().height())
            grp.update()
            grp.setPos(self.cursor_pressed_pos)
            self.scene_widget.addItem(grp)
            for n in grp.collidingItems():
                if n in self.nodes and not n.parentItem():
                    n.setSelected(False)
                    grp.add_node(n)
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
                        if self.is_debug():
                            print 'cycles are not allowed'
                        do_connect = False

        if do_connect:
            self.add_edge(p_itm, r_itm)
        super(GraphWidget, self).mouseReleaseEvent(event)

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

        grid_size = int(50)

        left = int(scene_rect.left()) - (int(scene_rect.left()) % grid_size)
        top = int(scene_rect.top()) - (int(scene_rect.top()) % grid_size)

        painter.setPen(QtGui.QPen(self.kGridColor, 0.5, QtCore.Qt.SolidLine))

        # draw grid vertical lines
        for x in xrange(left, int(scene_rect.right()), grid_size):
            painter.drawLine(x, scene_rect.top() ,x, scene_rect.bottom())

        # draw grid horizontal lines
        for y in xrange(top, int(scene_rect.bottom()), grid_size):
            painter.drawLine(scene_rect.left(), y, scene_rect.right(), y)


    def add_node(self, node, x, y):

        AGraph.add_node(self, node)
        if node:
            node.label.setPlainText(node.name)
            self.scene_widget.addItem(node)
            node.setPos(QtCore.QPointF(x, y))
            node.set_shadows_enabled(self._shadows)
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
            return edge

    def remove_edge(self, edge, call_connection_functions=True):

        AGraph.remove_edge(self, edge, call_connection_functions)
        self.edges.remove(edge)
        edge.prepareGeometryChange()
        self.scene_widget.removeItem(edge)

    def write_to_console(self, data):

        if self.parent:
            console = self.parent.console
            console.appendPlainText(str(data))

    def plot(self):
        AGraph.plot(self)
        self.write_to_console('>>>>>>> {0} <<<<<<<\n{1}\n'.format(self.name, ctime()))
        if self.parent:
            for n in self.nodes:
                self.write_to_console(n.name)
                for i in n.inputs+n.outputs:
                    self.write_to_console('|--- {0} data - {1} affects on {2} affected by {3} DIRTY {4}'.format(i.port_name(),
                                          i.current_data(),
                                          [p.port_name() for p in i.affects],
                                          [p.port_name() for p in i.affected_by],
                                          i.dirty))


    def scale_view(self, scale_factor):

        self.factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if self.factor < self.minimum_scale or self.factor > self.maximum_scale:
            return
        self.scale(scale_factor, scale_factor)
