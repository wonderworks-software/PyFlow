from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class MathAbstractLib(FunctionLibraryBase):
    '''doc string for MathAbstractLib'''
    def __init__(self, packageName):
        super(MathAbstractLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["="]})
    ## Is a equal b
    def isEqual(a=("AnyPin", None, {"constraint": "1"}),
                b=("AnyPin", None, {"constraint": "1"})):
        '''
        Is a equal b
        '''
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': [">"]})
    ## Is a > b
    def isGreater(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                "FloatVector3Pin", "FloatVector4Pin"]}),
                  b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                "FloatVector3Pin", "FloatVector4Pin"]})):
        '''
        Is a > b
        '''
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': [">"]})
    ## Is a >= b
    def isGreaterOrEqual(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                       "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                       "FloatVector3Pin", "FloatVector4Pin"]}),
                         b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                       "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                       "FloatVector3Pin", "FloatVector4Pin"]})):
        '''
        Is a >= b
        '''
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["<"]})
    ## Is a < b
    def isLess(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                             "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                             "FloatVector3Pin", "FloatVector4Pin"]}),
               b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                             "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                             "FloatVector3Pin", "FloatVector4Pin"]})):
        '''
        Is a < b
        '''
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["<"]})
    ## Is a <= b
    def isLessOrEqual(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                    "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                    "FloatVector3Pin", "FloatVector4Pin"]}),
                      b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                    "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                    "FloatVector3Pin", "FloatVector4Pin"]})):
        '''
        Is a <= b
        '''
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", None, {"constraint": "1"})), meta={'Category': 'Math|Basic', 'Keywords': ['+', 'append', "sum"]})
    ## Basic Sum
    def add(a=("AnyPin", None, {"constraint": "1"}), b=("AnyPin", None, {"constraint": "1"})):
        '''
        Basic Sum
        '''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", None, {"constraint": "1"})), meta={'Category': 'Math|Basic', 'Keywords': ['-']})
    ## Basic subtraction
    def subtract(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                               "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                               "FloatVector3Pin", "FloatVector4Pin"]}),
                 b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                               "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                               "FloatVector3Pin", "FloatVector4Pin"]})):
        '''
        Basic subtraction
        '''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1"}), meta={'Category': 'Math|Basic', 'Keywords': ['/', "divide"]})
    ## Basic division
    def divide(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                             "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                             "FloatVector3Pin", "FloatVector4Pin"]}),
               b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                             "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                             "FloatVector3Pin", "FloatVector4Pin"]}),
               result=("Reference", ("BoolPin", False))):
        '''
        Basic division
        '''
        try:
            d = a / b
            result(True)
            return d
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", None, {"constraint": "1"})), meta={'Category': 'Math|Basic', 'Keywords': ['*', "multiply"]})
    ## Basic multiplication
    def multiply(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                               "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                               "FloatVector3Pin", "FloatVector4Pin"]}),
                 b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                               "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                               "FloatVector3Pin", "FloatVector4Pin"]})):
        '''
        Basic multiplication
        '''
        return a * b

    @staticmethod
    @IMPLEMENT_NODE(returns=("FloatPin", 0.0), meta={'Category': 'Math|Basic', 'Keywords': ['vector', '|', 'dot', 'product']})
    def dotProduct(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatVector4Pin", "FloatVector3Pin", "QuatPin"]}),
                   b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatVector4Pin", "FloatVector3Pin", "QuatPin"]})):
        '''Dot product'''
        if type(a) == "Quaternion":
            return a.dot(b)
        return a | b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["in", "range"]})
    def inRange(Value=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                  "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                  "FloatVector3Pin", "FloatVector4Pin"]}),
                RangeMin=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                     "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                     "FloatVector3Pin", "FloatVector4Pin"]}),
                RangeMax=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["BoolPin", "FloatPin", "IntPin",
                                                                                     "Matrix33Pin", "Matrix44Pin", "QuatPin",
                                                                                     "FloatVector3Pin", "FloatVector4Pin"]}),
                InclusiveMin=("BoolPin", False),
                InclusiveMax=("BoolPin", False)):
        '''
        Returns true if value is between Min and Max (V &gt;= Min && V &lt;= Max) If InclusiveMin is true, value needs to be equal or larger than Min,\
             else it needs to be larger If InclusiveMax is true, value needs to be smaller or equal than Max, else it needs to be smaller
        '''
        return ((Value >= RangeMin) if InclusiveMin else (Value > RangeMin)) and ((Value <= RangeMax) if InclusiveMax else (Value < RangeMax))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Basic', 'Keywords': []})
    def mapRangeClamped(Value=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                        InRangeA=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                        InRangeB=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                        OutRangeA=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                        OutRangeB=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]})):
        '''
        Returns Value mapped from one range into another where the Value is clamped to the Input Range.\
             (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)
        '''
        ClampedPct = clamp(GetRangePct(InRangeA, InRangeB, Value), 0.0, 1.0)
        return lerp(OutRangeA, OutRangeB, ClampedPct)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Basic', 'Keywords': []})
    def mapRangeUnclamped(Value=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                          InRangeA=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                          InRangeB=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                          OutRangeA=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                          OutRangeB=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]})):
        '''
        Returns Value mapped from one range into another where the Value is clamped to the Input Range.\
             (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)
        '''
        return lerp(OutRangeA, OutRangeB, GetRangePct(InRangeA, InRangeB, Value))

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                    meta={'Category': 'Math|Basic', 'Keywords': ['clamp']})
    ## Clamp
    def clamp(i=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
              imin=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
              imax=("AnyPin", 0, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}, 0.0)):
        '''
        Clamp
        '''
        return clamp(i, imin, imax)

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}), meta={'Category': 'Math|Basic', 'Keywords': []})
    def modulo(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
               b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]})):
        '''
        Modulo (A % B)
        '''
        return a % b

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}), meta={'Category': 'Math|Basic', 'Keywords': []})
    ## Return the absolute value of a number
    def abs(inp=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]})):
        '''
        Return the absolute value of a number
        '''
        return abs(inp)
