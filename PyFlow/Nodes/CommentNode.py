from AbstractGraph import *
from Settings import *
from Node import Node
from Node import NodeName
from types import MethodType
from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsItemGroup
from Qt.QtWidgets import QStyle
from Qt import QtGui
from Qt import QtCore


class CommentNodeName(NodeName):
    """doc string for CommentNodeName"""
    def __init__(self, parent, bUseTextureBg=False, color=Colors.White):
        super(CommentNodeName, self).__init__(parent, bUseTextureBg, color=color)
        self.color = Colors.White
        self.color.setAlpha(80)
        self.setAcceptHoverEvents(True)
        self.setDefaultTextColor(QtGui.QColor(255, 255, 255, 255))
        self.width = QtGui.QFontMetricsF(self.font()).width(self.toPlainText()) + 5.0
        self.roundCornerFactor = 1.0
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)

    def keyPressEvent(self, event):
        QGraphicsTextItem.keyPressEvent(self, event)

        key = event.key()

        if (key == QtCore.Qt.Key_Return) or (key == QtCore.Qt.Key_Escape):
            # clear selection
            cursor = QtGui.QTextCursor(self.document())
            cursor.clearSelection()
            self.setTextCursor(cursor)
            # finish editing
            self.setEnabled(False)
            self.setEnabled(True)
        elif not key == QtCore.Qt.Key_Backspace:
            # if backspace is pressed do not change width
            width = QtGui.QFontMetricsF(self.font()).width(self.toPlainText()) + 10.0
            # change width if needed
            if width >= self.parentItem().rect.width():
                self.parentItem().rect.setRight(width)
                self.parentItem().update()
                self.width = width
                self.setTextWidth(width)
                self.update()

        self.width = self.parentItem().rect.width()
        self.setTextWidth(self.width)
        self.update()

    def paint(self, painter, option, widget):
        # super(CommentNodeName, self).paint(painter, option, widget)

        QGraphicsTextItem.paint(self, painter, option, widget)
        r = QtCore.QRectF(option.rect)
        r.setWidth(self.width)
        r.setX(0.25)
        r.setY(0.25)
        b = QtGui.QLinearGradient(0, 0, 0, r.height())
        b.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
        b.setColorAt(0.25, self.color)
        b.setColorAt(1, self.color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(b)
        painter.drawRoundedRect(r, self.roundCornerFactor, self.roundCornerFactor)

    def hoverEnterEvent(self, event):
        NodeName.hoverEnterEvent(self, event)


class CommentNode(Node, NodeBase):
    def __init__(self, name, graph, bUseTextureBg=False, headColor=Colors.White):
        super(CommentNode, self).__init__(name, graph, headColor=headColor)
        # self.label = weakref.ref(CommentNodeName(self, False, headColor))
        self.color = Colors.White
        self.nodesToMove = {}
        self.lastNodePos = self.scenePos()
        self.rect = self.childrenBoundingRect()
        self.initialRectWidth = 0.0
        self.initialRectHeight = 0.0
        self.mousePressPos = self.scenePos()
        self.resizeDirection = [-1, 0]
        self.bResize = False
        self.minWidth = self.rect.width()
        self.lastMousePos = QtCore.QPointF()

    def postCreate(self, jsonTemplate):
        Node.postCreate(self, jsonTemplate)
        self.rect = self.childrenBoundingRect()
        self.update()
        self.scene().removeItem(self.label())
        delattr(self, 'label')
        self.label = weakref.ref(CommentNodeName(self, False, Colors.White))
        self.label().setPlainText(self.__class__.__name__)
        self.label().width = self.boundingRect().width()
        self.label().update()
        # self.label().color = Colors.White
        # self.label().color.setAlpha(50)

    @staticmethod
    def isInRange(pos, val, width=10):
        '''check if val inside strip'''

        leftEdge = pos - width
        rightEdge = pos + width
        return leftEdge <= val <= rightEdge

    def boundingRect(self):
        return self.rect

    def mousePressEvent(self, event):
        QGraphicsItem.mousePressEvent(self, event)
        self.mousePressPos = event.scenePos()

        if event.pos().x() > (self.rect.width() - 20):
            self.initialRectWidth = self.rect.width()
            self.resizeDirection = [1, 0]
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.bResize = True
        elif (event.pos().y() + self.label().boundingRect().height()) > (self.rect.height() - 20):
            self.initialRectHeight = self.rect.height()
            self.resizeDirection = [0, 1]
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.bResize = True

        self.nodesToMove.clear()
        for node in [i for i in self.collidingItems() if isinstance(i, Node)]:
            self.nodesToMove[node] = node.scenePos()

    def mouseMoveEvent(self, event):
        QGraphicsItem.mouseMoveEvent(self, event)
        delta = self.lastMousePos - event.pos()
        # resize
        if self.bResize:
            delta = event.scenePos() - self.mousePressPos
            if self.resizeDirection == [1, 0]:
                # right edge resize
                newWidth = delta.x() + self.initialRectWidth
                self.label().width = newWidth
                self.rect.setRight(newWidth)
                self.label().setTextWidth(newWidth)
            elif self.resizeDirection == [0, 1]:
                newHeight = delta.y() + self.initialRectHeight
                # bottom edge resize
                self.rect.setHeight(newHeight)

            self.update()
            self.label().update()
        self.lastMousePos = event.pos()

    def itemChange(self, change, value):
        if change == self.ItemPositionChange:
            # grid snapping
            value.setX(roundup(value.x() - self.graph().grid_size + self.graph().grid_size / 3.0, self.graph().grid_size))
            value.setY(roundup(value.y() - self.graph().grid_size + self.graph().grid_size / 3.0, self.graph().grid_size))
            value.setY(value.y() - 2)
            try:
                deltaPos = value - self.lastNodePos
                for node, initialPos in self.nodesToMove.iteritems():
                    nodePos = node.scenePos()
                    newPos = nodePos + deltaPos
                    node.setPos(newPos)
                self.lastNodePos = value
            except:
                pass
            return value
        return QGraphicsItem.itemChange(self, change, value)

    def getNodesRect(self, nodes):
        rectangles = []

        for n in nodes:
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

    def mouseReleaseEvent(self, event):
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.bResize = False

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = Colors.NodeBackgrounds
        if self.isSelected():
            color = color.lighter(150)

        painter.setBrush(self.color)
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            if self.options:
                pen.setColor(Colors.Yellow)
                pen.setStyle(self.opt_pen_selected_type)
            else:
                pen.setColor(opt_selected_pen_color)
                pen.setStyle(self.opt_pen_selected_type)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect, self.sizes[4], self.sizes[5])

    def onUpdatePropertyView(self, formLayout):
        pass

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Comment node'
