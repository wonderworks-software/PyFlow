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

from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Utils.Settings import (Spacings, Colors)
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UINodeBase import NodeName
from PyFlow.UI.Canvas.UIPinBase import UICommentPinBase
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
import weakref


class UICommentNode(UINodeBase):
    layer = 0

    def __init__(self, raw_node):
        super(UICommentNode, self).__init__(raw_node)
        self.color = Colors.AbsoluteBlack
        self.color.setAlpha(80)
        self.isCommentNode = True
        self.resizable = True
        self.owningNodes = set()
        UICommentNode.layer += 1
        self.setZValue(UICommentNode.layer)

    def hideOwningNodes(self):
        for node in self.owningNodes:
            node.hide()

    def onVisibilityChanged(self, bVisible):
        for node in self.owningNodes:
            if not self.collapsed:
                node.setVisible(bVisible)

    def checkOwningCommentNode(self):
        super(UICommentNode, self).checkOwningCommentNode()
        if self.owningCommentNode is not None:
            self.setZValue(self.owningCommentNode.zValue() + 1)

    def mousePressEvent(self, event):
        super(UICommentNode, self).mousePressEvent(event)

        zValue = self.zValue()
        partiallyCollidedComments = set()
        for node in self.getCollidedNodes(False):
            if node.isCommentNode:
                partiallyCollidedComments.add(node)
                if self.zValue() <= node.zValue():
                    if self.sceneBoundingRect().contains(node.sceneBoundingRect()):
                        continue
                    zValue += 1
        if len(partiallyCollidedComments) == 0:
            zValue = 0
        self.setZValue(zValue)

    def mouseReleaseEvent(self, event):
        super(UICommentNode, self).mouseReleaseEvent(event)
        if not self.collapsed:
            for node in self.getCollidedNodes():
                node.checkOwningCommentNode()

    def aboutToCollapse(self, futureCollapseState):
        if futureCollapseState:
            for node in self.owningNodes:
                if node.owningCommentNode is self:
                    node.hide()
        else:
            for node in self.owningNodes:
                node.show()

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        # restore text and size
        self.minWidth = self.labelWidth
        height = self.minHeight
        text = self.__class__.__name__
        # initial color is black
        color = self.color

        if 'commentNode' in jsonTemplate['meta']:
            # labelHeight = jsonTemplate['meta']['commentNode']['labelHeight']
            text = jsonTemplate['meta']['commentNode']['text']
            color = QtGui.QColor(*jsonTemplate['meta']['commentNode']['color'])

    def translate(self, x, y):
        for n in self.owningNodes:
            if not n.isSelected():
                n.translate(x, y)
        super(UICommentNode, self).translate(x, y)

    def isRenamable(self):
        return True

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
        painter.drawRoundedRect(r, 3, 3)

        if option.state & QStyle.State_Selected:
            pen.setColor(Colors.Yellow)
            pen.setStyle(self.opt_pen_selected_type)
            pen.setWidth(pen.width() * 1.5)
            # pen.setColor(node.graph().parent.styleSheetEditor.style.MainColor)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.drawRoundedRect(r, 3, 3)
        NodePainter.drawResizeHandles(self, painter, option, widget)

    def createPropertiesWidget(self, propertiesWidget):
        baseCategory = CollapsibleFormWidget(headName="Base")
        # name
        le_name = QLineEdit(self.getName())
        le_name.setReadOnly(True)
        # if self.isRenamable():
        le_name.setReadOnly(False)
        le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        baseCategory.addWidget("Name", le_name)

        # type
        leType = QLineEdit(self.__class__.__name__)
        leType.setReadOnly(True)
        baseCategory.addWidget("Type", leType)

        # pos
        le_pos = QLineEdit("{0} x {1}".format(self.pos().x(), self.pos().y()))
        baseCategory.addWidget("Pos", le_pos)
        propertiesWidget.addWidget(baseCategory)

        appearanceCategory = CollapsibleFormWidget(headName="Appearance")
        pb = QPushButton("...")
        pb.clicked.connect(lambda: self.onChangeColor(True))
        appearanceCategory.addWidget("Color", pb)
        propertiesWidget.addWidget(appearanceCategory)

        infoCategory = CollapsibleFormWidget(headName="Info")

        doc = QTextBrowser()
        doc.setOpenExternalLinks(True)
        doc.setHtml(self.description())
        infoCategory.addWidget("", doc)
        propertiesWidget.addWidget(infoCategory)
