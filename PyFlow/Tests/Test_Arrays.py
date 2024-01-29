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


from PyFlow.Tests.TestsBase import *
from PyFlow.Core.Common import *
from collections import Counter


class TestArrays(unittest.TestCase):
    def setUp(self):
        print("\t[BEGIN TEST]", self._testMethodName)

    def tearDown(self):
        print("--------------------------------\n")

    def test_makeList_Node(self):
        packages = GET_PACKAGES()
        man = GraphManager()
        nodes = packages["PyFlowBase"].GetNodeClasses()
        foos = (
            packages["PyFlowBase"].GetFunctionLibraries()["DefaultLib"].getFunctions()
        )
        classNodes = packages["PyFlowBase"].GetNodeClasses()

        makeListNode = nodes["makeArray"]("mkList")
        man.activeGraph().addNode(makeListNode)
        makeIntNode = NodeBase.initializeFromFunction(foos["makeInt"])
        makeIntNode2 = NodeBase.initializeFromFunction(foos["makeInt"])
        man.activeGraph().addNode(makeIntNode)
        man.activeGraph().addNode(makeIntNode2)
        printNode = classNodes["consoleOutput"]("printer")
        man.activeGraph().addNode(printNode)

        connected = connectPins(makeIntNode[str("out")], makeListNode[str("data")])
        connected = connectPins(makeIntNode2[str("out")], makeListNode[str("data")])
        self.assertEqual(connected, True)
        connected = connectPins(makeListNode[str("out")], printNode[str("entity")])
        printNode[DEFAULT_IN_EXEC_NAME].call()
        result = makeListNode[str("out")].getData()
        self.assertEqual(Counter(result), Counter([0, 0]))
