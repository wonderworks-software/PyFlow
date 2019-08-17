## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from PyFlow.Packages.PyFlowBase.Nodes.switchOnString import switchOnString
from PyFlow.Packages.PyFlowBase.Nodes.getVar import getVar
from PyFlow.Packages.PyFlowBase.Nodes.setVar import setVar
from PyFlow.Packages.PyFlowBase.Nodes.sequence import sequence
from PyFlow.Packages.PyFlowBase.Nodes.pythonNode import pythonNode
from PyFlow.Packages.PyFlowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyFlowBase.Nodes.stickyNote import stickyNote
from PyFlow.Packages.PyFlowBase.Nodes.reroute import reroute
from PyFlow.Packages.PyFlowBase.Nodes.rerouteExecs import rerouteExecs
from PyFlow.Packages.PyFlowBase.Nodes.graphNodes import (
    graphInputs,
    graphOutputs
)
from PyFlow.Packages.PyFlowBase.Nodes.floatRamp import floatRamp
from PyFlow.Packages.PyFlowBase.Nodes.colorRamp import colorRamp

from PyFlow.Packages.PyFlowBase.Nodes.compound import compound
from PyFlow.Packages.PyFlowBase.Nodes.constant import constant
from PyFlow.Packages.PyFlowBase.Nodes.convertTo import convertTo
from PyFlow.Packages.PyFlowBase.Nodes.makeDict import makeDict
from PyFlow.Packages.PyFlowBase.Nodes.makeAnyDict import makeAnyDict

from PyFlow.Packages.PyFlowBase.Nodes.forLoopBegin import forLoopBegin

from PyFlow.Packages.PyFlowBase.Nodes.imageDisplay import imageDisplay
from PyFlow.Packages.PyFlowBase.UI.UIQimageDisplay import UIQimageDisplay

from PyFlow.Packages.PyFlowBase.UI.UISwitchOnStringNode import UISwitchOnString
from PyFlow.Packages.PyFlowBase.UI.UIGetVarNode import UIGetVarNode
from PyFlow.Packages.PyFlowBase.UI.UISetVarNode import UISetVarNode
from PyFlow.Packages.PyFlowBase.UI.UISequenceNode import UISequenceNode
from PyFlow.Packages.PyFlowBase.UI.UICommentNode import UICommentNode
from PyFlow.Packages.PyFlowBase.UI.UIstickyNote import UIstickyNote
from PyFlow.Packages.PyFlowBase.UI.UIRerouteNode import UIRerouteNode
from PyFlow.Packages.PyFlowBase.UI.UIRerouteNodeSmall import UIRerouteNodeSmall
from PyFlow.Packages.PyFlowBase.UI.UIPythonNode import UIPythonNode
from PyFlow.Packages.PyFlowBase.UI.UIGraphNodes import (
    UIGraphInputs,
    UIGraphOutputs
)
from PyFlow.Packages.PyFlowBase.UI.UIFloatRamp import UIFloatRamp
from PyFlow.Packages.PyFlowBase.UI.UIColorRamp import UIColorRamp

from PyFlow.Packages.PyFlowBase.UI.UICompoundNode import UICompoundNode
from PyFlow.Packages.PyFlowBase.UI.UIConstantNode import UIConstantNode
from PyFlow.Packages.PyFlowBase.UI.UIConvertToNode import UIConvertToNode
from PyFlow.Packages.PyFlowBase.UI.UIMakeDictNode import UIMakeDictNode
from PyFlow.Packages.PyFlowBase.UI.UIForLoopBeginNode import UIForLoopBeginNode

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
    if isinstance(raw_instance, stickyNote):
        return UIstickyNote(raw_instance)
    if isinstance(raw_instance, reroute) or isinstance(raw_instance, rerouteExecs):
        return UIRerouteNodeSmall(raw_instance)
    if isinstance(raw_instance, graphInputs):
        return UIGraphInputs(raw_instance)
    if isinstance(raw_instance, graphOutputs):
        return UIGraphOutputs(raw_instance)
    if isinstance(raw_instance, compound):
        return UICompoundNode(raw_instance)
    if isinstance(raw_instance, pythonNode):
        return UIPythonNode(raw_instance)
    if isinstance(raw_instance, constant):
        return UIConstantNode(raw_instance)
    if isinstance(raw_instance, convertTo):
        return UIConvertToNode(raw_instance)
    if isinstance(raw_instance, makeDict):
        return UIMakeDictNode(raw_instance)
    if isinstance(raw_instance, makeAnyDict):
        return UIMakeDictNode(raw_instance)
    if isinstance(raw_instance, floatRamp):
        return UIFloatRamp(raw_instance)
    if isinstance(raw_instance, colorRamp):
        return UIColorRamp(raw_instance)
    if isinstance(raw_instance, imageDisplay):
        return UIQimageDisplay(raw_instance)
    if isinstance(raw_instance,forLoopBegin):
        return UIForLoopBeginNode(raw_instance)
    return UINodeBase(raw_instance)
