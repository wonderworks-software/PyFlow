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
codeAssign Node - Represents a Python variable assignment.

Used for visual representation of code like:
    x = 5
    name = "hello"
    result = a + b

This node has exec pins for sequential flow and stores the assigned value.
"""

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


# Color for code visualization nodes (blue-ish)
CODE_VIS_COLOR = (70, 130, 180, 200)


class codeAssign(NodeBase):
    """Node representing a Python assignment statement.
    
    Stores a value and outputs it through a named pin.
    Has exec flow for sequential execution.
    """
    
    def __init__(self, name):
        super(codeAssign, self).__init__(name)
        
        # Execution pins
        self.inExec = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, "ExecPin")
        
        # Data pins
        self.inValue = self.createInputPin(
            "value", "AnyPin", structure=StructureType.Multi
        )
        self.inValue.enableOptions(PinOptions.AllowAny)
        
        self.outValue = self.createOutputPin(
            "out", "AnyPin", structure=StructureType.Multi
        )
        self.outValue.enableOptions(PinOptions.AllowAny)
        
        # Store the variable name and literal value
        self._varName = ""
        self._literalValue = None
        self._hasLiteral = False
        
        # Visual appearance
        self.headerColor = CODE_VIS_COLOR

    @property
    def varName(self):
        return self._varName
    
    @varName.setter
    def varName(self, name):
        self._varName = name
        # Update the output pin name to match variable
        if name and hasattr(self, 'outValue'):
            # Can't rename pins after creation, but we store it
            pass
    
    def setLiteralValue(self, value):
        """Set a literal value that this node outputs (e.g., 5, "hello", [1,2,3])."""
        self._literalValue = value
        self._hasLiteral = True
    
    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("ExecPin")
        helper.addOutputDataType("AnyPin")
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["assign", "set", "variable", "=", "code"]

    @staticmethod
    def description():
        return "Represents a Python assignment statement (x = value). Stores and outputs a value with exec flow."

    def serialize(self):
        """Save node state including variable name and literal value."""
        data = super(codeAssign, self).serialize()
        data["varName"] = self._varName
        data["literalValue"] = self._literalValue
        data["hasLiteral"] = self._hasLiteral
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codeAssign, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._varName = jsonTemplate.get("varName", "")
            self._literalValue = jsonTemplate.get("literalValue", None)
            self._hasLiteral = jsonTemplate.get("hasLiteral", False)

    def compute(self, *args, **kwargs):
        """Execute the assignment: get input value or use literal, output it, continue flow."""
        # Get value from input pin or use literal
        if self._hasLiteral:
            value = self._literalValue
        else:
            value = self.inValue.getData()
        
        # Output the value
        self.outValue.setData(value)
        
        # Continue execution flow
        self.outExec.call(*args, **kwargs)
