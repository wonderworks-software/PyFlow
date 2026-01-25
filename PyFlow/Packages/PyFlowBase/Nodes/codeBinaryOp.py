## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera
## Extended 2024 for Code Visualization

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

"""
codeBinaryOp Node - Represents binary operations.

Used for visual representation of code like:
    x + y
    a * b
    total - discount

Supports: +, -, *, /, //, %, **
This is a pure data node (no exec pins) since these are expressions.
"""

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


CODE_VIS_COLOR = (150, 150, 200, 200)  # Purple-ish for math


class codeBinaryOp(NodeBase):
    """Node representing a Python binary operation.
    
    Takes two inputs, outputs the result of the operation.
    Pure data node (no exec pins).
    """
    
    def __init__(self, name):
        super(codeBinaryOp, self).__init__(name)
        
        # Input pins
        self.inA = self.createInputPin(
            "a", "AnyPin", structure=StructureType.Single
        )
        self.inA.enableOptions(PinOptions.AllowAny)
        
        self.inB = self.createInputPin(
            "b", "AnyPin", structure=StructureType.Single
        )
        self.inB.enableOptions(PinOptions.AllowAny)
        
        # Output result
        self.outResult = self.createOutputPin(
            "result", "AnyPin", structure=StructureType.Single
        )
        self.outResult.enableOptions(PinOptions.AllowAny)
        
        # Store the operator
        self._operator = "+"  # Default: addition
        self._expression = ""  # Full expression for display
        
        # Connect input changes to recompute
        pinAffects(self.inA, self.outResult)
        pinAffects(self.inB, self.outResult)
        
        # Visual appearance
        self.headerColor = CODE_VIS_COLOR

    def setOperator(self, op):
        """Set the binary operator: +, -, *, /, //, %, **"""
        self._operator = op
    
    def setExpression(self, expr):
        """Set the full expression string for display (e.g., 'a + b')."""
        self._expression = expr

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("AnyPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["math", "add", "subtract", "multiply", "divide", "+", "-", "*", "/", "code"]

    @staticmethod
    def description():
        return "Represents a Python binary operation (a + b, x * y). Outputs the computed result."

    def serialize(self):
        """Save node state including operator."""
        data = super(codeBinaryOp, self).serialize()
        data["operator"] = self._operator
        data["expression"] = self._expression
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codeBinaryOp, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._operator = jsonTemplate.get("operator", "+")
            self._expression = jsonTemplate.get("expression", "")

    def compute(self, *args, **kwargs):
        """Compute the binary operation and output result."""
        a = self.inA.getData()
        b = self.inB.getData()
        
        result = None
        try:
            if self._operator == "+":
                result = a + b
            elif self._operator == "-":
                result = a - b
            elif self._operator == "*":
                result = a * b
            elif self._operator == "/":
                result = a / b if b != 0 else None
            elif self._operator == "//":
                result = a // b if b != 0 else None
            elif self._operator == "%":
                result = a % b if b != 0 else None
            elif self._operator == "**":
                result = a ** b
            else:
                # Default to addition
                result = a + b
        except (TypeError, ValueError, ZeroDivisionError):
            result = None
        
        self.outResult.setData(result)
