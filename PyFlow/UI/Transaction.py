from collections import OrderedDict

from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Core.GraphManager import GraphManagerSingleton


class Transaction(object):
    """docstring for Transaction."""
    def __init__(self, text):
        super(Transaction, self).__init__()
        self.text = text
        self.beginEditorState = None
        self.endEditorState = None

    def __repr__(self):
        return self.text

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()

    def begin(self):
        self.beginEditorState = GraphManagerSingleton().get().serialize()
        return self

    def end(self):
        self.endEditorState = GraphManagerSingleton().get().serialize()
        EditorHistory().push(self)


@SingletonDecorator
class EditorHistory(object):
    """docstring for EditorHistory."""
    def __init__(self, app):
        self.app = app
        self.currentIndex = 0
        self.stack = OrderedDict()

    def push(self, transaction):
        self.stack[len(self.stack)] = transaction
        self.currentIndex = len(self.stack)
        print("index:", self.currentIndex)

    def select(self, index):
        if index in self.stack:
            state = self.stack[index].beginEditorState
            self.app.loadFromData(state)
            self.currentIndex = index

    def stepBack(self):
        futureIndex = self.currentIndex - 1
        if futureIndex in self.stack:
            self.select(futureIndex)
            print("index:", self.currentIndex)

    def stepForward(self):
        futureIndex = self.currentIndex + 1
        if futureIndex in self.stack:
            self.select(futureIndex)
            print("index:", self.currentIndex)
