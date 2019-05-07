from PyFlow.UI.Canvas.UINodeBase import UINodeBase


class UISequenceNode(UINodeBase):
    def __init__(self, raw_node):
        super(UISequenceNode, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add out pin")
        actionAddOut.triggered.connect(self.onAddOutPin)

    def onPinWasKilled(self, uiPin):
        index = 1
        uiPin.OnPinDeleted.disconnect(self.onPinWasKilled)
        pins = list(self.UIoutputs.values())
        pins.sort(key=lambda x: int(x._rawPin.name))
        for outPin in pins:
            outPin.setName(str(index), True)
            outPin.setDisplayName("Then {}".format(index))
            index += 1

    def postCreate(self, jsonTemplate=None):
        super(UISequenceNode, self).postCreate(jsonTemplate)
        for outPin in self.UIoutputs.values():
            outPin.setDisplayName("Then {}".format(outPin._rawPin.name))
            outPin.OnPinDeleted.connect(self.onPinWasKilled)

    def onAddOutPin(self):
        rawPin = self._rawNode.createOutputPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.OnPinDeleted.connect(self.onPinWasKilled)
        uiPin.setDisplayName("Then {}".format(rawPin.name))
        self.updateWidth()
        return uiPin
