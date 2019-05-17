from PyFlow.Packages.PyflowBase.Nodes.switchOnString import switchOnString
from PyFlow.Packages.PyflowBase.Nodes.getVar import getVar
from PyFlow.Packages.PyflowBase.Nodes.setVar import setVar
from PyFlow.Packages.PyflowBase.Nodes.sequence import sequence
from PyFlow.Packages.PyflowBase.Nodes.pythonNode import pythonNode
from PyFlow.Packages.PyflowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyflowBase.Nodes.reroute import reroute
from PyFlow.Packages.PyflowBase.Nodes.rerouteExecs import rerouteExecs
from PyFlow.Packages.PyflowBase.Nodes.graphNodes import (
    graphInputs,
    graphOutputs
)
from PyFlow.Packages.PyflowBase.Nodes.compound import compound
from PyFlow.Packages.PyflowBase.Nodes.constant import constant

from PyFlow.Packages.PyflowBase.UI.UISwitchOnStringNode import UISwitchOnString
from PyFlow.Packages.PyflowBase.UI.UIGetVarNode import UIGetVarNode
from PyFlow.Packages.PyflowBase.UI.UISetVarNode import UISetVarNode
from PyFlow.Packages.PyflowBase.UI.UISequenceNode import UISequenceNode
from PyFlow.Packages.PyflowBase.UI.UICommentNode import UICommentNode
from PyFlow.Packages.PyflowBase.UI.UIRerouteNode import UIRerouteNode
from PyFlow.Packages.PyflowBase.UI.UIPythonNode import UIPythonNode
from PyFlow.Packages.PyflowBase.UI.UIGraphNodes import (
    UIGraphInputs,
    UIGraphOutputs
)
from PyFlow.Packages.PyflowBase.UI.UICompoundNode import UICompoundNode
from PyFlow.Packages.PyflowBase.UI.UIConstantNode import UIConstantNode
from PyFlow.UI.Canvas.UINodeBase import UINodeBase


def createUINode(raw_instance):
    if isinstance(raw_instance, getVar):
        return UIGetVarNode(raw_instance)
    if isinstance(raw_instance, setVar):
        return UISetVarNode(raw_instance)
    if isinstance(raw_instance, switchOnString):
        return UISwitchOnString(raw_instance)
    if isinstance(raw_instance, sequence):
        return UISequenceNode(raw_instance)
    if isinstance(raw_instance, commentNode):
        return UICommentNode(raw_instance)
    if isinstance(raw_instance, reroute) or isinstance(raw_instance, rerouteExecs):
        return UIRerouteNode(raw_instance)
    if isinstance(raw_instance, graphInputs):
        return UIGraphInputs(raw_instance)
    if isinstance(raw_instance, graphOutputs):
        return UIGraphOutputs(raw_instance)
    if isinstance(raw_instance, compound):
        return UICompoundNode(raw_instance)
    if isinstance(raw_instance, pythonNode):
        return UIPythonNode(raw_instance)
    if isinstance(raw_instance,constant):
        return UIConstantNode(raw_instance)
    return UINodeBase(raw_instance)
