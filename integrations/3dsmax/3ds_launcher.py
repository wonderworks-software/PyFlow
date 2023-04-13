import ptvsd
import pymxs
from PyFlow.PyFlow.App import PyFlow
from PySide2 import QtWidgets
from PySide2 import QtCore

ptvsd.enable_attach(address=('0.0.0.0', 3000), redirect_output=True)

mainWindow = QtWidgets.QWidget.find(pymxs.runtime.windows.getMAXHWND())

if PyFlow.appInstance is None:
    instance = PyFlow.instance(mainWindow, "3dsmax")
    instance.show()
