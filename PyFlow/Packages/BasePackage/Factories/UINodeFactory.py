from PyFlow.Packages.BasePackage.Nodes.switchOnString import switchOnString
from PyFlow.Packages.BasePackage.Nodes.implicitPinCall import implicitPinCall
from PyFlow.Packages.BasePackage.UI.UISwitchOnStringNode import UISwitchOnString
from PyFlow.Packages.BasePackage.UI.UIImplicitPinCallNode import UIImplicitPinCall
from PyFlow.UI.UINodeBase import UINodeBase


def createUINode(raw_instance):
    if isinstance(raw_instance, switchOnString):
        return UISwitchOnString(raw_instance)
    if isinstance(raw_instance, implicitPinCall):
        return UIImplicitPinCall(raw_instance)
    return UINodeBase(raw_instance)
