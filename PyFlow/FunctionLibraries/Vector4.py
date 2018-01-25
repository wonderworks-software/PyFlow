from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class Vector4(FunctionLibraryBase):
    '''doc string for Vector4'''
    def __init__(self):
        super(Vector4, self).__init__()

    @staticmethod
    @implementNode(returns=DataTypes.FloatVector4, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Vector4', 'Keywords': []})
    def zeroVector4():
        '''zero vector4'''
        return pyrr.Vector4()
