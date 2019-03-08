from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *

class BoolLib(FunctionLibraryBase):
    '''doc string for BoolLib'''
    def __init__(self,packageName):
        super(BoolLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolAnd(a=('BoolPin', False), b=('BoolPin', False)):
        '''
        Returns the logical AND of two values (A AND B)
        '''
        return a and b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNot(a=('BoolPin', False)):
        '''
        Returns the logical complement of the Boolean value (NOT A)
        '''
        return not a

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNand(a=('BoolPin', False), b=('BoolPin', False)):
        '''
        Returns the logical NAND of two values (A AND B)
        '''
        return not (a and b)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNor(a=('BoolPin', False), b=('BoolPin', False)):
        '''
        Returns the logical Not OR of two values (A NOR B)
        '''
        return not (a or b)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolOr(a=('BoolPin', False), b=('BoolPin', False)):
        '''
        Returns the logical OR of two values (A OR B)
        '''
        return a or b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolXor(a=('BoolPin', False), b=('BoolPin', False)):
        '''
        Returns the logical eXclusive OR of two values (A XOR B)
        '''
        return a ^ b
