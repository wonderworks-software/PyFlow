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
codeBranch Node - Represents a Python if statement for code visualization.

Used for visual representation of code like:
    if arr[i] > res:
    if x == y:
    if condition:

Enhanced version of branch with better integration for code visualization.
Stores the original condition expression for display.
"""

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


FLOW_CONTROL_COLOR = (255, 128, 64, 200)  # Orange-red for branch


class codeBranch(NodeBase):
    """Node representing a Python if statement.
    
    Takes a boolean condition, branches to True or False exec.
    Stores the original condition expression for display.
    """
    
    def __init__(self, name):
        super(codeBranch, self).__init__(name)
        
        # Execution input
        self.inExec = self.createInputPin(
            "In", "ExecPin", None, self.compute
        )
        
        # Condition input
        self.condition = self.createInputPin("Condition", "BoolPin")
        
        # Execution outputs
        self.trueExec = self.createOutputPin("True", "ExecPin")
        self.falseExec = self.createOutputPin("False", "ExecPin")
        
        # Store condition info for display
        self._conditionExpr = ""  # e.g., "arr[i] > res"
        self._fullExpr = ""  # e.g., "if arr[i] > res:"
        
        # Visual appearance
        self.headerColor = FLOW_CONTROL_COLOR

    def setConditionExpression(self, expr):
        """Set the condition expression (e.g., 'arr[i] > res')."""
        self._conditionExpr = expr
    
    def setFullExpression(self, expr):
        """Set the full if statement expression for display."""
        self._fullExpr = expr

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("BoolPin")
        helper.addOutputDataType("ExecPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["if", "branch", "condition", "else", "code"]

    @staticmethod
    def description():
        return "Represents a Python if statement. Branches to True or False based on condition."

    def serialize(self):
        """Save node state."""
        data = super(codeBranch, self).serialize()
        data["conditionExpr"] = self._conditionExpr
        data["fullExpr"] = self._fullExpr
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codeBranch, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._conditionExpr = jsonTemplate.get("conditionExpr", "")
            self._fullExpr = jsonTemplate.get("fullExpr", "")

    def compute(self, *args, **kwargs):
        """Branch based on condition."""
        data = self.condition.getData()
        if data:
            self.trueExec.call(*args, **kwargs)
        else:
            self.falseExec.call(*args, **kwargs)
