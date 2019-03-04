from PyFlow.UI.UIPinBase import UIPinBase
from PyFlow.Packages.BasePackage.Pins.AnyPin import AnyPin
from PyFlow.Packages.BasePackage.UI.UIAnyPin import UIAnyPin

def createUIPin(owningNode, raw_instance):
	if isinstance(raw_instance,AnyPin):
		return UIAnyPin(owningNode, raw_instance)
	else:
		return UIPinBase(owningNode, raw_instance)
