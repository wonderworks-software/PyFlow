from TestsBase import *


class TestGeneral(unittest.TestCase):
    def test_add_int_no_exec(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")
        intlib = packages['BasePackage'].GetFunctionLibraries()["IntLib"]
        mathFoos = intlib.getFunctions()

        addNode1 = NodeBase.initializeFromFunction(mathFoos["add"])
        addNode2 = NodeBase.initializeFromFunction(mathFoos["add"])

        g.addNode(addNode1)
        g.addNode(addNode2)

        addNode1.setData('a', 5)

        edge = g.addEdge(addNode1.getPinByName('out', PinSelectionGroup.Outputs), addNode2.getPinByName('a', PinSelectionGroup.Inputs))
        self.assertIsNotNone(edge, "FAILED TO ADD EDGE")
        self.assertEqual(addNode2.getData('out'), 5, "NODES EVALUATION IS INCORRECT")

    def test_foo_node_ref_set_data(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")
        randomLib = packages['BasePackage'].GetFunctionLibraries()["RandomLib"]
        defaultLib = packages['BasePackage'].GetFunctionLibraries()["DefaultLib"]
        randomLibFoos = randomLib.getFunctions()
        defaultLibFoos = defaultLib.getFunctions()

        randintNode = NodeBase.initializeFromFunction(randomLibFoos["randint"])
        printNode = NodeBase.initializeFromFunction(defaultLibFoos["pyprint"])
        converterNode = NodeBase.initializeFromFunction(defaultLibFoos["intToString"])

        self.assertIsNotNone(randintNode)
        self.assertIsNotNone(printNode)
        self.assertIsNotNone(converterNode)

        edge1 = g.addEdge(randintNode.getPinByName('out', PinSelectionGroup.Outputs), converterNode.getPinByName('i', PinSelectionGroup.Inputs))
        self.assertIsNotNone(edge1)


if __name__ == '__main__':
    unittest.main()
