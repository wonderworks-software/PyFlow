"""@file CommentNode.py
"""
from types import MethodType

from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QGraphicsItemGroup
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QTextBrowser
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QMenu
from Qt import QtGui
from Qt import QtCore

from PyFlow.UI.Utils.Settings import (Spacings, Colors)
from PyFlow.UI.Graph.UINodeBase import UINodeBase
from PyFlow.UI.Graph.UINodeBase import NodeName
from PyFlow.UI.Graph.UIPinBase import UICommentPinBase
import weakref

buttonStyle = """
QPushButton{color : rgba(255,255,255,255);
    background-color: rgba(0,0,0,0);
    border-width: 0px;
    border-color: transparent;
    border-style: solid;
    font-family: Microsoft YaHei;
    font-size: 20px;
    font-weight: bold;}
QPushButton:hover{
    color: rgba(255, 211, 25, 255);
}
QPushButton:pressed{
    color: rgba(255, 160, 47, 255)
}
"""


class commentNodeName(NodeName):
    """doc string for commentNodeName"""

    def __init__(self, parent, bUseTextureBg=False, color=Colors.AbsoluteBlack):
        super(commentNodeName, self).__init__(
            parent, bUseTextureBg, color=color)
        self.color = color
        self.color.setAlpha(80)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setDefaultTextColor(QtGui.QColor(255, 255, 255, 255))
        self.roundCornerFactor = 5
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.width = self.document().documentLayout().documentSize().width()
        self.icon = QtGui.QImage(':/icons/resources/py.png')
        self.setPos(15, -self.boundingRect().height() - 4)
        self.drawH = self.h

        self.hideButtomProxy = QGraphicsProxyWidget(self)
        self.hideButton = QPushButton("-")
        self.hideButtomProxy.setWidget(self.hideButton)
        self.hideButton.setStyleSheet(buttonStyle)
        self.hideButton.pressed.connect(self.parentItem().toggleCollapsed)
        self.hideButton.setFixedHeight(25)
        self.hideButton.setFixedWidth(25)
        self.leftWidget = UICommentPinBase(self)  # QGraphicsWidget(self)
        self.rigttWidget = UICommentPinBase(self)  # QGraphicsWidget(self)

    def mousePressEvent(self, event):
        if not self.parentItem().isSelected():
            self.parentItem().graph().clearSelection()
        if self.parentItem().expanded:
            self.parentItem().nodesToMove.clear()
            self.parentItem().updateChildren(self.parentItem().collidingItems())
        self.parentItem().setSelected(True)
        # NodeName.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        super(commentNodeName, self).mouseDoubleClickEvent(event)
        event.accept()
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)

    def focusOutEvent(self, event):
        super(commentNodeName, self).focusOutEvent(event)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

    def keyPressEvent(self, event):
        QGraphicsTextItem.keyPressEvent(self, event)
        modifires = event.modifiers()
        key = event.key()

        if key == QtCore.Qt.Key_Escape:
            # clear selection
            cursor = QtGui.QTextCursor(self.document())
            cursor.clearSelection()
            self.setTextCursor(cursor)
            # finish editing
            self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        elif not key == QtCore.Qt.Key_Backspace:
            # if backspace is pressed do not change width
            width = self.document().documentLayout().documentSize().width()
            self.h = self.document().documentLayout().documentSize().height()
            # change width if needed
            if width >= self.parentItem()._rect.width():
                self.width = width
            self.adjustSizes()

        self.width = self.parentItem()._rect.width()
        self.setTextWidth(self.width - 15)
        self.update()

    def adjustSizes(self):
        self.parentItem()._rect.setRight(self.width)
        self.setTextWidth(self.width - 15)
        self.h = self.document().documentLayout().documentSize().height()
        if not self.parentItem().expanded:
            self.parentItem()._rect.setHeight(self.h)
        self.update()
        self.parentItem().update()
        self.leftWidget.setPos(-20, self.boundingRect().center().y())
        self.rigttWidget.setPos(self.boundingRect().right(
        ) - 4.5, self.boundingRect().center().y())
        self.hideButtomProxy.setPos(-18, self.boundingRect().center().y() - 15)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width - 15.0, self.h)

    def paint(self, painter, option, widget):
        r = QtCore.QRectF(option.rect)
        r.setWidth(self.width)
        r.setY(0.25 + 1)
        # r.setHeight(r.height())
        painter.setPen(QtCore.Qt.NoPen)
        color = QtGui.QColor(self.color)
        painter.setBrush(color)
        r.setX(-13.5)
        r.setWidth(r.width() - 16.5)
        if self.parentItem().expanded:
            path = QtGui.QPainterPath()
            path.setFillRule(QtCore.Qt.WindingFill)
            path.addRoundedRect(
                r, self.parentItem().sizes[4], self.parentItem().sizes[5])
            r.setY(r.y() + self.parentItem().sizes[5])
            path.addRect(r)
            painter.fillPath(path, color)
        else:
            r.setHeight(r.height() - 1)
            #painter.drawRoundedRect(r, self.parentItem().sizes[4], self.parentItem().sizes[5])
        QGraphicsTextItem.paint(self, painter, option, widget)

    def hoverEnterEvent(self, event):
        NodeName.hoverEnterEvent(self, event)

# Comment node
#
# Can drag intersected nodes.
# You can also specify color and resize it.


class UIcommentNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIcommentNode, self).__init__(raw_node)
        self.color = Colors.AbsoluteBlack
        self.color.setAlpha(80)
        self.commentInputs = []
        self.commentOutpus = []
        self._rect = self.childrenBoundingRect()
        self.resizable = True
        self.minWidth = 105.0
        self.minHeight = 100.0
        self.sizes = [0, 0, self.w, self.h, 2, 2]
        self.setZValue(-2)
        self.expanded = True
        self.isCommentNode = True

    @staticmethod
    def isInRange(mid, val, width=10):
        '''check if val inside strip'''
        leftEdge = mid - width
        rightEdge = mid + width
        return leftEdge <= val <= rightEdge

    @staticmethod
    def getNodesRect(nodes):
        rectangles = []

        if len(nodes) == 0:
            return None

        for n in nodes:
            rectangles.append(n.sceneBoundingRect())

        minx_arr = [i.left() for i in rectangles]
        maxx_arr = [i.right() for i in rectangles]
        miny_arr = [i.top() for i in rectangles]
        maxy_arr = [i.bottom() for i in rectangles]

        min_x = min(minx_arr)
        min_y = min(miny_arr)

        max_x = max(maxx_arr)
        max_y = max(maxy_arr)

        return QtCore.QRect(QtCore.QPoint(min_x, min_y), QtCore.QPoint(max_x, max_y))

    def boundingRect(self):
        return self._rect

    def serialize(self):
        template = UINodeBase.serialize(self)
        # if self.expanded:
        #    bottom = self._rect.bottom()
        # else:
        bottom = self.prevRect
        template['meta']['commentNode'] = {
            'labelHeight': self.label().h,
            'text': self.label().toPlainText(),
            'color': (self.color.toTuple()),
            'expanded': self.expanded,
            'nodesToMove': [str(n.uid) for n in self.nodesToMove]
        }
        template['meta']['resize'] = {'h': bottom, 'w': self._rect.right()}
        return template

    def postCreate(self, jsonTemplate):
        width = self.minWidth
        UINodeBase.postCreate(self, jsonTemplate)
        # restore text and size
        self.minWidth = width
        height = self.minHeight
        labelHeight = self.label().h
        text = self.__class__.__name__
        # initial color is black
        color = self.color

        if 'resize' in jsonTemplate['meta']:
            width = jsonTemplate['meta']['resize']['w']
            height = jsonTemplate['meta']['resize']['h']

        if 'commentNode' in jsonTemplate['meta']:
            labelHeight = jsonTemplate['meta']['commentNode']['labelHeight']
            text = jsonTemplate['meta']['commentNode']['text']
            color = QtGui.QColor(*jsonTemplate['meta']['commentNode']['color'])

            if "nodesToMove" in jsonTemplate['meta']['commentNode']:
                self.nodesNamesToMove = jsonTemplate['meta']['commentNode']["nodesToMove"]
                for nodename in self.nodesNamesToMove:
                    for n in self.graph().nodes:
                        if str(n) == str(nodename):
                            self.nodesToMove[self.graph().nodes[n]] = self.graph(
                            ).nodes[n].scenePos()
                self.nodesNamesToMove = []

        self._rect.setBottom(height)
        self._rect.setRight(width)

        self.color = color
        self.update()
        self.scene().removeItem(self.label())
        delattr(self, 'label')
        self.label = weakref.ref(commentNodeName(self, False, Colors.White))
        self.label().setPlainText(text)
        self.label().width = self._rect.width()
        self.label().h = labelHeight
        self.label().color = color
        self.label().update()
        self.label().adjustSizes()
        try:
            if "expanded" in jsonTemplate['meta']['commentNode']:
                self.expanded = jsonTemplate['meta']['commentNode']["expanded"]
        except:
            self.expanded = True
        self.prevRect = self._rect.bottom()

    def updateChildren(self, nodes):
        self.commentInputs = []
        self.commentOutpus = []
        self.edgesToHide = []
        self.pinsToMove.clear()
        self.nodesToMove.clear()
        self.nodesNamesToMove = []
        connections = []
        for node in [i for i in nodes if isinstance(i, UINodeBase) and not i.isCommentNode and i.isVisible()]:
            self.nodesNamesToMove.append(node.uid)
            self.nodesToMove[node] = node.scenePos()
            node.groupNode = self
            for i in node.UIinputs.values():
                self.pinsToMove[i] = i.scenePos()
                self.commentInputs.append(i)
            for i in node.UIoutputs.values():
                self.pinsToMove[i] = i.scenePos()
                self.commentOutpus.append(i)
        for node in self.nodesToMove:
            for i in list(node.UIinputs.values()) + list(node.UIoutputs.values()):
                for edg in i.connections:
                    if edg.source().UiNode in self.nodesToMove and edg.destination().UiNode in self.nodesToMove:
                        self.edgesToHide.append(edg)

    def mouseDoubleClickEvent(self, event):
        super(UIcommentNode, self).mouseDoubleClickEvent(event)
        self.toggleCollapsed()
        event.accept()

    def mouseMoveEvent(self, event):
        super(UIcommentNode, self).mouseMoveEvent(event)
        self.label().adjustSizes()

    def toggleCollapsed(self):
        if self.expanded:
            self.updateChildren(self.collidingItems())
            self.label().hideButton.setText("+")
            self.expanded = False
            self.prevRect = self._rect.bottom()
            self._rect.setHeight(self.label().h)

            for node in self.nodesToMove:
                node.hide()

            for pin in self.pinsToMove:
                if pin in self.commentInputs:
                    for ege in pin.connections:
                        ege.drawDestination = self.label().leftWidget
                elif pin in self.commentOutpus:
                    for ege in pin.connections:
                        ege.drawSource = self.label().rigttWidget

            for connection in self.edgesToHide:
                connection.hide()
        else:
            self.label().hideButton.setText("-")
            self.expanded = True
            self._rect.setBottom(self.prevRect)
            for node in self.nodesToMove:
                node.show()
            for pin in self.pinsToMove:
                if pin in self.commentInputs:
                    for ege in pin.connections:
                        ege.drawDestination = pin
                elif pin in self.commentOutpus:
                    for ege in pin.connections:
                        ege.drawSource = pin
            for connection in self.edgesToHide:
                connection.show()
        self.update()

    def translate(self, x, y, moveChildren=True):
        super(UIcommentNode, self).translate(x, y, moveChildren)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = Colors.NodeBackgrounds
        if self.isSelected():
            color = color.lighter(150)

        painter.setBrush(self.color)
        pen = QtGui.QPen(QtCore.Qt.black, 0.75)
        if option.state & QStyle.State_Selected:
            # pen.setColor(self.graph().window().styleSheetEditor.style.MainColor)
            pen.setColor(Colors.Yellow)
            pen.setStyle(QtCore.Qt.SolidLine)
        painter.setPen(pen)
        r = QtCore.QRectF(self._rect)
        r.setWidth(r.width() - pen.width())
        r.setHeight(r.height() - pen.width())
        r.setX(pen.width())
        r.setY(r.y() + pen.width())
        painter.drawRoundedRect(r, self.sizes[4], self.sizes[5])

        if option.state & QStyle.State_Selected:
            pen.setColor(Colors.Yellow)
            pen.setStyle(self.opt_pen_selected_type)
            pen.setWidth(pen.width() * 1.5)
            # pen.setColor(node.graph().parent.styleSheetEditor.style.MainColor)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.drawRoundedRect(r, self.sizes[4], self.sizes[5])

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

        pb = QPushButton("...")
        pb.clicked.connect(lambda: self.onChangeColor(True))
        formLayout.addRow("Color", pb)

        doc_lb = QLabel()
        doc_lb.setStyleSheet("background-color: black;")
        doc_lb.setText("Description")
        formLayout.addRow("", doc_lb)
        doc = QTextBrowser()
        doc.setOpenExternalLinks(True)
        doc.setHtml(self.description())
        formLayout.addRow("", doc)
