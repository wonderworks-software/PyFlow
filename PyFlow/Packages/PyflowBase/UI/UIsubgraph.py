from Qt import QtWidgets

from PyFlow.UI.Graph.UINodeBase import UINodeBase

from PyFlow.Core.GraphTree import GraphTree
from PyFlow.Core.Common import *


class UIsubgraph(UINodeBase):
    def __init__(self, raw_node):
        super(UIsubgraph, self).__init__(raw_node)

    def updateSize(self, name):
        self.updateWidth()
        self.updateNodeShape()

    def onGraphInputPinExposed(self, rawPin):
        # create ui wrapper for raw exposed pin
        # and connect signals
        uiCompanionPin = self._createUIPinWrapper(rawPin)

    def serialize(self):
        default = super(UIsubgraph, self).serialize()

        return default

    def onGraphOutputPinExposed(self, rawPin):
        uiCompanionPin = self._createUIPinWrapper(rawPin)

    def mouseDoubleClickEvent(self, event):
        GraphTree().switchGraph(self._rawNode.rawGraph.name)
        event.accept()

    def kill(self):
        super(UIsubgraph, self).kill()

    def postCreate(self, jsonTemplate=None):
        super(UIsubgraph, self).postCreate(jsonTemplate)
