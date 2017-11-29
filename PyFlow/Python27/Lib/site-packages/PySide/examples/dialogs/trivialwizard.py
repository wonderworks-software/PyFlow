#!/usr/bin/env python

"""PyQt4 port of the dialogs/trivialwizard example from Qt v4.x"""

from PySide import QtGui


def createIntroPage():
    page = QtGui.QWizardPage()
    page.setTitle("Introduction")

    label = QtGui.QLabel("This wizard will help you register your copy of "
            "Super Product Two.")
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


def createRegistrationPage():
    page = QtGui.QWizardPage()
    page.setTitle("Registration")
    page.setSubTitle("Please fill both fields.")

    nameLabel = QtGui.QLabel("Name:")
    nameLineEdit = QtGui.QLineEdit()

    emailLabel = QtGui.QLabel("Email address:")
    emailLineEdit = QtGui.QLineEdit()

    layout = QtGui.QGridLayout()
    layout.addWidget(nameLabel, 0, 0)
    layout.addWidget(nameLineEdit, 0, 1)
    layout.addWidget(emailLabel, 1, 0)
    layout.addWidget(emailLineEdit, 1, 1)
    page.setLayout(layout)

    return page


def createConclusionPage():
    page = QtGui.QWizardPage()
    page.setTitle("Conclusion")

    label = QtGui.QLabel("You are now successfully registered. Have a nice day!")
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    wizard = QtGui.QWizard()
    wizard.addPage(createIntroPage())
    wizard.addPage(createRegistrationPage())
    wizard.addPage(createConclusionPage())

    wizard.setWindowTitle("Trivial Wizard")
    wizard.show()

    sys.exit(wizard.exec_())
