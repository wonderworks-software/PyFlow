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


import asyncio
import time

from PyFlow.Core import NodeBase, PinBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR
import json


class subProcess(NodeBase):
    def __init__(self, name):
        super(subProcess, self).__init__(name)
        self.bCacheEnabled = False
        self.inExecPin = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.cwd = self.createInputPin('cwd', 'StringPin', "")
        self.cmd = self.createInputPin('cmd', 'StringPin')
        self.cmd_end = self.createInputPin('cmd_end', 'StringPin')
        self.cmd_end.enableOptions(PinOptions.AllowMultipleConnections)
        self.cmd_opt = self.createInputPin('cmd_opt', 'StringPin')
        self.cmd_opt.enableOptions(PinOptions.AllowMultipleConnections)
        self.outExecPin = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.error_num = self.createOutputPin('error_num', 'IntPin')
        self.std_msg = self.createOutputPin('std_msg', 'StringPin')
        self.error_msg = self.createOutputPin('error_msg', 'StringPin')
        self.all_msg = self.createOutputPin('all_msg', 'StringPin')
        self.is_running = self.createOutputPin('is_running', 'BoolPin', False)
        self.headerColor = FLOW_CONTROL_COLOR
        self.proc = None
        self.proc_task:asyncio.Task = None
        self.proc_task_uuid = uuid.uuid4()
        self.proc_task_args = None
        self.proc_task_kwargs =None

    def addInPin(self, name, dataType):
        p = self.createInputPin(name, dataType)
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic 
                        | PinOptions.AllowMultipleConnections | PinOptions.Storable)
        return p

    def postCreate(self, jsonTemplate=None):
        super(subProcess, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        existingPins = self.namePinInputsMap
        if jsonTemplate is not None:
            sortedInputs = sorted(jsonTemplate["inputs"], key=lambda x: x["pinIndex"])
            for inPinJson in sortedInputs:
                if inPinJson['name'] not in existingPins:
                    inDyn = self.addInPin(inPinJson['name'], inPinJson["dataType"])
                    inDyn.uid = uuid.UUID(inPinJson['uuid'])
                    try:
                        val = json.loads(inPinJson['value'], cls=inDyn.jsonDecoderClass())
                        inDyn.setData(val)
                    except:
                        inDyn.setData(inDyn.defaultValue())

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('StringPin')
        helper.addInputDataType('StringPin')
        helper.addInputDataType('StringPin')
        helper.addInputDataType('StringPin')
        helper.addOutputDataType('ExecPin')
        helper.addOutputDataType('IntPin')
        helper.addOutputDataType('StringPin')
        helper.addOutputDataType('StringPin')
        helper.addOutputDataType('StringPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'Cmd'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'call an subprocess'

    def compute(self, *args, **kwargs):
        cmd_head = str(self.cmd.getData())
        if len(cmd_head) <= 0:
            self.error_num.setData(-1)
            self.std_msg.setData("")
            self.error_msg.setData("")
            self.all_msg.setData("")
            self.outExecPin.call(*args, **kwargs)
        else:
            cmd_opt = str(self.cmd_opt.getData())
            cmd_end = str(self.cmd_end.getData())
            opt_except_pin = [self.inExecPin, self.cmd, self.cmd_end, self.cmd_opt, self.cwd]
            cmd_opt_ext = ""
            for elem in self.orderedInputs.values():
                if elem in opt_except_pin:
                    continue
                name = elem.name.lstrip()
                if 0 == len(name) or name.isdigit():
                    cmd_opt_ext += " {0} ".format(elem.getData())
                    continue
                if 1 == len(name) and name.isalpha():
                    cmd_opt_ext += " -{0} {1} ".format(name ,elem.getData()) 
                    continue
                if name[:1] == "-":
                    cmd_opt_ext += " {0} {1} ".format(name ,elem.getData())    
                    continue 
                cmd_opt_ext += " --{0} {1} ".format(name ,elem.getData()) 
            cmd = f"{cmd_head} {cmd_opt} {cmd_opt_ext} {cmd_end} "  
            if self.proc_task:
                self.proc_task.cancel("interrupt")
                self.proc_task = None
            self.proc_task_uuid = uuid.uuid4()
            self.proc_task_args = args
            self.proc_task_kwargs = kwargs
            self.is_running.setData(True)
            self.proc_task = asyncio.get_event_loop().create_task(self._run_cmd(self.proc_task_uuid, cmd, self.cwd.getData()))
        
    async def _run_cmd(self, _uuid, cmd, cwd):
        if None != self.proc and None == self.proc.returncode:
            self.proc.terminate()
        self.computing.send()
        self.proc = None
        uuid = _uuid
        if len(cwd.strip(" ")) > 0:
            proc:asyncio.subprocess.Process = await asyncio.create_subprocess_shell(
                cmd, cwd=cwd, stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
        else:
            proc:asyncio.subprocess.Process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
        self.proc = proc
        stdout, stderr = await proc.communicate()
        ret_code = proc.returncode
        if uuid == self.proc_task_uuid:
            self.proc = None
        return uuid, ret_code, stdout, stderr
    
    def Tick(self, delta):
        super(subProcess, self).Tick(delta)
        if self.proc_task and self.proc_task.done():
            proc_task:asyncio.Task = self.proc_task
            self.proc_task = None
            if not proc_task.cancelled():
                try:
                    uuid, error_num, stdout, stderr = proc_task.result()
                    if uuid == self.proc_task_uuid:
                        self.error_num.setData(error_num)
                        self.std_msg.setData(stdout)
                        self.error_msg.setData(stderr)
                        self.all_msg.setData(f"{stdout}\n{stderr}")
                except Exception as e:
                    print("subProcess proc task raise exception", e)
                    self.error_num.setData(-1)
                    self.std_msg.setData("")
                    self.error_msg.setData(str(e))
                    self.all_msg.setData(str(e))
            if self.proc:
                if None == self.proc.returncode:
                    self.proc.terminate()
                self.proc = None
            self.computed.send()
            self.is_running.setData(False)
            self.outExecPin.call(*self.proc_task_args, **self.proc_task_kwargs)