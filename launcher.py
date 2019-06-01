import sys
import os
from Qt.QtWidgets import QApplication, QStyleFactory
from PyFlow.App import PyFlow
from PyFlow.UI.Utils.stylesheet import editableStyleSheet

FILE_DIR = os.path.abspath(os.path.dirname(__file__))
STYLE_PATH = os.path.join(FILE_DIR, "PyFlow", "style.css")

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("plastique"))


app.setStyleSheet(editableStyleSheet().getStyleSheet())
instance = PyFlow.instance()
app.setActiveWindow(instance)
instance.show()

try:
    sys.exit(app.exec_())
except Exception as e:
    print(e)
