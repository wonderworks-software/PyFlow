import uuid
from blinker import Signal
from collections import OrderedDict

from PyFlow.Core.Common import clamp
from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Core.GraphManager import GraphManagerSingleton


class EditorState(object):
    """docstring for EditorState."""
    def __init__(self, text):
        super(EditorState, self).__init__()
        self.text = text
        self.editorState = GraphManagerSingleton().get().serialize()
        EditorHistory().push(self)

    def __repr__(self):
        return self.text


@SingletonDecorator
class EditorHistory(object):
    """docstring for EditorHistory."""
    def __init__(self, app):

        self.statePushed = Signal(object)

        self.app = app
        self._currentIndex = 0
        self.lastIndex = self._currentIndex
        self._shiftDirection = True
        self._lastShiftDirection = self._shiftDirection
        self.stack = OrderedDict()
        self._capacity = 50
        self.activeStateUid = None

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        # TODO: cut states that beyond capacity value

    def clear(self):
        self.stack.clear()
        self.currentIndex = 0

    @property
    def shiftDirection(self):
        return self._shiftDirection

    @shiftDirection.setter
    def shiftDirection(self, value):
        self._lastShiftDirection = self._shiftDirection
        self._shiftDirection = value

    @property
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, value):
        self.lastIndex = self._currentIndex
        self._currentIndex = value

    def push(self, edState):
        if len(self.stack) > 0:
            self.currentIndex += 1
        self.stack[self.currentIndex] = edState
        print("pushed to:", self.currentIndex, edState.text)

        if len(self.stack) >= self.capacity:
            print("remove:", list(self.stack.keys())[0])
            self.stack.popitem(last=False)

        # future history is incompatible. Remove it
        if self.currentIndex < self.maxIndex():
            for i in range(self.currentIndex, self.maxIndex()):
                self.stack.popitem()

        self.statePushed.send(edState)

    def maxIndex(self):
        return max(self.stack.keys())

    def minIndex(self):
        return min(self.stack.keys())

    def select(self, index):
        index = clamp(index, self.minIndex(), self.maxIndex())

        if index == self.currentIndex:
            return

        state = self.stack[index].editorState

        self.app.loadFromData(state)
        self.currentIndex = index
        print("select:", self.currentIndex, self.stack[self.currentIndex].text)

    def stepBack(self):
        self.select(self.currentIndex - 1)

    def isAtLastIndex(self):
        return self.currentIndex == self.maxIndex()

    def isAtFirstIndex(self):
        return self.currentIndex == self.minIndex()

    def stepForward(self):
        self.select(self.currentIndex + 1)
