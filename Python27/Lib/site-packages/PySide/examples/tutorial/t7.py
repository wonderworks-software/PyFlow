#!/usr/bin/env python

# PyQt tutorial 7


import sys
from PySide import QtCore, QtGui


class LCDRange(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        lcd = QtGui.QLCDNumber(2)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)

        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     lcd, QtCore.SLOT("display(int)"))
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self, QtCore.SIGNAL("valueChanged(int)"))

        layout = QtGui.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        self.setLayout(layout)

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        quit = QtGui.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))

        grid = QtGui.QGridLayout()
        previousRange = None


        layout = QtGui.QVBoxLayout()
        layout.addWidget(quit)
        layout.addLayout(grid)
        self.setLayout(layout)

        for row in range(3):
            for column in range(3):
                lcdRange = LCDRange()
                grid.addWidget(lcdRange, row, column)

                if previousRange:
                    self.connect(lcdRange, QtCore.SIGNAL("valueChanged(int)"),
                                 previousRange.setValue)

                previousRange = lcdRange



app = QtGui.QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec_())
