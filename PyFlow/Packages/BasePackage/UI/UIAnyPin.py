from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *
from PyFlow.UI.Settings import Colors
from PyFlow import getAllPinClasses

from PyFlow.UI.UIPinBase import UIPinBase
class UIAnyPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIAnyPin, self).__init__(owningNode, raw_pin)
             
        
    
