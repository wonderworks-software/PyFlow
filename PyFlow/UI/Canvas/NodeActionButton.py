## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from qtpy import QtCore, QtGui
from qtpy.QtWidgets import QGraphicsWidget
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtSvgWidgets import QGraphicsSvgItem

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
        self.svgIcon = QGraphicsSvgItem(svgFilePath, self)
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

    def setGeometry(self, rect):
        self.prepareGeometryChange()
        super(QGraphicsWidget, self).setGeometry(rect)
        self.setPos(rect.topLeft())

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(10, 10)
