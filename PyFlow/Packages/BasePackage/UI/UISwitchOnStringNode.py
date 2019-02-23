from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.Settings import *


class UISwitchOnString(UINodeBase):
    def __init__(self, raw_node):
        super(UISwitchOnString, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("add out pin")
        actionAddOut.triggered.connect(self.onAddOutPin)

    def onAddOutPin(self):
        rawPin = self._rawNode.addOutPin()
        uiPin = self._createUIPinWrapper(rawPin)
        return uiPin

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        createdPinNames = [pin.name for pin in self.outputs.values()]
        for outPin in jsonTemplate["outputs"]:
            if outPin['name'] not in createdPinNames:
                uiPin = self.onAddOutPin()
                # TODO: restore names
