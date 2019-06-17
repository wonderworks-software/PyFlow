import math
import random

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class MathLib(FunctionLibraryBase):
    """
    Python builtin math module wrapper
    """

    def __init__(self, packageName):
        super(MathLib, self).__init__(packageName)

    # ###################
    # builtin python math
    # ###################
    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", 0, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def copysign(x=("AnyPin", 0, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}), y=("AnyPin", 0, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]})):
        '''Return `x` with the sign of `y`. On a platform that supports signed zeros, `copysign(1.0, -0.0)` returns `-1.0`.'''
        return math.copysign(x, y)

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", 0, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def fmod(x=("AnyPin", 0, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}), y=("AnyPin", 0, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]})):
        '''Return `fmod(x, y)`, as defined by the platform C library.'''
        return math.fmod(x, y)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def modf(x=("FloatPin", 0.0), f=("Reference", ('FloatPin', 0.0)), i=("Reference", ('FloatPin', 0.0))):
        '''Return the fractional and integer parts of `x`. Both results carry the sign of `x` and are floats.'''
        t = math.modf(x)
        f(t[0])
        i(t[1])

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def ceil(x=('FloatPin', 0.0)):
        '''Return the ceiling of `x` as a float, the smallest integer value greater than or equal to `x`.'''
        return math.ceil(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def factorial(x=('IntPin', 0), result=("Reference", ('BoolPin', False))):
        '''Return `x` factorial. Raises ValueError if `x` is not integral or is negative.'''
        try:
            f = math.factorial(x)
            result(True)
            return f
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def floor(x=('FloatPin', 0.0)):
        '''Return the floor of x as an Integral.'''
        return math.floor(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def frexp(x=('FloatPin', 0.0), m=("Reference", ('FloatPin', 0.0)), e=("Reference", ('IntPin', 0))):
        '''Return the mantissa and exponent of `x` as the pair (m, e). m is `x` float and e is an integer such that `x == m * 2**e` exactly.'''
        t = math.frexp(x)
        m(t[0])
        e(t[1])

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def fsum(arr=('FloatPin', []), result=("Reference", ('BoolPin', False))):
        '''Return an accurate floating point sum of values in the iterable. Avoids loss of precision by tracking multiple intermediate partial sums.'''
        try:
            s = math.fsum([i for i in arr])
            result(True)
            return s
        except:
            result(False)
            return 0.0

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def isinf(x=('FloatPin', 0.0)):
        '''Check if the float `x` is positive or negative infinity.'''
        return math.isinf(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def isnan(x=('FloatPin', 0.0)):
        '''Check if the float `x` is a NaN (not a number).'''
        return math.isnan(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def ldexp(x=('FloatPin', 0.0), i=('IntPin', 0)):
        '''Return `x * (2**i)`. This is essentially the inverse of function `frexp()`.'''
        return math.ldexp(x, i)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Math|Python math|Number-theoretic and representation functions', 'Keywords': []})
    def trunc(x=('FloatPin', 0.0)):
        '''Return the Real value `x` truncated to an Integral (usually a long integer).'''
        return math.trunc(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Power and logarithmic functions', 'Keywords': []})
    def exp(x=('FloatPin', 0.0)):
        '''Return e**x.'''
        return math.exp(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Power and logarithmic functions', 'Keywords': []})
    def expm1(x=('FloatPin', 0.1)):
        '''Return `e**x - 1`. For small floats `x`, the subtraction in `exp(x) - 1` can result in a significant loss of precision.'''
        return math.expm1(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Power and logarithmic functions', 'Keywords': []})
    def log(x=('FloatPin', 1.0), base=('FloatPin', math.e), result=("Reference", ('BoolPin', False))):
        '''Return the logarithm of `x` to the given base, calculated as `log(x)/log(base)`.'''
        try:
            result(True)
            return math.log(x, base)
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Power and logarithmic functions', 'Keywords': []})
    def log1p(x=('FloatPin', 1.0), result=("Reference", ('BoolPin', False))):
        '''Return the natural logarithm of `1+x` (base e). The result is calculated in a way which is accurate for `x` near zero.'''
        try:
            result(True)
            return math.log1p(x)
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Power and logarithmic functions', 'Keywords': []})
    def log10(x=('FloatPin', 1.0), result=("Reference", ('BoolPin', False))):
        '''Return the base-10 logarithm of `x`. This is usually more accurate than `log(x, 10)`.'''
        try:
            result(True)
            return math.log10(x)
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Power and logarithmic functions', 'Keywords': []})
    def power(x=('FloatPin', 0.0), y=('FloatPin', 0.0), result=("Reference", ('BoolPin', False))):
        '''Return `x` raised to the power `y`.'''
        try:
            result(True)
            return math.pow(x, y)
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Power and logarithmic functions', 'Keywords': []})
    def sqrt(x=('FloatPin', 0.0), result=("Reference", ('BoolPin', False))):
        '''Return the square root of `x`.'''
        try:
            result(True)
            return math.sqrt(x)
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Trigonometry', 'Keywords': []})
    def cos(rad=('FloatPin', 0.0)):
        '''Return the cosine of `x` radians.'''
        return math.cos(rad)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Trigonometry', 'Keywords': []})
    def acos(rad=('FloatPin', 0.0)):
        '''Return the arc cosine of `x`, in radians.'''
        return math.acos(rad)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Trigonometry', 'Keywords': []})
    def sin(rad=('FloatPin', 0.0)):
        '''Return the sine of `x` radians.'''
        return math.sin(rad)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Trigonometry', 'Keywords': []})
    def asin(rad=('FloatPin', 0.0)):
        '''Return the arc sine of `x`, in radians.'''
        return math.asin(rad)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Trigonometry', 'Keywords': []})
    def tan(rad=('FloatPin', 0.0)):
        '''Return the tangent of `x` radians.'''
        return math.tan(rad)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Trigonometry', 'Keywords': []})
    def atan(rad=('FloatPin', 0.0)):
        '''Return the arc tangent of `x`, in radians.'''
        return math.atan(rad)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Trigonometry', 'Keywords': []})
    def atan2(x=('FloatPin', 0.0), y=('FloatPin', 0.0)):
        '''Return `atan(a / b)`, in radians. The result is between `-pi` and `pi`.\nThe vector in the plane from the origin to point (x, y) makes this angle with the positive X axis. The point of `atan2()` is that the signs of both inputs are known to it, so it can compute the correct quadrant for the angle.\nFor example, `atan(1)` and `atan2(1, 1)` are both `pi/4`, but `atan2(-1, -1)` is `-3*pi/4`.'''
        return math.atan2(x, y)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Trigonometry', 'Keywords': []})
    def hypot(x=('FloatPin', 0.0), y=('FloatPin', 0.0)):
        '''Return the Euclidean norm, `sqrt(x*x + y*y)`. This is the length of the vector from the origin to point (x, y).'''
        return math.hypot(x, y)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Angular conversion', 'Keywords': []})
    def degtorad(deg=('FloatPin', 0.0)):
        '''Convert angle `x` from degrees to radians.'''
        return math.radians(deg)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Angular conversion', 'Keywords': []})
    def radtodeg(rad=('FloatPin', 0.0)):
        '''Convert angle `x` from radians to degrees.'''
        return math.degrees(rad)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Hyperbolic functions', 'Keywords': []})
    def acosh(x=('FloatPin', 0.0), Result=("Reference", ('BoolPin', False))):
        '''Return the inverse hyperbolic cosine of `x`.'''
        try:
            Result(True)
            return math.acosh(x)
        except:
            Result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Hyperbolic functions', 'Keywords': []})
    def asinh(x=('FloatPin', 0.0)):
        '''Return the inverse hyperbolic sine of x.'''
        return math.asinh(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Hyperbolic functions', 'Keywords': []})
    def atanh(x=('FloatPin', 0.0), Result=("Reference", ('BoolPin', False))):
        '''Return the inverse hyperbolic tangent of `x`.'''
        try:
            Result(True)
            return math.atanh(x)
        except:
            Result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Hyperbolic functions', 'Keywords': []})
    def cosh(x=('FloatPin', 0.0), Result=("Reference", ('BoolPin', False))):
        '''Return the hyperbolic cosine of `x`.'''
        try:
            Result(True)
            return math.cosh(x)
        except:
            Result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Hyperbolic functions', 'Keywords': []})
    def sinh(x=('FloatPin', 0.0), Result=("Reference", ('BoolPin', False))):
        '''Return the hyperbolic sine of `x`.'''
        try:
            Result(True)
            return math.sinh(x)
        except:
            Result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Hyperbolic functions', 'Keywords': []})
    def tanh(x=('FloatPin', 0.0)):
        '''Return the hyperbolic tangent of `x`.'''
        return math.tanh(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Special functions', 'Keywords': []})
    def erf(x=('FloatPin', 0.0)):
        '''Return the error function at `x`.'''
        return math.erf(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Special functions', 'Keywords': []})
    def erfc(x=('FloatPin', 0.0)):
        '''Return the complementary error function at `x`.'''
        return math.erfc(x)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Special functions', 'Keywords': []})
    def gamma(x=('FloatPin', 0.0), Result=("Reference", ('BoolPin', False))):
        '''Return the Gamma function at `x`.'''
        try:
            Result(True)
            return math.gamma(x)
        except:
            Result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Special functions', 'Keywords': []})
    def lgamma(x=('FloatPin', 0.0), Result=("Reference", ('BoolPin', False))):
        '''Return the natural logarithm of the absolute value of the Gamma function at `x`.'''
        try:
            Result(True)
            return math.lgamma(x)
        except:
            Result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Constants', 'Keywords': []})
    def e():
        '''The mathematical constant `e = 2.718281`, to available precision.'''
        return math.e

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Python math|Constants', 'Keywords': []})
    def pi():
        '''The mathematical constant = `3.141592`, to available precision.'''
        return math.pi
