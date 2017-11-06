from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode

DESC = '''This node's purpose is change flow of edges
'''


class Reroute(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Reroute, self).__init__(name, graph, spacings=Spacings)
        self.h = 25
        self.sizes[4] = self.h
        # self.v_form.setGeometry(QtCore.QRectF(0, 0, self.w + self.spacings.kPortOffset, self.h))
        self.label.hide()

        newColor = QtGui.QColor(25, 25, 25, 255)

        self.inp0 = BaseNode.Port('in', self, AGPortDataTypes.tReroute, 10, 10, newColor)
        self.inp0.type = AGPortTypes.kInput
        self.inp0.setParentItem(self)
        self.inp0.setY(5.0)
        self.inputs.append(self.inp0)

        self.out0 = BaseNode.Port('out', self, AGPortDataTypes.tReroute, 10, 10, newColor)
        self.out0.type = AGPortTypes.kOutput
        self.out0.setParentItem(self)
        self.out0.setPos(10.0, 5.0)
        self.outputs.append(self.out0)

        portAffects(self.inp0, self.out0)

    @staticmethod
    def get_category():
        return 'Common'

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 20, 20)

    def paint(self, painter, option, widget):
        # painter.setPen(QtCore.Qt.NoPen)
        # painter.setBrush(QtCore.Qt.darkGray)
        # painter.drawRect(self.boundingRect())
        pass

    @staticmethod
    def description():
        return DESC

    def compute(self):

        data = self.inp0.get_data()
        try:
            self.out0.set_data(data, False)
            pass
        except Exception as e:
            print(e)
