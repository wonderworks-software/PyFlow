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

from qtpy import QtGui
from qtpy import QtCore
from qtpy.QtWidgets import QGraphicsWidget


class backDrop(QGraphicsWidget):
    def __init__(self, parent):
        super(backDrop, self).__init__()
        self.parent = parent
        self.rect = QtCore.QRectF()
        try:
            self.parent._rawNode.killed.connect(self.parentNodeKilled)
        except:
            pass

    def parentNodeKilled(self):
        scene = self.scene()
        if scene is not None:
            scene.removeItem(self)
            del self

    def boundingRect(self):
        try:
            return QtCore.QRectF(
                QtCore.QPointF(self.parent.left - 5, self.parent.top + 5),
                QtCore.QPointF(self.parent.right + 5, self.parent.down - 5),
            )
        except:
            return QtCore.QRectF(0, 0, 0, 0)

    def paint(self, painter, option, widget):
        if not self.parent.isUnderActiveGraph():
            return

        roundRectPath = QtGui.QPainterPath()
        self.parent.computeHull()
        if self.parent.poly is not None:
            color = QtGui.QColor(self.parent.headColorOverride)
            color.setAlpha(50)
            pen = QtGui.QPen(self.parent.headColorOverride, 0.5)
            painter.setPen(pen)
            painter.fillPath(self.parent.poly, color)
            painter.drawPath(self.parent.poly)
