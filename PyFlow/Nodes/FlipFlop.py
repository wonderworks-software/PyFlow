from AbstractGraph import *
from Settings import *
from Node import Node


class FlipFlop(Node, NodeBase):
    def __init__(self, name, graph):
        super(FlipFlop, self).__init__(name, graph)
        self.bState = True
        self.inp0 = self.addInputPin('in0', DataTypes.Exec, self.compute, hideLabel=True)
        self.outA = self.addOutputPin('A', DataTypes.Exec)
        self.outB = self.addOutputPin('B', DataTypes.Exec)
        self.bIsA = self.addOutputPin('IsA', DataTypes.Bool)

    @staticmethod
    def pinTypeHints():
        '''
            used by nodebox to suggest supported pins
            when drop wire from pin into empty space
        '''
        return {'inputs': [DataTypes.Exec], 'outputs': [DataTypes.Exec, DataTypes.Bool]}

    @staticmethod
    def category():
        '''
            used by nodebox to place in tree
            to make nested one - use '|' like this ( 'CatName|SubCatName' )
        '''
        return 'FlowControl'

    @staticmethod
    def keywords():
        '''
            used by nodebox filter while typing
        '''
        return []

    @staticmethod
    def description():
        '''
            used by property view and node box widgets
        '''
        return 'Changes flow each time called'

    def compute(self):
        if self.bState:
            self.bIsA.setData(self.bState)
            self.outA.call()
        else:
            self.bIsA.setData(self.bState)
            self.outB.call()
        self.bState = not self.bState
