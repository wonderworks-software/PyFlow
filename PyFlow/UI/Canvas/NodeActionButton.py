from Qt import QtCore, QtGui
from Qt import QtSvg
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QSizePolicy


class NodeActionButtonBase(QGraphicsWidget):
    """Base class for all node's actions buttons.

    By default it calls action `triggered` signal. Have default svg 10x10 icon.
    """
    def __init__(self, svgFilePath, action, uiNode):
        super(NodeActionButtonBase, self).__init__(uiNode)
        self.setAcceptHoverEvents(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setGraphicsItem(self)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
        self.action = action
        self.svgIcon = QtSvg.QGraphicsSvgItem(svgFilePath, self)
        self.setToolTip(self.action.toolTip())
        self.hovered = False
        uiNode._actionButtons.add(self)

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        if self.parentItem().isSelected():
            self.parentItem().setSelected(False)

        if self.action is not None and self.hasFocus():
            self.action.triggered.emit()
            self.clearFocus()

    def paint(self, painter, option, widget):
        super(NodeActionButtonBase, self).paint(painter, option, widget)
        if self.hovered:
            frame = QtCore.QRectF(QtCore.QPointF(0, 0), self.geometry().size())
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QColor(50, 50, 50, 50))
            painter.drawRoundedRect(frame, 2, 2)

    def setGeometry(self, rect):
        self.prepareGeometryChange()
        super(QGraphicsWidget, self).setGeometry(rect)
        self.setPos(rect.topLeft())

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(10, 10)
