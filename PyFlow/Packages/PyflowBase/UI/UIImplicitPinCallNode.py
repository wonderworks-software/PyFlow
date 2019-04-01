from PyFlow.UI.Graph.UINodeBase import UINodeBase
import uuid


class UIImplicitPinCall(UINodeBase):
    def __init__(self, raw_node):
        super(UIImplicitPinCall, self).__init__(raw_node)
        findPinAction = self._menu.addAction("FindPin")
        findPinAction.triggered.connect(self.OnFindPin)

    def OnFindPin(self):
        # we can safely access member .uidInp of raw node. Since we know that this UI class will
        # be used only with implicitPinCall underlined class
        # this relationship defined in UINodeFactory.py
        uidStr = self._rawNode.uidInp.getData()
        if len(uidStr) == 0:
            return
        try:
            uid = uuid.UUID(uidStr)
            pin = self.graph().findPin(uid)
            self.graph().frameRect(pin.owningNode().sceneBoundingRect())
            pin.highlight()
        except Exception as e:
            print(e)
            pass
