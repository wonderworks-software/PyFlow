from Qt import QtWidgets

from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.Widget import GraphWidgetUI
from PyFlow.Core.Common import *


class UIsubgraph(UINodeBase):
    def __init__(self, raw_node):
        super(UIsubgraph, self).__init__(raw_node)
        actionExport = self._menu.addAction("export")
        actionExport.triggered.connect(self.export)

        self._category = "CustomGraphs"
        self._keywords = "CustomGraphs"
        self._description = "Custom SubGraph"
        # self.bCallable = True
        self.dinOutputs = {}
        self.dinInputs = {}
        # self.label().hide()

    def onAddInPin(self, pin):
        rawPin = self._rawNode.addInPin(pin=pin._rawPin)
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.setDynamic(True)
        uiPin.setRenamingEnabled(True)
        pin.nameChanged.connect(uiPin.setName)
        pin.OnPinDeleted.connect(self.deletePort)
        pin.dataBeenSet.connect(uiPin.setData)
        pin.dataBeenSet.connect(self.test)
        pinAffects(uiPin._rawPin, pin._rawPin)
        self.dinInputs[pin] = uiPin
        for i in self.inputs.values():
            for o in self.outputs.values():
                pinAffects(i, o)
        self.updateWidth()
        return uiPin

    def test(self, data):
        print(data)

    def onAddOutPin(self, pin):
        rawPin = self._rawNode.addOutPin(pin=pin._rawPin)
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.setDynamic(True)
        uiPin.setRenamingEnabled(True)
        pin.OnPinDeleted.connect(self.deletePort)
        pin.dataBeenSet.connect(uiPin.setData)
        pinAffects(pin._rawPin, uiPin._rawPin)
        self.dinOutputs[pin] = uiPin
        for i in self.inputs.values():
            for o in self.outputs.values():
                pinAffects(i, o)
        self.updateWidth()
        return uiPin

    def serialize(self):
        template = super(UIsubgraph, self).serialize()
        graphData = self._graph.getGraphSaveData()
        template["graphData"] = graphData
        return template

    def postCreate(self, jsonTemplate):
        super(UIsubgraph, self).postCreate(jsonTemplate)
        self._graph = GraphWidgetUI(self.graph().parent, graphBase=self._rawNode.rawGraph)
        self._graph.outPinCreated.connect(self.onAddOutPin)
        self._graph.inPinCreated.connect(self.onAddInPin)

        self.dlg = MyDialog()
        # self.styleSheetEditor = self.graph().styleSheetEditor
        # self.dlg.setStyleSheet(self.styleSheetEditor.getStyleSheet())
        self.dlg.setLayout(QtWidgets.QHBoxLayout())
        self.dlg.layout().addWidget(self._graph)
        if "graphData" in jsonTemplate:
            self._graph.loadFromData(jsonTemplate["graphData"])
        # restore pins
        for node in self._graph.getNodesByClassName("graphInputs"):
            for inp in node.outputs.values():
                self.onAddInPin(inp)
        for node in self._graph.getNodesByClassName("graphInputs"):
            for out in node.inputs.values():
                self.onAddOutPin(out)

    def deletePort(self, pin):
        if pin in self.dinInputs:
            self.dinInputs[pin].kill()
            del self.dinInputs[pin]
        elif pin in self.dinOutputs:
            self.dinOutputs[pin].kill()
            del self.dinOutputs[pin]

    def mouseDoubleClickEvent(self, event):
        # Node.mouseDoubleClickEvent( event)
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()

    def OnDoubleClick(self, pos):
        self.dlg.show()

    def export(self):
        from . import _nodeClasses
        from ..FunctionLibraries import _foos
        from ..SubGraphs import _subgraphClasses
        from .. import SubGraphs
        existing_nodes = [n for n in _nodeClasses]
        existing_nodes += [n for n in _foos]
        existing_nodes += [n for n in _subgraphClasses]

        graphData = self._graph.getGraphSaveData()
        graphData["Type"] = "subgraph"
        graphData["category"] = self._category
        graphData["keywords"] = self._keywords
        graphData["description"] = self._description
        name_filter = "Graph files (*.pySubgraph)"

        pth = QFileDialog.getSaveFileName(filter=name_filter)
        if not pth == '':
            file_path = pth
            path, name = os.path.split(file_path)
            name, ext = os.path.splitext(name)
            if name in existing_nodes:
                print("[ERROR] Node {0} already exists! Chose another name".format(name))
                return
            # write to file. delete older if needed
            with open(file_path, "wb") as f:
                def to_serializable(val):
                    return {
                        "name": None
                    }
                    return str(val)
                json.dump(graphData, f, skipkeys=True, default=to_serializable, indent=2)
            reload(SubGraphs)
            SubGraphs._getClasses()


class MyDialog(QtWidgets.QDialog):
    # ...
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        # when you want to destroy the dialog set this to True
        self._want_to_close = False

    def closeEvent(self, evnt):
        if self._want_to_close:
            super(MyDialog, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()
