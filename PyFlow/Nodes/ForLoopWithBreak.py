from AbstractGraph import *
from Settings import *
from Node import Node


class ForLoopWithBreak(Node, NodeBase):
    def __init__(self, name, graph):
        super(ForLoopWithBreak, self).__init__(name, graph, w=100, spacings=Spacings)
        self.stop = False
        self.inExec = self.add_input_port('inExec', DataTypes.Exec, self.compute, hideLabel=True)
        self.firstIndex = self.add_input_port('from', DataTypes.Int)
        self.lastIndex = self.add_input_port('to', DataTypes.Int)
        self.step = self.add_input_port('step', DataTypes.Int)
        self.breakExec = self.add_input_port('break', DataTypes.Exec, self.interrupt)
        self.step.set_data(1)

        self.loopBody = self.add_output_port('LoopBody', DataTypes.Exec)
        self.index = self.add_output_port('Index', DataTypes.Int)
        self.completed = self.add_output_port('Completed', DataTypes.Exec)

        portAffects(self.firstIndex, self.index)
        portAffects(self.lastIndex, self.index)
        portAffects(self.step, self.index)

    def interrupt(self):
        self.stop = True

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter']

    @staticmethod
    def description():
        return 'For loop with ability to break'

    def compute(self):
        indexFrom = self.firstIndex.get_data()
        indexTo = self.lastIndex.get_data()
        step = self.step.get_data()
        for i in range(indexFrom, indexTo, step):
            if self.stop:
                break
            self.index.set_data(i)
            self.loopBody.call()
            push(self.index)
        self.completed.call()
        self.stop = False
