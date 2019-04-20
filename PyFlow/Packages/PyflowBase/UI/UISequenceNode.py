from PyFlow.UI.Canvas.UINodeBase import UINodeBase


class UISequenceNode(UINodeBase):
    def __init__(self, raw_node):
        super(UISequenceNode, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add out pin")
        actionAddOut.triggered.connect(self.onAddOutPin)
        self.outPins = set()

    def onPinWasKilled(self, uiPin):
        print("reorder pins", uiPin.getName())
        index = 1
        for outPin in self.UIoutputs.values():
            outPin.setName(str(index))
            outPin.setDisplayName(str(index))
            index += 1
        self.outPins.remove(uiPin)

    def onAddOutPin(self):
        rawPin = self._rawNode.createOutputPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.OnPinDeleted.connect(self.onPinWasKilled)
        self.outPins.add(uiPin)
        uiPin.setDynamic(True)
        # uiPin.setDisplayName("Then {}".format(rawPin.name))
        self.updateWidth()
        return uiPin
