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
        makeListNode = nodes['makeArray']("mkList")
        man.activeGraph().addNode(makeListNode)
        makeIntNode = NodeBase.initializeFromFunction(foos['makeInt'])
        makeIntNode2 = NodeBase.initializeFromFunction(foos['makeInt'])
        man.activeGraph().addNode(makeIntNode)
        man.activeGraph().addNode(makeIntNode2)
        connected = connectPins(makeIntNode[str('out')], makeListNode[str('data')])
        connected = connectPins(makeIntNode2[str('out')], makeListNode[str('data')])
        self.assertEqual(connected, True)
        result = makeListNode[str('out')].getData()
        self.assertEqual(Counter(result), Counter([0, 0]))
