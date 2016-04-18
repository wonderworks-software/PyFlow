#!/usr/bin/env python

# PyQt tutorial 2


import sys
from PySide import QtCore, QtGui


app = QtGui.QApplication(sys.argv)

quit = QtGui.QPushButton("Quit")
quit.resize(75, 30)
quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

QtCore.QObject.connect(quit, QtCore.SIGNAL("clicked()"),
                       app, QtCore.SLOT("quit()"))

quit.show()
sys.exit(app.exec_())
