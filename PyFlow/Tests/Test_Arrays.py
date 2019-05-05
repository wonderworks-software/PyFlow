from PyFlow.Tests.TestsBase import *
from PyFlow.Core.Common import *


class TestArrays(unittest.TestCase):

    def setUp(self):
        print('\t[BEGIN TEST]', self._testMethodName)

    def tearDown(self):
        print('--------------------------------\n')

    def test_connectToArray(self):
        packages = GET_PACKAGES()
        man = GraphManager()
        nodes = packages['PyflowBase'].GetNodeClasses()
        foos = packages['PyflowBase'].GetFunctionLibraries()["DefaultLib"].getFunctions()
        makeListNode = nodes['makeList']("mkList")
        man.activeGraph().addNode(makeListNode)
        makeIntNode = NodeBase.initializeFromFunction(foos['makeInt'])
        man.activeGraph().addNode(makeIntNode)
        connected = connectPins(makeIntNode['out'], makeListNode['data'])
        self.assertEqual(connected, True)
        result = makeListNode['out'].getData()
        self.assertCountEqual(result, [0])
