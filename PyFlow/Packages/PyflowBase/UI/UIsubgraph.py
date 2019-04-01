from Qt import QtWidgets

from PyFlow.UI.Graph.UINodeBase import UINodeBase
from PyFlow.UI.Graph.Widget import GraphWidgetUI

from PyFlow.Core.GraphTree import GraphTree
from PyFlow.Core.Common import *


class UIsubgraph(UINodeBase):
    def __init__(self, raw_node):
        super(UIsubgraph, self).__init__(raw_node)

    def updateSize(self, name):
        self.updateWidth()
        self.updateNodeShape()

    def inputPinExposed(self, rawPin):
        # create ui wrapper for raw exposed pin
        # and connect signals
        uiCompanionPin = self._createUIPinWrapper(rawPin)
        rawPin.killed.connect(uiCompanionPin.kill)
        pass

    def mouseDoubleClickEvent(self, event):
        GraphTree().switchGraph(self._rawNode.rawGraph.name)
        event.accept()

    def kill(self):
        super(UIsubgraph, self).kill()
