from PyFlow.Tests.TestsBase import *
from PyFlow.Core.Common import *
from collections import Counter


class TestArrays(unittest.TestCase):

    def setUp(self):
        print('\t[BEGIN TEST]', self._testMethodName)

    def tearDown(self):
        print('--------------------------------\n')

    def test_makeList_Node(self):
        packages = GET_PACKAGES()
        man = GraphManager()
        nodes = packages['PyflowBase'].GetNodeClasses()
        foos = packages['PyflowBase'].GetFunctionLibraries()["DefaultLib"].getFunctions()
        classNodes = packages['PyflowBase'].GetNodeClasses()

        makeListNode = nodes['makeArray']("mkList")
        man.activeGraph().addNode(makeListNode)
        makeIntNode = NodeBase.initializeFromFunction(foos['makeInt'])
        makeIntNode2 = NodeBase.initializeFromFunction(foos['makeInt'])
        man.activeGraph().addNode(makeIntNode)
        man.activeGraph().addNode(makeIntNode2)
        printNode = classNodes["consoleOutput"]("printer")
        man.activeGraph().addNode(printNode)

        connected = connectPins(makeIntNode[str('out')], makeListNode[str('data')])
        connected = connectPins(makeIntNode2[str('out')], makeListNode[str('data')])
        self.assertEqual(connected, True)
        connected = connectPins(makeListNode[str('out')], printNode[str("entity")])
        printNode[DEFAULT_IN_EXEC_NAME].call()
        result = makeListNode[str('out')].getData()
        self.assertEqual(Counter(result), Counter([0, 0]))
