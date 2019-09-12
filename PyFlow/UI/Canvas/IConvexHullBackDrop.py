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


from Qt import QtGui
from Qt import QtCore
from PyFlow.UI.Canvas.loopBackDrop import backDrop
from PyFlow.Core.PathsRegistry import PathsRegistry
from PyFlow.UI.Utils.ConvexHull import convex_hull
from PyFlow.UI.Canvas.Painters import ConnectionPainter

class IConvexHullBackDrop(object):
    """Convex hull backdrop routines. Used by for loop and while loop nodes"""

    def __init__(self):
        super(IConvexHullBackDrop, self).__init__()
        self.poly = None
        self.left = 0
        self.top = 0
        self.right = 0
        self.down = 0
        self.convex_hull = []
        self.backDrop = backDrop(self)

    def computeHull(self):

        loopEndNodePath = self.getPinSG("Paired block").getData()
        loopEndNode = PathsRegistry().getEntity(loopEndNodePath)

        if loopEndNode is None:
            self.poly = QtGui.QPainterPath()
            return
        if self.isUnderCollapsedComment():
            p = [self.getTopMostOwningCollapsedComment()]
        else:
            p = [self]
        if loopEndNode.__class__.__name__ == "loopEnd" and loopEndNode.getWrapper() is not None:
            uiLoopEnd = loopEndNode.getWrapper()
            if loopEndNode.isUnderActiveGraph():
                if uiLoopEnd.isUnderCollapsedComment():
                    p.append(uiLoopEnd.getTopMostOwningCollapsedComment())
                else:
                    p.append(uiLoopEnd)

        else:
            self.poly = QtGui.QPainterPath()
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
            path = []
            for i in self.convex_hull:
                path.append(QtCore.QPointF(i[0], i[1]))
            self.poly,none = ConnectionPainter.roundCornersPath(path,6,True)
