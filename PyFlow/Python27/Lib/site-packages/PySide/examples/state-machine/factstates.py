#!/usr/bin/env python
#Author velociraptor Genjix <aphidia@hotmail.com>

from PySide.QtGui import *
from PySide.QtCore import *

class Factorial(QObject):
    xChanged = Signal(int)
    def __init__(self):
        super(Factorial, self).__init__()
        self.xval = -1
        self.facval = 1
    def getX(self):
        return self.xval
    def setX(self, x):
        if self.xval == x:
            return
        self.xval = x
        self.xChanged.emit(x)
    x = Property(int, getX, setX)
    def getFact(self):
        return self.facval
    def setFact(self, fac):
        self.facval = fac
    fac = Property(int, getFact, setFact)

class FactorialLoopTransition(QSignalTransition):
    def __init__(self, fact):
        super(FactorialLoopTransition, self).__init__(fact, SIGNAL('xChanged(int)'))
        self.fact = fact
    def eventTest(self, e):
        if not super(FactorialLoopTransition, self).eventTest(e):
            return False
        return e.arguments()[0] > 1
    def onTransition(self, e):
        x = e.arguments()[0]
        fac = self.fact.fac
        self.fact.fac = x * fac
        self.fact.x = x - 1

class FactorialDoneTransition(QSignalTransition):
    def __init__(self, fact):
        super(FactorialDoneTransition, self).__init__(fact, SIGNAL('xChanged(int)'))
        self.fact = fact
    def eventTest(self, e):
        if not super(FactorialDoneTransition, self).eventTest(e):
            return False
        return e.arguments()[0] <= 1
    def onTransition(self, e):
        print(self.fact.fac)

if __name__ == '__main__':
    import sys
    app = QCoreApplication(sys.argv)
    factorial = Factorial()
    machine = QStateMachine()

    compute = QState(machine)
    compute.assignProperty(factorial, 'fac', 1)
    compute.assignProperty(factorial, 'x', 6)
    compute.addTransition(FactorialLoopTransition(factorial))

    done = QFinalState(machine)
    doneTransition = FactorialDoneTransition(factorial)
    doneTransition.setTargetState(done)
    compute.addTransition(doneTransition)

    machine.setInitialState(compute)
    machine.finished.connect(app.quit)
    machine.start()

    sys.exit(app.exec_())
