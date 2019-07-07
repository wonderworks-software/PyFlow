import uuid
from blinker import Signal
from collections import OrderedDict

from PyFlow.Core.Common import clamp
from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Core.GraphManager import GraphManagerSingleton
from PyFlow.ConfigManager import ConfigManager


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
        self.stack = list()
        try:
            self._capacity = int(ConfigManager().getPrefsValue("PREFS", "General/HistoryDepth"))
        except:
            self._capacity = 10

        self.activeState = None

    def getStack(self):
        return self.stack

    def count(self):
        return len(self.stack)

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        if value < len(self.stack):
            for i in range(len(self.stack) - value):
                state = self.stack.pop()
                self.stateRemoved.send(state)

    def clear(self):
        self.stack.clear()

    def stateIndex(self, state):
        if state in self.stack:
            return self.stack.index(state)
        return -1

    @property
    def currentIndex(self):
        if self.activeState is not None:
            return self.stateIndex(self.activeState)
        return -1

    def push(self, edState):

        if self.currentIndex < self.count() - 1:
            nextState = None
            while True:
                index = self.count() - 1
                nextState = self.stack[index]
                if nextState == self.activeState:
                    break
                state = self.stack.pop()
                self.stateRemoved.send(state)

        self.stack.append(edState)

        if len(self.stack) >= self.capacity:
            poppedState = self.stack.pop(0)
            self.stateRemoved.send(poppedState)

        self.statePushed.send(edState)
        self.activeState = edState
        self.stateSelected.send(edState)

    def selectState(self, state):
        for st in self.stack:
            if state == st:
                self.app.loadFromData(st.editorState)
                self.activeState = st
                self.stateSelected.send(st)
                break

    def select(self, index):
        index = clamp(index, 0, self.count() - 1)

        if index == self.currentIndex:
            return

        if len(self.stack) == 0:
            return

        stateData = self.stack[index].editorState

        self.app.loadFromData(stateData)

        state = self.stack[index]
        self.activeState = state
        self.stateSelected.send(state)

    def saveState(self, text):
        self.push(_EditorState(text))

    def undo(self):
        if self.currentIndex > 0:
            self.select(self.currentIndex - 1)

    def redo(self):
        self.select(self.currentIndex + 1)
