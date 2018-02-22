from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
import pymel.core as pm
import pyrr


class MayaLib(FunctionLibraryBase):
    '''
    Autodesk maya
    '''
    def __init__(self):
        super(MayaLib, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), nodeType=NodeTypes.Callable, meta={'Category': 'Maya', 'Keywords': []})
    def objExists(DagPath=(DataTypes.String, "")):
        return pm.objExists(DagPath)

    @staticmethod
    @implementNode(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'Maya', 'Keywords': []})
    def setTransform(DagPath=(DataTypes.String, ""), Location=(DataTypes.FloatVector3, pyrr.Vector3()), Rotation=(DataTypes.FloatVector3, pyrr.Vector3()), Scale=(DataTypes.FloatVector3, pyrr.Vector3([1.0, 1.0, 1.0])), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        '''
        Sets transform to PyNode
        '''
        if pm.objExists(DagPath):
            node = pm.PyNode(DagPath)
            node.t.set(Location.x, Location.y, Location.z)
            node.r.set(Rotation.x, Rotation.y, Rotation.z)
            node.s.set(Scale.x, Scale.y, Scale.z)
            Result.setData(True)
        else:
            Result.setData(False)
