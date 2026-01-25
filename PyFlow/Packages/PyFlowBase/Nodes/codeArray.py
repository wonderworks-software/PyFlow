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
codeArray Node - Represents a Python array/list literal.

Used for visual representation of code like:
    arr = [10, 324, 45, 90]
    items = [1, 2, 3]

This node has exec pins for sequential flow and outputs the array.
Unlike makeArray, this stores a literal array value and has exec pins.
"""

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


CODE_VIS_COLOR = (70, 130, 180, 200)


class codeArray(NodeBase):
    """Node representing a Python list/array literal.
    
    Stores an array value and outputs it.
    Has exec flow for sequential execution.
    """
    
    def __init__(self, name):
        super(codeArray, self).__init__(name)
        
        # Execution pins
        self.inExec = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, "ExecPin")
        
        # Output array pin
        self.outArray = self.createOutputPin(
            "array", "AnyPin", structure=StructureType.Array
        )
        self.outArray.enableOptions(PinOptions.AllowAny)
        
        # Store the literal array elements
        self._elements = []
        self._varName = ""
        
        # Visual appearance
        self.headerColor = CODE_VIS_COLOR

    @property
    def varName(self):
        return self._varName
    
    @varName.setter
    def varName(self, name):
        self._varName = name
    
    def setElements(self, elements):
        """Set the array elements (e.g., [10, 324, 45])."""
        self._elements = list(elements) if elements else []
    
    def getElements(self):
        return self._elements

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addOutputDataType("ExecPin")
        helper.addOutputDataType("AnyPin")
        helper.addOutputStruct(StructureType.Array)
        helper.addInputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["array", "list", "[]", "code", "literal"]

    @staticmethod
    def description():
        return "Represents a Python list literal ([1, 2, 3]). Stores and outputs an array with exec flow."

    def serialize(self):
        """Save node state including array elements."""
        data = super(codeArray, self).serialize()
        data["elements"] = self._elements
        data["varName"] = self._varName
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codeArray, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._elements = jsonTemplate.get("elements", [])
            self._varName = jsonTemplate.get("varName", "")

    def compute(self, *args, **kwargs):
        """Output the stored array and continue execution flow."""
        # Output the array
        self.outArray.setData(self._elements)
        
        # Continue execution flow
        self.outExec.call(*args, **kwargs)
