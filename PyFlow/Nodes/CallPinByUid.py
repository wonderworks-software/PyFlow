from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QMenu


class CallPinByUid(Node):
    def __init__(self, name, graph):
        super(CallPinByUid, self).__init__(name, graph)
        self.inExec = self.addInputPin('inp', DataTypes.Exec, self.compute)
        self.uidInp = self.addInputPin('uuid', DataTypes.String)
        self.outExec = self.addOutputPin('out', DataTypes.Exec)
        self.menu = QMenu()
        self.actionFindPin = self.menu.addAction('Find pin')
        self.actionFindPin.triggered.connect(self.OnFindPin)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        '''
            used by nodebox to suggest supported pins
            when drop wire from pin into empty space
        '''
        return {'inputs': [DataTypes.String, DataTypes.Exec], 'outputs': [DataTypes.Exec]}

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
        return 'Implicit execution pin call'

    def OnFindPin(self):
        uidStr = self.uidInp.getData()
        try:
            uid = uuid.UUID(uidStr)
            self.graph().findPin(uid)
        except Exception as e:
            print(e)
            pass

    def compute(self):
        '''
            1) get data from inputs
            2) do stuff
            3) put data to outputs
            4) call output execs

            IMPORTANT!:
                Call output execs after all data was written into value pins
                otherwise recursive loop may occur
        '''

        uidStr = self.uidInp.getData()
        uid = uuid.UUID(uidStr)
        if uid in self.graph().pins:
            self.graph().pins[uid].call()
