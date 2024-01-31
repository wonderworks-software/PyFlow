## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from PyFlow.Core import FunctionLibraryBase, IMPLEMENT_NODE
from PyFlow.Core.Common import *


class MathAbstractLib(FunctionLibraryBase):
    """doc string for MathAbstractLib"""

    def __init__(self, packageName):
        super(MathAbstractLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: ["=", "operator"]},
    )
    # Is a equal b
    def isEqual(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
    ):
        """Is a equal b."""
        return a == b
    
    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={NodeMeta.CATEGORY: 'Math|Basic', NodeMeta.KEYWORDS: ["!=", "operator"]})
    ## Is a equal b
    def notEqual(a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
                b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"})):
        """Is a equal b."""
        return a != b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: [">", "operator"]},
    )
    def isGreater(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        result=(REF, ("BoolPin", False)),
    ):
        """Operator **>**."""
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: [">", "operator"]},
    )
    def isGreaterOrEqual(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        result=(REF, ("BoolPin", False)),
    ):
        """Operator **>=**."""
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: ["<", "operator"]},
    )
    def isLess(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        result=(REF, ("BoolPin", False)),
    ):
        """Operator **<**."""
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: ["<", "operator"]},
    )
    def isLessOrEqual(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
    ):
        """Operator **<=**."""
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        meta={
            NodeMeta.CATEGORY: "Math|Basic",
            NodeMeta.KEYWORDS: ["+", "append", "sum", "operator"],
        },
    )
    def add(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
    ):
        """Operator **+**."""
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        meta={
            NodeMeta.CATEGORY: "Math|Basic",
            NodeMeta.KEYWORDS: ["-", "operator", "minus"],
        },
    )
    def subtract(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
    ):
        """Operator **-**."""
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        meta={
            NodeMeta.CATEGORY: "Math|Basic",
            NodeMeta.KEYWORDS: ["/", "divide", "operator"],
        },
    )
    def divide(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
    ):
        """Operator **/**."""
        return a / b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        meta={
            NodeMeta.CATEGORY: "Math|Basic",
            NodeMeta.KEYWORDS: ["*", "multiply", "operator"],
        },
    )
    def multiply(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        b=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
    ):
        """Operator *****."""
        return a * b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}),
        meta={
            NodeMeta.CATEGORY: "Math|Basic",
            NodeMeta.KEYWORDS: ["*", "multiply", "operator"],
        },
    )
    def multiply_by_float(
        a=("AnyPin", None, {PinSpecifiers.CONSTRAINT: "1"}), b=("FloatPin", 1.0)
    ):
        """Operator *****."""
        return a * b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: ["in", "range"]},
    )
    def inRange(
        Value=(
            "AnyPin",
            None,
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"],
            },
        ),
        RangeMin=(
            "AnyPin",
            None,
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"],
            },
        ),
        RangeMax=(
            "AnyPin",
            None,
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"],
            },
        ),
        InclusiveMin=("BoolPin", False),
        InclusiveMax=("BoolPin", False),
    ):
        """Returns true if value is between Min and Max (V >= Min && V <= Max) If InclusiveMin is true, value needs to be equal or larger than Min,\
             else it needs to be larger If InclusiveMax is true, value needs to be smaller or equal than Max, else it needs to be smaller
        """
        return ((Value >= RangeMin) if InclusiveMin else (Value > RangeMin)) and (
            (Value <= RangeMax) if InclusiveMax else (Value < RangeMax)
        )

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: []},
    )
    def mapRangeClamped(
        Value=("FloatPin", 0.0),
        InRangeA=("FloatPin", 0.0),
        InRangeB=("FloatPin", 0.0),
        OutRangeA=("FloatPin", 0.0),
        OutRangeB=("FloatPin", 0.0),
    ):
        """Returns Value mapped from one range into another where the Value is clamped to the Input Range.\
             (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)"""
        return mapRangeClamped(Value, InRangeA, InRangeB, OutRangeA, OutRangeB)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: []},
    )
    def mapRangeUnclamped(
        Value=("FloatPin", 0.0),
        InRangeA=("FloatPin", 0.0),
        InRangeB=("FloatPin", 0.0),
        OutRangeA=("FloatPin", 0.0),
        OutRangeB=("FloatPin", 0.0),
    ):
        """Returns Value mapped from one range into another where the Value is clamped to the Input Range.\
             (e.g. 0.5 normalized from the range 0->1 to 0->50 would result in 25)"""
        return mapRangeUnclamped(Value, InRangeA, InRangeB, OutRangeA, OutRangeB)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: ["clamp"]},
    )
    def clamp(i=("FloatPin", 0.0), imin=("FloatPin", 0.0), imax=("FloatPin", 0.0)):
        """Clamp."""
        return clamp(i, imin, imax)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=(
            "AnyPin",
            None,
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"],
            },
        ),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: ["operator"]},
    )
    def modulo(
        a=(
            "AnyPin",
            None,
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"],
            },
        ),
        b=(
            "AnyPin",
            None,
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"],
            },
        ),
    ):
        """Modulo (A % B)."""
        return a % b

    @staticmethod
    @IMPLEMENT_NODE(
        returns=(
            "AnyPin",
            None,
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"],
            },
        ),
        meta={NodeMeta.CATEGORY: "Math|Basic", NodeMeta.KEYWORDS: []},
    )
    def abs(
        inp=(
            "AnyPin",
            None,
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin"],
            },
        )
    ):
        """Return the absolute value of a number."""
        return abs(inp)
