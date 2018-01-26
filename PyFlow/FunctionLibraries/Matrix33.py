from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class Matrix33(FunctionLibraryBase):
    '''doc string for Matrix33'''
    def __init__(self):
        super(Matrix33, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Matrix33', 'Keywords': []})
    def zeroMatrix33():
        '''zero matrix33'''
        return pyrr.Matrix33()

    @staticmethod
    @implementNode(returns=(DataTypes.String, str(pyrr.Matrix33())), meta={'Category': 'Math|Matrix33', 'Keywords': []})
    def matrix33ToString(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        return str(m)

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33.identity()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Matrix33', 'Keywords': []})
    def identityMatrix33():
        '''identity matrix33'''
        return pyrr.Matrix33.identity()
