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


class BoolLib(FunctionLibraryBase):
    '''doc string for BoolLib'''
    def __init__(self, packageName):
        super(BoolLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'Math|Bool', NodeMeta.KEYWORDS: []})
    def boolAnd(a=('BoolPin', False), b=('BoolPin', False)):
        '''Returns the logical `AND` of two values `(A AND B)`.'''
        return a and b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'Math|Bool', NodeMeta.KEYWORDS: []})
    def boolNot(a=('BoolPin', False)):
        '''Returns the logical complement of the Boolean value `(NOT A)`.'''
        return not a

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'Math|Bool', NodeMeta.KEYWORDS: []})
    def boolNand(a=('BoolPin', False), b=('BoolPin', False)):
        '''Returns the logical `NAND` of two values `(A AND B)`.'''
        return not (a and b)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'Math|Bool', NodeMeta.KEYWORDS: []})
    def boolNor(a=('BoolPin', False), b=('BoolPin', False)):
        '''Returns the logical `Not OR` of two values `(A NOR B)`.'''
        return not (a or b)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'Math|Bool', NodeMeta.KEYWORDS: []})
    def boolOr(a=('BoolPin', False), b=('BoolPin', False)):
        '''Returns the logical `OR` of two values `(A OR B)`.'''
        return a or b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'Math|Bool', NodeMeta.KEYWORDS: []})
    def boolXor(a=('BoolPin', False), b=('BoolPin', False)):
        '''Returns the logical `eXclusive OR` of two values `(A XOR B)`.'''
        return a ^ b
