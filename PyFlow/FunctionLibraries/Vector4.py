from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class Vector4(FunctionLibraryBase):
    '''doc string for Vector4'''
    def __init__(self):
        super(Vector4, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector4', 'Keywords': []})
    def zeroVector4():
        '''zero vector4'''
        return pyrr.Vector4()

    @staticmethod
    @implementNode(returns=(DataTypes.String, str(pyrr.Vector4())), meta={'Category': 'Math|Vector4', 'Keywords': []})
    def vector4ToString(v=(DataTypes.FloatVector4, pyrr.Vector4())):
        return str(v)
