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
codeLen Node - Represents len() function call.

Used for visual representation of code like:
    n = len(arr)
    for i in range(len(items)):

This is a pure data node that outputs the length of an iterable.
"""

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


CODE_VIS_COLOR = (100, 150, 200, 200)  # Light blue for functions


class codeLen(NodeBase):
    """Node representing Python's len() function.
    
    Takes an iterable input, outputs its length.
    Pure data node (no exec pins) - used in expressions.
    """
    
    def __init__(self, name):
        super(codeLen, self).__init__(name)
        
        # Input - the iterable (array, string, dict, etc.)
        self.inIterable = self.createInputPin(
            "iterable", "AnyPin", structure=StructureType.Multi
        )
        self.inIterable.enableOptions(PinOptions.AllowAny)
        
        # Output - the length
        self.outLength = self.createOutputPin("length", "IntPin")
        
        # Store variable name for display
        self._iterableName = ""
        
        # Connect input to output
        pinAffects(self.inIterable, self.outLength)
        
        # Visual appearance
        self.headerColor = CODE_VIS_COLOR

    def setIterableName(self, name):
        """Set the iterable variable name for display (e.g., 'arr')."""
        self._iterableName = name

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("IntPin")
        helper.addInputStruct(StructureType.Multi)
        helper.addInputStruct(StructureType.Array)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["len", "length", "size", "count", "code"]

    @staticmethod
    def description():
        return "Represents Python's len() function. Outputs the length of an iterable."

    def serialize(self):
        """Save node state."""
        data = super(codeLen, self).serialize()
        data["iterableName"] = self._iterableName
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codeLen, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._iterableName = jsonTemplate.get("iterableName", "")

    def compute(self, *args, **kwargs):
        """Compute the length of the input."""
        iterable = self.inIterable.getData()
        
        length = 0
        if iterable is not None:
            try:
                length = len(iterable)
            except TypeError:
                length = 0
        
        self.outLength.setData(length)
