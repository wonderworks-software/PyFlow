from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *


class CanvasBase(QGraphicsView):
    def __init__(self):
        super(CanvasBase, self).__init__()
