import sys
from PyFlow.App import PyFlow
from PyFlow.UI.Utils.stylesheet import editableStyleSheet
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QStyleFactory

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("plastique"))
app.setStyleSheet(editableStyleSheet().getStyleSheet())

instance = PyFlow.instance()
if instance is not None:
    app.setActiveWindow(instance)
    instance.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
