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


from PyFlow.PyFlow.Core import NodeBase
from PyFlow.PyFlow.Core.PathsRegistry import PathsRegistry
from PyFlow.PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.PyFlow.Core.Common import *
from PyFlow.PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_ORANGE

import threading

class forLoopBegin(NodeBase):
    def __init__(self, name):
        super(forLoopBegin, self).__init__(name)
        self._working = False
        self.currentIndex = 0
        self.prevIndex = -1
        self.inExec = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.firstIndex = self.createInputPin('Start', 'IntPin')
        self.lastIndex = self.createInputPin('Stop', 'IntPin')
        self.loopEndNode = self.createInputPin('Paired block', 'StringPin')
        self.loopEndNode.setInputWidgetVariant("ObjectPathWIdget")

        self.loopBody = self.createOutputPin('LoopBody', 'ExecPin')
        self.index = self.createOutputPin('Index', 'IntPin')
        self.headerColor = FLOW_CONTROL_ORANGE
        self.setExperimental()

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('IntPin')
        helper.addOutputDataType('ExecPin')
        helper.addOutputDataType('IntPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter']

    @staticmethod
    def description():
        return 'For loop begin block'

    def reset(self):
        self.currentIndex = 0
        self.prevIndex = -1
        #self._working = False

    def isDone(self):
        indexTo = self.lastIndex.getData()
        if self.currentIndex >= indexTo:
            self.reset()
            #loopEndNode = PathsRegistry().getEntity(self.loopEndNode.getData())
            #loopEndNode.completed.call()
            self._working = False
            return True
        return False

    def onNext(self, *args, **kwargs):
        while not self.isDone():
            if self.currentIndex > self.prevIndex:
                self.index.setData(self.currentIndex)
                self.prevIndex = self.currentIndex 
                self.loopBody.call()

    def compute(self, *args, **kwargs):
        self.reset()
        endNodePath = self.loopEndNode.getData()
        loopEndNode = PathsRegistry().getEntity(endNodePath)
        if loopEndNode is not None:
            if loopEndNode.loopBeginNode.getData() != self.path():
                self.setError("Invalid pair")
                return
            if self.graph() is not loopEndNode.graph():
                err = "block ends in different graphs"
                self.setError(err)
                loopEndNode.setError(err)
                return
        else:
            self.setError("{} not found".format(endNodePath))
        if not self._working:
            self.thread = threading.Thread(target=self.onNext,args=(self, args, kwargs))
            self.thread.start() 
            self._working = True
        #self.onNext(*args, **kwargs)
