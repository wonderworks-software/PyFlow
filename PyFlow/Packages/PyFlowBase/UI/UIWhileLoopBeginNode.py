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

import uuid
from Qt import QtGui
from Qt import QtCore
from Qt.QtWidgets import *
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.IConvexHullBackDrop import IConvexHullBackDrop
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodeBase


class UIWhileLoopBeginNode(UINodeBase, IConvexHullBackDrop):
    def __init__(self, raw_node):
        super(UIWhileLoopBeginNode, self).__init__(raw_node)
        IConvexHullBackDrop.__init__(self)
        self.headColorOverride = Colors.Orange
        self.poly = None

    def postCreate(self, jsonTemplate=None):
        super(UIWhileLoopBeginNode, self).postCreate(jsonTemplate)
        self.scene().addItem(self.backDrop)
        self.computeHull()
        self.backDrop.update()

    def eventDropOnCanvas(self):
        # TODO: try to simplify this with Canvas.spawnNode
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate['package'] = "PyFlowBase"
        nodeTemplate['lib'] = ""
        nodeTemplate['type'] = "loopEnd"
        nodeTemplate['name'] = self.canvasRef().graphManager.getUniqNodeName("loopEnd")
        nodeTemplate['x'] = self.scenePos().x() + self.geometry().width() + 30
        nodeTemplate['y'] = self.scenePos().y()
        nodeTemplate['uuid'] = str(uuid.uuid4())
        endNode = self.canvasRef()._createNode(nodeTemplate)
        self.getPinSG("Paired block").setData(str(endNode.path()))
        endNode.getPinSG("Paired block").setData(self.path())
        self.canvasRef().connectPins(self.getPinSG("LoopBody"), endNode.getPinSG(DEFAULT_IN_EXEC_NAME))

    def paint(self, painter, option, widget):
        self.computeHull()
        self.backDrop.update()
        NodePainter.default(self, painter, option, widget)
