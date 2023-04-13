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


from PyFlow.PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.PyFlow.Core.Common import *


class IntLib(FunctionLibraryBase):
    """doc string for IntLib"""
    def __init__(self, packageName):
        super(IntLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def bitwiseAnd(a=('IntPin', 0), b=('IntPin', 0)):
        """Bitwise AND ``(A & B)``"""
        return a & b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def bitwiseNot(a=('IntPin', 0)):
        """Bitwise NOT ``(~A)``"""
        return ~a

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def bitwiseOr(a=('IntPin', 0), b=('IntPin', 0)):
        """Bitwise OR ``(A | B)``"""
        return a | b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def bitwiseXor(a=('IntPin', 0), b=('IntPin', 0)):
        """Bitwise XOR ``(A ^ B)``"""
        return a ^ b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def binaryLeftShift(a=('IntPin', 0), b=('IntPin', 0)):
        """Binary left shift ``a << b``"""
        return a << b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def binaryRightShift(a=('IntPin', 0), b=('IntPin', 0)):
        """Binary right shift ``a << b``"""
        return a >> b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def testBit(intType=('IntPin', 0), offset=('IntPin', 0)):
        """Returns a nonzero result, 2**offset, if the bit at 'offset' is one"""
        mask = 1 << offset
        return(intType & mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def setBit(intType=('IntPin', 0), offset=('IntPin', 0)):
        """Returns an integer with the bit at 'offset' set to 1."""
        mask = 1 << offset
        return(intType | mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def clearBit(intType=('IntPin', 0), offset=('IntPin', 0)):
        """Returns an integer with the bit at 'offset' cleared."""
        mask = ~(1 << offset)
        return(intType & mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Bits manipulation', NodeMeta.KEYWORDS: []})
    def toggleBit(intType=('IntPin', 0), offset=('IntPin', 0)):
        """Returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0."""
        mask = 1 << offset
        return(intType ^ mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'Math|Int', NodeMeta.KEYWORDS: []})
    def sign(x=('IntPin', 0)):
        """Sign (integer, returns -1 if A < 0, 0 if A is zero, and +1 if A > 0)"""
        return int(sign(x))
