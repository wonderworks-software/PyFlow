import pymel.core as pm
import pyrr

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.BasePackage import PACKAGE_NAME


class MayaLib(FunctionLibraryBase):
    '''
    Autodesk maya
    '''
    def __init__(self):
        super(MayaLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), nodeType=NodeTypes.Callable, meta={'Category': 'Maya', 'Keywords': []}, packageName=PACKAGE_NAME)
    def objExists(DagPath=('StringPin', "")):
        return pm.objExists(DagPath)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'Maya', 'Keywords': []}, packageName=PACKAGE_NAME)
    def setTransform(DagPath=('StringPin', ""),
                     Location=('FloatVector3Pin', pyrr.Vector3()),
                     Rotation=('FloatVector3Pin', pyrr.Vector3()),
                     Scale=('FloatVector3Pin', pyrr.Vector3([1.0, 1.0, 1.0])),
                     Result=("Reference", ('BoolPin', False))):
        '''
        Sets transform to PyNode
        '''
        if pm.objExists(DagPath):
            node = pm.PyNode(DagPath)
            node.t.set(Location.x, Location.y, Location.z)
            node.r.set(Rotation.x, Rotation.y, Rotation.z)
            node.s.set(Scale.x, Scale.y, Scale.z)
            Result(True)
        else:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('ListPin', []), meta={'Category': 'Maya', 'Keywords': []}, packageName=PACKAGE_NAME)
    def listSelection():
        return pm.ls(sl=True)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Maya', 'Keywords': []}, packageName=PACKAGE_NAME)
    def currentFrame():
        return pm.currentTime(q=True)

    @staticmethod
    @IMPLEMENT_NODE(returns=None,
                    nodeType=NodeTypes.Callable,
                    meta={'Category': 'Maya', 'Keywords': []}, packageName=PACKAGE_NAME)
    def setCurrentFrame(CurrentFrame=('IntPin', 0)):
        pm.setCurrentTime(CurrentFrame)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Maya', 'Keywords': []}, packageName=PACKAGE_NAME)
    def frameRange(Min=("Reference", ('IntPin', 0)),
                   Max=("Reference", ('IntPin', 0))):
        '''
        Returns time slader min and max.
        '''
        Min(pm.playbackOptions(q=True, min=True))
        Max(pm.playbackOptions(q=True, max=True))

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'Maya', 'Keywords': []}, packageName=PACKAGE_NAME)
    def setKeyFrame(DagPath=('StringPin', ''),
                    AttributeName=('StringPin', ''),
                    Result=("Reference", ('BoolPin', False))):

        if not pm.objExists(DagPath):
            Result(False)
            return

        if AttributeName == '':
            pm.setKeyframe(DagPath)
            Result(True)
        else:
            try:
                pm.setKeyframe(DagPath, at=AttributeName)
                Result(True)
            except:
                Result(False)
