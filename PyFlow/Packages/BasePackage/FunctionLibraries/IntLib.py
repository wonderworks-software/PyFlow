from numpy import sign

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.BasePackage import PACKAGE_NAME


class IntLib(FunctionLibraryBase):
    '''doc string for IntLib'''
    def __init__(self):
        super(IntLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is two integers equal
    def isequal(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Ints equal
        '''
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is a > b
    def isGreater(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Is a > b
        '''
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is a >= b
    def isGreaterOrEqual(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Is a >= b
        '''
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is a < b
    def isLess(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Is a < b
        '''
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is a <= b
    def isLessOrEqual(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Is a <= b
        '''
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Int', 'Keywords': ['+', 'append']}, packageName=PACKAGE_NAME)
    ## Sum of two ints
    def add(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Sum of two ints
        '''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Int', 'Keywords': ['-']}, packageName=PACKAGE_NAME)
    ## Int substraction
    def substract(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Int substraction
        '''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Int', 'Keywords': ['/']}, packageName=PACKAGE_NAME)
    ## Integer devision
    def divide(a=('IntPin', 0), b=('IntPin', 0), result=("Reference", ('BoolPin', False))):
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
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Int', 'Keywords': ['*']}, packageName=PACKAGE_NAME)
    ## Integer multiplication
    def mult(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Integer multiplication
        '''
        return a * b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    def modulo(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Modulo (A % B)
        '''
        return (a % b) if b != 0 else 0

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def bitwiseAnd(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Bitwise AND (A & B)
        '''
        return a & b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def bitwiseNot(a=('IntPin', 0)):
        '''
        Bitwise NOT (~A)
        '''
        return ~a

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def bitwiseOr(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Bitwise OR (A | B)
        '''
        return a | b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def bitwiseXor(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Bitwise XOR (A ^ B)
        '''
        return a ^ b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def binaryLeftShift(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Binary left shift a << b
        '''
        return a << b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def binaryRightShift(a=('IntPin', 0), b=('IntPin', 0)):
        '''
        Binary right shift a << b
        '''
        return a >> b

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def testBit(intType=('IntPin', 0), offset=('IntPin', 0)):
        '''
        Returns a nonzero result, 2**offset, if the bit at 'offset' is one
        '''
        mask = 1 << offset
        return(intType & mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def setBit(intType=('IntPin', 0), offset=('IntPin', 0)):
        '''
        Returns an integer with the bit at 'offset' set to 1'
        '''
        mask = 1 << offset
        return(intType | mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def clearBit(intType=('IntPin', 0), offset=('IntPin', 0)):
        '''
        Returns an integer with the bit at 'offset' cleared.
        '''
        mask = ~(1 << offset)
        return(intType & mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []}, packageName=PACKAGE_NAME)
    def toggleBit(intType=('IntPin', 0), offset=('IntPin', 0)):
        '''
        Returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.
        '''
        mask = 1 << offset
        return(intType ^ mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    def clampInt(Value=('IntPin', 0), Min=('IntPin', 0), Max=('IntPin', 0)):
        '''
        Returns Value clamped to be between A and B (inclusive)
        '''
        return clamp(Value, Min, Max)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    def inRange(Value=('IntPin', 0),
                RangeMin=('IntPin', 0),
                RangeMax=('IntPin', 0),
                InclusiveMin=('BoolPin', False),
                InclusiveMax=('BoolPin', False)):
        '''
        Returns true if value is between Min and Max (V &gt;= Min && V &lt;= Max) If InclusiveMin is true, value needs to be equal or larger than Min, else it needs to be larger If InclusiveMax is true, value needs to be smaller or equal than Max, else it needs to be smaller
        '''
        return ((Value >= RangeMin) if InclusiveMin else (Value > RangeMin)) and ((Value <= RangeMax) if InclusiveMax else (Value < RangeMax))

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    def selectInt(A=('IntPin', 0), B=('IntPin', 0), PickA=('BoolPin', False)):
        '''
        If bPickA is true, A is returned, otherwise B is
        '''
        return A if PickA else B

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Int', 'Keywords': []}, packageName=PACKAGE_NAME)
    def sign(a=('IntPin', 0)):
        '''
        Sign (integer, returns -1 if A &lt; 0, 0 if A is zero, and +1 if A &gt; 0)
        '''
        return sign(a)
