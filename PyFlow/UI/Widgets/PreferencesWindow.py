from Qt.QtWidgets import *


class PreferencesWindow(QMainWindow):
    """docstring for PreferencesWindow."""
    def __init__(self, parent=None):
        super(PreferencesWindow, self).__init__(parent)


if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)

    w = PreferencesWindow()
    w.show()

    sys.exit(a.exec_())
