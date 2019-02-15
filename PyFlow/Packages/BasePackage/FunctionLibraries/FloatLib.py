from math import pi
from numpy import sign

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.BasePackage import PACKAGE_NAME


## Calculates the percentage along a line from MinValue to MaxValue that Value is.
def GetRangePct(MinValue, MaxValue, Value):
    return (Value - MinValue) / (MaxValue - MinValue)


class FloatLib(FunctionLibraryBase):
    '''doc string for FloatLib'''
    def __init__(self):
        super(FloatLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is two floats equal
    def isEqualf(a=('FloatPin', 0.0), b=('FloatPin', 0.0)):
        '''
        Floats equal
        '''
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is a > b
    def isGreaterf(a=('FloatPin', 0.0), b=('FloatPin', 0.0)):
        '''
        Is a > b
        '''
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is a >= b
    def isGreaterOrEqualf(a=('FloatPin', 0.0), b=('FloatPin', 0.0)):
        '''
        Is a >= b
        '''
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is a < b
    def isLessf(a=('FloatPin', 0.0), b=('FloatPin', 0.0)):
        '''
        Is a < b
        '''
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Is a <= b
    def isLessOrEqualf(a=('FloatPin', 0.0), b=('FloatPin', 0.0)):
        '''
        Is a <= b
        '''
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': ['+', 'append']}, packageName=PACKAGE_NAME)
    ## Sum of two floats
    def addf(a=('FloatPin', 0.0), b=('FloatPin', 0.0)):
        '''
        Sum of two floats
        '''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': ['-']}, packageName=PACKAGE_NAME)
    ## Float substraction
    def substractf(a=('FloatPin', 0), b=('FloatPin', 0)):
        '''
        Float substraction
        '''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': ['/']}, packageName=PACKAGE_NAME)
    ## Float devision
    def dividef(a=('FloatPin', 0.0), b=('FloatPin', 0.0), result=("Reference", ('BoolPin', False))):
        '''
        Float devision
        '''
        try:
            d = a / b
            result(True)
            return d
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': ['*']}, packageName=PACKAGE_NAME)
    ## Float multiplication
    def multf(a=('FloatPin', 0.0), b=('FloatPin', 0.0)):
        '''
        Float multiplication
        '''
        return a * b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Bult-in functions', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Return the absolute value of a number
    def absfloat(inp=('FloatPin', 0.0)):
        '''
        Return the absolute value of a number
        '''
        return abs(inp)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': ['lerp']}, packageName=PACKAGE_NAME)
    ## Linear interpolate
    def lerpf(a=('FloatPin', 0.0), b=('FloatPin', 0.0), alpha=('FloatPin', 0.0)):
        '''
        Linear interpolate
        '''
        return lerp(a, b, clamp(alpha, 0.0, 1.0))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': ['clamp']}, packageName=PACKAGE_NAME)
    ## Clamp float
    def clampf(i=('FloatPin', 0.0), imin=('FloatPin', 0.0), imax=('FloatPin', 0.0)):
        '''
        Clamp float
        '''
        return clamp(i, imin, imax)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def modulof(a=('FloatPin', 0.0), b=('FloatPin', 0.0)):
        '''
        Modulo (A % B)
        '''
        return a % b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def mapRangeClamped(Value=('FloatPin', 0.0),
                        InRangeA=('FloatPin', 0.0),
                        InRangeB=('FloatPin', 1.0),
                        OutRangeA=('FloatPin', 0.0),
                        OutRangeB=('FloatPin', 10.0)):
        '''
        Returns Value mapped from one range into another where the Value is clamped to the Input Range. (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)
        '''
        ClampedPct = clamp(GetRangePct(InRangeA, InRangeB, Value), 0.0, 1.0)
        return lerp(OutRangeA, OutRangeB, ClampedPct)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def mapRangeUnclamped(Value=('FloatPin', 0.0),
                          InRangeA=('FloatPin', 0.0),
                          InRangeB=('FloatPin', 1.0),
                          OutRangeA=('FloatPin', 0.0),
                          OutRangeB=('FloatPin', 10.0)):
        '''
        Returns Value mapped from one range into another where the Value is clamped to the Input Range. (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)
        '''
        return lerp(OutRangeA, OutRangeB, GetRangePct(InRangeA, InRangeB, Value))

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def nearlyEqual(a=('FloatPin', 0.0), b=('FloatPin', 0.0), abs_tol=('FloatPin', 0.0)):
        return abs(a - b) < abs_tol

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def multByPi(a=('FloatPin', 0.0)):
        '''
        Multiplies the input value by pi
        '''
        return a * pi

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def normalizeToRange(Value=('FloatPin', 0.0), RangeMin=('FloatPin', 0.0), RangeMax=('FloatPin', 0.0)):
        '''
        Returns Value normalized to the given range. (e.g. 20 normalized to the range 10->50 would result in 0.25)
        '''
        if RangeMin == RangeMax:
            return RangeMin

        if RangeMin > RangeMax:
            RangeMin, RangeMax = RangeMax, RangeMin
        return (Value - RangeMin) / (RangeMax - RangeMin)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def selectFloat(A=('FloatPin', 0.0), B=('FloatPin', 0.0), PickA=('BoolPin', False)):
        '''
        If bPickA is true, A is returned, otherwise B is
        '''
        return A if PickA else B

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def signf(a=('FloatPin', 0.0)):
        '''
        Returns -1 if x &lt; 0, 0 if x==0, 1 if x &gt; 0
        '''
        return sign(a)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []}, packageName=PACKAGE_NAME)
    def roundf(Value=('FloatPin', 0.0), Digits=('IntPin', 1)):
        '''
        Round a number to a given precision in decimal digits (default 0 digits)
        '''
        return round(Value, Digits)
