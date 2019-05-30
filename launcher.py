from nine import str
from Qt.QtWidgets import QApplication, QStyleFactory
from Qt import QtGui
from Qt import QtCore
import sys
import os

from PyFlow.App import PyFlow

FILE_DIR = os.path.abspath(os.path.dirname(__file__))
STYLE_PATH = os.path.join(FILE_DIR, "PyFlow", "style.css")

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("plastique"))

dark_palette = app.palette()

dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
#app.setPalette(dark_palette)

try:
    with open(STYLE_PATH, 'r') as f:
        styleString = f.read()
        app.setStyleSheet(styleString)
except Exception as e:
    print(e)

instance = PyFlow.instance()
app.setActiveWindow(instance)
instance.show()

try:
    sys.exit(app.exec_())
except Exception as e:
    print(e)
