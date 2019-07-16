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


from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from nine import *
import logging

class consoleOutput(NodeBase):
    def __init__(self, name):
        super(consoleOutput, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.entity = self.createInputPin('entity', 'AnyPin', structure=PinStructure.Multi)
        self.entity.enableOptions(PinOptions.AllowAny)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(PinStructure.Multi)
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return ['print']

    @staticmethod
    def description():
        return "Python's 'print' function wrapper"

    def compute(self, *args, **kwargs):
        if self.getWrapper() is not None:
            data = str(self.entity.getData())
            if self.entity.dataType != "StringPin":
                data = data.encode('unicode-escape')
            data = data.replace("\\n", "<br/>")

            errorLink = """<a href=%s><span style=" text-decoration: underline; color:green;">%s</span></a></p>""" % (self.name, "<br/>%s" % data)
            logging.getLogger(None).consoleoutput(errorLink)
        else:
            print("{0}: {1}".format(self.name, self.entity.getData()))
        self.outExec.call()
