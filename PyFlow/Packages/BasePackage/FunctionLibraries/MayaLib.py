from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
import pymel.core as pm
import pyrr


class MayaLib(FunctionLibraryBase):
    '''
    Autodesk maya
    '''
    def __init__(self):
        super(MayaLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), nodeType=NodeTypes.Callable, meta={'Category': 'Maya', 'Keywords': []})
    def objExists(DagPath=(DataTypes.String, "")):
        return pm.objExists(DagPath)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'Maya', 'Keywords': []})
    def setTransform(DagPath=(DataTypes.String, ""),
                     Location=(DataTypes.FloatVector3, pyrr.Vector3()),
                     Rotation=(DataTypes.FloatVector3, pyrr.Vector3()),
                     Scale=(DataTypes.FloatVector3, pyrr.Vector3([1.0, 1.0, 1.0])),
                     Result=(DataTypes.Reference, (DataTypes.Bool, False))):
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
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'Maya', 'Keywords': []})
    def listSelection():
        return pm.ls(sl=True)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Maya', 'Keywords': []})
    def currentFrame():
        return pm.currentTime(q=True)

    @staticmethod
    @IMPLEMENT_NODE(returns=None,
                    nodeType=NodeTypes.Callable,
                    meta={'Category': 'Maya', 'Keywords': []})
    def setCurrentFrame(CurrentFrame=(DataTypes.Int, 0)):
        pm.setCurrentTime(CurrentFrame)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Maya', 'Keywords': []})
    def frameRange(Min=(DataTypes.Reference, (DataTypes.Int, 0)),
                   Max=(DataTypes.Reference, (DataTypes.Int, 0))):
        '''
        Returns time slader min and max.
        '''
        Min(pm.playbackOptions(q=True, min=True))
        Max(pm.playbackOptions(q=True, max=True))

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'Maya', 'Keywords': []})
    def setKeyFrame(DagPath=(DataTypes.String, ''),
                    AttributeName=(DataTypes.String, ''),
                    Result=(DataTypes.Reference, (DataTypes.Bool, False))):

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
