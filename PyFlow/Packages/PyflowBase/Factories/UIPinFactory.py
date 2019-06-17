from PyFlow.UI.Canvas.UIPinBase import UIPinBase
from PyFlow.Packages.PyFlowBase.Pins.AnyPin import AnyPin
from PyFlow.Packages.PyFlowBase.Pins.ExecPin import ExecPin

from PyFlow.Packages.PyFlowBase.UI.UIAnyPin import UIAnyPin
from PyFlow.Packages.PyFlowBase.UI.UIExecPin import UIExecPin


def createUIPin(owningNode, raw_instance):
    if isinstance(raw_instance, AnyPin):
        return UIAnyPin(owningNode, raw_instance)
    elif isinstance(raw_instance, ExecPin):
        return UIExecPin(owningNode, raw_instance)
    else:
        return UIPinBase(owningNode, raw_instance)
