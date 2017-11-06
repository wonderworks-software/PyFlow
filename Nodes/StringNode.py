from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class LEdit(QtGui.QLineEdit):
    def __init__(self, foo):
        super(LEdit, self).__init__()
        self.foo = foo
        self.textEdited.connect(self.foo)


class StringNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(StringNode, self).__init__(name, graph, spacings=Spacings)
        self.output = self.add_output_port('out', AGPortDataTypes.tString)

        self.line_edit = LEdit(self.set_data)
        self.line_edit.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.line_edit.setText("None")

        # hack! overload the output's port 'set_data' method to update lineEdit
        def set_data_overloads(data, dirty_propagate=True):
            self.line_edit.setText(data)
        self.output.set_data_overload = set_data_overloads

        line_edit_proxy = QtGui.QGraphicsProxyWidget()
        line_edit_proxy.setWidget(self.line_edit)
        self.output.get_container().layout().insertItem(0, line_edit_proxy)
        self.compute()

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def set_data(self):
        self.output.set_data(self.line_edit.text().replace("/", "|"), True)

    def compute(self):
        self.output.set_data(self.line_edit.text(), False)
