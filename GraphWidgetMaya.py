from PyFlow import PyFlow
import shiboken2
import maya.OpenMayaUI as omui
from Qt.QtWidgets import QWidget

MAYA_MAIN_WINDOW = shiboken2.wrapInstance(long(omui.MQtUtil.mainWindow()), QWidget)

instance = PyFlow.instance(MAYA_MAIN_WINDOW)
instance.G.disableSortcuts()
instance.show()
