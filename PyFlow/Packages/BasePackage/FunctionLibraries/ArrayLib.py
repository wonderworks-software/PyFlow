from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.BasePackage import PACKAGE_NAME


class ArrayLib(FunctionLibraryBase):
    '''doc string for ArrayLib'''
    def __init__(self):
        super(ArrayLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'Array', 'Keywords': []}, packageName=PACKAGE_NAME)
    def arrayToString(arr=('ListPin', [])):
        return str(arr)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Array', 'Keywords': []}, packageName=PACKAGE_NAME)
    def arrayLen(arr=('ListPin', [])):
        return len(arr)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Array', 'Keywords': []}, packageName=PACKAGE_NAME)
    def Any(List=('ListPin', [])):
        return any(List)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Array', 'Keywords': []}, packageName=PACKAGE_NAME)
    def All(List=('ListPin', [])):
        return all(List)

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", ''), meta={'Category': 'Array', 'Keywords': []}, packageName=PACKAGE_NAME)
    def selectInArray(arr=('ListPin', []), Index=("IntPin", 0), Result=("Reference", ("BoolPin", False))):
        try:
            element = arr[Index]
            Result(True)
            return element
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=("IntPin", False), meta={'Category': 'Array', 'Keywords': []}, packageName=PACKAGE_NAME)
    def findInArray(List=('ListPin', []), Value=("AnyPin", 0),Result=("Reference", ("BoolPin", False))):
        find = Value in List
        if find:
            Result(True)
            return List.index(Value)
        else:
            Result(False)
            return -1
