import uuid
from blinker import Signal
from collections import OrderedDict

from PyFlow.Core.Common import clamp
from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Core.GraphManager import GraphManagerSingleton


class _EditorState(object):
    """docstring for _EditorState."""
    def __init__(self, text):
        super(_EditorState, self).__init__()
        self.text = text
        self.editorState = GraphManagerSingleton().get().serialize()

    def __repr__(self):
        return self.text


@SingletonDecorator
class EditorHistory(object):

    """docstring for EditorHistory."""
    def __init__(self, app):

        self.statePushed = Signal(object)
        self.stateRemoved = Signal(object)
        self.stateSelected = Signal(object)

        self.app = app
        self._currentIndex = 0
        self.lastIndex = self._currentIndex
        self._shiftDirection = True
        self._lastShiftDirection = self._shiftDirection
        self.stack = OrderedDict()
        self._capacity = 10
        self.activeState = None

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

        # future history is incompatible. Remove it
        maIndex = self.maxIndex()
        if self.currentIndex < maIndex:
            nextState = None
            while True:
                index = list(self.stack.keys())[-1]
                nextState = self.stack[index]
                if nextState == self.activeState:
                    break
                _index, state = self.stack.popitem()
                self.stateRemoved.send(state)

        self.stack[self.currentIndex] = edState

        if len(self.stack) >= self.capacity:
            index, poppedState = self.stack.popitem(last=False)
            self.stateRemoved.send(poppedState)

        self.statePushed.send(edState)

    def maxIndex(self):
        if len(self.stack) == 0:
            return 0
        return max(self.stack.keys())

    def minIndex(self):
        if len(self.stack) == 0:
            return 0
        return min(self.stack.keys())

    def selectState(self, state):
        for index, st in self.stack.items():
            if state == st:
                self.app.loadFromData(st.editorState)
                self.currentIndex = index
                self.activeState = st
                self.stateSelected.send(st)
                break

    def select(self, index):
        index = clamp(index, self.minIndex(), self.maxIndex())

        if index == self.currentIndex:
            return

        state = self.stack[index].editorState

        self.app.loadFromData(state)
        self.currentIndex = index
        state = self.stack[self.currentIndex]
        self.activeState = state
        self.stateSelected.send(state)

    def saveState(self, text):
        self.push(_EditorState(text))

    def undo(self):
        self.select(self.currentIndex - 1)

    def isAtLastIndex(self):
        return self.currentIndex == self.maxIndex()

    def isAtFirstIndex(self):
        return self.currentIndex == self.minIndex()

    def redo(self):
        self.select(self.currentIndex + 1)
