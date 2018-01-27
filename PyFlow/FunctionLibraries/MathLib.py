from FunctionLibrary import *
from AGraphCommon import *
import math
import random
import pyrr


class MathLib(FunctionLibraryBase):
    """doc string for MathLib"""
    def __init__(self):
        super(MathLib, self).__init__()

    # ###################
    # builtin python math
    # ###################

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def ceil(a=(DataTypes.Float, 0.0)):
        '''Return the ceiling of x as a float, the smallest integer value greater than or equal to x.'''
        return math.ceil(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def copysignf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''Return x with the sign of y. On a platform that supports signed zeros, copysign(1.0, -0.0) returns -1.0.'''
        return math.copysign(a, b)

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def copysign(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''Return x with the sign of y. On a platform that supports signed zeros, copysign(1.0, -0.0) returns -1.0.'''
        return math.copysign(a, b)

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def factorial(a=(DataTypes.Int, 0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return x factorial. Raises ValueError if x is not integral or is negative.'''
        try:
            f = math.factorial(a)
            result.setData(True)
            return f
        except:
            result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def floor(a=(DataTypes.Float, 0.0)):
        '''Sum of two flaots.'''
        return math.floor(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def fmodf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''Return fmod(x, y), as defined by the platform C library.'''
        return math.fmod(a, b)

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def fmod(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''Python x % y.'''
        return a % b

    @staticmethod
    @implementNode(returns=None, meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def frexp(a=(DataTypes.Float, 0.0), m=(DataTypes.Reference, DataTypes.Float), e=(DataTypes.Reference, DataTypes.Int)):
        '''Return the mantissa and exponent of x as the pair (m, e). m is a float and e is an integer such that x == m * 2**e exactly.'''
        t = math.frexp(a)
        m.setData(t[0])
        e.setData(t[1])

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def fsum(arr=(DataTypes.Array, []), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return an accurate floating point sum of values in the iterable. Avoids loss of precision by tracking multiple intermediate partial sums.'''
        try:
            s = math.fsum([float(i) for i in arr])
            result.setData(True)
            return s
        except:
            result.setData(False)
            return 0.0

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def isinf(a=(DataTypes.Float, 0.0)):
        '''Check if the float x is positive or negative infinity.'''
        return math.isinf(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def isnan(a=(DataTypes.Float, 0.0)):
        '''Check if the float x is a NaN (not a number).'''
        return math.isnan(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def ldexp(a=(DataTypes.Float, 0.0), i=(DataTypes.Int, 0)):
        '''Return x * (2**i). This is essentially the inverse of function frexp().'''
        return math.ldexp(a, i)

    @staticmethod
    @implementNode(returns=None, meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def modf(a=(DataTypes.Int, 0), f=(DataTypes.Reference, DataTypes.Float), i=(DataTypes.Reference, DataTypes.Int)):
        '''Return the fractional and integer parts of x. Both results carry the sign of x and are floats.'''
        t = math.modf(a)
        f.setData(t[0])
        i.setData(t[1])

    @staticmethod
    @implementNode(returns=None, meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def fmodf(a=(DataTypes.Float, 0), f=(DataTypes.Reference, DataTypes.Float), i=(DataTypes.Reference, DataTypes.Int)):
        '''Return the fractional and integer parts of x. Both results carry the sign of x and are floats.'''
        t = math.modf(a)
        f.setData(t[0])
        i.setData(t[1])

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Number-theoretic and representation functions', 'Keywords': []})
    def trunc(a=(DataTypes.Float, 0)):
        '''Return the Real value x truncated to an Integral (usually a long integer).'''
        return math.trunc(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Power and logarithmic functions', 'Keywords': []})
    def exp(a=(DataTypes.Float, 0.0)):
        '''Return e**x.'''
        return math.exp(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Power and logarithmic functions', 'Keywords': []})
    def expm1(a=(DataTypes.Float, 0.1)):
        '''Return e**x - 1. For small floats x, the subtraction in exp(x) - 1 can result in a significant loss of precision.'''
        return math.expm1(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Power and logarithmic functions', 'Keywords': []})
    def log(a=(DataTypes.Float, 1.0), base=(DataTypes.Float, math.e), result=(DataTypes.Reference, DataTypes.Bool)):
        '''With one argument, return the natural logarithm of x (to base e).\nWith two arguments, return the logarithm of x to the given base, calculated as log(x)/log(base).'''
        try:
            result.setData(True)
            return math.log(a, base)
        except:
            result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Power and logarithmic functions', 'Keywords': []})
    def log1p(a=(DataTypes.Float, 1.0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the natural logarithm of 1+x (base e). The result is calculated in a way which is accurate for x near zero.'''
        try:
            result.setData(True)
            return math.log1p(a)
        except:
            result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Power and logarithmic functions', 'Keywords': []})
    def log10(a=(DataTypes.Float, 1.0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the base-10 logarithm of x. This is usually more accurate than log(x, 10).'''
        try:
            result.setData(True)
            return math.log10(a)
        except:
            result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Power and logarithmic functions', 'Keywords': []})
    def power(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return x raised to the power y.'''
        try:
            result.setData(True)
            return math.pow(a, b)
        except:
            result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Power and logarithmic functions', 'Keywords': []})
    def sqrt(a=(DataTypes.Float, 0.0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the square root of x.'''
        try:
            result.setData(True)
            return math.sqrt(a)
        except:
            result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bult-in functions', 'Keywords': ['+']})
    def Sum(arr=(DataTypes.Array, []), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Sums start and the items of an iterable from left to right and returns the total.'''
        try:
            s = math.fsum([int(i) for i in arr])
            result.setData(True)
            return s
        except:
            result.setData(False)
            return 0

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math', 'Keywords': ['+', 'append']})
    def addf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''Sum of two floats.'''
        return a + b

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math', 'Keywords': ['+', 'append']})
    def add(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''Sum of two ints.'''
        return a + b

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math', 'Keywords': ['-']})
    def substract(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''Int substraction.'''
        return a - b

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math', 'Keywords': ['-']})
    def substractf(a=(DataTypes.Float, 0), b=(DataTypes.Float, 0)):
        '''Int substraction.'''
        return a - b

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math', 'Keywords': ['/']})
    def divide(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Integer devision.'''
        try:
            d = a / b
            result.setData(True)
            return d
        except:
            result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math', 'Keywords': ['/']})
    def dividef(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Float devision.'''
        try:
            d = a / b
            result.setData(True)
            return d
        except:
            result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math', 'Keywords': ['*']})
    def mult(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''Integer multiplication.'''
        return a * b

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math', 'Keywords': ['*']})
    def multf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''Float multiplication.'''
        return a * b

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bult-in functions', 'Keywords': []})
    def absint(inp=(DataTypes.Int, 0)):
        '''Return the absolute value of a number.'''
        return abs(inp)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Bult-in functions', 'Keywords': []})
    def absfloat(inp=(DataTypes.Float, 0.0)):
        '''Return the absolute value of a number.'''
        return abs(inp)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Trigonometry', 'Keywords': []})
    def cos(rad=(DataTypes.Float, 0.0)):
        '''Return the cosine of x radians.'''
        return math.cos(rad)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Trigonometry', 'Keywords': []})
    def acos(rad=(DataTypes.Float, 0.0)):
        '''Return the arc cosine of x, in radians.'''
        return math.acos(rad)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Trigonometry', 'Keywords': []})
    def sin(rad=(DataTypes.Float, 0.0)):
        '''Return the sine of x radians.'''
        return math.sin(rad)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Trigonometry', 'Keywords': []})
    def asin(rad=(DataTypes.Float, 0.0)):
        '''Return the arc sine of x, in radians.'''
        return math.asin(rad)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Trigonometry', 'Keywords': []})
    def tan(rad=(DataTypes.Float, 0.0)):
        '''Return the tangent of x radians.'''
        return math.tan(rad)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Trigonometry', 'Keywords': []})
    def atan(rad=(DataTypes.Float, 0.0)):
        '''Return the arc tangent of x, in radians.'''
        return math.atan(rad)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Trigonometry', 'Keywords': []})
    def atan2(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''Return atan(a / b), in radians. The result is between -pi and pi.\nThe vector in the plane from the origin to point (a, b) makes this angle with the positive X axis. The point of atan2() is that the signs of both inputs are known to it, so it can compute the correct quadrant for the angle.\nFor example, atan(1) and atan2(1, 1) are both pi/4, but atan2(-1, -1) is -3*pi/4.'''
        return math.atan2(a, b)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Trigonometry', 'Keywords': []})
    def hypot(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0)):
        '''Return the Euclidean norm, sqrt(x*x + y*y). This is the length of the vector from the origin to point (x, y).'''
        return math.hypot(a, b)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Angular conversion', 'Keywords': []})
    def degtorad(deg=(DataTypes.Float, 0.0)):
        '''Convert angle x from degrees to radians.'''
        return math.radians(deg)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Angular conversion', 'Keywords': []})
    def radtodeg(rad=(DataTypes.Float, 0.0)):
        '''Convert angle x from radians to degrees.'''
        return math.degrees(rad)

    @staticmethod
    @implementNode(returns=None, meta={'Category': 'Math|random', 'Keywords': []})
    def randint(start=(DataTypes.Int, 0), end=(DataTypes.Int, 10), Result=(DataTypes.Reference, DataTypes.Int)):
        '''Return a random integer N such that a <= N <= b.'''
        Result.setData(random.randint(start, end))

    @staticmethod
    @implementNode(returns=None, meta={'Category': 'Math|random', 'Keywords': []})
    def shuffle(seq=(DataTypes.Array, []), Result=(DataTypes.Reference, DataTypes.Array)):
        '''Shuffle the sequence x in place.'''
        random.shuffle(seq)
        Result.setData(seq)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Hyperbolic functions', 'Keywords': []})
    def acosh(a=(DataTypes.Float, 0.0), Result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the inverse hyperbolic cosine of x.'''
        try:
            Result.setData(True)
            return math.acosh(a)
        except:
            Result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Hyperbolic functions', 'Keywords': []})
    def asinh(a=(DataTypes.Float, 0.0)):
        '''Return the inverse hyperbolic sine of x.'''
        return math.asinh(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Hyperbolic functions', 'Keywords': []})
    def atanh(a=(DataTypes.Float, 0.0), Result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the inverse hyperbolic tangent of x.'''
        try:
            Result.setData(True)
            return math.atanh(a)
        except:
            Result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Hyperbolic functions', 'Keywords': []})
    def cosh(a=(DataTypes.Float, 0.0), Result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the hyperbolic cosine of x.'''
        try:
            Result.setData(True)
            return math.cosh(a)
        except:
            Result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Hyperbolic functions', 'Keywords': []})
    def sinh(a=(DataTypes.Float, 0.0), Result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the hyperbolic sine of x.'''
        try:
            Result.setData(True)
            return math.sinh(a)
        except:
            Result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Hyperbolic functions', 'Keywords': []})
    def tanh(a=(DataTypes.Float, 0.0)):
        '''Return the hyperbolic tangent of x.'''
        return math.tanh(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Special functions', 'Keywords': []})
    def erf(a=(DataTypes.Float, 0.0)):
        '''Return the error function at x.'''
        return math.erf(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Special functions', 'Keywords': []})
    def erfc(a=(DataTypes.Float, 0.0)):
        '''Return the complementary error function at x.'''
        return math.erfc(a)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Special functions', 'Keywords': []})
    def gamma(a=(DataTypes.Float, 0.0), Result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the Gamma function at x.'''
        try:
            Result.setData(True)
            return math.gamma(a)
        except:
            Result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Special functions', 'Keywords': []})
    def lgamma(a=(DataTypes.Float, 0.0), Result=(DataTypes.Reference, DataTypes.Bool)):
        '''Return the natural logarithm of the absolute value of the Gamma function at x.'''
        try:
            Result.setData(True)
            return math.lgamma(a)
        except:
            Result.setData(False)
            return -1

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Constants', 'Keywords': []})
    def e():
        '''The mathematical constant e = 2.718281, to available precision.'''
        return math.e

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Constants', 'Keywords': []})
    def pi():
        '''The mathematical constant = 3.141592, to available precision.'''
        return math.pi

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math', 'Keywords': ['lerp']})
    def lerpf(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), alpha=(DataTypes.Float, 0.0)):
        return lerp(a, b, clamp(alpha, 0.0, 1.0))

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math', 'Keywords': ['clamp']})
    def clampf(i=(DataTypes.Float, 0.0), imin=(DataTypes.Float, 0.0), imax=(DataTypes.Float, 0.0)):
        return clamp(i, imin, imax)
