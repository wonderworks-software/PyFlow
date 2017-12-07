from FunctionLibrary import *
from AGraphCommon import *
from Reference import Ref


class MathLib(FunctionLibraryBase):
    """doc string for MathLib"""
    def __init__(self):
        super(MathLib, self).__init__()

    @staticmethod
    @annotated(returns=DataTypes.Float)
    def AddFloat2(A=(DataTypes.Float, 0.0), B=(DataTypes.Float, 0.0)):
        return A + B

    @staticmethod
    @annotated(returns=DataTypes.Int)
    def AddInt2(A=(DataTypes.Int, 0), B=(DataTypes.Int, 0)):
        return A + B
