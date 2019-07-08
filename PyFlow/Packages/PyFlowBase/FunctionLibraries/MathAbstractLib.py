from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class MathAbstractLib(FunctionLibraryBase):
    """doc string for MathAbstractLib"""
    def __init__(self, packageName):
        super(MathAbstractLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["=", "operator"]})
    ## Is a equal b
    def isEqual(a=("AnyPin", None, {"constraint": "1"}),
                b=("AnyPin", None, {"constraint": "1"})):
        """Is a equal b."""
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': [">", "operator"]})
    def isGreater(a=("AnyPin", None, {"constraint": "1"}),
                  b=("AnyPin", None, {"constraint": "1"}),
                  result=("Reference", ("BoolPin", False))):
        """Operator **>**."""
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': [">", "operator"]})
    def isGreaterOrEqual(a=("AnyPin", None, {"constraint": "1"}),
                         b=("AnyPin", None, {"constraint": "1"}),
                         result=("Reference", ("BoolPin", False))):
        """Operator **>=**."""
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["<", "operator"]})
    def isLess(a=("AnyPin", None, {"constraint": "1"}), b=("AnyPin", None, {"constraint": "1"}),
               result=("Reference", ("BoolPin", False))):
        """Operator **<**."""
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["<", "operator"]})
    def isLessOrEqual(a=("AnyPin", None, {"constraint": "1"}), b=("AnyPin", None, {"constraint": "1"})):
        """Operator **<=**."""
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", None, {"constraint": "1"})), meta={'Category': 'Math|Basic', 'Keywords': ['+', 'append', "sum", "operator"]})
    def add(a=("AnyPin", None, {"constraint": "1"}), b=("AnyPin", None, {"constraint": "1"})):
        """Operator **+**."""
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", None, {"constraint": "1"})), meta={'Category': 'Math|Basic', 'Keywords': ['-', "operator", "minus"]})
    def subtract(a=("AnyPin", None, {"constraint": "1"}), b=("AnyPin", None, {"constraint": "1"})):
        """Operator **-**."""
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1"}), meta={'Category': 'Math|Basic', 'Keywords': ['/', "divide", "operator"]})
    def divide(a=("AnyPin", None, {"constraint": "1"}), b=("AnyPin", None, {"constraint": "1"})):
        """Operator **/**."""
        return a / b

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", None, {"constraint": "1"})), meta={'Category': 'Math|Basic', 'Keywords': ['*', "multiply", "operator"]})
    def multiply(a=("AnyPin", None, {"constraint": "1"}), b=("AnyPin", None, {"constraint": "1"})):
        """Operator *****."""
        return a * b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["in", "range"]})
    def inRange(Value=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                RangeMin=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                RangeMax=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
                InclusiveMin=("BoolPin", False),
                InclusiveMax=("BoolPin", False)):
        """Returns true if value is between Min and Max (V >= Min && V <= Max) If InclusiveMin is true, value needs to be equal or larger than Min,\
             else it needs to be larger If InclusiveMax is true, value needs to be smaller or equal than Max, else it needs to be smaller
        """
        return ((Value >= RangeMin) if InclusiveMin else (Value > RangeMin)) and ((Value <= RangeMax) if InclusiveMax else (Value < RangeMax))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Basic', 'Keywords': []})
    def mapRangeClamped(Value=("FloatPin", 0.0),
                        InRangeA=("FloatPin", 0.0),
                        InRangeB=("FloatPin", 0.0),
                        OutRangeA=("FloatPin", 0.0),
                        OutRangeB=("FloatPin", 0.0)):
        """Returns Value mapped from one range into another where the Value is clamped to the Input Range.\
             (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)"""
        ClampedPct = clamp(GetRangePct(InRangeA, InRangeB, Value), 0.0, 1.0)
        return lerp(OutRangeA, OutRangeB, ClampedPct)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Basic', 'Keywords': []})
    def mapRangeUnclamped(Value=("FloatPin", 0.0),
                          InRangeA=("FloatPin", 0.0),
                          InRangeB=("FloatPin", 0.0),
                          OutRangeA=("FloatPin", 0.0),
                          OutRangeB=("FloatPin", 0.0)):
        """Returns Value mapped from one range into another where the Value is clamped to the Input Range.\
             (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)"""
        return lerp(OutRangeA, OutRangeB, GetRangePct(InRangeA, InRangeB, Value))

    @staticmethod
    @IMPLEMENT_NODE(returns=("FloatPin", None), meta={'Category': 'Math|Basic', 'Keywords': ['clamp']})
    def clamp(i=("FloatPin", None),
              imin=("FloatPin", 0.0),
              imax=("FloatPin", 0)):
        """Clamp."""
        return clamp(i, imin, imax)

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}), meta={'Category': 'Math|Basic', 'Keywords': ["operator"]})
    def modulo(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}),
               b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]})):
        """Modulo (A % B)."""
        return a % b

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]}), meta={'Category': 'Math|Basic', 'Keywords': []})
    def abs(inp=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatPin", "IntPin"]})):
        """Return the absolute value of a number."""
        return abs(inp)
