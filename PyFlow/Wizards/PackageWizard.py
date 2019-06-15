from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *

from PyFlow.Wizards.WizardDialogueBase import WizardDialogueBase


class PackageWizard(WizardDialogueBase):
    """docstring for PackageWizard."""
    def __init__(self, parent=None):
        super(PackageWizard, self).__init__(parent)

    def populate(self):
        self.addPageWidget(QPushButton("TEst"), "*Click* it!")

    @staticmethod
    def run():
        instance = PackageWizard()
        instance.exec()
