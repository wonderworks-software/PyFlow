from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *


class ArrayLib(FunctionLibraryBase):
    '''doc string for ArrayLib'''
    def __init__(self):
        super(ArrayLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'Array', 'Keywords': []})
    def arrayToString(arr=('ListPin', [])):
        return str(arr)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getStringFromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Array', 'Keywords': []})
    def arrayLen(arr=('ListPin', [])):
        return len(arr)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Array', 'Keywords': []})
    def isIntInList(List=('ListPin', []), Value=('IntPin', 0)):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getIntFromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Array', 'Keywords': []})
    def isFloatInList(List=('ListPin', []), Value=('FloatPin', 0.0)):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getFloatFromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Array', 'Keywords': []})
    def isStringInList(List=('ListPin', []), Value=('StringPin', "")):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Array', 'Keywords': []})
    def Any(List=('ListPin', [])):
        return any(List)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Array', 'Keywords': []})
    def All(List=('ListPin', [])):
        return all(List)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getQuatFromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getVector3FromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getVector4FromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getM33FromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getM44FromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', ''), meta={'Category': 'Array', 'Keywords': []})
    def getBoolFromList(arr=('ListPin', []), Index=('IntPin', 0), Result=("Reference", ('BoolPin', False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)
