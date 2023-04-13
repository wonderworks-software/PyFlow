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

import os
import sys
import json
import threading
import time

from qtpy.QtWidgets import *
from qtpy import QtGui
from qtpy import QtCore
from PyFlow.PyFlow import INITIALIZE
from PyFlow.PyFlow.Core.Common import *
from PyFlow.PyFlow.Core.GraphManager import GraphManagerSingleton
from PyFlow.PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.PyFlow.UI.Utils.stylesheet import editableStyleSheet
from PyFlow.PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
import PyFlow.UI.resources


def run(filePath):
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("plastique"))
    app.setStyleSheet(editableStyleSheet().getStyleSheet())

    msg = QMessageBox()
    msg.setWindowIcon(QtGui.QIcon(":/LogoBpApp.png"))
    msg.setIcon(QMessageBox.Critical)

    if os.path.exists(filePath):
        with open(filePath, 'r') as f:
            data = json.load(f)

        # Window to display inputs
        prop = QDialog()
        prop.setLayout(QVBoxLayout())
        prop.setWindowTitle(filePath)
        prop.setWindowIcon(QtGui.QIcon(":/LogoBpApp.png"))
        # Initialize packages
        try:
            INITIALIZE()
            man = GraphManagerSingleton().get()
            man.deserialize(data)
            grph = man.findRootGraph()
            inputs = grph.getNodesByClassName("graphInputs")
            if len(inputs) > 0:
                for inp in inputs:
                    uiNode = getUINodeInstance(inp)
                    uiNodeJsonTemplate = inp.serialize()
                    uiNodeJsonTemplate["wrapper"] = inp.wrapperJsonData
                    uiNode.postCreate(uiNodeJsonTemplate)
                    cat = CollapsibleFormWidget(headName=inp.name)
                    prop.layout().addWidget(cat) 
                    cat = uiNode.createOutputWidgets(cat)

                nodes = grph.getNodesList()
                if len(nodes) > 0:
                    for node in nodes:
                        uiNode = getUINodeInstance(node)
                        uiNodeJsonTemplate = node.serialize()
                        uiNodeJsonTemplate["wrapper"] = node.wrapperJsonData
                        uiNode.postCreate(uiNodeJsonTemplate)
                        if uiNode.bExposeInputsToCompound:
                            cat = CollapsibleFormWidget(headName="{} inputs".format(node.name))
                            prop.layout().addWidget(cat)                        
                            uiNode.createInputWidgets(cat, pins=False)
                prop.show()
                def programLoop():
                    while True:
                        man.Tick(deltaTime=0.02)
                        time.sleep(0.02)
                        if man.terminationRequested:
                            break
                t = threading.Thread(target=programLoop)
                t.start()

                def quitEvent():
                    man.terminationRequested = True
                    t.join()
                app.aboutToQuit.connect(quitEvent)
            # If no GraphInput Nodes Exit propgram   
            else:
                msg.setInformativeText(filePath)
                msg.setDetailedText("The file doesn't contain graphInputs nodes")
                msg.setWindowTitle("PyFlow Ui Graph Parser")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.show()

        except Exception as e:
            msg.setText("Error reading Graph")
            msg.setInformativeText(filePath)
            msg.setDetailedText(str(e))
            msg.setWindowTitle("PyFlow Ui Graph Parser")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()

    else:
        msg.setText("File Not Found")
        msg.setInformativeText(filePath)
        msg.setWindowTitle("PyFlow Ui Graph Parser")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
