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


from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UINodeBase import UINodeBase


class UIRerouteNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIRerouteNode, self).__init__(raw_node)
        self.hover = False
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray
        self.image = RESOURCES_DIR + "/reroute.svg"

    def kill(self, *args, **kwargs):
        inp = list(self.UIinputs.values())[0]
        out = list(self.UIoutputs.values())[0]
        newOuts = []
        for i in self.UIoutputs.values():
            for connection in i.connections:
                newOuts.append([connection.destination(),
                                connection.drawDestination])
        if inp.connections:
            source = inp.connections[0].source()
            for out in newOuts:
                drawSource = inp.connections[0].drawSource
                self.canvasRef().connectPins(source, out[0])
        super(UIRerouteNode, self).kill()

    def postCreate(self, jsonTemplate=None):
        super(UIRerouteNode, self).postCreate(jsonTemplate)
        self.input = self.getPinSG("in")
        self.output = self.getPinSG("out")
        self.updateNodeShape()

    def paint(self, painter, option, widget):
        NodePainter.default(self, painter, option, widget)
