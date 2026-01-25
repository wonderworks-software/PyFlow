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
codeForLoop Node - Represents a Python for loop for code visualization.

Used for visual representation of code like:
    for i in range(1, len(arr)):
    for x in items:

Enhanced version of forLoop with better integration for code visualization.
Stores the original code expression for display.
"""

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


FLOW_CONTROL_COLOR = (255, 150, 100, 200)  # Orange for control flow


class codeForLoop(NodeBase):
    """Node representing a Python for loop.
    
    Iterates from Start to Stop, outputs current Index.
    Has LoopBody exec for each iteration, Completed exec when done.
    """
    
    def __init__(self, name):
        super(codeForLoop, self).__init__(name)
        
        # Execution input
        self.inExec = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        
        # Loop parameters
        self.firstIndex = self.createInputPin("Start", "IntPin")
        self.firstIndex.setData(0)
        
        self.lastIndex = self.createInputPin("Stop", "IntPin")
        self.lastIndex.setData(10)
        
        self.step = self.createInputPin("Step", "IntPin")
        self.step.setData(1)
        
        # Execution outputs
        self.loopBody = self.createOutputPin("LoopBody", "ExecPin")
        self.completed = self.createOutputPin("Completed", "ExecPin")
        
        # Data output
        self.index = self.createOutputPin("Index", "IntPin")
        
        # Store loop info for display
        self._loopVar = "i"
        self._iterableExpr = ""  # e.g., "range(1, len(arr))"
        self._fullExpr = ""  # e.g., "for i in range(1, len(arr))"
        
        # Visual appearance
        self.headerColor = FLOW_CONTROL_COLOR

    def setLoopVariable(self, var):
        """Set the loop variable name (e.g., 'i')."""
        self._loopVar = var
    
    def setIterableExpression(self, expr):
        """Set the iterable expression (e.g., 'range(1, len(arr))')."""
        self._iterableExpr = expr
    
    def setFullExpression(self, expr):
        """Set the full loop expression for display."""
        self._fullExpr = expr

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("IntPin")
        helper.addOutputDataType("ExecPin")
        helper.addOutputDataType("IntPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["for", "loop", "iterate", "range", "code"]

    @staticmethod
    def description():
        return "Represents a Python for loop. Iterates from Start to Stop, outputting Index each iteration."

    def serialize(self):
        """Save node state."""
        data = super(codeForLoop, self).serialize()
        data["loopVar"] = self._loopVar
        data["iterableExpr"] = self._iterableExpr
        data["fullExpr"] = self._fullExpr
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codeForLoop, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._loopVar = jsonTemplate.get("loopVar", "i")
            self._iterableExpr = jsonTemplate.get("iterableExpr", "")
            self._fullExpr = jsonTemplate.get("fullExpr", "")

    def compute(self, *args, **kwargs):
        """Execute the for loop."""
        indexFrom = self.firstIndex.getData()
        indexTo = self.lastIndex.getData()
        stepVal = self.step.getData()
        
        if stepVal == 0:
            # Avoid infinite loop
            self.completed.call(*args, **kwargs)
        else:
            for i in range(indexFrom, indexTo, stepVal):
                # Set current index
                self.index.setData(i)
                push(self.index)
                
                # Execute loop body
                self.loopBody.call(*args, **kwargs)
            
            # Loop completed
            self.completed.call(*args, **kwargs)
