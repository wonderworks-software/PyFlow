from PyFlow.UI.Canvas.UICommon import DEFAULT_IN_EXEC_NAME
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import NodeActionButtonInfo


class UISwitchOnString(UINodeBase):
    def __init__(self, raw_node):
        super(UISwitchOnString, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add out pin")
        actionAddOut.setToolTip("Adds an option")
        actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
        actionAddOut.triggered.connect(self.onAddOutPin)

    def postCreate(self, jsonTemplate=None):
        super(UISwitchOnString, self).postCreate(jsonTemplate=jsonTemplate)
        inExecPin = self.getPinSG(DEFAULT_IN_EXEC_NAME)
        inExecPin.bLabelHidden = True

    def onAddOutPin(self):
        rawPin = self._rawNode.addOutPin()
        uiPin = self._createUIPinWrapper(rawPin)
        return uiPin
