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
        printNode1 = NodeBase.initializeFromFunction(foos["pyprint"])
        man.activeGraph().addNode(printNode1)
        printNode1.setData('entity', "first")

        branchNode = nodes["branch"]("branchNODE")
        self.assertIsNotNone(branchNode, "branch node is not created")
        man.activeGraph().addNode(branchNode)
        branchNode.setData('Condition', True)

        connected = connectPins(printNode1.getPin(DEFAULT_OUT_EXEC_NAME), branchNode.getPin("In"))
        self.assertEqual(connected, True, "failed to connect")

        printNodeTrue = NodeBase.initializeFromFunction(foos["pyprint"])
        man.activeGraph().addNode(printNodeTrue)
        printNodeTrue.setData('entity', "True executed")

        printNodeFalse = NodeBase.initializeFromFunction(foos["pyprint"])
        man.activeGraph().addNode(printNodeFalse)
        printNodeFalse.setData('entity', "False executed")

        connectPins(branchNode.getPin('True'), printNodeTrue.getPin(DEFAULT_IN_EXEC_NAME))
        connectPins(branchNode.getPin('False'), printNodeFalse.getPin(DEFAULT_IN_EXEC_NAME))

        printNode1.call(DEFAULT_IN_EXEC_NAME, message="TEST MESSAGE")
