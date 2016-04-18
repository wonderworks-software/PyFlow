#!/usr/bin/env python

# PyQt tutorial 1


import sys
from PySide import QtGui


app = QtGui.QApplication(sys.argv)

hello = QtGui.QPushButton("Hello world!")
hello.resize(100, 30)

hello.show()

sys.exit(app.exec_())
