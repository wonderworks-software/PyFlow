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
import unittest

from PyFlow.App import PyFlow
from PyFlow.Core.Common import currentProcessorTime
from PyFlow.Packages.PyFlowBase.Nodes.subProcess import subProcess
from PyFlow.Tests.TestsBase import INITIALIZE


class _TickRecorder(object):
    def __init__(self):
        self.deltas = []

    def get(self):
        return self

    def Tick(self, delta):
        self.deltas.append(delta)


class _DummyPyFlow(object):
    def __init__(self):
        self._lastClock = currentProcessorTime()
        self.fps = 0
        self.graphManager = _TickRecorder()
        self.canvasWidget = _TickRecorder()

    async def _tick_asyncio(self):
        await asyncio.sleep(0)


class TestAsyncioCompatibility(unittest.TestCase):
    def setUp(self):
        self._loops = []
        asyncio.set_event_loop(None)
        INITIALIZE()

    def tearDown(self):
        for loop in self._loops:
            if loop is None or loop.is_closed():
                continue
            pending = [task for task in asyncio.all_tasks(loop) if not task.done()]
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(
                    asyncio.gather(*pending, return_exceptions=True)
                )
            loop.close()

        asyncio.set_event_loop(None)

    def test_main_loop_runs_without_implicit_default_event_loop(self):
        dummy = _DummyPyFlow()

        PyFlow.mainLoop(dummy)
        self._loops.append(asyncio.get_event_loop())

        self.assertEqual(len(dummy.graphManager.deltas), 1)
        self.assertEqual(len(dummy.canvasWidget.deltas), 1)

    def test_subprocess_compute_creates_task_without_implicit_default_event_loop(self):
        node = subProcess("cmd")
        node.cmd.setData("echo")

        node.compute()

        self.assertIsNotNone(node.proc_task)
        self._loops.append(node.proc_task.get_loop())
