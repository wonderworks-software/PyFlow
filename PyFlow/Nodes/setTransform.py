from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node
import pymel.core as pm


class setTransform(Node):
    def __init__(self, name, graph):
        super(setTransform, self).__init__(name, graph)
        self.inExecPin = self.addInputPin('inExec', DataTypes.Exec, self.compute)
        self.outExecPin = self.addOutputPin('outExec', DataTypes.Exec)
        self.result = self.addOutputPin('Result', DataTypes.Bool)
        self.dagPathPin = self.addInputPin('DagPath', DataTypes.String)
        self.locationPin = self.addInputPin('Location', DataTypes.FloatVector3)
        self.rotationPin = self.addInputPin('Rotation', DataTypes.FloatVector3)
        self.scalePin = self.addInputPin('Scale', DataTypes.FloatVector3)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.String, DataTypes.Exec, DataTypes.FloatVector3], 'outputs': [DataTypes.Bool, DataTypes.Exec]}

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
        inLocation = self.locationPin.getData()
        inRotation = self.rotationPin.getData()
        inScale = self.scalePin.getData()
        try:
            node = pm.PyNode(path)
            node.t.set((inLocation.x, inLocation.x, inLocation.z))
            node.r.set((inRotation.x, inRotation.x, inRotation.z))
            node.s.set((inScale.x, inScale.x, inScale.z))
            self.result.setData(True)
        except:
            self.result.setData(False)
