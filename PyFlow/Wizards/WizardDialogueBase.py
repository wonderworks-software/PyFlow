from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *
from docutils import core
import resources


def rst2html(rst):
    if rst is not None:
        return core.publish_string(rst, writer_name="html").decode("utf-8")
    return ""


class WizardDialogueBase(QDialog):
    """docstring for WizardDialogueBase."""
    def __init__(self, parent=None):
        super(WizardDialogueBase, self).__init__(parent)
        self.resize(700, 500)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setSpacing(1)
        self.mainLayout.setContentsMargins(1, 1, 1, 1)
        self.stackWidget = QStackedWidget()

        # message section
        self.messageLayout = QHBoxLayout()
        self.messageWidget = QLabel()
        self.messageWidget.setTextFormat(QtCore.Qt.RichText)
        self.messageWidget.setWordWrap(True)
        self.messageWidget.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont("Consolas", 20)
        self.messageWidget.setFont(font)
        wizardImage = QLabel("test")
        wizardImage.setPixmap(QtGui.QPixmap(":wizard-cat.png").scaled(250, 250))
        wizardImage.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.messageLayout.addWidget(wizardImage)
        self.messageLayout.addWidget(self.messageWidget)
        self.mainLayout.addLayout(self.messageLayout)

        # add user input section
        # ...
        self.mainLayout.addWidget(self.stackWidget)

        # add navigation buttons
        # ...

        self.setMessageRst("**Hello buddy!** lets create some new stuff!")

    def setMessageRst(self, rst):
        self.messageWidget.setText(rst2html(rst))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    w = WizardDialogueBase()
    w.show()

    sys.exit(app.exec_())
