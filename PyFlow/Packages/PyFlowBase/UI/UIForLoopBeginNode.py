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

from PyFlow.Core.NodeBase import NodeBase
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.PathsRegistry import PathsRegistry
from Qt import QtGui
from Qt import QtCore
from PyFlow.UI.Utils.ConvexHull import convex_hull
import uuid
from Qt.QtWidgets import *


class backDrop(QGraphicsWidget):
    def __init__(self, parent):
        super(backDrop, self).__init__()
        self.parent = parent
        self.rect = QtCore.QRectF()

    def boundingRect(self):
        try:
            return QtCore.QRectF(QtCore.QPointF(self.parent.left - 5, self.parent.top + 5), QtCore.QPointF(self.parent.right + 5, self.parent.down - 5))
        except:
            return QtCore.QRectF(0, 0, 0, 0)

    def paint(self, painter, option, widget):
        roundRectPath = QtGui.QPainterPath()
        self.parent.computeHull()
        if self.parent.poly:
            path = QtGui.QPainterPath()
            path.addPolygon(self.parent.poly)
            color = QtGui.QColor(self.parent.headColorOverride)
            color.setAlpha(50)
            pen = QtGui.QPen(self.parent.headColorOverride, 0.5)
            painter.setPen(pen)
            painter.fillPath(path, color)
            painter.drawPath(path)


class UIForLoopBeginNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIForLoopBeginNode, self).__init__(raw_node)
        self.headColorOverride = Colors.Orange
        self.poly = None
        self.owningLoopBeginNode = self
        self.owningNodes = []
        self.backDrop = backDrop(self)

    def postCreate(self, jsonTemplate=None):
        super(UIForLoopBeginNode, self).postCreate(jsonTemplate)
        self.scene().addItem(self.backDrop)
        self.computeHull()
        self.backDrop.update()

    def eventDropOnCanvas(self):
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate['package'] = "PyFlowBase"
        nodeTemplate['lib'] = ""
        nodeTemplate['type'] = "forLoopEnd"
        nodeTemplate['name'] = self.canvasRef( ).graphManager.getUniqNodeName("forLoopEnd")
        nodeTemplate['x'] = self.scenePos().x() + self.geometry().width() + 30
        nodeTemplate['y'] = self.scenePos().y()
        nodeTemplate['uuid'] = str(uuid.uuid4())
        endNode = self.canvasRef()._createNode(nodeTemplate)
        self.getPinSG("Paired block").setData(str(endNode.path()))
        endNode.getPinSG("Paired block").setData(self.path())
        self.canvasRef().connectPins(self.getPinSG("LoopBody"), endNode.getPinSG(DEFAULT_IN_EXEC_NAME))

    def computeHull(self):
        loopEndNode = PathsRegistry().getEntity(self.getPinSG("Paired block").getData())
        p = [self]
        if loopEndNode.__class__.__name__ == "forLoopEnd" and loopEndNode.getWrapper() is not None:
            p.append(loopEndNode.getWrapper())
        else:
            self.poly = QtGui.QPolygonF()
            return

        p += self.getBetwenLoopNodes(self)

        path = []
        self.left = 0
        self.top = 0
        self.right = 0
        self.down = 0
        for i in p:
            relPos = i.scenePos()
            self.left = min(self.left, relPos.x())
            self.top = max(self.top, relPos.y())
            self.right = max(self.right, relPos.x())
            self.down = min(self.down, relPos.y())
            relSize = QtCore.QPointF(i.getNodeWidth(), i.geometry().height())
            path.append((relPos.x() - 5, relPos.y() - 5))
            path.append((relPos.x() + relSize.x() + 5, relPos.y() - 5))
            path.append((relPos.x() + relSize.x() + 5, relPos.y() + relSize.y() + 5))
            path.append((relPos.x() - 5, relPos.y() + relSize.y() + 5))

        if len(path) >= 3:
            self.convex_hull = convex_hull(path)
            self.poly = QtGui.QPolygonF()
            for i in self.convex_hull:
                self.poly.append(QtCore.QPointF(i[0], i[1]))
            self.poly.append(QtCore.QPointF(
                self.convex_hull[0][0], self.convex_hull[0][1]))

    def paint(self, painter, option, widget):
        self.computeHull()
        self.backDrop.update()
        NodePainter.default(self, painter, option, widget)
