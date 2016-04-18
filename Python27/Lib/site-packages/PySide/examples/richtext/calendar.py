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

from PySide import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.selectedDate = QtCore.QDate.currentDate()
        self.fontSize = 10

        centralWidget = QtGui.QWidget()

        dateLabel = QtGui.QLabel("Date:")
        monthCombo = QtGui.QComboBox()

        for month in range(1, 13):
            monthCombo.addItem(QtCore.QDate.longMonthName(month))

        yearEdit = QtGui.QDateTimeEdit()
        yearEdit.setDisplayFormat('yyyy')
        yearEdit.setDateRange(QtCore.QDate(1753, 1, 1),
                QtCore.QDate(8000, 1, 1))

        monthCombo.setCurrentIndex(self.selectedDate.month() - 1)
        yearEdit.setDate(self.selectedDate)

        self.fontSizeLabel = QtGui.QLabel("Font size:")
        self.fontSizeSpinBox = QtGui.QSpinBox()
        self.fontSizeSpinBox.setRange(1, 64)
        self.fontSizeSpinBox.setValue(10)

        self.editor = QtGui.QTextBrowser()
        self.insertCalendar()

        monthCombo.activated[int].connect(self.setMonth)
        yearEdit.dateChanged.connect(self.setYear)
        self.fontSizeSpinBox.valueChanged.connect(self.setfontSize)

        controlsLayout = QtGui.QHBoxLayout()
        controlsLayout.addWidget(dateLabel)
        controlsLayout.addWidget(monthCombo)
        controlsLayout.addWidget(yearEdit)
        controlsLayout.addSpacing(24)
        controlsLayout.addWidget(self.fontSizeLabel)
        controlsLayout.addWidget(self.fontSizeSpinBox)
        controlsLayout.addStretch(1)

        centralLayout = QtGui.QVBoxLayout()
        centralLayout.addLayout(controlsLayout)
        centralLayout.addWidget(self.editor, 1)
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)

    def insertCalendar(self):
        self.editor.clear()
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()

        date = QtCore.QDate(self.selectedDate.year(),
                self.selectedDate.month(), 1)

        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setAlignment(QtCore.Qt.AlignHCenter)
        tableFormat.setBackground(QtGui.QColor('#e0e0e0'))
        tableFormat.setCellPadding(2)
        tableFormat.setCellSpacing(4)
        constraints = [QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 14),
                       QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 14),
                       QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 14),
                       QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 14),
                       QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 14),
                       QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 14),
                       QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 14)]

        tableFormat.setColumnWidthConstraints(constraints)

        table = cursor.insertTable(1, 7, tableFormat)

        frame = cursor.currentFrame()
        frameFormat = frame.frameFormat()
        frameFormat.setBorder(1)
        frame.setFrameFormat(frameFormat)

        format = cursor.charFormat()
        format.setFontPointSize(float(self.fontSize))

        boldFormat = QtGui.QTextCharFormat(format)
        boldFormat.setFontWeight(QtGui.QFont.Bold)

        highlightedFormat = QtGui.QTextCharFormat(boldFormat)
        highlightedFormat.setBackground(QtCore.Qt.yellow)

        for weekDay in range(1, 8):
            cell = table.cellAt(0, weekDay-1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(QtCore.QDate.longDayName(weekDay),
                    boldFormat)

        table.insertRows(table.rows(), 1)

        while date.month() == self.selectedDate.month():
            weekDay = date.dayOfWeek()
            cell = table.cellAt(table.rows()-1, weekDay-1)
            cellCursor = cell.firstCursorPosition()

            if date == QtCore.QDate.currentDate():
                cellCursor.insertText(str(date.day()), highlightedFormat)
            else:
                cellCursor.insertText(str(date.day()), format)

            date = date.addDays(1)

            if weekDay == 7 and date.month() == self.selectedDate.month():
                table.insertRows(table.rows(), 1)

        cursor.endEditBlock()

        self.setWindowTitle("Calendar for %s %d" % (QtCore.QDate.longMonthName(self.selectedDate.month()), self.selectedDate.year()))

    def setfontSize(self, size):
        self.fontSize = size
        self.insertCalendar()

    def setMonth(self, month):
        self.selectedDate = QtCore.QDate(self.selectedDate.year(), month + 1,
                self.selectedDate.day())
        self.insertCalendar()

    def setYear(self, date):
        self.selectedDate = QtCore.QDate(date.year(),
                self.selectedDate.month(), self.selectedDate.day())
        self.insertCalendar()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 256)
    window.show()
    sys.exit(app.exec_())
