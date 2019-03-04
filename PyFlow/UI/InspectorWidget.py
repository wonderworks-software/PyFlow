import json

from Qt.QtWidgets import QWidget
from Qt.QtCore import QTimer
from Qt.QtGui import QColor

from PyFlow.UI.Widgets.Inspector_ui import Ui_Form


class InspectorWidget(QWidget, Ui_Form):
    def __init__(self, rootGraph, parent=None):
        super(InspectorWidget, self).__init__(parent)
        self.setupUi(self)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._graph = rootGraph
        self.textEdit.setTextColor(QColor(200, 200, 200, 255))

    def closeEvent(self, event):
        self._timer.stop()
        event.accept()

    def show(self):
        super(InspectorWidget, self).show()
        self._timer.start(500)

    def update(self):
        self.textEdit.clear()

        data = "<font color='white'><b>NODES</b></font><br>"
        for node in self._graph.getNodes():
            data += '<font color="white"><b>{0} - {1}</b></font><br>'.format(node.getName(), str(node.uid))
            data += '<font color="red">&nbsp;&nbsp;&nbsp;&nbsp;INPUTS</font><br>'
            for uid, pin in node.inputs.items():
                uiPin = pin.getWrapper()()
                jsn = uiPin.serialize()
                data += "<font color='green'>==========</font><br>"
                for k, v in jsn.items():
                    data += '<font color="white">&nbsp;&nbsp;&nbsp;&nbsp;{0}: {1}</font><br>'.format(k, v)
            data += '<font color="red">&nbsp;&nbsp;&nbsp;&nbsp;OUTPUTS</font><br>'
            for uid, pin in node.outputs.items():
                uiPin = pin.getWrapper()()
                jsn = uiPin.serialize()
                data += "<font color='green'>==========</font><br>"
                for k, v in jsn.items():
                    data += '<font color="white">&nbsp;&nbsp;&nbsp;&nbsp;{0}: {1}</font><br>'.format(k, v)
            data += "<br>"

        data += "<font color='white'><b>VARS</b></font><br>"
        for var in self._graph.getVars():
            data += '<font color="white"><b>{0} - {1}</b></font><br>'.format(var.name, str(var.uid))
            data += '<font color="white">type - {}</b></font><br>'.format(var.dataType)
            data += "<br>"

        self.textEdit.setHtml(data)
