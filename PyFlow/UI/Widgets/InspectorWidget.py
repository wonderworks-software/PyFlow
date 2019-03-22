import json

from Qt.QtWidgets import QWidget
from Qt.QtCore import QTimer
from Qt.QtGui import QColor

from PyFlow.UI.Widgets.Ui_Inspector import Ui_Form


class InspectorWidget(QWidget, Ui_Form):
    def __init__(self, rootGraph, parent=None):
        super(InspectorWidget, self).__init__(parent)
        self.setupUi(self)
        self._graph = rootGraph
