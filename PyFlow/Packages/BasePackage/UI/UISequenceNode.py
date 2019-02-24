from PyFlow.UI.UINodeBase import UINodeBase


class UISequenceNode(UINodeBase):
    def __init__(self, raw_node):
        super(UISequenceNode, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add out pin")
        actionAddOut.triggered.connect(self.onAddOutPin)

    def onAddOutPin(self):
        rawPin = self._rawNode.addOutPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.setDynamic(True)
        uiPin.setDisplayName("Then {}".format(str(len(self.outputs) - 1)))
        return uiPin

    def updateNodeShape(self, label=None):
        UINodeBase.updateNodeShape(self, label)
        for i in range(0, len(self.outputs)):
            pin = list(self.outputs.values())[i]
            pin.getWrapper()().setName(str(i))
            pin.getWrapper()().setDisplayName("Then {}".format(i))

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        # recreate dynamically created pins
        createdPinNames = [pin.name for pin in self.outputs.values()]
        for outPin in jsonTemplate["outputs"]:
            if outPin['name'] not in createdPinNames:
                uiPin = self.onAddOutPin()
