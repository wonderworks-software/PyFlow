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
            if IS_PYTHON2:
                data = data.replace("\\n","<br/>")
            else:
                data = data.replace(b"\\n", b"<br/>").decode('unicode-escape')

            errorLink = """<a href=%s><span style=" text-decoration: underline; color:green;">%s</span></a></p>"""%(self.name,"<br/>%s"%data)
            logging.getLogger(None).consoleoutput(errorLink)
        else:         
            print("%s: %s"%(self.name,self.entity.getData()))
        self.outExec.call()
