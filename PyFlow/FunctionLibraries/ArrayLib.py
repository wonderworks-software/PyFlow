from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
import pyrr


class ArrayLib(FunctionLibraryBase):
    '''doc string for ArrayLib'''
    def __init__(self):
        super(ArrayLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, ''), meta={'Category': 'Array', 'Keywords': []})
    def arrayToString(arr=(DataTypes.Array, [])):
        return str(arr)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, ''), meta={'Category': 'Array', 'Keywords': []})
    def getStringFromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Array', 'Keywords': []})
    def arrayLen(arr=(DataTypes.Array, [])):
        return len(arr)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def isIntInList(List=(DataTypes.Array, []), Value=(DataTypes.Int, 0)):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, ''), meta={'Category': 'Array', 'Keywords': []})
    def getIntFromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def isFloatInList(List=(DataTypes.Array, []), Value=(DataTypes.Float, 0.0)):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, ''), meta={'Category': 'Array', 'Keywords': []})
    def getFloatFromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def isStringInList(List=(DataTypes.Array, []), Value=(DataTypes.String, "")):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def Any(List=(DataTypes.Array, [])):
        return any(List)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def All(List=(DataTypes.Array, [])):
        return all(List)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def isQuatInList(List=(DataTypes.Array, []), Value=(DataTypes.Quaternion, pyrr.Quaternion())):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Quaternion, ''), meta={'Category': 'Array', 'Keywords': []})
    def getQuatFromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def isVector3InList(List=(DataTypes.Array, []), Value=(DataTypes.FloatVector3, pyrr.Vector3())):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, ''), meta={'Category': 'Array', 'Keywords': []})
    def getVector3FromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def isVector4InList(List=(DataTypes.Array, []), Value=(DataTypes.FloatVector4, pyrr.Vector4())):
        return Value in List

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector4, ''), meta={'Category': 'Array', 'Keywords': []})
    def getVector4FromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Matrix33, ''), meta={'Category': 'Array', 'Keywords': []})
    def getM33FromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Matrix44, ''), meta={'Category': 'Array', 'Keywords': []})
    def getM44FromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, ''), meta={'Category': 'Array', 'Keywords': []})
    def getBoolFromList(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            string = arr[Index]
            Result(True)
            return string
        except:
            Result(False)
