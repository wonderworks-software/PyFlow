#!/usr/bin/env python

"""PyQt4 port of the dialogs/extension example from Qt v4.x"""

from PySide import QtCore, QtGui


class FindDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)

        label = QtGui.QLabel("Find &what:")
        lineEdit = QtGui.QLineEdit()
        label.setBuddy(lineEdit)

        caseCheckBox = QtGui.QCheckBox("Match &case")
        fromStartCheckBox = QtGui.QCheckBox("Search from &start")
        fromStartCheckBox.setChecked(True)

        findButton = QtGui.QPushButton("&Find")
        findButton.setDefault(True)

        moreButton = QtGui.QPushButton("&More")
        moreButton.setCheckable(True)
        moreButton.setAutoDefault(False)

        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Vertical)
        buttonBox.addButton(findButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(moreButton, QtGui.QDialogButtonBox.ActionRole)

        extension = QtGui.QWidget()

        wholeWordsCheckBox = QtGui.QCheckBox("&Whole words")
        backwardCheckBox = QtGui.QCheckBox("Search &backward")
        searchSelectionCheckBox = QtGui.QCheckBox("Search se&lection")

        moreButton.toggled.connect(extension.setVisible)

        extensionLayout = QtGui.QVBoxLayout()
        extensionLayout.setContentsMargins(0, 0, 0, 0)
        extensionLayout.addWidget(wholeWordsCheckBox)
        extensionLayout.addWidget(backwardCheckBox)
        extensionLayout.addWidget(searchSelectionCheckBox)
        extension.setLayout(extensionLayout)

        topLeftLayout = QtGui.QHBoxLayout()
        topLeftLayout.addWidget(label)
        topLeftLayout.addWidget(lineEdit)

        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addLayout(topLeftLayout)
        leftLayout.addWidget(caseCheckBox)
        leftLayout.addWidget(fromStartCheckBox)
        leftLayout.addStretch(1)

        mainLayout = QtGui.QGridLayout()
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addWidget(buttonBox, 0, 1)
        mainLayout.addWidget(extension, 1, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Extension")
        extension.hide()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = FindDialog()
    sys.exit(dialog.exec_())
