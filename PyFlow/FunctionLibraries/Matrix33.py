from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class Matrix33(FunctionLibraryBase):
    '''doc string for Matrix33'''
    def __init__(self):
        super(Matrix33, self).__init__()

    @staticmethod
    @annotated(returns=DataTypes.Matrix33, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Matrix33', 'Keywords': []})
    def zeroMatrix33():
        '''zero matrix33'''
        return pyrr.Matrix33()

    @staticmethod
    @annotated(returns=DataTypes.Matrix33, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Matrix33', 'Keywords': []})
    def identityMatrix33():
        '''identity matrix33'''
        return pyrr.Matrix33.identity()
