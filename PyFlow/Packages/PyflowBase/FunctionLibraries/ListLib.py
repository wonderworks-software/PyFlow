from copy import copy, deepcopy

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
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'List', 'Keywords': ['in']})
    def listContains(ls=('AnyPin', [], {'constraint': '1'}), element=("AnyPin", None, {'constraint': '1'})):
        return element in ls

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'List', 'Keywords': []})
    def appendToList(ls=('AnyPin', [], {'constraint': '1'}), elem=('AnyPin', None, {'constraint': '1'}), duplicate=('BoolPin', True), deepCopy=('BoolPin', False), result=('Reference', ('AnyPin', [], {'constraint': '1'}))):
        outArr = ls
        if duplicate:
            copyFunction = deepcopy if deepCopy else copy
            outArr = copyFunction(ls)
        outArr.append(elem)
        result(outArr)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'List', 'Keywords': []})
    def removeFromList(ls=('AnyPin', [], {'constraint': '1'}), elem=('AnyPin', None, {'constraint': '1'}), result=('Reference', ('BoolPin', False, {'constraint': '1'}))):
        if elem not in ls:
            result(False)
            return
        ls.remove(elem)
        result(True)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'List', 'Keywords': []})
    def clearList(ls=('AnyPin', [], {'constraint': '1'}), duplicate=('BoolPin', True), deepCopy=('BoolPin', False), result=('Reference', ('AnyPin', [], {'constraint': '1'}))):
        outArr = ls
        if duplicate:
            copyFunction = deepcopy if deepCopy else copy
            outArr = copyFunction(ls)
        outArr.clear()
        result(outArr)
