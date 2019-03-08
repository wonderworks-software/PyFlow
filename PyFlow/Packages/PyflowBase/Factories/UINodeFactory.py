from PyFlow.Packages.PyflowBase.Nodes.switchOnString import switchOnString
from PyFlow.Packages.PyflowBase.Nodes.getVar import getVar
from PyFlow.Packages.PyflowBase.Nodes.setVar import setVar
from PyFlow.Packages.PyflowBase.Nodes.implicitPinCall import implicitPinCall
from PyFlow.Packages.PyflowBase.Nodes.sequence import sequence
from PyFlow.Packages.PyflowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyflowBase.UI.UISwitchOnStringNode import UISwitchOnString
from PyFlow.Packages.PyflowBase.UI.UIGetVarNode import UIGetVarNode
from PyFlow.Packages.PyflowBase.UI.UISetVarNode import UISetVarNode
from PyFlow.Packages.PyflowBase.UI.UIImplicitPinCallNode import UIImplicitPinCall
from PyFlow.Packages.PyflowBase.UI.UISequenceNode import UISequenceNode
from PyFlow.Packages.PyflowBase.UI.UIcommentNode import UIcommentNode
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
