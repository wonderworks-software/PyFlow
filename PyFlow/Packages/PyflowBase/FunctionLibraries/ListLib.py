from copy import deepcopy

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class ListLib(FunctionLibraryBase):
    '''doc string for ListLib'''
    def __init__(self, packageName):
        super(ListLib, self).__init__(packageName)

    # TODO: Create pin descriptor/builder class to pass as function arguments instead of tuples
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {'constraint': '1'}), meta={'Category': 'List', 'Keywords': []})
    def selectInList(arr=('AnyPin', [], {'constraint': '1'}), Index=("IntPin", 0), Result=("Reference", ("BoolPin", False))):
        try:
            element = arr[Index]
            Result(True)
            return element
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'List', 'Keywords': []})
    def appendToList(arr=('AnyPin', [], {'constraint': '1'}), elem=('AnyPin', None, {'constraint': '1'}), duplicate=('BoolPin', True), result=('Reference', ('AnyPin', [], {'constraint': '1'}))):
        outArr = arr
        if duplicate:
            outArr = deepcopy(arr)
        outArr.append(elem)
        result(outArr)
