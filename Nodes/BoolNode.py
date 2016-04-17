from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class BoolNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(BoolNode, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.cb = QtGui.QCheckBox()
        self.cb.stateChanged.connect(lambda: self.on_set_cb_state(self.cb.isChecked()))
        self.output = self.add_output_port('out', AGPortDataTypes.tBool)

        def set_data_overloads(data, dirty_propagate=True):
            if data:
                self.cb.setCheckState(QtCore.Qt.Checked)
            else:
                self.cb.setCheckState(QtCore.Qt.Unchecked)
        self.output.set_data_overload = set_data_overloads

        prx_cb = QtGui.QGraphicsProxyWidget()
        prx_cb.setWidget(self.cb)
        self.output.getLayout().insertItem(0, prx_cb)

    def on_set_cb_state(self, state):
        self.output.set_data(state, True)

    def compute(self):

        self.output.set_data(self.cb.isChecked(), False)
