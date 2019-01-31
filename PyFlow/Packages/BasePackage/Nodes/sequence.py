from PyFlow.Core import NodeBase

# TODO: remove this
from Qt.QtWidgets import QMenu
# from ..Core.Pin import PinWidgetBase


class sequence(NodeBase):
    def __init__(self, name, graph):
        super(sequence, self).__init__(name, graph)
        self.inExecPin = self.addInputPin('inExec', 'ExecPin', None, self.compute)
        self.menu = QMenu()
        self.action = self.menu.addAction('add pin')
        self.action.triggered.connect(self.addOutPin)

    def addOutPin(self):
        p = self.addOutputPin(str(len(self.outputs)), 'ExecPin')

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'The Sequence node allows for a single execution pulse to trigger a series of events in order. The node may have any number of outputs, all of which get called as soon as the Sequence node receives an input. They will always get called in order, but without any delay. To a typical user, the outputs will likely appear to have been triggered simultaneously.'

    def postCreate(self, jsonTemplate):
        Node.postCreate(self, jsonTemplate)

        # restore dynamically created  outputs
        if len(jsonTemplate['outputs']) == 0:
            self.addOutPin()
            self.addOutPin()
        else:
            # for out in jsonTemplate['outputs']:
            #     PinWidgetBase.deserialize(self, out)
            pass

    def compute(self):
        for out in self.outputs.values():
            out.call()
