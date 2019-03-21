from TestsBase import *


class TestGeneral(unittest.TestCase):

    def setUp(self):
        print('\t[BEGIN TEST]', self._testMethodName)

    def tearDown(self):
        print('--------------------------------\n')

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

        connection = g.connectPins(addNode1.getPinByName('out', PinSelectionGroup.Outputs), addNode2.getPinByName('a', PinSelectionGroup.Inputs))
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

        edge1Created = g.connectPins(pRandIntOutExecPin, pPrintInputExecPin)
        edge2Created = g.connectPins(pRandIntResultPin, pPrintInputValuePin)
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
        c1 = g.connectPins(n1Out, n3b)
        # check connection was created
        self.assertEqual(c1, True)
        # check n1.out affects on n3.b
        self.assertEqual(n3b in n1Out.affects, True)
        # check n3.b affected by n1.out
        self.assertEqual(n1Out in n3b.affected_by, True)

        n2Out = n2.getPinByName('out', PinSelectionGroup.Outputs)
        # connect n2.out to n3.b
        # n3.b is connected with n1.out
        # we expect n3.b breaks all connections before connecting with n2.out
        c2 = g.connectPins(n2Out, n3b)
        # check connections successfull
        self.assertEqual(c2, True)
        # check n2.out afffects on n3.b
        self.assertEqual(n3b in n2Out.affects, True, "incorrect connection")
        # check n3.b affected by n2.out
        self.assertEqual(n2Out in n3b.affected_by, True, "incorrect")
        # check n1.out really disconnected
        self.assertEqual(n1Out.affects, set(), "not cleared")

    def test_are_pins_connected(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")
        intlib = packages['PyflowBase'].GetFunctionLibraries()["IntLib"]
        mathFoos = intlib.getFunctions()

        addNode1 = NodeBase.initializeFromFunction(mathFoos["add"])
        addNode2 = NodeBase.initializeFromFunction(mathFoos["add"])

        g.addNode(addNode1)
        g.addNode(addNode2)

        pinOut = addNode1.getPinByName('out', PinSelectionGroup.Outputs)
        pinInp = addNode2.getPinByName('a', PinSelectionGroup.Inputs)
        bConnected = g.connectPins(pinOut, pinInp)
        self.assertEqual(bConnected, True, "FAILED TO ADD EDGE")
        self.assertEqual(arePinsConnected(pinOut, pinInp), True)

        disconnected = disconnectPins(pinInp, pinOut)
        self.assertEqual(disconnected, True, "pins are not disconnected")
        self.assertEqual(arePinsConnected(pinOut, pinInp), False)

    def test_create_var(self):
        g = GraphBase("testGraph")
        v1 = g.createVariable()
        self.assertEqual(v1.uid in g.vars, True)

    def test_get_any_var(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")

        # create any type variable
        v1 = g.createVariable()
        v1.value = False

        # create variable getter node
        varGetterClass = packages["PyflowBase"].GetNodeClasses()['getVar']
        varGetterInstance = varGetterClass('v1Getter', v1)
        g.addNode(varGetterInstance)

        # create print node
        defaultLib = packages["PyflowBase"].GetFunctionLibraries()['DefaultLib']
        printerInstance = NodeBase.initializeFromFunction(defaultLib.getFunctions()['pyprint'])
        g.addNode(printerInstance)

        # connect to print node input
        varOutPin = varGetterInstance.getPinByName('value', PinSelectionGroup.Outputs)
        self.assertIsNotNone(varOutPin)
        printInPin = printerInstance.getPinByName('entity', PinSelectionGroup.Inputs)
        printInExecPin = printerInstance.getPinByName('inExec', PinSelectionGroup.Inputs)
        connected = g.connectPins(varOutPin, printInPin)
        self.assertEqual(connected, True, "var getter is not connected")

        # print variable value and check it
        printInExecPin.call()
        self.assertEqual(printInPin.currentData(), False)
        # next, change variable value (Not varGetterInstance varOutPin! Note we are not touching it anymore)
        # this will broadcast valueChanged on v1, which will trigger dirty propagation from varOutPin
        # varGetterInstance.onVarValueChanged and v1.valueChanged were connected in getVar.postCreate
        v1.value = True
        # following line will trigger compute on print node, which will ask data on it's inputs
        # Inputs on print node will be dirty, data will be asked on varGetterInstance varOutPin
        printInExecPin.call()
        self.assertEqual(printInPin.currentData(), True)

    def test_get_bool_var(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")

        # create bool variable
        v1 = g.createVariable('BoolPin')
        v1.value = False

        # create variable getter node
        varGetterClass = packages["PyflowBase"].GetNodeClasses()['getVar']
        # since variable is bool, bool pin will be created
        varGetterInstance = varGetterClass('v1Getter', v1)
        g.addNode(varGetterInstance)

        # create print node
        defaultLib = packages["PyflowBase"].GetFunctionLibraries()['DefaultLib']
        printerInstance = NodeBase.initializeFromFunction(defaultLib.getFunctions()['pyprint'])
        g.addNode(printerInstance)

        # connect to print node input
        varOutPin = varGetterInstance.getPinByName('value', PinSelectionGroup.Outputs)
        printInPin = printerInstance.getPinByName('entity', PinSelectionGroup.Inputs)
        printInExecPin = printerInstance.getPinByName('inExec', PinSelectionGroup.Inputs)
        connected = g.connectPins(varOutPin, printInPin)
        self.assertEqual(connected, True, "var getter is not connected")

        # print variable value and check it
        printInExecPin.call()
        self.assertEqual(printInPin.currentData(), False)
        # next, change variable value (Not varGetterInstance varOutPin! Note we are not touching it anymore)
        # this will broadcast valueChanged on v1, which will trigger dirty propagation from varOutPin
        # varGetterInstance.onVarValueChanged and v1.valueChanged were connected in getVar.postCreate
        v1.value = True
        # following line will trigger compute on print node, which will ask data on it's inputs
        # Inputs on print node will be dirty, data will be asked on varGetterInstance varOutPin
        printInExecPin.call()
        self.assertEqual(printInPin.currentData(), True)

    def test_kill_variable(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")

        # create any type variable
        v1 = g.createVariable()
        v1.value = False

        # create variable getter node
        varGetterClass = packages["PyflowBase"].GetNodeClasses()['getVar']
        varGetterInstance = varGetterClass('v1Getter', v1)
        g.addNode(varGetterInstance)

        # create print node
        defaultLib = packages["PyflowBase"].GetFunctionLibraries()['DefaultLib']
        printerInstance = NodeBase.initializeFromFunction(defaultLib.getFunctions()['pyprint'])
        g.addNode(printerInstance)

        # connect to print node input
        varOutPin = varGetterInstance.getPinByName('value', PinSelectionGroup.Outputs)
        printInPin = printerInstance.getPinByName('entity', PinSelectionGroup.Inputs)
        printInExecPin = printerInstance.getPinByName('inExec', PinSelectionGroup.Inputs)
        connected = g.connectPins(varOutPin, printInPin)
        self.assertEqual(connected, True, "var getter is not connected")

        g.killVariable(v1)
        self.assertEqual(v1 not in g.vars, True, "variable not killed")
        self.assertEqual(varGetterInstance.uid not in g.nodes, True, "get var not killed")
        connected = arePinsConnected(varOutPin, printInPin)
        self.assertEqual(connected, False, "get var node is removed, but pins are still connected")

    def test_set_any_var(self):
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")

        # create any type variable
        v1 = g.createVariable()
        # type checking will not be performed since this is any type
        v1.value = False

        # create variable setter node
        varSetterClass = packages["PyflowBase"].GetNodeClasses()['setVar']
        varSetterInstance = varSetterClass('v1Setter', v1)
        setterAdded = g.addNode(varSetterInstance)
        self.assertEqual(setterAdded, True)

        # set new value to setter node input pin
        inExecPin = varSetterInstance.getPinByName('exec', PinSelectionGroup.Inputs)
        inPin = varSetterInstance.getPinByName('inp', PinSelectionGroup.Inputs)
        outPin = varSetterInstance.getPinByName('out', PinSelectionGroup.Outputs)
        self.assertIsNotNone(inExecPin)
        self.assertIsNotNone(inPin)
        self.assertIsNotNone(outPin)
        # next we set data to setter node
        inPin.setData(True)
        # And fire input exec pin.
        # We expect it will call compute
        # which will update variable value
        inExecPin.call()
        # check variable value
        self.assertEqual(v1.value, True, "variable value is not set")

    def test_set_bool_var(self):
        import pyrr
        packages = GET_PACKAGES()
        g = GraphBase("testGraph")

        # create bool type variable
        v1 = g.createVariable('BoolPin')
        # this will accept only bools
        v1.value = False

        # create variable setter node
        varSetterClass = packages["PyflowBase"].GetNodeClasses()['setVar']
        varSetterInstance = varSetterClass('v1Setter', v1)
        setterAdded = g.addNode(varSetterInstance)
        self.assertEqual(setterAdded, True)

        # set new value to setter node input pin
        inExecPin = varSetterInstance.getPinByName('exec', PinSelectionGroup.Inputs)
        inPin = varSetterInstance.getPinByName('inp', PinSelectionGroup.Inputs)
        outPin = varSetterInstance.getPinByName('out', PinSelectionGroup.Outputs)
        self.assertIsNotNone(inExecPin)
        self.assertIsNotNone(inPin)
        self.assertIsNotNone(outPin)
        # next we set data to setter node
        inPin.setData(True)
        # And fire input exec pin.
        # We expect it will call compute
        # which will update variable value
        inExecPin.call()
        # check variable value
        self.assertEqual(v1.value, True, "variable value is not set")

if __name__ == '__main__':
    unittest.main()
