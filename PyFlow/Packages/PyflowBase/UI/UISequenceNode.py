from PyFlow.UI.Canvas.UINodeBase import UINodeBase


class UISequenceNode(UINodeBase):
    def __init__(self, raw_node):
        super(UISequenceNode, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add out pin")
        actionAddOut.triggered.connect(self.onAddOutPin)
        self.outPins = set()

    def onPinWasKilled(self, uiPin):
        index = 1
        uiPin.OnPinDeleted.disconnect(self.onPinWasKilled)
        for outPin in self.UIoutputs.values():
            outPin.setName(str(index))
            outPin.setDisplayName("Then {}".format(index))
            index += 1
        self.outPins.remove(uiPin)

    def postCreate(self, jsonTemplate=None):
        super(UISequenceNode, self).postCreate(jsonTemplate)
        for outPin in self.UIoutputs.values():
            outPin.setDisplayName("Then {}".format(outPin._rawPin.name))

    def onAddOutPin(self):
        rawPin = self._rawNode.createOutputPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.OnPinDeleted.connect(self.onPinWasKilled)
        uiPin.setDisplayName("Then {}".format(rawPin.name))
        self.outPins.add(uiPin)
        uiPin.setDynamic(True)
        self.updateWidth()
        return uiPin
