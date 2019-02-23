from PyFlow.Packages.BasePackage.Nodes.switchOnString import switchOnString
from PyFlow.Packages.BasePackage.UI.UISwitchOnStringNode import UISwitchOnString
from PyFlow.UI.UINodeBase import UINodeBase


def createUINode(raw_instance):
    if isinstance(raw_instance, switchOnString):
        return UISwitchOnString(raw_instance)
    return UINodeBase(raw_instance)
