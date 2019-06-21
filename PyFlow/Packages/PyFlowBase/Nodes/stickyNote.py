from PyFlow.Core import NodeBase


class stickyNote(NodeBase):
    def __init__(self, name):
        super(stickyNote, self).__init__(name)

    @staticmethod
    def category():
        return 'UI'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Sticky Note to save info with the graph'
