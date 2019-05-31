import sys
import os
from Qt.QtWidgets import QApplication, QStyleFactory
from Qt import QtGui
from PyFlow.App import PyFlow
from PyFlow.UI import InteractiveColor as color

FILE_DIR = os.path.abspath(os.path.dirname(__file__))
STYLE_PATH = os.path.join(FILE_DIR, "PyFlow", "style.css")

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("plastique"))

try:
    with open(STYLE_PATH, 'r') as f:
        styleString = f.read()
        app.setStyleSheet(styleString.replace("rgba(215, 128, 26","rgb(%s"%color))
except Exception as e:
    print(e)

instance = PyFlow.instance()
app.setActiveWindow(instance)
instance.show()

try:
    sys.exit(app.exec_())
except Exception as e:
    print(e)
