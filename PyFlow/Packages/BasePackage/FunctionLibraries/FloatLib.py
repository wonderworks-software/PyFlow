from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from math import pi
from numpy import sign


## Calculates the percentage along a line from MinValue to MaxValue that Value is.
def GetRangePct(MinValue, MaxValue, Value):
    return (Value - MinValue) / (MaxValue - MinValue)


class FloatLib(FunctionLibraryBase):
    '''doc string for FloatLib'''
    def __init__(self):
        super(FloatLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Float', 'Keywords': []})
    ## Is two floats equal
    def isEqualf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''
        Floats equal
        '''
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Float', 'Keywords': []})
    ## Is a > b
    def isGreaterf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''
        Is a > b
        '''
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Float', 'Keywords': []})
    ## Is a >= b
    def isGreaterOrEqualf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''
        Is a >= b
        '''
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Float', 'Keywords': []})
    ## Is a < b
    def isLessf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''
        Is a < b
        '''
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Float', 'Keywords': []})
    ## Is a <= b
    def isLessOrEqualf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''
        Is a <= b
        '''
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': ['+', 'append']})
    ## Sum of two floats
    def addf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''
        Sum of two floats
        '''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': ['-']})
    ## Float substraction
    def substractf(a=(DataTypes.Float, 0), b=(DataTypes.Float, 0)):
        '''
        Float substraction
        '''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': ['/']})
    ## Float devision
    def dividef(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), result=(DataTypes.Reference, (DataTypes.Bool, False))):
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
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': ['*']})
    ## Float multiplication
    def multf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''
        Float multiplication
        '''
        return a * b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Python math|Bult-in functions', 'Keywords': []})
    ## Return the absolute value of a number
    def absfloat(inp=(DataTypes.Float, 0.0)):
        '''
        Return the absolute value of a number
        '''
        return abs(inp)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': ['lerp']})
    ## Linear interpolate
    def lerpf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), alpha=(DataTypes.Float, 0.0)):
        '''
        Linear interpolate
        '''
        return lerp(a, b, clamp(alpha, 0.0, 1.0))

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': ['clamp']})
    ## Clamp float
    def clampf(i=(DataTypes.Float, 0.0), imin=(DataTypes.Float, 0.0), imax=(DataTypes.Float, 0.0)):
        '''
        Clamp float
        '''
        return clamp(i, imin, imax)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def modulof(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''
        Modulo (A % B)
        '''
        return a % b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def mapRangeClamped(Value=(DataTypes.Float, 0.0),
                        InRangeA=(DataTypes.Float, 0.0),
                        InRangeB=(DataTypes.Float, 1.0),
                        OutRangeA=(DataTypes.Float, 0.0),
                        OutRangeB=(DataTypes.Float, 10.0)):
        '''
        Returns Value mapped from one range into another where the Value is clamped to the Input Range. (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)
        '''
        ClampedPct = clamp(GetRangePct(InRangeA, InRangeB, Value), 0.0, 1.0)
        return lerp(OutRangeA, OutRangeB, ClampedPct)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def mapRangeUnclamped(Value=(DataTypes.Float, 0.0),
                          InRangeA=(DataTypes.Float, 0.0),
                          InRangeB=(DataTypes.Float, 1.0),
                          OutRangeA=(DataTypes.Float, 0.0),
                          OutRangeB=(DataTypes.Float, 10.0)):
        '''
        Returns Value mapped from one range into another where the Value is clamped to the Input Range. (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)
        '''
        return lerp(OutRangeA, OutRangeB, GetRangePct(InRangeA, InRangeB, Value))

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Float', 'Keywords': []})
    def nearlyEqual(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), abs_tol=(DataTypes.Float, 0.0)):
        return abs(a - b) < abs_tol

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def multByPi(a=(DataTypes.Float, 0.0)):
        '''
        Multiplies the input value by pi
        '''
        return a * pi

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def normalizeToRange(Value=(DataTypes.Float, 0.0), RangeMin=(DataTypes.Float, 0.0), RangeMax=(DataTypes.Float, 0.0)):
        '''
        Returns Value normalized to the given range. (e.g. 20 normalized to the range 10->50 would result in 0.25)
        '''
        if RangeMin == RangeMax:
            return RangeMin

        if RangeMin > RangeMax:
            RangeMin, RangeMax = RangeMax, RangeMin
        return (Value - RangeMin) / (RangeMax - RangeMin)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def selectFloat(A=(DataTypes.Float, 0.0), B=(DataTypes.Float, 0.0), PickA=(DataTypes.Bool, False)):
        '''
        If bPickA is true, A is returned, otherwise B is
        '''
        return A if PickA else B

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def signf(a=(DataTypes.Float, 0.0)):
        '''
        Returns -1 if x &lt; 0, 0 if x==0, 1 if x &gt; 0
        '''
        return sign(a)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def roundf(Value=(DataTypes.Float, 0.0), Digits=(DataTypes.Int, 1)):
        '''
        Round a number to a given precision in decimal digits (default 0 digits)
        '''
        return round(Value, Digits)
