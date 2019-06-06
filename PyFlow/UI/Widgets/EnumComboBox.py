from Qt import QtCore
from Qt.QtWidgets import QComboBox


class EnumComboBox(QComboBox):
    """docstring for EnumComboBox."""

    changeCallback = QtCore.Signal(str)

    def __init__(self, values=[], parent=None):
        super(EnumComboBox, self).__init__(parent)
        self.addItems([i for i in values])
        self.currentTextChanged.connect(self.changeCallback.emit)


if __name__ == "__main__":
    import sys
    from Qt.QtWidgets import QApplication
    a = QApplication(sys.argv)

    def clb(string):
        print(string)

    w = EnumComboBox(["A", "B"])
    w.changeCallback.connect(clb)

    w.show()

    sys.exit(a.exec_())
