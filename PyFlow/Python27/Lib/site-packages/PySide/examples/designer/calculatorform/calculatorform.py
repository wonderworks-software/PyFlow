#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

import sys
from PySide import QtCore, QtGui

from ui_calculatorform import Ui_CalculatorForm


class CalculatorForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_CalculatorForm()

        self.ui.setupUi(self)

    @QtCore.Slot(int)
    def on_inputSpinBox1_valueChanged(self, value):
        self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox2.value()))

    @QtCore.Slot(int)
    def on_inputSpinBox2_valueChanged(self, value):
        self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox1.value()))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    calculator = CalculatorForm()
    calculator.show()
    sys.exit(app.exec_())
