from PyFlow.UI.Canvas.UINodeBase import UINodeBase


class UISequenceNode(UINodeBase):
    def __init__(self, raw_node):
        super(UISequenceNode, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add out pin")
        actionAddOut.triggered.connect(self.onAddOutPin)

    def onAddOutPin(self):
        rawPin = self._rawNode.createOutputPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.setDynamic(True)
        uiPin.setDisplayName("Then {}".format(rawPin.name))
        self.updateWidth()
        return uiPin
