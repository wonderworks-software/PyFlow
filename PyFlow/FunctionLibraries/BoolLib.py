from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *


class BoolLib(FunctionLibraryBase):
    '''doc string for BoolLib'''
    def __init__(self):
        super(BoolLib, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    ## make simple boolean
    def makeBool(b=(DataTypes.Bool, False)):
        '''
        make boolean
        '''
        return b

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bool|Conversion', 'Keywords': []})
    def boolToInt(b=(DataTypes.Bool, False)):
        return int(b)

    @staticmethod
    @implementNode(returns=(DataTypes.String, ''), meta={'Category': 'Math|Bool|Conversion', 'Keywords': []})
    def boolToString(b=(DataTypes.Bool, str(False))):
        return str(b)

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolAnd(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical AND of two values (A AND B)
        '''
        return a and b

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolEquals(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns true if the values are equal (A == B)
        '''
        return a == b

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNotEquals(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns true if the values are not equal (A != B)
        '''
        return a != b

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNot(a=(DataTypes.Bool, False)):
        '''
        Returns the logical complement of the Boolean value (NOT A)
        '''
        return not a

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNand(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical NAND of two values (A AND B)
        '''
        return not (a and b)

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNor(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical Not OR of two values (A NOR B)
        '''
        return not (a or b)

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolOr(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical OR of two values (A OR B)
        '''
        return a or b

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolXor(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical eXclusive OR of two values (A XOR B)
        '''
        return a ^ b
