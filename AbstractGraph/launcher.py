from AbstractGraph import *
from AGraphCommon import *


class PrintString(AGNode):
	def __init__(self, name, graph):
		super(PrintString, self).__init__(name, graph)
		self.data = self.add_input_port("data", AGPortDataTypes.tString)
		self.InputExec = self.add_input_port("IN", AGPortDataTypes.tExec, self.In)
		self.outputExec = self.add_output_port("OUT", AGPortDataTypes.tExec)

	def In(self):
		print(self.data.get_data())
		self.outputExec.call()

g = AGraph("test")

inst = PrintString("PrintString", g)
inst.data.set_data("LALALA")

inst.InputExec.call()
