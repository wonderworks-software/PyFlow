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
        self.assertEqual(edge, True, "FAILED TO ADD EDGE")
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

        g.addNode(randintNode)
        g.addNode(printNode)
        g.addNode(converterNode)

        self.assertIsNotNone(randintNode)
        self.assertIsNotNone(printNode)
        self.assertIsNotNone(converterNode)

        pRandIntResultPin = randintNode.getPinByName('Result', PinSelectionGroup.Outputs)
        pRandIntOutExecPin = randintNode.getPinByName('outExec', PinSelectionGroup.Outputs)
        pRandIntInExecPin = randintNode.getPinByName('inExec', PinSelectionGroup.Inputs)
        pConverterInputPin = converterNode.getPinByName('i', PinSelectionGroup.Inputs)
        pConverterOutPin = converterNode.getPinByName('out', PinSelectionGroup.Outputs)
        pPrintInputValuePin = printNode.getPinByName('entity', PinSelectionGroup.Inputs)
        pPrintInputExecPin = printNode.getPinByName('inExec', PinSelectionGroup.Inputs)
        self.assertIsNotNone(pRandIntResultPin)
        self.assertIsNotNone(pConverterInputPin)
        self.assertIsNotNone(pConverterOutPin)
        self.assertIsNotNone(pPrintInputValuePin)
        self.assertIsNotNone(pRandIntOutExecPin)
        self.assertIsNotNone(pPrintInputExecPin)

        edge1Created = g.addEdge(pRandIntResultPin, pConverterInputPin)
        edge2Created = g.addEdge(pConverterOutPin, pPrintInputValuePin)
        edge3Created = g.addEdge(pRandIntOutExecPin, pPrintInputExecPin)
        self.assertEqual(edge1Created, True, "FAILED TO ADD EDGE 1")
        self.assertEqual(edge2Created, True, "FAILED TO ADD EDGE 2")
        self.assertEqual(edge3Created, True, "FAILED TO ADD EDGE 3")

        g.plot()
        pRandIntInExecPin.call()


if __name__ == '__main__':
    unittest.main()
