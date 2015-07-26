import BaseNode
from PySide import QtCore
from AbstractGraph import *
from Settings import *
from threading import Timer


class GetterNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph, colors=Colors):
        super(GetterNode, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.input = self.add_input_port('input', AGPortDataTypes.tAny)
        self.input.port_connected = self.input_connected
        self.input.port_disconnected = self.input_disconnected
        self.period = self.add_input_port('period', AGPortDataTypes.tNumeric)
        self.period.set_data(2)
        self.colors = colors
        self.lbl = QtGui.QLabel('None')
        prx = QtGui.QGraphicsProxyWidget()
        prx.setWidget(self.lbl)
        prx.setParentItem(self)
        prx.setPos(self.sizes[2]-self.lbl.width(), -self.lbl.height())
        self._active = False
        self.threads = []
        self.stop = False

    def input_connected(self):

        print 'console input connencted. call compute'
        self._active = True
        self.compute()

    def input_disconnected(self):

        print 'console input disconnected'
        self._active = False
        self.lbl.setText('None')

    def compute(self):

        if self._active:
            if self.input.dirty:
                data = self.input.get_data()
                self.lbl.setText(str(data))
            else:
                self.lbl.setText(str(self.input._data))
            if self.period.dirty:
                period = self.period.get_data()
            else:
                period = self.period._data
            if period <= 0.5:
                period = 0.5
            thread = Timer(period, self.compute)
            thread.start()
