from PyFlow.Packages.BasePackage.Nodes.switchOnString import switchOnString
from PyFlow.Packages.BasePackage.Nodes.getVar import getVar
from PyFlow.Packages.BasePackage.Nodes.setVar import setVar
from PyFlow.Packages.BasePackage.Nodes.implicitPinCall import implicitPinCall
from PyFlow.Packages.BasePackage.Nodes.sequence import sequence
from PyFlow.Packages.BasePackage.Nodes.commentNode import commentNode
from PyFlow.Packages.BasePackage.UI.UISwitchOnStringNode import UISwitchOnString
from PyFlow.Packages.BasePackage.UI.UIGetVarNode import UIGetVarNode
from PyFlow.Packages.BasePackage.UI.UISetVarNode import UISetVarNode
from PyFlow.Packages.BasePackage.UI.UIImplicitPinCallNode import UIImplicitPinCall
from PyFlow.Packages.BasePackage.UI.UISequenceNode import UISequenceNode
from PyFlow.Packages.BasePackage.UI.UIcommentNode import UIcommentNode
from PyFlow.UI.UINodeBase import UINodeBase


def createUINode(raw_instance):
    if isinstance(raw_instance, getVar):
        return UIGetVarNode(raw_instance)
    if isinstance(raw_instance, setVar):
        return UISetVarNode(raw_instance)
    if isinstance(raw_instance, switchOnString):
        return UISwitchOnString(raw_instance)
    if isinstance(raw_instance, implicitPinCall):
        return UIImplicitPinCall(raw_instance)
    if isinstance(raw_instance, sequence):
        return UISequenceNode(raw_instance)
    if isinstance(raw_instance, commentNode):
        return UIcommentNode(raw_instance)
    return UINodeBase(raw_instance)
