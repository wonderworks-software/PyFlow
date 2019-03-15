from TestsBase import *


class TestGeneral(unittest.TestCase):
    def test_add_int_no_exec(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")
        intlib = packages['PyflowBase'].GetFunctionLibraries()["IntLib"]
        mathFoos = intlib.getFunctions()

        addNode1 = NodeBase.initializeFromFunction(mathFoos["add"])
        addNode2 = NodeBase.initializeFromFunction(mathFoos["add"])

        g.addNode(addNode1)
        g.addNode(addNode2)

        addNode1.setData('a', 5)

        connection = g.addConnection(addNode1.getPinByName('out', PinSelectionGroup.Outputs), addNode2.getPinByName('a', PinSelectionGroup.Inputs))
        self.assertEqual(connection, True, "FAILED TO ADD EDGE")
        self.assertEqual(addNode2.getData('out'), 5, "NODES EVALUATION IS INCORRECT")

    def test_foo_node_ref_set_data(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")
        randomLib = packages['PyflowBase'].GetFunctionLibraries()["RandomLib"]
        defaultLib = packages['PyflowBase'].GetFunctionLibraries()["DefaultLib"]
        randomLibFoos = randomLib.getFunctions()
        defaultLibFoos = defaultLib.getFunctions()

        randintNode = NodeBase.initializeFromFunction(randomLibFoos["randint"])
        printNode = NodeBase.initializeFromFunction(defaultLibFoos["pyprint"])

        g.addNode(randintNode)
        g.addNode(printNode)

        self.assertIsNotNone(randintNode)
        self.assertIsNotNone(printNode)

        pRandIntResultPin = randintNode.getPinByName('Result', PinSelectionGroup.Outputs)
        pRandIntOutExecPin = randintNode.getPinByName('outExec', PinSelectionGroup.Outputs)
        pRandIntInExecPin = randintNode.getPinByName('inExec', PinSelectionGroup.Inputs)
        pPrintInputValuePin = printNode.getPinByName('entity', PinSelectionGroup.Inputs)
        pPrintInputExecPin = printNode.getPinByName('inExec', PinSelectionGroup.Inputs)
        self.assertIsNotNone(pRandIntResultPin)
        self.assertIsNotNone(pPrintInputValuePin)
        self.assertIsNotNone(pRandIntOutExecPin)
        self.assertIsNotNone(pPrintInputExecPin)

        edge1Created = g.addConnection(pRandIntOutExecPin, pPrintInputExecPin)
        edge2Created = g.addConnection(pRandIntResultPin, pPrintInputValuePin)
        self.assertEqual(edge1Created, True, "FAILED TO CONNECT EXECS")
        self.assertEqual(edge2Created, True, "FAILED TO CONNECT INT AND ANY")

        values = set()
        for i in range(10):
            pRandIntInExecPin.call()
            values.add(pPrintInputValuePin.currentData())
        self.assertGreater(len(values), 1)

    def test_reconnect_value(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")
        defaultLib = packages['PyflowBase'].GetFunctionLibraries()["DefaultLib"]
        foos = defaultLib.getFunctions()

        n1 = NodeBase.initializeFromFunction(foos["makeBool"])
        n2 = NodeBase.initializeFromFunction(foos["makeBool"])
        n3 = NodeBase.initializeFromFunction(foos["makeBool"])

        g.addNode(n1)
        g.addNode(n2)
        g.addNode(n3)

        n1Out = n1.getPinByName('out', PinSelectionGroup.Outputs)
        n3b = n3.getPinByName('b', PinSelectionGroup.Inputs)
        # connect n1.out and n3.b
        c1 = g.addConnection(n1Out, n3b)
        # check connection was created
        self.assertEqual(c1, True)
        # check n1.out affects on n3.b
        self.assertListEqual(n1Out.affects, [n3b])
        # check n3.b affected by n1.out
        self.assertListEqual(n3b.affected_by, [n1Out])

        n2Out = n2.getPinByName('out', PinSelectionGroup.Outputs)
        # connect n2.out to n3.b
        # n3.b is connected with n1.out
        # we expect n3.b breaks all connections before connecting with n2.out
        c2 = g.addConnection(n2Out, n3b)
        # check connections successfull
        self.assertEqual(c2, True)
        # check n2.out afffects on n3.b
        self.assertListEqual(n2Out.affects, [n3b], "incorrect connection")
        # check n3.b affected by n2.out
        self.assertListEqual(n3b.affected_by, [n2Out], "incorrect")
        # check n1.out really disconnected
        self.assertListEqual(n1Out.affects, [], "not cleared")

if __name__ == '__main__':
    unittest.main()
