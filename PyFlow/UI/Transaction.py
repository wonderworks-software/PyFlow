from blinker import Signal
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

        self.transactionPushed = Signal(object)

        self.app = app
        self.currentIndex = 0
        self.stack = OrderedDict()
        self.transaction = None

    def clear(self):
        self.stack.clear()
        self.currentIndex = 0

    def beginTransaction(self, text):
        if self.transaction is None:
            self.transaction = Transaction(text).begin()

    def endTransaction(self):
        if self.transaction is not None:
            self.transaction.end()
        self.transaction = None

    def push(self, transaction):
        if len(self.stack) > 0:
            self.currentIndex += 1
        self.stack[self.currentIndex] = transaction
        print("pushed to:", self.currentIndex)

    def select(self, index, bBegin=True):
        if index in self.stack:
            state = self.stack[index].beginEditorState if bBegin else self.stack[index].endEditorState
            self.app.loadFromData(state)
            self.currentIndex = index
            print("select:", self.currentIndex)

    def stepBack(self):
        futureIndex = self.currentIndex - 1
        if self.currentIndex == 0 and self.currentIndex in self.stack:
            self.select(self.currentIndex)
        else:
            if futureIndex in self.stack:
                self.select(futureIndex, bBegin=False)

    def stepForward(self):
        futureIndex = self.currentIndex + 1
        if self.currentIndex == 0 and len(self.stack) == 1:
            self.select(self.currentIndex, bBegin=False)
        elif self.currentIndex == list(self.stack.keys())[-1] and len(self.stack) > 1:
            if self.currentIndex in self.stack:
                self.select(self.currentIndex, bBegin=False)
        else:
            if futureIndex in self.stack:
                self.select(futureIndex)


class ScopedEditorTransaction(object):
    """docstring for ScopedEditorTransaction."""
    def __init__(self, text):
        super(ScopedEditorTransaction, self).__init__()
        self.text = text

    def __enter__(self):
        EditorHistory().beginTransaction(self.text)

    def __exit__(self, exceptionType, exceptionValue, traceback):
        EditorHistory().endTransaction()
