from Qt import QtWidgets

from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.Widget import GraphWidgetUI
from PyFlow.Core.GraphTree import GraphTree
from PyFlow.Core.Common import *


class UIsubgraph(UINodeBase):
    def __init__(self, raw_node):
        super(UIsubgraph, self).__init__(raw_node)

    def updateSize(self, name):
        self.updateWidth()
        self.updateNodeShape()

    def mouseDoubleClickEvent(self, event):
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()

    def OnDoubleClick(self, pos):
        GraphTree().switchGraph(self._rawNode.rawGraph.name)

    def kill(self):
        super(UIsubgraph, self).kill()
