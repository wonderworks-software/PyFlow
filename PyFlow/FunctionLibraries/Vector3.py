from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class Vector3(FunctionLibraryBase):
    '''doc string for Vector3'''
    def __init__(self):
        super(Vector3, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def zeroVector3():
        '''zero Vector3'''
        v = pyrr.Vector3()
        return v

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, True), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def Vector3Equals(a=(DataTypes.FloatVector3, pyrr.Vector3()), b=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Check if vectors are equals'''
        return a == b

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def makeVector3(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0)):
        '''creates Vector3 from given components'''
        return pyrr.Vector3([a, b, c])

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def addVector3(a=(DataTypes.FloatVector3, pyrr.Vector3()), b=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''adds vector a and b'''
        return a + b

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def substractVector3(a=(DataTypes.FloatVector3, pyrr.Vector3()), b=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''substracts vector a and b'''
        return a - b

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def dotVector3(a=(DataTypes.FloatVector3, pyrr.Vector3()), b=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''dot product of two vectors'''
        return a | b

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def crossVector3(a=(DataTypes.FloatVector3, pyrr.Vector3()), b=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''cross product of two vectors'''
        return a ^ b

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def rotateVector3byM33(v=(DataTypes.FloatVector3, pyrr.Vector3()), m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''rotates a vector3 by a matrix33'''
        return m * v

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector3', 'Keywords': []})
    def rotateVector3byQuat(v=(DataTypes.FloatVector3, pyrr.Vector3()), q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''rotates a vector3 by a quaternion'''
        return q * v
