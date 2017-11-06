from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class LEdit(QtGui.QLineEdit):
    def __init__(self, foo):
        super(LEdit, self).__init__()
        self.foo = foo
        self.editingFinished.connect(self.foo)
        self.setValidator(QtGui.QIntValidator(-999999999, 999999999, self))
        self.setText('0')
        self.setMaximumWidth(40)


class MakeInt(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(MakeInt, self).__init__(name, graph, spacings=Spacings)
        self.output = self.add_output_port('', AGPortDataTypes.tInt)
        self.input = self.add_input_port('', AGPortDataTypes.tInt)
        self.input.port_connected = self.OnInputConnected
        self.input.port_disconnected = self.OnInputDisconnected
        self.ledit = LEdit(self.set_data)

        # hack! overload the output's port 'set_data' method to update lineEdit
        def set_data_overloads(data, dirty_propagate=True):
            self.ledit.setText(str(int(data)))
        self.output.set_data_overload = set_data_overloads

        line_edit_proxy = QtGui.QGraphicsProxyWidget()
        line_edit_proxy.setWidget(self.ledit)
        self.output.get_container().layout().insertItem(0, line_edit_proxy)
        portAffects(self.input, self.output)
        self.compute()

    def OnInputConnected(self):
        self.ledit.hide()

    def OnInputDisconnected(self):
        self.ledit.show()

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def set_data(self):
        self.output.set_data(int(self.ledit.text()), True)

    def compute(self):
        self.output.set_data(int(self.ledit.text()), False)
