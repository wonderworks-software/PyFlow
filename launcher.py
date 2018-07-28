from Qt.QtWidgets import QApplication
from Qt import QtGui
from Qt import QtCore
import sys
from os import path
from PyFlow.App import PyFlow

FILE_DIR = path.abspath(path.dirname(__file__))
SETTINGS_PATH = path.join(FILE_DIR, "PyFlow", "appConfig.ini")
STYLE_PATH = path.join(FILE_DIR, "PyFlow", "style.css")

app = QApplication(sys.argv)

dark_palette = app.palette()

dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.black)
dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)

app.setPalette(dark_palette)

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
