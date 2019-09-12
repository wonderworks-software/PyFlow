## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


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
    @IMPLEMENT_NODE(returns=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1'}), meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: []})
    def extendArray(lhs=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                    rhs=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny})):
        """Extend the list by appending all the items from the iterable."""
        lhs.extend(rhs)
        return lhs

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: []})
    def insertToArray(ls=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                      elem=('AnyPin', None, {PinSpecifires.CONSTRAINT: '1'}),
                      index=('IntPin', 0)):
        """Insert an item at a given position. The first argument is the index of the element before which to insert."""
        ls.insert(index, elem)
        return ls

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: []})
    def removeFromArray(ls=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                        elem=('AnyPin', None, {PinSpecifires.CONSTRAINT: '1'}),
                        removed=(REF, ('BoolPin', False))):
        """Remove the first item from the list whose value is equal to x."""
        if elem not in ls:
            removed(False)
            return
        ls.remove(elem)
        removed(True)
        return ls

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {PinSpecifires.CONSTRAINT: '1'}), meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: []})
    def popFromArray(ls=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                     index=('IntPin', -1),
                     popped=(REF, ('BoolPin', False)),
                     outLs=(REF, ('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}))):
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
    @IMPLEMENT_NODE(returns=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: []})
    def clearArray(ls=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny})):
        """Remove all items from the list."""
        return clearList(ls)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: ['in']})
    def arrayElementIndex(ls=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                          element=("AnyPin", None, {PinSpecifires.CONSTRAINT: '1'}),
                          result=(REF, ("BoolPin", False))):
        """Returns index of array element if it present. If element is not in array -1 will be returned."""
        if element in ls:
            result(True)
            return ls.index(element)
        else:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: ['in']})
    def arrayElementCount(ls=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                          element=("AnyPin", None, {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.AllowAny}),
                          result=(REF, ("BoolPin", False))):
        """Returns len of passed array."""
        if element in ls:
            result(True)
            return ls.count(element)
        else:
            result(False)
            return 0

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {PinSpecifires.CONSTRAINT: '1'}), meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: []})
    def arraySum(Value=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"]})):
        """Python **sum()** function."""
        return sum(Value)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: ['in']})
    def arraySlice(ls=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                   start=("IntPin", 0),
                   end=("IntPin", 1),
                   result=(REF, ("BoolPin", False))):
        """Array slice."""
        try:
            result(True)
            return ls[start:end]
        except:
            result(False)
            return ls
