#!/usr/bin/env python
#Author velociraptor Genjix <aphidia@hotmail.com>

from PySide.QtGui import *
from PySide.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        button = QPushButton(self)
        button.setGeometry(QRect(100, 100, 100, 100))

        machine = QStateMachine(self)
        s1 = QState()
        s1.assignProperty(button, 'text', 'Outside')
        s2 = QState()
        s2.assignProperty(button, 'text', 'Inside')

        enterTransition = QEventTransition(button, QEvent.Enter)
        enterTransition.setTargetState(s2)
        s1.addTransition(enterTransition)

        leaveTransition = QEventTransition(button, QEvent.Leave)
        leaveTransition.setTargetState(s1)
        s2.addTransition(leaveTransition)

        s3 = QState()
        s3.assignProperty(button, 'text', 'Pressing...')

        pressTransition = QEventTransition(button, QEvent.MouseButtonPress)
        pressTransition.setTargetState(s3)
        s2.addTransition(pressTransition)

        releaseTransition = QEventTransition(button, QEvent.MouseButtonRelease)
        releaseTransition.setTargetState(s2)
        s3.addTransition(releaseTransition)

        machine.addState(s1)
        machine.addState(s2)
        machine.addState(s3)

        machine.setInitialState(s1)
        machine.start()

        self.setCentralWidget(button)
        self.show()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
