from TestsBase import *


class TestGeneral(unittest.TestCase):
    def test_add_int(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")
        intlib = packages['BasePackage'].GetFunctionLibraries()["IntLib"]
        mathFoos = intlib.getFunctions()

        addNode1 = NodeBase.initializeFromFunction(dict(mathFoos)["add"])
        addNode2 = NodeBase.initializeFromFunction(dict(mathFoos)["add"])

        g.addNode(addNode1)
        g.addNode(addNode2)

        addNode1.setData('a', 5)

        edge = g.addEdge(addNode1.getPinByName('out', PinSelectionGroup.Outputs), addNode2.getPinByName('a', PinSelectionGroup.Inputs))
        self.assertIsNotNone(edge, "FAILED TO ADD EDGE")
        self.assertEqual(addNode2.getData('out'), 5, "NODES EVALUATION IS INCORRECT")


if __name__ == '__main__':
    unittest.main()
