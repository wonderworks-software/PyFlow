"""@file CommentNode.py
"""
from types import MethodType

from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsItemGroup
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QTextBrowser
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QColorDialog
from Qt import QtGui
from Qt import QtCore

from PyFlow.UI.Settings import (Spacings, Colors)
from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.UINodeBase import NodeName

class commentNodeName(NodeName):
    """doc string for commentNodeName"""
    def __init__(self, parent, bUseTextureBg=False, color=Colors.AbsoluteBlack):
        super(commentNodeName, self).__init__(parent, bUseTextureBg, color=color)
        self.color = color
        self.color.setAlpha(80)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setDefaultTextColor(QtGui.QColor(255, 255, 255, 255))
        self.roundCornerFactor = 5
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.width = self.document().documentLayout().documentSize().width()
        self.icon = QtGui.QImage(':/icons/resources/py.png')

    def mousePressEvent(self, event):
        if not self.parentItem().isSelected():
            self.parentItem().graph().clearSelection()
        if self.parentItem().expanded:
            self.parentItem().nodesToMove.clear()
            self.parentItem().updateChildrens(self.parentItem().collidingItems())
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
            if width >= self.parentItem().rect.width():
                self.width = width
                self.adjustSizes()

        self.width = self.parentItem().rect.width()
        self.setTextWidth(self.width)
        self.update()

    def adjustSizes(self):
        self.parentItem().rect.setRight(self.width)
        self.setTextWidth(self.width)
        self.h = self.document().documentLayout().documentSize().height()
        self.update()
        self.parentItem().update()

    def paint(self, painter, option, widget):
        QGraphicsTextItem.paint(self, painter, option, widget)
        r = QtCore.QRectF(option.rect)
        r.setWidth(self.width)
        r.setX(0.25)
        r.setY(0.25)
        r.setHeight(r.height() - 1)
        b = QtGui.QLinearGradient(0, 0, 0, r.height())
        b.setColorAt(0, self.color)
        b.setColorAt(0.25, self.color.lighter(1))
        #b.setColorAt(0.5, self.color)
        b.setColorAt(1, self.color.lighter(100))
        painter.setPen(QtCore.Qt.NoPen)
        color = QtGui.QColor(self.color)
        #color.setAlpha(150)
        painter.setBrush(color)

        
        painter.drawRoundedRect(0, 0, r.width(), r.height(), self.parentItem().sizes[4], self.parentItem().sizes[5], QtCore.Qt.AbsoluteSize)
        #painter.drawRect(1, r.height() * 0.5 + 2, r.width(), r.height() * 0.5)
        parentRet = self.parentItem().childrenBoundingRect()

        # painter.drawRoundedRect(r, self.roundCornerFactor, self.roundCornerFactor)

    def hoverEnterEvent(self, event):
        NodeName.hoverEnterEvent(self, event)


import weakref
## Comment node
#
# Can drag intersected nodes.
# You can also specify color and resize it.
class UIcommentNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIcommentNode, self).__init__(raw_node)
        self.color = Colors.AbsoluteBlack
        self.color.setAlpha(80)
        self.nodesToMove = {}
        self.edgesToHide = []       
        self.nodesNamesToMove = []
        self.pinsToMove = {}
        self.commentInputs = []
        self.commentOutpus = []
        self.lastNodePos = self.scenePos()
        self.rect = self.childrenBoundingRect()
        self.initialRectWidth = 0.0
        self.initialRectHeight = 0.0
        self.mousePressPos = self.scenePos()
        self.resizeDirection = (0, 0)
        self.bResize = False
        self.bMove = False
        self.minWidth = 100.0
        self.minHeight = 100.0
        self.lastMousePos = QtCore.QPointF()
        self.setZValue(-2)
        self.expanded = True
        self.isCommentNode = True

    def onChangeColor(self):
        res = QColorDialog.getColor(self.color, None, 'Comment node color setup')
        if res.isValid():
            res.setAlpha(80)
            self.color = res
            self.label().color = res
            self.update()
            self.label().update()

    def serialize(self):
        template = UINodeBase.serialize(self)
        if self.expanded:
            bottom = self.rect.bottom()
        else:
            bottom = self.prevRect
        template['meta']['commentNode'] = {
            'w': self.rect.right(),
            'h': bottom,
            'labelHeight': self.label().h,
            'text': self.label().toPlainText(),
            'color': (self.color.toTuple()),
            'expanded': self.expanded,
            'nodesToMove': [str(n.uid) for n in self.nodesToMove]
        }
        return template

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        # restore text and size
        width = self.minWidth
        height = self.minHeight
        labelHeight = self.label().h
        text = self.__class__.__name__
        # initial color is black
        color = self.color
        self.rect.setBottom(height)
        self.rect.setRight(width)
        try:
            # if copied in runtime
            width = jsonTemplate['meta']['commentNode']['w']
            height = jsonTemplate['meta']['commentNode']['h']
            labelHeight = jsonTemplate['meta']['commentNode']['labelHeight']
            text = jsonTemplate['meta']['commentNode']['text']
            color = QtGui.QColor(*jsonTemplate['meta']['commentNode']['color'])
            self.rect.setBottom(height)
            self.rect.setRight(width)
            if "nodesToMove" in jsonTemplate['meta']['commentNode']:
                self.nodesNamesToMove = jsonTemplate['meta']['commentNode']["nodesToMove"]   
                for nodename in self.nodesNamesToMove:
                    n = self.graph().nodes[uuid.UUID(nodename)]
                    uuid.UUID(nodename)
                    if n is not None and n not in self.nodesToMove:
                        self.nodesToMove[n] = n.scenePos()
                self.nodesNamesToMove = []
            if "expanded" in jsonTemplate['meta']['commentNode']:
                self.expanded = jsonTemplate['meta']['commentNode']["expanded"]

        except:
            pass

        self.color = color
        self.update()
        self.scene().removeItem(self.label())
        delattr(self, 'label')
        self.label = weakref.ref(commentNodeName(self, False, Colors.White))
        self.label().setPlainText(text)
        self.label().width = self.rect.width()
        self.label().h = labelHeight
        self.label().color = color
        self.label().update()
        self.label().adjustSizes()

    @staticmethod
    def isInRange(mid, val, width=10):
        '''check if val inside strip'''
        leftEdge = mid - width
        rightEdge = mid + width
        return leftEdge <= val <= rightEdge

    def boundingRect(self):
        return self.rect

    def updateChildrens(self, nodes):
        self.commentInputs = []
        self.commentOutpus = []
        self.edgesToHide = []
        self.pinsToMove.clear()
        self.nodesNamesToMove = []
        edges = []
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
                for edg in i.edge_list:
                    if edg.source().UiNode in self.nodesToMove and edg.destination().UiNode in self.nodesToMove:
                        self.edgesToHide.append(edg)

    def mousePressEvent(self, event):
        margin = 4
        QGraphicsItem.mousePressEvent(self, event)
        self.mousePressPos = event.scenePos()
        self.origPos = self.pos()
        self.lastNodePos = self.scenePos()
        pBottomRight = self.rect.bottomRight()
        pBottomLeft = self.rect.bottomLeft()
        bottomRightRect = QtCore.QRectF(pBottomRight.x() - margin, pBottomRight.y() - margin, margin, margin)
        bottomLeftRect = QtCore.QRectF(pBottomLeft.x(), pBottomLeft.y() - margin, 5, 5)
        # detect where on the node
        self.initialRect = self.rect
        if self.expanded:
            if bottomRightRect.contains(event.pos()):
                self.initialRectWidth = self.rect.width()
                self.initialRectHeight = self.rect.height()
                self.resizeDirection = (1, -1)
                self.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.bResize = True
            elif bottomLeftRect.contains(event.pos()):
                self.initialRectWidth = self.rect.width()
                self.initialRectHeight = self.rect.height()
                self.resizeDirection = (-1, -1)
                self.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.bResize = True                
            elif event.pos().x() > (self.rect.width() - margin):
                self.initialRectWidth = self.rect.width()
                self.resizeDirection = (1, 0)
                self.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.bResize = True
            elif event.pos().y()>(self.rect.bottom()-margin):#elif (event.pos().y() + self.label().defaultHeight) > (self.rect.height() - 15):
                self.initialRectHeight = self.rect.height()
                self.resizeDirection = (0, -1)
                self.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.bResize = True
            elif event.pos().x() < (self.rect.x() + margin):
                self.initialRectWidth = self.rect.width()
                self.resizeDirection = (-1, 0)
                self.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.bResize = True

            self.nodesToMove.clear()
            self.updateChildrens(self.collidingItems())
        else:
            nodes = []
            for nodename in self.nodesNamesToMove:
                nodes.append(self.graph().nodes[nodename])
            self.updateChildrens(nodes)
        # for node in [i for i in self.collidingItems() if isinstance(i, UINodeBase) and not isinstance(i, UIcommentNode)]:
        #    self.nodesToMove[node] = node.scenePos()

    def mouseMoveEvent(self, event):
        QGraphicsItem.mouseMoveEvent(self, event)
        delta = self.lastMousePos - event.pos()
        self.lastNodePos = self.scenePos()
        # resize
        if self.bResize:
            delta = event.scenePos() - self.mousePressPos
            if self.resizeDirection == (1, 0):
                # right edge resize
                newWidth = delta.x() + self.initialRectWidth
                if newWidth > self.minWidth:
                    self.label().width = newWidth
                    self.rect.setWidth(newWidth)
                    self.label().adjustSizes()
            elif self.resizeDirection == (0, -1):
                newHeight = delta.y() + self.initialRectHeight
                newHeight = max(newHeight, self.label().h + 20.0)
                if newHeight > self.minHeight:
                    # bottom edge resize
                    self.rect.setHeight(newHeight)
            elif self.resizeDirection == (1, -1):
                newWidth = delta.x() + self.initialRectWidth
                newHeight = delta.y() + self.initialRectHeight
                newHeight = max(newHeight, self.label().h + 20.0)
                if newWidth > self.minWidth:
                    self.label().width = newWidth
                    self.rect.setWidth(newWidth)
                    self.label().setTextWidth(newWidth)
                if newHeight > self.minHeight:                    
                    self.rect.setHeight(newHeight)
            elif self.resizeDirection == (-1, 0):
                # left edge resize
                newWidth = (1-delta.x()) + self.initialRectWidth
                posdelta = event.scenePos() - self.origPos
                if newWidth > self.minWidth:
                    self.translate(posdelta.x(),0,False)
                    self.origPos = self.pos()
                    self.label().width = newWidth
                    self.label().adjustSizes()    
            elif self.resizeDirection == (-1, -1):            
                newWidth = (1-delta.x()) + self.initialRectWidth
                newHeight = delta.y() + self.initialRectHeight
                newHeight = max(newHeight, self.label().h + 20.0)
                posdelta = event.scenePos() - self.origPos
                if newWidth > self.minWidth:
                    self.translate(posdelta.x(),0,False)
                    self.origPos = self.pos()                    
                    self.label().width = newWidth
                    self.rect.setWidth(newWidth)
                    self.label().setTextWidth(newWidth)
                if newHeight > self.minHeight :                    
                    self.rect.setHeight(newHeight)
            self.update()
            self.label().update()
        self.lastMousePos = event.pos()

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

    def getCursorResizing(self, cursorPos):
        pBottomRight = self.rect.bottomRight()
        pBottomLeft = self.rect.bottomLeft()
        margin = 4
        bottomRightRect = QtCore.QRectF(pBottomRight.x() - margin, pBottomRight.y() - margin, margin, margin)
        bottomLeftRect = QtCore.QRectF(pBottomLeft.x(), pBottomLeft.y() - margin, 5, 5)
        # detect where on the node
        if self.expanded:
            cursor = self.mapFromScene(cursorPos)
            if not self.bResize:
                if bottomRightRect.contains(cursor):
                    self.resizeDirectionArrow = 0
                    self.cursorResize = True
                elif bottomLeftRect.contains(cursor):
                    self.resizeDirectionArrow = 4
                    self.cursorResize = True      
                elif cursor.x() > (self.rect.width() - margin):
                    self.resizeDirectionArrow = 1
                    self.cursorResize = True
                elif cursor.y()>(self.rect.bottom()-margin):
                    self.resizeDirectionArrow = 2
                    self.cursorResize = True
                elif cursor.x() < (self.rect.x() + margin):
                    self.resizeDirectionArrow = 3
                    self.cursorResize = True   
                else:
                    self.cursorResize = False
                    self.resizeDirectionArrow = 0                      

    def mouseReleaseEvent(self, event):
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.bResize = False

    def mouseDoubleClickEvent(self, event):
        super(UIcommentNode, self).mouseDoubleClickEvent(event)
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()

    def OnDoubleClick(self, pos):
        if self.expanded:
            self.expanded = False
            self.prevRect = self.rect.bottom()
            self.rect.setBottom(self.label().h / 2)

            for node in self.nodesToMove:
                node.hide()

            for pin in self.pinsToMove:
                if pin in self.commentInputs:
                    pin.prevPos = QtCore.QPointF(self.scenePos().x() - 8, self.scenePos().y()) - pin.scenePos()
                elif pin in self.commentOutpus:
                    pin.prevPos = QtCore.QPointF(self.scenePos().x() + self.boundingRect().width() - 8, self.scenePos().y()) - pin.scenePos()
                pin.moveBy(pin.prevPos.x(), pin.prevPos.y())
                pin.update()

            for edge in self.edgesToHide:
                edge.hide()
        else:
            self.expanded = True
            self.rect.setBottom(self.prevRect)
            for node in self.nodesToMove:
                node.show()
            for pin in self.pinsToMove:
                pin.moveBy(-pin.prevPos.x(), -pin.prevPos.y())
            for edge in self.edgesToHide:
                edge.show()
        self.update()

    def translate(self, x, y,moveChildren=True):
        if moveChildren:
            for n in self.nodesToMove:
                if not n.isSelected():
                    n.translate(x, y)
        super(UIcommentNode, self).translate(x, y)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = Colors.NodeBackgrounds
        if self.isSelected():
            color = color.lighter(150)

        painter.setBrush(self.color)
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            # pen.setColor(self.graph().window().styleSheetEditor.style.MainColor)
            pen.setColor(Colors.Yellow)
            pen.setStyle(QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect, self.sizes[4], self.sizes[5])

        pen.setColor(Colors.White)
        painter.setPen(pen)

        # draw bottom right resizer
        pBottomRight = self.rect.bottomRight()
        bottomRightRect = QtCore.QRectF(pBottomRight.x() - 6, pBottomRight.y() - 6, 5, 5)
        painter.drawLine(bottomRightRect.bottomLeft(), bottomRightRect.topRight())

        bottomRightRect.setRight(bottomRightRect.left() + bottomRightRect.width() / 2)
        bottomRightRect.setBottom(bottomRightRect.top() + bottomRightRect.height() / 2)
        painter.drawLine(bottomRightRect.bottomLeft(), bottomRightRect.topRight())
        # draw bottom left resizer
        pBottomLeft = self.rect.bottomLeft()
        pBottomLeftRect = QtCore.QRectF(pBottomLeft.x(), pBottomLeft.y() - 6, 5, 5)
        painter.drawLine(pBottomLeftRect.bottomRight(), pBottomLeftRect.topLeft())

        pBottomLeftRect.setLeft(pBottomLeftRect.left() + pBottomLeftRect.width() / 2)
        pBottomLeftRect.setBottom(pBottomLeftRect.top() + pBottomLeftRect.height() / 2)
        painter.drawLine(pBottomLeftRect.bottomRight(), pBottomLeftRect.topLeft())


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
        pb.clicked.connect(self.onChangeColor)
        formLayout.addRow("Color", pb)

        doc_lb = QLabel()
        doc_lb.setStyleSheet("background-color: black;")
        doc_lb.setText("Description")
        formLayout.addRow("", doc_lb)
        doc = QTextBrowser()
        doc.setOpenExternalLinks(True)
        doc.setHtml(self.description())
        formLayout.addRow("", doc)

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Can drag intersected nodes. You can also specify color and resize it.'
