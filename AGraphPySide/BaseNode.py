from Settings import *
from PySide import QtGui
from PySide import QtCore
from Port import Port
from AbstractGraph import *


class NodeName(QtGui.QGraphicsTextItem):

    def __init__(self, name, parent, color=Colors.kNodeNameRect):
        QtGui.QGraphicsTextItem.__init__(self)
        self.Type = 'NODE_NAME'
        self.name = name
        self.color = color
        self.parent = parent
        self.setPlainText(self.name)
        self.setParentItem(parent)
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setPos(self.parent.sizes[0], self.parent.sizes[1]-self.boundingRect().height())

    def keyPressEvent(self, event):
        key = event.key()
        if (key == QtCore.Qt.Key_Return) or (key == QtCore.Qt.Key_Escape):
            self.setEnabled(False)
            self.setEnabled(True)
            return
        else:
            QtGui.QGraphicsTextItem.keyPressEvent(self, event)

    def paint(self, painter, option, widget):
        # paint the background
        painter.fillRect(option.rect, QtGui.QColor(self.color))

        # paint the normal TextItem with the default 'paint' method
        super(NodeName, self).paint(painter, option, widget)

    def focusOutEvent(self, event):
        new_name = self.parent.name = self.toPlainText()
        print 'OLD NAME: ', self.name
        for i in self.parent.get_input_edges().iterkeys():
            if self.name == i.connection['From'].split('.')[0]:
                i.connection['From'] = i.connection['From'].replace(self.name, new_name)
            if self.name == i.connection['To'].split('.')[0]:
                i.connection['To'] = i.connection['To'].replace(self.name, new_name)
        for i in self.parent.get_output_edges().iterkeys():
            if self.name == i.connection['From'].split('.')[0]:
                i.connection['From'] = i.connection['From'].replace(self.name, new_name)
            if self.name == i.connection['To'].split('.')[0]:
                i.connection['To'] = i.connection['To'].replace(self.name, new_name)
        self.name = new_name
        super(NodeName, self).focusOutEvent(event)


class Node(QtGui.QGraphicsItem, AGNode):
    def __init__(self, name, graph, w=120, colors=Colors, spacings=Spacings, port_types=AGPortTypes):
        QtGui.QGraphicsItem.__init__(self)
        AGNode.__init__(self, name, graph)
        self._color_idx = 1
        self.colors = colors
        self.height_offset = 3
        self.spacings = spacings
        self.port_types = port_types
        self.v_form = QtGui.QGraphicsWidget()
        self.w = w
        self.h = 40
        self.sizes = [0, 0, self.w, self.h, 2, 2]
        self.setFlag(self.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        self.setFlag(self.ItemIsSelectable)
        # set node name
        self.label = NodeName(self.name, self)
        # set node layout
        self.v_form.setMaximumWidth(self.boundingRect().width()+self.spacings.kPortOffset)
        self.v_form.setGeometry(QtCore.QRectF(0, 0, self.w+self.spacings.kPortOffset, self.h))
        self.v_form.setParentItem(self)
        self.layout = QtGui.QGraphicsLinearLayout()
        self.layout.setOrientation(QtCore.Qt.Vertical)
        self.layout.setSpacing(self.spacings.kPortSpacing)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.v_form.setLayout(self.layout)
        self.v_form.setX(self.v_form.x()-self.spacings.kPortOffset/2)
        # effect = QtGui.QGraphicsDropShadowEffect()
        # effect.setColor(Colors.kShadow)
        # effect.setParent(self.graph)
        # effect.setBlurRadius(3)
        # effect.setOffset(-30, -20)
        # self.setGraphicsEffect(effect)

    def boundingRect(self):

        pen_width = 1.0
        return QtCore.QRectF(self.sizes[0] - pen_width / 2, self.sizes[1] - pen_width / 2,
                             self.sizes[2] + pen_width, self.v_form.boundingRect().bottomRight().y() + pen_width + self.height_offset)

    def update_ports(self):
        [i.update() for i in self.inputs]
        [i.update() for i in self.outputs]

    def paint(self, painter, option, widget):

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawRoundedRect(self.sizes[0], self.sizes[1],
                                self.sizes[2], self.v_form.boundingRect().bottomRight().y()+self.height_offset,
                                self.sizes[4], self.sizes[5])

        color = self.colors.kNodeBackgrounds
        if self.isSelected():
            color = color.lighter(160)

        painter.setBrush(QtGui.QBrush(color))
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QtGui.QStyle.State_Selected:
            pen.setColor(Colors.kWhite)
            pen.setStyle(QtCore.Qt.DotLine)
        painter.setPen(pen)
        painter.drawRoundedRect(self.sizes[0], self.sizes[1],
                                self.sizes[2], self.v_form.boundingRect().bottomRight().y()+self.height_offset,
                                self.sizes[4], self.sizes[5])

    def get_input_edges(self):
        out = {}
        for i in [i.edge_list for i in self.inputs]:
            if not i.__len__() == 0:
                out[i[0]] = [e.connection for e in i]
        return out

    def get_output_edges(self):
        out = {}
        for i in [i.edge_list for i in self.outputs]:
            if not i.__len__() == 0:
                out[i[0]] = [e.connection for e in i]
        return out

    def mousePressEvent(self, event):

        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):

        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)

    def add_input_port(self, port_name, data_type):

        p = self._add_port(AGPortTypes.kInput, data_type, port_name)
        return p

    def add_output_port(self, port_name, data_type):

        p = self._add_port(AGPortTypes.kOutput, data_type, port_name)
        return p

    def add_layout(self):

        form = QtGui.QGraphicsWidget()
        lyt = QtGui.QGraphicsLinearLayout()
        lyt.setSpacing(self.spacings.kPortSpacing)
        lyt.setContentsMargins(1, 1, 1, 1)
        lyt.setMaximumHeight(self.spacings.kPortOffset)
        form.setLayout(lyt)
        form.setZValue(1)
        form.setAutoFillBackground(True)
        form.setGeometry(QtCore.QRectF(0, 0, self.w+self.spacings.kPortOffset+3, self.h))
        # set color
        palette = form.palette()
        if self._color_idx > 0:
            palette.setColor(palette.Window, self.colors.kPortLinesA)
            self._color_idx *= -1
        else:
            palette.setColor(palette.Window, self.colors.kPortLinesB)
            self._color_idx *= -1
        form.setPalette(palette)
        self.layout.addItem(form)
        return lyt

    # def kill(self):

    #     # self.prepareGeometryChange()
    #     # self.label.prepareGeometryChange()
    #     AGNode.kill(self)
    #     # self.scene().removeItem(self)

    def _add_port(self, port_type, data_type, name, color=QtGui.QColor(0, 100, 0, 255)):

        p = Port(name, self, data_type, 10, 10, color)
        p.type = port_type
        p.parent = self
        connector_name = QtGui.QGraphicsProxyWidget()
        lbl = QtGui.QLabel(name)
        lbl.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        connector_name.setWidget(lbl)
        lyt = self.add_layout()
        if port_type == self.port_types.kInput:
            lbl.setAlignment(QtCore.Qt.AlignLeft)
            lyt.addItem(p)
            lyt.addItem(connector_name)
            self.inputs.append(p)
        elif port_type == self.port_types.kOutput:
            lbl.setAlignment(QtCore.Qt.AlignRight)
            lyt.addItem(connector_name)
            lyt.addItem(p)
            self.outputs.append(p)
        return p
