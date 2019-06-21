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
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1'}), meta={'Category': 'Array', 'Keywords': []})
    def extendArray(lhs=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                    rhs=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny})):
        """Extend the list by appending all the items from the iterable."""
        lhs.extend(rhs)
        return lhs

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={'Category': 'Array', 'Keywords': []})
    def insertToArray(ls=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                      elem=('AnyPin', None, {'constraint': '1'}),
                      index=('IntPin', 0)):
        """Insert an item at a given position. The first argument is the index of the element before which to insert."""
        ls.insert(index, elem)
        return ls

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'Array', 'Keywords': []})
    def removeFromArray(ls=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                        elem=('AnyPin', None, {'constraint': '1'}),
                        removed=('Reference', ('BoolPin', False))):
        """Remove the first item from the list whose value is equal to x."""
        if elem not in ls:
            removed(False)
            return
        ls.remove(elem)
        removed(True)
        return ls

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {'constraint': '1'}), meta={'Category': 'Array', 'Keywords': []})
    def popFromArray(ls=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                     index=('IntPin', -1),
                     popped=('Reference', ('BoolPin', False)),
                     outLs=('Reference', ('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}))):
        """Remove the item at the given position in the array, and return it. If no index is specified, ``a.pop()`` removes and returns the last item in the list."""
        poppedElem = None
        try:
            poppedElem = ls.pop(index)
            popped(True)
        except:
            popped(False)
        outLs(ls)

        return poppedElem if poppedElem is not None else 0

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={'Category': 'Array', 'Keywords': []})
    def clearArray(ls=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny})):
        """Remove all items from the list."""
        return clearList(ls)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Array', 'Keywords': ['in']})
    def arrayElementIndex(ls=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                          element=("AnyPin", None, {'constraint': '1'}),
                          result=("Reference", ("BoolPin", False))):
        """Returns index of array element if it present. If element is not in array -1 will be returned."""
        if element in ls:
            result(True)
            return ls.index(element)
        else:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Array', 'Keywords': ['in']})
    def arrayElementCount(ls=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                          element=("AnyPin", None, {'constraint': '1',"enabledOptions": PinOptions.AllowAny}),
                          result=("Reference", ("BoolPin", False))):
        """Returns len of passed array."""
        if element in ls:
            result(True)
            return ls.count(element)
        else:
            result(False)
            return 0

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {'constraint': '1'}), meta={'Category': 'Array', 'Keywords': []})
    def arraySum(Value=('AnyPin', [], {'constraint': '1', "supportedDataTypes": ["FloatPin", "IntPin"]})):
        """Python **sum()** function."""
        return sum(Value)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={'Category': 'Array', 'Keywords': ['in']})
    def arraySlice(ls=('AnyPin', [], {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                   start=("IntPin", 0),
                   end=("IntPin", 1),
                   result=("Reference", ("BoolPin", False))):
        """Array slice."""
        try:
            result(True)
            return ls[start:end]
        except:
            result(False)
            return ls
