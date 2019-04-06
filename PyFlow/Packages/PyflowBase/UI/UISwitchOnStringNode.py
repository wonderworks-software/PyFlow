from PyFlow.UI.Canvas.UINodeBase import UINodeBase


class UISwitchOnString(UINodeBase):
    def __init__(self, raw_node):
        super(UISwitchOnString, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("add out pin")
        actionAddOut.triggered.connect(self.onAddOutPin)
        self.resizable = True

    def onAddOutPin(self):
        rawPin = self._rawNode.addOutPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.setRenamingEnabled(True)
        uiPin.setDynamic(True)
        return uiPin

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        # recreate dynamically created pins
        createdPinNames = [pin.name for pin in self.outputs.values()]
        for outPin in jsonTemplate["outputs"]:
            if outPin['name'] not in createdPinNames:
                uiPin = self.onAddOutPin()
