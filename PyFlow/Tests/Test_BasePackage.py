from PyFlow.Tests.TestsBase import *
from PyFlow.Core.Common import *


class TestBasePackage(unittest.TestCase):

    def setUp(self):
        print('\t[BEGIN TEST]', self._testMethodName)

    def tearDown(self):
        print('--------------------------------\n')

    def test_branch_node(self):
        packages = GET_PACKAGES()
        man = GraphManager()
        foos = packages['PyflowBase'].GetFunctionLibraries()["DefaultLib"].getFunctions()
        nodes = packages['PyflowBase'].GetNodeClasses()
        printNode1 = nodes["consoleOutput"]("print")
        man.activeGraph().addNode(printNode1)
        printNode1.setData(str('entity'), "first")

        branchNode = nodes["branch"]("branchNODE")
        self.assertIsNotNone(branchNode, "branch node is not created")
        man.activeGraph().addNode(branchNode)
        branchNode.setData('Condition', True)

        connected = connectPins(printNode1[str(DEFAULT_OUT_EXEC_NAME)], branchNode[str("In")])
        self.assertEqual(connected, True, "failed to connect")

        printNodeTrue = nodes["consoleOutput"]("print")
        man.activeGraph().addNode(printNodeTrue)
        printNodeTrue.setData('entity', "True executed")

        printNodeFalse = nodes["consoleOutput"]("print")
        man.activeGraph().addNode(printNodeFalse)
        printNodeFalse.setData('entity', "False executed")

        connectPins(branchNode[str('True')], printNodeTrue[DEFAULT_IN_EXEC_NAME])
        connectPins(branchNode[str('False')], printNodeFalse[DEFAULT_IN_EXEC_NAME])

        printNode1.call(DEFAULT_IN_EXEC_NAME, message="TEST MESSAGE")
