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
codeArrayAccess Node - Represents array element access.

Used for visual representation of code like:
    x = arr[0]
    value = items[i]
    result = data[index]

This node takes an array and index, outputs the element at that index.
"""

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


CODE_VIS_COLOR = (70, 130, 180, 200)


class codeArrayAccess(NodeBase):
    """Node representing array element access (arr[i]).
    
    Takes array and index inputs, outputs the element.
    Has exec flow for sequential execution.
    """
    
    def __init__(self, name):
        super(codeArrayAccess, self).__init__(name)
        
        # Execution pins
        self.inExec = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, "ExecPin")
        
        # Input pins
        self.inArray = self.createInputPin(
            "array", "AnyPin", structure=StructureType.Array
        )
        self.inArray.enableOptions(PinOptions.AllowAny)
        
        self.inIndex = self.createInputPin("index", "IntPin")
        self.inIndex.setData(0)
        
        # Output element pin
        self.outElement = self.createOutputPin(
            "element", "AnyPin", structure=StructureType.Single
        )
        self.outElement.enableOptions(PinOptions.AllowAny)
        
        # Store variable names for display
        self._arrayName = ""
        self._resultName = ""
        
        # Visual appearance
        self.headerColor = CODE_VIS_COLOR

    def setArrayName(self, name):
        """Set the array variable name for display (e.g., 'arr')."""
        self._arrayName = name
    
    def setResultName(self, name):
        """Set the result variable name for display (e.g., 'x')."""
        self._resultName = name

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("AnyPin")
        helper.addInputDataType("IntPin")
        helper.addOutputDataType("ExecPin")
        helper.addOutputDataType("AnyPin")
        helper.addInputStruct(StructureType.Array)
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["array", "index", "access", "[]", "element", "code"]

    @staticmethod
    def description():
        return "Represents array element access (arr[i]). Gets element at index from array."

    def serialize(self):
        """Save node state."""
        data = super(codeArrayAccess, self).serialize()
        data["arrayName"] = self._arrayName
        data["resultName"] = self._resultName
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codeArrayAccess, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._arrayName = jsonTemplate.get("arrayName", "")
            self._resultName = jsonTemplate.get("resultName", "")

    def compute(self, *args, **kwargs):
        """Get element at index from array and continue flow."""
        arr = self.inArray.getData()
        index = self.inIndex.getData()
        
        # Get element safely
        element = None
        if arr is not None and isinstance(arr, (list, tuple)):
            if 0 <= index < len(arr):
                element = arr[index]
            elif index < 0 and abs(index) <= len(arr):
                element = arr[index]  # Support negative indexing
        
        # Output the element
        self.outElement.setData(element)
        
        # Continue execution flow
        self.outExec.call(*args, **kwargs)
