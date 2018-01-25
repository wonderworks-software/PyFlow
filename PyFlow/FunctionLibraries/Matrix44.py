from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class Matrix44(FunctionLibraryBase):
    '''doc string for Matrix44'''
    def __init__(self):
        super(Matrix44, self).__init__()

    @staticmethod
    @implementNode(returns=DataTypes.Matrix44, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Matrix44', 'Keywords': []})
    def zeroMatrix44():
        '''zero matrix44'''
        return pyrr.Matrix44()

    @staticmethod
    @implementNode(returns=DataTypes.Matrix44, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Matrix44', 'Keywords': []})
    def identityMatrix44():
        '''identity matrix44'''
        return pyrr.Matrix44.identity()
