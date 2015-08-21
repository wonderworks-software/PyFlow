import sys
from PySide import QtGui, QtCore
path = r'd:\Ilgar\GIT\GraphModel'
import pymel.core as pm
if path not in sys.path:
    sys.path.append(path)
if pm.about(q=1, v=1) == '2016':
    import shiboken
else:
    from shiboken import shiboken
import maya.OpenMayaUI as omui
import AGraphPySide
reload(AGraphPySide)

DOCK_NAME = 'GRAPH_DOCK'
LYT_NAME = 'GRAPH_LYT_NAME'
WIN_NAME = 'GRAPH_WIN_NAME'
AREA = 'left'

MAYA_MAIN_WINDOW = shiboken.wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget)
w = AGraphPySide.Widget.GraphWidget('maya graph')

if pm.window(WIN_NAME, ex=1):
    pm.deleteUI(WIN_NAME)

class GRAPHCLASS(QtGui.QMainWindow):
    def __init__(self, parent):
        super(GRAPHCLASS, self).__init__(parent)
        self.setObjectName(WIN_NAME)
        self.resize(500, 500)
        self.setWindowTitle(w.name)
        self.central_widget = QtGui.QWidget(self)
        self.central_widget.setObjectName('graph_central_widget')
        self.grid_lyt = QtGui.QGridLayout(self.central_widget)
        self.grid_lyt.setObjectName("graph_gridLayout")
        self.grid_lyt.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.grid_lyt.addWidget(w)
        self.setCentralWidget(self.central_widget)


wnd = GRAPHCLASS(MAYA_MAIN_WINDOW)
wnd.show()

# dock window
if pm.dockControl(DOCK_NAME, ex=1):
    pm.deleteUI(DOCK_NAME)
dockLayout = pm.paneLayout(LYT_NAME, configuration='single', parent=WIN_NAME, width = 500, height = 500 )
pm.dockControl(DOCK_NAME, aa=['left','right'], a=AREA , floating=0, content=dockLayout, l='Graph widget im maya')
pm.control(WIN_NAME, e=True, parent=dockLayout)
if pm.dockControl( DOCK_NAME, ex = 1 ):
    pm.control( WIN_NAME, e = 1, p = dockLayout )
    pm.dockControl( DOCK_NAME, e = 1, a = AREA, fl = 0 )
    pm.dockControl( DOCK_NAME, e = 1, vis = 1 )
    pm.dockControl( DOCK_NAME, e = 1, w = 500 )
