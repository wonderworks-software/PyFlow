from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget


class MakeConstArray(Node, NodeBase):
    def __init__(self, name, graph):
        super(MakeConstArray, self).__init__(name, graph)
        con = self.addContainer(PinTypes.Output)

        pb = QPushButton('+')
        pb.setMaximumWidth(30)
        pb.clicked.connect(self.addInPort)
        prx_btn = QGraphicsProxyWidget()
        prx_btn.setWidget(pb)
        con.layout().addItem(prx_btn)
        self.out_arr = self.addOutputPin('out', DataTypes.Array)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Any], 'outputs': [DataTypes.Array]}

    def addInPort(self):
        index = len(self.inputs)
        Pin = self.addInputPin(str(index), DataTypes.Any)
        portAffects(Pin, self.out_arr)
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
        push(self.out_arr)
