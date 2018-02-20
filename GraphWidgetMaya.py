import PyFlow.PyFlow as PyFlow
import shiboken2
import maya.OpenMayaUI as omui
from Qt.QtWidgets import QWidget

MAYA_MAIN_WINDOW = shiboken2.wrapInstance(long(omui.MQtUtil.mainWindow()), QWidget)

instance = PyFlow.PyFlow(MAYA_MAIN_WINDOW)
instance.startMainLoop()
instance.show()
