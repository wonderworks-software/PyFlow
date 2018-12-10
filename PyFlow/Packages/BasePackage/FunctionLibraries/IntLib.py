from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from numpy import sign


class IntLib(FunctionLibraryBase):
    '''doc string for IntLib'''
    def __init__(self):
        super(IntLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Int', 'Keywords': []})
    ## Is two integers equal
    def isequal(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Ints equal
        '''
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Int', 'Keywords': []})
    ## Is a > b
    def isGreater(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Is a > b
        '''
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Int', 'Keywords': []})
    ## Is a >= b
    def isGreaterOrEqual(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Is a >= b
        '''
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Int', 'Keywords': []})
    ## Is a < b
    def isLess(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Is a < b
        '''
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Int', 'Keywords': []})
    ## Is a <= b
    def isLessOrEqual(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Is a <= b
        '''
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': ['+', 'append']})
    ## Sum of two ints
    def add(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Sum of two ints
        '''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': ['-']})
    ## Int substraction
    def substract(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Int substraction
        '''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Int', 'Keywords': ['/']})
    ## Integer devision
    def divide(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0), result=(DataTypes.Reference, (DataTypes.Bool, False))):
        '''
        Integer devision
        '''
        try:
            d = a / b
            result(True)
            return d
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': ['*']})
    ## Integer multiplication
    def mult(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Integer multiplication
        '''
        return a * b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': []})
    def modulo(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Modulo (A % B)
        '''
        return (a % b) if b != 0 else 0

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def bitwiseAnd(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Bitwise AND (A & B)
        '''
        return a & b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def bitwiseNot(a=(DataTypes.Int, 0)):
        '''
        Bitwise NOT (~A)
        '''
        return ~a

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def bitwiseOr(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Bitwise OR (A | B)
        '''
        return a | b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def bitwiseXor(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Bitwise XOR (A ^ B)
        '''
        return a ^ b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def binaryLeftShift(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Binary left shift a << b
        '''
        return a << b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def binaryRightShift(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Binary right shift a << b
        '''
        return a >> b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def testBit(intType=(DataTypes.Int, 0), offset=(DataTypes.Int, 0)):
        '''
        Returns a nonzero result, 2**offset, if the bit at 'offset' is one
        '''
        mask = 1 << offset
        return(intType & mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def setBit(intType=(DataTypes.Int, 0), offset=(DataTypes.Int, 0)):
        '''
        Returns an integer with the bit at 'offset' set to 1'
        '''
        mask = 1 << offset
        return(intType | mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def clearBit(intType=(DataTypes.Int, 0), offset=(DataTypes.Int, 0)):
        '''
        Returns an integer with the bit at 'offset' cleared.
        '''
        mask = ~(1 << offset)
        return(intType & mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def toggleBit(intType=(DataTypes.Int, 0), offset=(DataTypes.Int, 0)):
        '''
        Returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.
        '''
        mask = 1 << offset
        return(intType ^ mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': []})
    def clampInt(Value=(DataTypes.Int, 0), Min=(DataTypes.Int, 0), Max=(DataTypes.Int, 0)):
        '''
        Returns Value clamped to be between A and B (inclusive)
        '''
        return clamp(Value, Min, Max)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Int', 'Keywords': []})
    def inRange(Value=(DataTypes.Int, 0),
                RangeMin=(DataTypes.Int, 0),
                RangeMax=(DataTypes.Int, 0),
                InclusiveMin=(DataTypes.Bool, False),
                InclusiveMax=(DataTypes.Bool, False)):
        '''
        Returns true if value is between Min and Max (V &gt;= Min && V &lt;= Max) If InclusiveMin is true, value needs to be equal or larger than Min, else it needs to be larger If InclusiveMax is true, value needs to be smaller or equal than Max, else it needs to be smaller
        '''
        return ((Value >= RangeMin) if InclusiveMin else (Value > RangeMin)) and ((Value <= RangeMax) if InclusiveMax else (Value < RangeMax))

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': []})
    def selectInt(A=(DataTypes.Int, 0), B=(DataTypes.Int, 0), PickA=(DataTypes.Bool, False)):
        '''
        If bPickA is true, A is returned, otherwise B is
        '''
        return A if PickA else B

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': []})
    def sign(a=(DataTypes.Int, 0)):
        '''
        Sign (integer, returns -1 if A &lt; 0, 0 if A is zero, and +1 if A &gt; 0)
        '''
        return sign(a)
