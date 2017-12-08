from FunctionLibrary import *
from AGraphCommon import *


class MathLib(FunctionLibraryBase):
    """doc string for MathLib"""
    def __init__(self):
        super(MathLib, self).__init__()

    @staticmethod
    @annotated(returns=DataTypes.Float, nodeType=NodeTypes.Callable, meta={'Category': 'Math', 'Keywords': []})
    def AddFloat2(A=(DataTypes.Float, 0.0), B=(DataTypes.Float, 0.0)):
        return A + B

    @staticmethod
    @annotated(returns=DataTypes.Int, meta={'Category': 'Math', 'Keywords': []})
    def AddInt2(A=(DataTypes.Int, 0), B=(DataTypes.Int, 0)):
        return A + B

    @staticmethod
    @annotated(returns=DataTypes.Float, nodeType=NodeTypes.Callable, meta={'Category': 'Math', 'Keywords': []})
    def AddFloatWithResult(A=(DataTypes.Float, 0.0), B=(DataTypes.Float, 0.0), Result=(DataTypes.Reference, DataTypes.Bool)):
        return A + B
