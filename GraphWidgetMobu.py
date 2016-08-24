from pyfbsdk import *
from pyfbsdk_additions import *
from PySide import QtGui
from PySide import QtCore
from PySide import shiboken
import sys
path = r'd:\GIT\NodesRepo'
if path not in sys.path:
    sys.path.append(path)
import AGraphPySide
reload(AGraphPySide)
from Launcher import W

class NativeWidgetHolder(FBWidgetHolder):

    def WidgetCreate(self, pWidgetParent):
        # self.mNativeQtWidget = AGraphPySide.Widget.GraphWidget('in mobu')
        self.mNativeQtWidget = W()
        return shiboken.getCppPointer(self.mNativeQtWidget)[0]


class CharacterReplacerClass(FBTool):

    def __init__(self, name):

        FBTool.__init__(self, name)
        self.mNativeWidgetHolder = NativeWidgetHolder()
        self.BuildLayout()
        self.StartSizeX = 315
        self.StartSizeY = 550

    def BuildLayout(self):

        x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
        y = FBAddRegionParam(0, FBAttachType.kFBAttachTop, "")
        w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
        h = FBAddRegionParam(0, FBAttachType.kFBAttachBottom, "")
        self.AddRegion("main", "main", x, y, w, h)
        self.SetControl("main", self.mNativeWidgetHolder)

def SHOW():

    gToolName = "Graph in mobu"
    gDEVELOPMENT = True
    if gDEVELOPMENT:
        FBDestroyToolByName(gToolName)
    if gToolName in FBToolList:
        tool = FBToolList[gToolName]
        ShowTool(tool)
    else:
        tool = CharacterReplacerClass(gToolName)
        FBAddTool(tool)
        if gDEVELOPMENT:
            ShowTool(tool)

SHOW()
