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


import argparse
import sys
import os
import json
from PyFlow.App import PyFlow
from PyFlow import graphUiParser
from Qt.QtWidgets import QApplication
from PyFlow import INITIALIZE
from PyFlow.Core.Common import *
from PyFlow.Core.GraphManager import GraphManager


def getGraphArguments(data, parser):

    typeMapping = {
        "BoolPin": bool,
        "StringPin": str,
        "IntPin": int,
        "FloatPin": float
    }

    graphNode = None
    for node in data["nodes"]:
        if node["type"] == "graphInputs":
            graphNode = node
            break

    for outPin in graphNode["outputs"]:
        pinType = outPin["dataType"]
        if pinType != "ExecPin":
            parser.add_argument("--{0}".format(outPin["name"]), type=typeMapping[pinType])


def main():
    parser = argparse.ArgumentParser(description="PyFlow CLI")
    parser.add_argument("-m", "--mode", type=str, default="edit", choices=["edit", "run", "runui"])
    parser.add_argument("-f", "--filePath", type=str, default="untitled.json")
    parsedArguments, unknown = parser.parse_known_args(sys.argv[1:])

    filePath = parsedArguments.filePath

    if not filePath.endswith(".json"):
        filePath += ".json"

    if parsedArguments.mode == "edit":
        app = QApplication(sys.argv)

        instance = PyFlow.instance(software="standalone")
        if instance is not None:
            app.setActiveWindow(instance)
            instance.show()
            if os.path.exists(filePath):
                with open(filePath, 'r') as f:
                    data = json.load(f)
                    instance.loadFromData(data)

            try:
                sys.exit(app.exec_())
            except Exception as e:
                print(e)

    if parsedArguments.mode == "run":
        data = None
        with open(filePath, 'r') as f:
            data = json.load(f)
        getGraphArguments(data, parser)
        parsedArguments = parser.parse_args()

        # load updated data
        INITIALIZE()
        GM = GraphManager()
        GM.deserialize(data)

        # call graph inputs nodes
        root = GM.findRootGraph()
        graphInputNodes = root.getNodesList(classNameFilters=["graphInputs"])
        evalFunctions = []
        for graphInput in graphInputNodes:
            # update data
            for outPin in graphInput.outputs.values():
                if outPin.isExec():
                    evalFunctions.append(outPin.call)
                if hasattr(parsedArguments, outPin.name):
                    cliValue = getattr(parsedArguments, outPin.name)
                    if cliValue is not None:
                        outPin.setData(cliValue)

        for foo in evalFunctions:
            foo()

    if parsedArguments.mode == "runui":
        graphUiParser.run(filePath)
