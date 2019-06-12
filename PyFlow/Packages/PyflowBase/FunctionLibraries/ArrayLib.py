from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class ArrayLib(FunctionLibraryBase):
    '''doc string for ArrayLib'''
    def __init__(self, packageName):
        super(ArrayLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1'}), nodeType=NodeTypes.Callable, meta={'Category': 'Array', 'Keywords': []})
    def extendArray(lhs=('AnyPin', [], {'constraint': '1'}),
                    rhs=('AnyPin', [], {'constraint': '1'})):
        """Extend the list by appending all the items from the iterable."""
        lhs.extend(rhs)
        return lhs

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1'}), nodeType=NodeTypes.Callable, meta={'Category': 'Array', 'Keywords': []})
    def insertToArray(ls=('AnyPin', [], {'constraint': '1'}),
                      elem=('AnyPin', None, {'constraint': '1'}),
                      index=('IntPin', 0)):
        """Insert an item at a given position. The first argument is the index of the element before which to insert."""
        ls.insert(index, elem)
        return ls

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", [], {'constraint': '1'}), nodeType=NodeTypes.Callable, meta={'Category': 'Array', 'Keywords': []})
    def removeFromArray(ls=('AnyPin', [], {'constraint': '1'}),
                        elem=('AnyPin', None, {'constraint': '1'}),
                        removed=('Reference', ('BoolPin', False))):
        if elem not in ls:
            removed(False)
            return
        ls.remove(elem)
        removed(True)
        return ls

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {'constraint': '1'}), nodeType=NodeTypes.Callable, meta={'Category': 'Array', 'Keywords': []})
    def popFromArray(ls=('AnyPin', [], {'constraint': '1'}),
                     index=('IntPin', -1),
                     popped=('Reference', ('BoolPin', False)),
                     outLs=('Reference', ('AnyPin', [], {'constraint': '1'}))):
        poppedElem = None
        try:
            poppedElem = ls.pop(index)
            popped(True)
        except:
            popped(False)
        outLs(ls)

        return poppedElem if poppedElem is not None else 0

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {'constraint': '1'}), meta={'Category': 'Array', 'Keywords': []})
    def selectInArray(arr=('AnyPin', [], {'constraint': '1'}),
                      Index=("IntPin", 0),
                      Result=("Reference", ("BoolPin", False))):
        try:
            element = arr[Index]
            Result(True)
            return element
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Array', 'Keywords': ['in']})
    def arrayContains(ls=('AnyPin', [], {'constraint': '1'}), element=("AnyPin", None, {'constraint': '1'})):
        return element in ls

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1'}), nodeType=NodeTypes.Callable, meta={'Category': 'Array', 'Keywords': []})
    def clearArray(ls=('AnyPin', [], {'constraint': '1'})):
        ls.clear()
        return ls

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Array', 'Keywords': ['in']})
    def arrayElementIndex(ls=('AnyPin', [], {'constraint': '1'}),
                          element=("AnyPin", None, {'constraint': '1'}),
                          result=("Reference", ("BoolPin", False))):
        if element in ls:
            result(True)
            return ls.index(element)
        else:
            result(False)
            return 0

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Array', 'Keywords': ['in']})
    def arrayElementCount(ls=('AnyPin', [], {'constraint': '1'}),
                          element=("AnyPin", None, {'constraint': '1'}),
                          result=("Reference", ("BoolPin", False))):
        if element in ls:
            result(True)
            return ls.count(element)
        else:
            result(False)
            return 0

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin',None, {'constraint': '1'}), meta={'Category': 'Array', 'Keywords': []})
    def arraySum(Value=('AnyPin', [], {'constraint': '1'})):
        '''
        Sum of list of floats
        '''
        return sum(Value)