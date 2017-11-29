#!/usr/bin/env python

"""PySide port of the layouts/dynamiclayouts example from Qt v4.x"""

from PySide.QtCore import Qt, QSize
from PySide.QtGui import (QApplication, QDialog, QLayout, QGridLayout,
                          QMessageBox, QGroupBox, QSpinBox, QSlider,
                          QProgressBar, QDial, QDialogButtonBox,
                          QComboBox, QLabel)

class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        
        self.rotableWidgets = []
        
        self.createRotableGroupBox()
        self.createOptionsGroupBox()
        self.createButtonBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.rotableGroupBox, 0, 0)
        mainLayout.addWidget(self.optionsGroupBox, 1, 0)
        mainLayout.addWidget(self.buttonBox, 2, 0)
        mainLayout.setSizeConstraint(QLayout.SetMinimumSize)

        self.mainLayout = mainLayout
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Dynamic Layouts")

    def rotateWidgets(self):
        count = len(self.rotableWidgets)
        if count % 2 == 1:
            raise AssertionError("Number of widgets must be even")
        
        for widget in self.rotableWidgets:
            self.rotableLayout.removeWidget(widget)

        self.rotableWidgets.append(self.rotableWidgets.pop(0))
        
        for i in range(count//2):
            self.rotableLayout.addWidget(self.rotableWidgets[count - i - 1], 0, i)
            self.rotableLayout.addWidget(self.rotableWidgets[i], 1, i)

        
    def buttonsOrientationChanged(self, index):
        self.mainLayout.setSizeConstraint(QLayout.SetNoConstraint);
        self.setMinimumSize(0, 0);

        orientation = Qt.Orientation(int(self.buttonsOrientationComboBox.itemData(index)))

        if orientation == self.buttonBox.orientation():
            return

        self.mainLayout.removeWidget(self.buttonBox);

        spacing = self.mainLayout.spacing()

        oldSizeHint = self.buttonBox.sizeHint() + QSize(spacing, spacing);
        self.buttonBox.setOrientation(orientation)
        newSizeHint = self.buttonBox.sizeHint() + QSize(spacing, spacing)

        if orientation == Qt.Horizontal:
            self.mainLayout.addWidget(self.buttonBox, 2, 0);
            self.resize(self.size() + QSize(-oldSizeHint.width(), newSizeHint.height()))
        else:
            self.mainLayout.addWidget(self.buttonBox, 0, 3, 2, 1);
            self.resize(self.size() + QSize(newSizeHint.width(), -oldSizeHint.height()))

        self.mainLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

    def show_help(self):
        QMessageBox.information(self, "Dynamic Layouts Help",
                            "This example shows how to change layouts "
                            "dynamically.")

    def createRotableGroupBox(self):
        self.rotableGroupBox = QGroupBox("Rotable Widgets")
        
        self.rotableWidgets.append(QSpinBox())
        self.rotableWidgets.append(QSlider())
        self.rotableWidgets.append(QDial())
        self.rotableWidgets.append(QProgressBar())
        count = len(self.rotableWidgets)
        for i in range(count):
            self.rotableWidgets[i].valueChanged[int].\
                connect(self.rotableWidgets[(i+1) % count].setValue)

        self.rotableLayout = QGridLayout()    
        self.rotableGroupBox.setLayout(self.rotableLayout)

        self.rotateWidgets()
                    
    def createOptionsGroupBox(self):
        self.optionsGroupBox = QGroupBox("Options")

        buttonsOrientationLabel = QLabel("Orientation of buttons:")

        buttonsOrientationComboBox = QComboBox()
        buttonsOrientationComboBox.addItem("Horizontal", Qt.Horizontal)
        buttonsOrientationComboBox.addItem("Vertical", Qt.Vertical)
        buttonsOrientationComboBox.currentIndexChanged[int].connect(self.buttonsOrientationChanged)

        self.buttonsOrientationComboBox = buttonsOrientationComboBox

        optionsLayout = QGridLayout()
        optionsLayout.addWidget(buttonsOrientationLabel, 0, 0)
        optionsLayout.addWidget(self.buttonsOrientationComboBox, 0, 1)
        optionsLayout.setColumnStretch(2, 1)
        self.optionsGroupBox.setLayout(optionsLayout)
    
    def createButtonBox(self):
        self.buttonBox = QDialogButtonBox()

        closeButton = self.buttonBox.addButton(QDialogButtonBox.Close)
        helpButton = self.buttonBox.addButton(QDialogButtonBox.Help)
        rotateWidgetsButton = self.buttonBox.addButton("Rotate &Widgets", QDialogButtonBox.ActionRole)

        rotateWidgetsButton.clicked.connect(self.rotateWidgets)
        closeButton.clicked.connect(self.close)
        helpButton.clicked.connect(self.show_help)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec_()
