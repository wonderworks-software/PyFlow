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


class TestBasePackage(unittest.TestCase):
    def setUp(self):
        print("\t[BEGIN TEST]", self._testMethodName)

    def tearDown(self):
        print("--------------------------------\n")

    def test_branch_node(self):
        packages = GET_PACKAGES()
        man = GraphManager()
        foos = (
            packages["PyFlowBase"].GetFunctionLibraries()["DefaultLib"].getFunctions()
        )
        nodes = packages["PyFlowBase"].GetNodeClasses()
        printNode1 = nodes["consoleOutput"]("print")
        man.activeGraph().addNode(printNode1)
        printNode1.setData(str("entity"), "first")

        branchNode = nodes["branch"]("branchNODE")
        self.assertIsNotNone(branchNode, "branch node is not created")
        man.activeGraph().addNode(branchNode)
        branchNode.setData("Condition", True)

        connected = connectPins(
            printNode1[str(DEFAULT_OUT_EXEC_NAME)], branchNode[str("In")]
        )
        self.assertEqual(connected, True, "failed to connect")

        printNodeTrue = nodes["consoleOutput"]("print")
        man.activeGraph().addNode(printNodeTrue)
        printNodeTrue.setData("entity", "True executed")

        printNodeFalse = nodes["consoleOutput"]("print")
        man.activeGraph().addNode(printNodeFalse)
        printNodeFalse.setData("entity", "False executed")

        connectPins(branchNode[str("True")], printNodeTrue[DEFAULT_IN_EXEC_NAME])
        connectPins(branchNode[str("False")], printNodeFalse[DEFAULT_IN_EXEC_NAME])

        printNode1.call(DEFAULT_IN_EXEC_NAME, message="TEST MESSAGE")
