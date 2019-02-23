from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.Settings import *


class UISwitchOnString(UINodeBase):
    def __init__(self, raw_node, w=80, color=Colors.NodeBackgrounds, headColor=Colors.NodeNameRect, bUseTextureBg=True):
        super(UISwitchOnString, self).__init__(raw_node, w=w, color=color, headColor=headColor, bUseTextureBg=bUseTextureBg)
