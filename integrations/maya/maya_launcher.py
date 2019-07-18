import ptvsd
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance 
from PyFlow.App import PyFlow
from PySide2.QtWidgets import QWidget

ptvsd.enable_attach(address=('0.0.0.0', 3000), redirect_output=True)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)

if PyFlow.appInstance is None:
    instance = PyFlow.instance(mayaMainWindow, "maya")
    instance.show()
