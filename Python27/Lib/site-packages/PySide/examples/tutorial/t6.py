#!/usr/bin/env python

# PyQt tutorial 6


import sys
from PySide import QtCore, QtGui


class LCDRange(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        lcd = QtGui.QLCDNumber(2)
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 99)
        slider.setValue(0)
        self.connect(slider, QtCore.SIGNAL("valueChanged(int)"),
                     lcd, QtCore.SLOT("display(int)"))

        layout = QtGui.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(slider)
        self.setLayout(layout)


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        quit = QtGui.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))

        grid = QtGui.QGridLayout()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(quit)
        layout.addLayout(grid)
        self.setLayout(layout)
        for row in range(3):
            for column in range(3):
                grid.addWidget(LCDRange(), row, column)




app = QtGui.QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec_())
