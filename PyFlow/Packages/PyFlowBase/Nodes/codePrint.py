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
codePrint Node - Represents print() function call.

Used for visual representation of code like:
    print(result)
    print("Hello", x, y)

This node has exec pins and prints the value to console.
Similar to consoleOutput but styled for code visualization.
"""

import logging

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.ConfigManager import ConfigManager
from PyFlow.Core.Common import *


CODE_VIS_COLOR = (255, 200, 100, 200)  # Yellowish for output


class codePrint(NodeBase):
    """Node representing Python's print() function.
    
    Prints the input value and continues execution flow.
    Has exec pins for sequential execution.
    """
    
    def __init__(self, name):
        super(codePrint, self).__init__(name)
        
        # Execution pins
        self.inExec = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, "ExecPin")
        
        # Input value to print
        self.entity = self.createInputPin(
            "entity", "AnyPin", structure=StructureType.Multi
        )
        self.entity.enableOptions(PinOptions.AllowAny)
        
        # Store what we're printing for display
        self._printExpr = ""
        
        # Visual appearance
        self.headerColor = CODE_VIS_COLOR

    def setPrintExpression(self, expr):
        """Set the expression being printed for display (e.g., 'res')."""
        self._printExpr = expr

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("ExecPin")
        helper.addInputStruct(StructureType.Multi)
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CodeVisualization"

    @staticmethod
    def keywords():
        return ["print", "output", "console", "code"]

    @staticmethod
    def description():
        return "Represents Python's print() function. Outputs value to console with exec flow."

    def serialize(self):
        """Save node state."""
        data = super(codePrint, self).serialize()
        data["printExpr"] = self._printExpr
        return data

    def postCreate(self, jsonTemplate=None):
        """Restore node state from saved data."""
        super(codePrint, self).postCreate(jsonTemplate)
        if jsonTemplate:
            self._printExpr = jsonTemplate.get("printExpr", "")

    def compute(self, *args, **kwargs):
        """Print the value and continue execution flow."""
        # Check if output should be redirected to PyFlow console
        redirectionEnabled = ConfigManager().shouldRedirectOutput()
        
        if self.getWrapper() is not None and redirectionEnabled:
            data = str(self.entity.getData())
            if self.entity.dataType != "StringPin":
                data = data.encode("unicode-escape")
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            data = str(data).replace("\\n", "<br/>")

            errorLink = (
                """<a href=%s><span style=" text-decoration: underline; color:green;">%s</span></a></p>"""
                % (self.name, "<br/>%s" % data)
            )
            logging.getLogger(None).consoleoutput(errorLink)
        else:
            # Regular print
            print(self.entity.getData())
        
        # Continue execution flow
        self.outExec.call(*args, **kwargs)
