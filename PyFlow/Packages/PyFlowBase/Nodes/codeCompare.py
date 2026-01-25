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
codeCompare Node - Represents comparison operations.

Used for visual representation of code like:
    if a > b:
    while x != 0:
    result = a == b

Supports: ==, !=, <, >, <=, >=, in, not in
This is a pure data node (no exec pins) since comparisons are expressions.
"""

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


CODE_VIS_COLOR = (100, 200, 150, 200)  # Greenish for comparison


class codeCompare(NodeBase):
    """Node representing a Python comparison operation.
    
    Takes two inputs, outputs boolean result.
    This is a pure data node (no exec pins) - feeds into branch nodes.
    """
    
    def __init__(self, name):
        super(codeCompare, self).__init__(name)
        
        # Input pins
        self.inA = self.createInputPin(
            "a", "AnyPin", structure=StructureType.Single
        )
        self.inA.enableOptions(PinOptions.AllowAny)
        
        self.inB = self.createInputPin(
            "b", "AnyPin", structure=StructureType.Single
        )
        self.inB.enableOptions(PinOptions.AllowAny)
        
        # Output boolean result
        self.outResult = self.createOutputPin("result", "BoolPin")
        
        # Store the comparison operator
        self._operator = ">"  # Default: greater than
        self._expression = ""  # Full expression for display
        
        # Connect input changes to recompute
        pinAffects(self.inA, self.outResult)
        pinAffects(self.inB, self.outResult)
        
        # Visual appearance
        self.headerColor = CODE_VIS_COLOR

    def setOperator(self, op):
        """Set the comparison operator: ==, !=, <, >, <=, >=, in, not in"""
        self._operator = op
    
    def setExpression(self, expr):
        """Set the full expression string for display (e.g., 'arr[i] > res')."""
        self._expression = expr

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("BoolPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["compare", "condition", ">", "<", "==", "!=", ">=", "<=", "code"]

    @staticmethod
    def description():
        return "Represents a Python comparison (a > b, x == y). Outputs boolean result."

    def serialize(self):
        """Save node state including operator."""
        data = super(codeCompare, self).serialize()
        data["operator"] = self._operator
        data["expression"] = self._expression
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codeCompare, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._operator = jsonTemplate.get("operator", ">")
            self._expression = jsonTemplate.get("expression", "")

    def compute(self, *args, **kwargs):
        """Compute the comparison and output result."""
        a = self.inA.getData()
        b = self.inB.getData()
        
        result = False
        try:
            if self._operator == "==":
                result = a == b
            elif self._operator == "!=":
                result = a != b
            elif self._operator == "<":
                result = a < b
            elif self._operator == ">":
                result = a > b
            elif self._operator == "<=":
                result = a <= b
            elif self._operator == ">=":
                result = a >= b
            elif self._operator == "in":
                result = a in b
            elif self._operator == "not in":
                result = a not in b
            else:
                # Default to greater than
                result = a > b
        except (TypeError, ValueError):
            result = False
        
        self.outResult.setData(result)
