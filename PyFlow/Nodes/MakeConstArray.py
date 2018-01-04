from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QMenu
from inspect import getmembers


class MakeConstArray(Node, NodeBase):
    def __init__(self, name, graph):
        super(MakeConstArray, self).__init__(name, graph)
        self.menu = QMenu()

        valueDataTypes = [i[1] for i in getmembers(DataTypes) if isinstance(i[1], int) and i[1] not in [DataTypes.Reference, DataTypes.Exec]]
        for dataType in valueDataTypes:
            self.action = self.menu.addAction('Add {0}'.format(getDataTypeName(dataType)))
            self.action.triggered.connect(lambda t=dataType: self.addInPin(t))
        # con = self.addContainer(PinTypes.Output)

        # pb = QPushButton('+')
        # pb.setMaximumWidth(30)
        # pb.clicked.connect(self.addInPin)
        # prx_btn = QGraphicsProxyWidget()
        # prx_btn.setWidget(pb)
        # con.layout().addItem(prx_btn)
        self.out_arr = self.addOutputPin('out', DataTypes.Array)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Any], 'outputs': [DataTypes.Array]}

    def addInPin(self, dataType):
        index = len(self.inputs)
        Pin = self.addInputPin(str(index), dataType)
        pinAffects(Pin, self.out_arr)
        push(self.out_arr)

    def postCreate(self, jsonTemplate=None):
        Node.postCreate(self, jsonTemplate)
        for inpJson in jsonTemplate['inputs']:
            pin = self.addInputPin(inpJson['name'], inpJson['dataType'], None, inpJson['bLabelHidden'])
            pin.setData(inpJson['value'])
            pin.uid = uuid.UUID(inpJson['uuid'])

    @staticmethod
    def category():
        return 'Array'

    def compute(self):
        self.out_arr.setData(list([i.getData() for i in self.inputs.values()]))
