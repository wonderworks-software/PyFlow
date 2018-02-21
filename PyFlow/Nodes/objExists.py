from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node
import pymel.core as pm


class objExists(Node):
    def __init__(self, name, graph):
        super(objExists, self).__init__(name, graph)
        self.dagPathPin = self.addInputPin('DagPath', DataTypes.String)
        self.bFound = self.addOutputPin('Exists', DataTypes.Bool)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.String], 'outputs': [DataTypes.Bool]}

    @staticmethod
    def category():
        return 'Maya'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'default description'

    def compute(self):
        path = self.dagPathPin.getData()
        self.bFound.setData(pm.objExists(path))
