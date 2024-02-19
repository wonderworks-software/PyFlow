from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *

import threading

import time
   
@SingletonDecorator
class singletonThread():
    isRunning = False
    instanceCount = 0
    def __init__(self):
        self.Runner = threading.Thread(target=self.run_loop, daemon=True)
        self.value = 0
        if not self.isRunning:
            self.Runner.start()
            self.isRunning = True

    def run_loop(self):
        self.isRunning = True
        while self.isRunning:
            time.sleep(0.1)
            print("running")
            self.value +=1

    def cleanUp(self):
        print(self.instanceCount)
        self.instanceCount -= 1
        if self.instanceCount == 0:        
            self.isRunning = False
            self.Runner.join()
            del self
            print("cleanUp")

class singletonThreadSampleNode(NodeBase):
    def __init__(self, name):
        super(singletonThreadSampleNode, self).__init__(name)
        self.singletonThread = None
        self.value = self.createOutputPin('value', 'IntPin')

    def postCreate(self, jsonTemplate=None):
        self.singletonThread = singletonThread()
        if not self.singletonThread.isRunning:
            self.singletonThread.Runner = threading.Thread(target=self.singletonThread.run_loop, daemon=True)
            self.singletonThread.Runner.start()        
        self.bCacheEnabled = False
        super(singletonThreadSampleNode, self).postCreate(jsonTemplate=jsonTemplate)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('StringPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Dict)
        return helper

    @staticmethod
    def category():
        return 'Interactive singletonThreads'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Get singletonThreadSampleNode Infos."

    def kill(self, *args, **kwargs):
        print("deleting singletonThreadSampleNode")
        self.singletonThread.cleanUp()
        super(singletonThreadSampleNode, self).kill(*args, **kwargs)

    def compute(self, *args, **kwargs):
        if not self.singletonThread.isRunning:
            self.singletonThread.Runner = threading.Thread(target=self.singletonThread.run_loop, daemon=True)
            self.singletonThread.Runner.start()
        self.value.setData(self.singletonThread.value)