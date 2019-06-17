from PyFlow.Tests.TestsBase import *
from PyFlow.Core.Common import *
from collections import Counter
from PyFlow.Input import *
from Qt import QtCore


class TestGeneral(unittest.TestCase):

    def setUp(self):
        print('\t[BEGIN TEST]', self._testMethodName)

    def tearDown(self):
        print('--------------------------------\n')

    def test_connect_pins_by_indexes(self):
        man = GraphManager()
        packages = GET_PACKAGES()
        mathLib = packages['PyFlowBase'].GetFunctionLibraries()["MathAbstractLib"]
        defaultLib = packages['PyFlowBase'].GetFunctionLibraries()["DefaultLib"]
        classNodes = packages['PyFlowBase'].GetNodeClasses()
        foos = mathLib.getFunctions()
        defaultLibFoos = defaultLib.getFunctions()

        makeIntNode = NodeBase.initializeFromFunction(defaultLibFoos["makeInt"])
        addNode2 = NodeBase.initializeFromFunction(foos["add"])
        printNode = classNodes["consoleOutput"]("print")

        man.activeGraph().addNode(makeIntNode)
        man.activeGraph().addNode(addNode2)
        man.activeGraph().addNode(printNode)

        makeIntNode.setData('i', 5)

        connection = connectPinsByIndexes(makeIntNode, 0, addNode2, 0)
        self.assertEqual(connection, True, "FAILED TO ADD EDGE")

        connection = connectPinsByIndexes(addNode2, 0, printNode, 1)
        self.assertEqual(connection, True, "FAILED TO ADD EDGE")
        printNode[DEFAULT_IN_EXEC_NAME].call()

        self.assertEqual(addNode2.getData('out'), 5, "NODES EVALUATION IS INCORRECT")

    def test_graph_location(self):
        packages = GET_PACKAGES()
        man = GraphManager()
        subgraphNodeClass = packages['PyFlowBase'].GetNodeClasses()['compound']
        subgraphNodeInstance = subgraphNodeClass(str('compound'))
        man.activeGraph().addNode(subgraphNodeInstance)

        # step inside compound
        man.selectGraph(subgraphNodeInstance.name)
        self.assertEqual(Counter(man.location()), Counter([man.findRootGraph().name, subgraphNodeInstance.name]))
        self.assertEqual(Counter(subgraphNodeInstance.rawGraph.location()), Counter(man.location()))

    def test_input_action(self):
        # TODO: move this ui stuff out of here
        a1 = InputAction("a1", InputActionType.Keyboard, "g1", QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.NoButton, QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
        a2 = InputAction("a1", InputActionType.Keyboard, "g1", QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.NoButton, QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
        self.assertEqual(a1, a2)

        a2.setModifiers(QtCore.Qt.ControlModifier)
        self.assertNotEqual(a1, a2)

        a1jsn = a1.toJson()
        a1Restored = InputAction("a1Restored")
        a1Restored.fromJson(a1jsn)

        self.assertEqual(a1, a1Restored)

    def test_add_int_no_exec(self):
        man = GraphManager()
        packages = GET_PACKAGES()
        mathLib = packages['PyFlowBase'].GetFunctionLibraries()["MathAbstractLib"]
        defaultLib = packages['PyFlowBase'].GetFunctionLibraries()["DefaultLib"]
        classNodes = packages['PyFlowBase'].GetNodeClasses()
        foos = mathLib.getFunctions()
        defaultLibFoos = defaultLib.getFunctions()

        makeIntNode = NodeBase.initializeFromFunction(defaultLibFoos["makeInt"])
        addNode2 = NodeBase.initializeFromFunction(foos["add"])
        printNode = classNodes["consoleOutput"]("print")

        man.activeGraph().addNode(makeIntNode)
        man.activeGraph().addNode(addNode2)
        man.activeGraph().addNode(printNode)

        makeIntNode.setData('i', 5)

        connection = connectPins(makeIntNode[str('out')], addNode2[str('a')])
        self.assertEqual(connection, True, "FAILED TO ADD EDGE")

        connection = connectPins(addNode2[str('out')], printNode[str("entity")])
        self.assertEqual(connection, True, "FAILED TO ADD EDGE")
        printNode[DEFAULT_IN_EXEC_NAME].call()

        self.assertEqual(addNode2.getData('out'), 5, "NODES EVALUATION IS INCORRECT")

    def test_foo_node_ref_set_data(self):
        packages = GET_PACKAGES()
        randomLib = packages['PyFlowBase'].GetFunctionLibraries()["RandomLib"]
        defaultLib = packages['PyFlowBase'].GetFunctionLibraries()["DefaultLib"]
        classNodes = packages['PyFlowBase'].GetNodeClasses()
        randomLibFoos = randomLib.getFunctions()
        defaultLibFoos = defaultLib.getFunctions()

        randintNode = NodeBase.initializeFromFunction(randomLibFoos["randint"])
        printNode = classNodes["consoleOutput"]("print")

        man = GraphManager()

        man.activeGraph().addNode(randintNode)
        man.activeGraph().addNode(printNode)

        self.assertIsNotNone(randintNode)
        self.assertIsNotNone(printNode)

        pPrintInputValuePin = printNode[str('entity')]

        edge2Created = connectPins(randintNode[str('Result')], pPrintInputValuePin)
        self.assertEqual(edge2Created, True, "FAILED TO CONNECT INT AND ANY")

        values = set()
        for i in range(10):
            printNode[DEFAULT_IN_EXEC_NAME].call()
            values.add(pPrintInputValuePin.currentData())
        self.assertGreater(len(values), 1)

    def test_reconnect_value(self):
        packages = GET_PACKAGES()

        defaultLib = packages['PyFlowBase'].GetFunctionLibraries()["DefaultLib"]
        foos = defaultLib.getFunctions()

        n1 = NodeBase.initializeFromFunction(foos["makeBool"])
        n2 = NodeBase.initializeFromFunction(foos["makeBool"])
        n3 = NodeBase.initializeFromFunction(foos["makeBool"])

        man = GraphManager()
        man.activeGraph().addNode(n1)
        man.activeGraph().addNode(n2)
        man.activeGraph().addNode(n3)

        n1Out = n1.getPin(str('out'), PinSelectionGroup.Outputs)
        n3b = n3.getPin(str('b'), PinSelectionGroup.Inputs)
        # connect n1.out and n3.b
        c1 = connectPins(n1Out, n3b)
        # check connection was created
        self.assertEqual(c1, True)
        # check n1.out affects on n3.b
        self.assertEqual(n3b in n1Out.affects, True)
        # check n3.b affected by n1.out
        self.assertEqual(n1Out in n3b.affected_by, True)

        n2Out = n2.getPin(str('out'), PinSelectionGroup.Outputs)
        # connect n2.out to n3.b
        # n3.b is connected with n1.out
        # we expect n3.b breaks all connections before connecting with n2.out
        c2 = connectPins(n2Out, n3b)
        # check connections successfull
        self.assertEqual(c2, True)
        # check n2.out affects on n3.b
        self.assertEqual(n3b in n2Out.affects, True, "incorrect connection")
        # check n3.b affected by n2.out
        self.assertEqual(n2Out in n3b.affected_by, True, "incorrect")
        # check n1.out really disconnected
        self.assertEqual(n1Out.affects, set(), "not cleared")

    def test_are_pins_connected(self):
        packages = GET_PACKAGES()
        intlib = packages['PyFlowBase'].GetFunctionLibraries()["MathAbstractLib"]
        foos = intlib.getFunctions()

        addNode1 = NodeBase.initializeFromFunction(foos["add"])
        addNode2 = NodeBase.initializeFromFunction(foos["add"])

        man = GraphManager()

        man.activeGraph().addNode(addNode1)
        man.activeGraph().addNode(addNode2)

        pinOut = addNode1.getPin(str('out'), PinSelectionGroup.Outputs)
        pinInp = addNode2.getPin(str('a'), PinSelectionGroup.Inputs)
        bConnected = connectPins(pinOut, pinInp)
        self.assertEqual(bConnected, True, "FAILED TO ADD EDGE")
        self.assertEqual(arePinsConnected(pinOut, pinInp), True)

        disconnected = disconnectPins(pinInp, pinOut)
        self.assertEqual(disconnected, True, "pins are not disconnected")
        self.assertEqual(arePinsConnected(pinOut, pinInp), False)

    def test_create_var(self):
        man = GraphManager()
        v1 = man.activeGraph().createVariable()
        self.assertEqual(v1.uid in man.activeGraph().vars, True)

    def test_variable_scope(self):
        man = GraphManager()
        # add variable to root graph
        rootVariable = man.activeGraph().createVariable(name="v0")
        rootVariable.value = 0
        self.assertEqual(rootVariable.uid in man.activeGraph().vars, True)

        vars = man.activeGraph().getVarList()
        self.assertEqual(len(vars), 1, "failed to gather variables")

        # create two subgraphs and variables inside
        packages = GET_PACKAGES()
        subgraphNodeClass = packages['PyFlowBase'].GetNodeClasses()['compound']
        varGetterClass = packages['PyFlowBase'].GetNodeClasses()['getVar']
        varSetterClass = packages['PyFlowBase'].GetNodeClasses()['setVar']

        subgraphNodeInstance1 = subgraphNodeClass('subgraph1')
        subgraphNodeInstance2 = subgraphNodeClass('subgraph2')
        self.assertEqual(man.activeGraph().addNode(subgraphNodeInstance1), True)
        self.assertEqual(man.activeGraph().addNode(subgraphNodeInstance2), True)

        # goto subgraph1 and create variable
        man.selectGraph(subgraphNodeInstance1.name)
        sg1Var = man.activeGraph().createVariable(name="v1")
        sg1Var.value = 1
        v1Getter = varGetterClass("v1Get", sg1Var)
        v1Setter = varSetterClass("v1Set", sg1Var)
        self.assertEqual(man.activeGraph().addNode(v1Getter), True)
        self.assertEqual(man.activeGraph().addNode(v1Setter), True)
        man.selectRootGraph()

        # Check variables scope visibility
        self.assertEqual(man.activeGraph().addNode(v1Getter), False, "Variable access error! Variables in child graphs should not be visible to parent ones!")
        self.assertEqual(man.activeGraph().addNode(v1Setter), False, "Variable access error! Variables in child graphs should not be visible to parent ones!")

        # goto subgraph2 and create variable there
        man.selectGraph(subgraphNodeInstance2.name)
        sg2Var = man.activeGraph().createVariable(name="v2")
        sg2Var.value = 2
        man.selectRootGraph()

        # ask variables from rootgraph.
        vars = man.activeGraph().getVarList()
        self.assertEqual(len(vars), 1, "failed to gather variables")
        # check variable value is 0
        self.assertEqual(vars[0].value, 0, "invalid variable")

        # go to subgraph1 and ask variables there
        man.selectGraph(subgraphNodeInstance1.name)
        vars = man.activeGraph().getVarList()
        # two variables. One from subgraph1 + one from root
        self.assertEqual(len(vars), 2, "failed to gather variables")
        varsValues = [i.value for i in vars]
        self.assertEqual(Counter(varsValues), Counter([0, 1]), "variables are incorrect")
        man.selectRootGraph()

        # goto subgraph2 and ask variables there
        man.selectGraph(subgraphNodeInstance2.name)
        vars = man.activeGraph().getVarList()
        # two variables. One from subgraph2 + one from root
        self.assertEqual(len(vars), 2, "failed to gather variables")
        varsValues = [i.value for i in vars]
        self.assertEqual(Counter(varsValues), Counter([0, 2]), "variables are incorrect")
        man.selectRootGraph()

    def test_get_bool_var(self):
        packages = GET_PACKAGES()
        classNodes = packages["PyFlowBase"].GetNodeClasses()

        man = GraphManager()

        # create bool variable
        v1 = man.activeGraph().createVariable(str('BoolPin'))
        v1.value = False

        # create variable getter node
        varGetterClass = packages["PyFlowBase"].GetNodeClasses()['getVar']
        # since variable is bool, bool pin will be created
        varGetterInstance = varGetterClass(str('v1Getter'), v1)
        man.activeGraph().addNode(varGetterInstance)

        # create print node
        defaultLib = packages["PyFlowBase"].GetFunctionLibraries()['DefaultLib']
        printerInstance = classNodes["consoleOutput"]("print")
        man.activeGraph().addNode(printerInstance)

        # connect to print node input
        varOutPin = varGetterInstance.getPin(str('out'), PinSelectionGroup.Outputs)
        printInPin = printerInstance.getPin(str('entity'), PinSelectionGroup.Inputs)
        printInExecPin = printerInstance.getPin(str('inExec'), PinSelectionGroup.Inputs)
        connected = connectPins(varOutPin, printInPin)
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

        man = GraphManager()

        # create any type variable
        v1 = man.activeGraph().createVariable()
        v1.value = False

        # create variable getter node
        varGetterClass = packages["PyFlowBase"].GetNodeClasses()['getVar']
        varGetterInstance = varGetterClass(str('v1Getter'), v1)
        man.activeGraph().addNode(varGetterInstance)

        # create print node
        defaultLib = packages["PyFlowBase"].GetFunctionLibraries()['DefaultLib']
        printerInstance = packages["PyFlowBase"].GetNodeClasses()['consoleOutput']("print")
        man.activeGraph().addNode(printerInstance)

        # connect to print node input
        varOutPin = varGetterInstance.getPin(str('out'), PinSelectionGroup.Outputs)
        printInPin = printerInstance.getPin(str('entity'), PinSelectionGroup.Inputs)
        printInExecPin = printerInstance.getPin(str('inExec'), PinSelectionGroup.Inputs)
        connected = connectPins(varOutPin, printInPin)
        self.assertEqual(connected, True, "var getter is not connected")

        man.activeGraph().killVariable(v1)
        self.assertEqual(v1 not in man.activeGraph().vars, True, "variable not killed")

    def test_set_bool_var(self):
        import pyrr
        packages = GET_PACKAGES()

        man = GraphManager()

        # create bool type variable
        v1 = man.activeGraph().createVariable(str('BoolPin'))
        # this will accept only bools
        v1.value = False

        # create variable setter node
        varSetterClass = packages["PyFlowBase"].GetNodeClasses()['setVar']
        varSetterInstance = varSetterClass(str('v1Setter'), v1)
        setterAdded = man.activeGraph().addNode(varSetterInstance)
        self.assertEqual(setterAdded, True)

        # set new value to setter node input pin
        inExecPin = varSetterInstance.getPin(DEFAULT_IN_EXEC_NAME, PinSelectionGroup.Inputs)
        inPin = varSetterInstance.getPin(str('inp'), PinSelectionGroup.Inputs)
        outPin = varSetterInstance.getPin(str('out'), PinSelectionGroup.Outputs)
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

    def test_subgraph_execs(self):
        packages = GET_PACKAGES()

        man = GraphManager()

        # create empty compound
        subgraphNodeClass = packages['PyFlowBase'].GetNodeClasses()['compound']
        subgraphNodeInstance = subgraphNodeClass(str('compound'))
        man.activeGraph().addNode(subgraphNodeInstance)

        # step inside compound
        man.selectGraph(subgraphNodeInstance.name)
        # self.assertEqual(graph.name, subgraphNodeInstance.name, "failed to enter compound")

        # add input output nodes to expose pins to outer compound node
        inputs1 = man.activeGraph().getInputNode()
        outputs1 = man.activeGraph().getOutputNode()
        self.assertIsNotNone(inputs1, "failed to create graph inputs node")
        self.assertIsNotNone(outputs1, "failed to create graph outputs node")

        # create out pin on graphInputs node
        # this should expose input pin on compound node
        outPin = inputs1.addOutPin()
        man.Tick(0.02)
        self.assertEqual(len(subgraphNodeInstance.namePinInputsMap), 1, "failed to expose input pin")
        self.assertEqual(list(subgraphNodeInstance.inputs.values())[0].name, outPin.name)
        outPin.setName('inAnyExec')

        # create input pin on graphOutputs node
        # this should expose output pin on compound node
        inPin = outputs1.addInPin()
        man.Tick(0.02)
        self.assertEqual(len(subgraphNodeInstance.namePinOutputsMap), 1, "failed to expose input pin")
        self.assertEqual(list(subgraphNodeInstance.outputs.values())[0].name, inPin.name)
        inPin.setName('outAnyExec')

        subgraphInAnyExec = subgraphNodeInstance.getPin(str('inAnyExec'), PinSelectionGroup.Inputs)
        self.assertIsNotNone(subgraphInAnyExec, "failed to find compound input exec pin")
        subgraphOutAnyExec = subgraphNodeInstance.getPin(str('outAnyExec'), PinSelectionGroup.Outputs)
        self.assertIsNotNone(subgraphOutAnyExec, "failed to find compound out exec pin")

        # add print node inside
        foos = packages['PyFlowBase'].GetFunctionLibraries()["DefaultLib"].getFunctions()

        printNode1 = packages["PyFlowBase"].GetNodeClasses()['consoleOutput']("print")
        man.activeGraph().addNode(printNode1)
        printNode1.setData("entity", "hello from compound")

    def test_graph_serialization(self):
        man = GraphManager()
        packages = GET_PACKAGES()
        lib = packages['PyFlowBase'].GetFunctionLibraries()["MathAbstractLib"]
        defaultLib = packages['PyFlowBase'].GetFunctionLibraries()["DefaultLib"]
        classNodes = packages['PyFlowBase'].GetNodeClasses()
        foos = lib.getFunctions()
        defFoos = defaultLib.getFunctions()

        makeInt = NodeBase.initializeFromFunction(defFoos["makeInt"])
        addNode2 = NodeBase.initializeFromFunction(foos["add"])
        printNode = classNodes["consoleOutput"]("printer")

        man.activeGraph().addNode(makeInt)
        man.activeGraph().addNode(addNode2)
        man.activeGraph().addNode(printNode)

        makeInt.setData('i', 5)

        connected = connectPins(makeInt[str('out')], addNode2[str('a')])
        self.assertEqual(connected, True)

        connected = connectPins(addNode2[str('out')], printNode[str('entity')])
        self.assertEqual(connected, True)

        printNode[DEFAULT_IN_EXEC_NAME].call()

        self.assertEqual(addNode2.getData(str('out')), 5, "Incorrect calc")

        # save and clear
        dataJson = man.serialize()
        man.clear(keepRoot=False)

        # load
        man.deserialize(dataJson)

        restoredAddNode2 = man.activeGraph().findNode(str('makeInt'))
        self.assertEqual(restoredAddNode2.getData('out'), 5, "Incorrect calc")

    def test_graph_depth(self):
        man = GraphManager()
        packages = GET_PACKAGES()

        subgraphNodeClass = packages['PyFlowBase'].GetNodeClasses()['compound']
        subgraphNodeInstance = subgraphNodeClass(str(str('compound')))
        man.activeGraph().addNode(subgraphNodeInstance)

        self.assertEqual(man.activeGraph().depth(), 1)

        man.selectGraph(subgraphNodeInstance)
        self.assertEqual(man.activeGraph().depth(), 2)

    def test_manager_serialization(self):
        man = GraphManager()
        packages = GET_PACKAGES()

        subgraphNodeClass = packages['PyFlowBase'].GetNodeClasses()['compound']
        subgraphNodeInstance = subgraphNodeClass(str('compound'))
        man.activeGraph().addNode(subgraphNodeInstance)
        man.selectGraph(subgraphNodeInstance)

        inputs1 = man.activeGraph().getInputNode()
        outputs1 = man.activeGraph().getOutputNode()

        # create out pin on graphInputs node
        # this should expose input pin on compound node
        outPin = inputs1.addOutPin()
        man.Tick(0.02)
        self.assertEqual(len(subgraphNodeInstance.namePinInputsMap), 1, "failed to expose input pin")
        self.assertEqual(list(subgraphNodeInstance.inputs.values())[0].name, outPin.name)
        self.assertEqual(outPin.optionEnabled(PinOptions.Dynamic), True)

        # change inner pin name and check it is reflected outside
        outPin.setName("first")
        self.assertEqual(list(subgraphNodeInstance.inputs.values())[0].name, outPin.name, "name is not synchronized")

        # create input pin on graphOutputs node
        # this should expose output pin on compound node
        inPin = outputs1.addInPin()
        man.Tick(0.02)
        self.assertEqual(len(subgraphNodeInstance.namePinOutputsMap), 1, "failed to expose input pin")
        self.assertEqual(list(subgraphNodeInstance.outputs.values())[0].name, inPin.name)
        self.assertEqual(inPin.optionEnabled(PinOptions.RenamingEnabled), True)

        # change inner pin name and check it is reflected outside
        inPin.setName("first")
        self.assertEqual(list(subgraphNodeInstance.outputs.values())[0].name, inPin.name, "name is not synchronized")

        depthsBefore = [g.depth() for g in man.getAllGraphs()]

        nameBefore = subgraphNodeInstance.name
        saved = man.serialize()
        man.clear(keepRoot=False)
        self.assertEqual(man.activeGraph(), None)
        man.deserialize(saved)
        self.assertIsNotNone(man.activeGraph())
        nameAfter = man.getAllNodes(classNameFilters="compound")[0].name
        self.assertEqual(nameBefore, nameAfter, "names are incorrect {0} - {1}".format(nameBefore, nameAfter))
        depthsAfter = [g.depth() for g in man.getAllGraphs()]
        self.assertEqual(Counter(depthsBefore), Counter(depthsAfter), "failed to restore graphs depths")


if __name__ == '__main__':
    unittest.main()
