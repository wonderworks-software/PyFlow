#!/usr/bin/env python

"""***************************************************************************
**
** Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
**
** This file is part of the example classes of the Qt Toolkit.
**
** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
***************************************************************************"""

import sys
from PySide import QtCore, QtGui

import basicdrawing_rc


class RenderArea(QtGui.QWidget):
    points = QtGui.QPolygon([
        QtCore.QPoint(10, 80),
        QtCore.QPoint(20, 10),
        QtCore.QPoint(80, 30),
        QtCore.QPoint(90, 70)
    ])

    Line, Points, Polyline, Polygon, Rect, RoundRect, Ellipse, Arc, \
    Chord, Pie, Path, Text, Pixmap = range(13)

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.shape = RenderArea.Polygon
        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
        self.antialiased = False
        self.transformed = False
        self.pixmap = QtGui.QPixmap()
        self.pixmap.load(":/images/qt-logo.png")

        self.setBackgroundRole(QtGui.QPalette.Base)

    def minimumSizeHint(self):
        return QtCore.QSize(100, 100)

    def sizeHint(self):
        return QtCore.QSize(400, 200)

    def setShape(self, shape):
        self.shape = shape
        self.update()

    def setPen(self, pen):
        self.pen = pen
        self.update()

    def setBrush(self, brush):
        self.brush = brush
        self.update()

    def setAntialiased(self, antialiased):
        self.antialiased = antialiased
        self.update()

    def setTransformed(self, transformed):
        self.transformed = transformed
        self.update()

    def paintEvent(self, event):
        rect = QtCore.QRect(10, 20, 80, 60)

        path = QtGui.QPainterPath()
        path.moveTo(20, 80)
        path.lineTo(20, 30)
        path.cubicTo(80, 0, 50, 50, 80, 80)

        startAngle = 30 * 16
        arcLength = 120 * 16

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        if self.antialiased:
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

        for x in range(0, self.width(), 100):
            for y in range(0, self.height(), 100):
                painter.save()
                painter.translate(x, y)
                if self.transformed:
                    painter.translate(50, 50)
                    painter.rotate(60.0)
                    painter.scale(0.6, 0.9)
                    painter.translate(-50, -50)

                if self.shape == RenderArea.Line:
                    painter.drawLine(rect.bottomLeft(), rect.topRight())
                elif self.shape == RenderArea.Points:
                    painter.drawPoints(RenderArea.points)
                elif self.shape == RenderArea.Polyline:
                    painter.drawPolyline(RenderArea.points)
                elif self.shape == RenderArea.Polygon:
                    painter.drawPolygon(RenderArea.points)
                elif self.shape == RenderArea.Rect:
                    painter.drawRect(rect)
                elif self.shape == RenderArea.RoundRect:
                    painter.drawRoundRect(rect)
                elif self.shape == RenderArea.Ellipse:
                    painter.drawEllipse(rect)
                elif self.shape == RenderArea.Arc:
                    painter.drawArc(rect, startAngle, arcLength)
                elif self.shape == RenderArea.Chord:
                    painter.drawChord(rect, startAngle, arcLength)
                elif self.shape == RenderArea.Pie:
                    painter.drawPie(rect, startAngle, arcLength)
                elif self.shape == RenderArea.Path:
                    painter.drawPath(path)
                elif self.shape == RenderArea.Text:
                    painter.drawText(rect, QtCore.Qt.AlignCenter, self.tr("Qt by\nTrolltech"))
                elif self.shape == RenderArea.Pixmap:
                    painter.drawPixmap(10, 10, self.pixmap)

                painter.restore()

        painter.end()


IdRole = QtCore.Qt.UserRole

class Window(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.renderArea = RenderArea()

        self.shapeComboBox = QtGui.QComboBox()
        self.shapeComboBox.addItem(self.tr("Rectangle"), RenderArea.Rect)
        self.shapeComboBox.addItem(self.tr("Round Rectangle"), RenderArea.RoundRect)
        self.shapeComboBox.addItem(self.tr("Ellipse"), RenderArea.Ellipse)
        self.shapeComboBox.addItem(self.tr("Pie"), RenderArea.Pie)
        self.shapeComboBox.addItem(self.tr("Chord"), RenderArea.Chord)
        self.shapeComboBox.addItem(self.tr("Polygon"), RenderArea.Polygon)
        self.shapeComboBox.addItem(self.tr("Path"), RenderArea.Path)
        self.shapeComboBox.addItem(self.tr("Line"), RenderArea.Line)
        self.shapeComboBox.addItem(self.tr("Polyline"), RenderArea.Polyline)
        self.shapeComboBox.addItem(self.tr("Arc"), RenderArea.Arc)
        self.shapeComboBox.addItem(self.tr("Points"), RenderArea.Points)
        self.shapeComboBox.addItem(self.tr("Text"), RenderArea.Text)
        self.shapeComboBox.addItem(self.tr("Pixmap"), RenderArea.Pixmap)

        self.shapeLabel = QtGui.QLabel(self.tr("&Shape:"))
        self.shapeLabel.setBuddy(self.shapeComboBox)

        self.penWidthSpinBox = QtGui.QSpinBox()
        self.penWidthSpinBox.setRange(0, 20)

        self.penWidthLabel = QtGui.QLabel(self.tr("Pen &Width:"))
        self.penWidthLabel.setBuddy(self.penWidthSpinBox)

        self.penStyleComboBox = QtGui.QComboBox()
        self.penStyleComboBox.addItem(self.tr("Solid"), QtCore.Qt.SolidLine)
        self.penStyleComboBox.addItem(self.tr("Dash"), QtCore.Qt.DashLine)
        self.penStyleComboBox.addItem(self.tr("Dot"), QtCore.Qt.DotLine)
        self.penStyleComboBox.addItem(self.tr("Dash Dot"), QtCore.Qt.DashDotLine)
        self.penStyleComboBox.addItem(self.tr("Dash Dot Dot"), QtCore.Qt.DashDotDotLine)
        self.penStyleComboBox.addItem(self.tr("None"), QtCore.Qt.NoPen)

        self.penStyleLabel = QtGui.QLabel(self.tr("&Pen Style:"))
        self.penStyleLabel.setBuddy(self.penStyleComboBox)

        self.penCapComboBox = QtGui.QComboBox()
        self.penCapComboBox.addItem(self.tr("Flat"), QtCore.Qt.FlatCap)
        self.penCapComboBox.addItem(self.tr("Square"), QtCore.Qt.SquareCap)
        self.penCapComboBox.addItem(self.tr("Round"), QtCore.Qt.RoundCap)

        self.penCapLabel = QtGui.QLabel(self.tr("Pen &Cap:"))
        self.penCapLabel.setBuddy(self.penCapComboBox)

        self.penJoinComboBox = QtGui.QComboBox()
        self.penJoinComboBox.addItem(self.tr("Miter"), QtCore.Qt.MiterJoin)
        self.penJoinComboBox.addItem(self.tr("Bevel"), QtCore.Qt.BevelJoin)
        self.penJoinComboBox.addItem(self.tr("Round"), QtCore.Qt.RoundJoin)

        self.penJoinLabel = QtGui.QLabel(self.tr("Pen &Join:"))
        self.penJoinLabel.setBuddy(self.penJoinComboBox)

        self.brushStyleComboBox = QtGui.QComboBox()
        self.brushStyleComboBox.addItem(self.tr("Linear Gradient"),
                QtCore.Qt.LinearGradientPattern)
        self.brushStyleComboBox.addItem(self.tr("Radial Gradient"),
                QtCore.Qt.RadialGradientPattern)
        self.brushStyleComboBox.addItem(self.tr("Conical Gradient"),
                QtCore.Qt.ConicalGradientPattern)
        self.brushStyleComboBox.addItem(self.tr("Texture"), QtCore.Qt.TexturePattern)
        self.brushStyleComboBox.addItem(self.tr("Solid"), QtCore.Qt.SolidPattern)
        self.brushStyleComboBox.addItem(self.tr("Horizontal"), QtCore.Qt.HorPattern)
        self.brushStyleComboBox.addItem(self.tr("Vertical"), QtCore.Qt.VerPattern)
        self.brushStyleComboBox.addItem(self.tr("Cross"), QtCore.Qt.CrossPattern)
        self.brushStyleComboBox.addItem(self.tr("Backward Diagonal"), QtCore.Qt.BDiagPattern)
        self.brushStyleComboBox.addItem(self.tr("Forward Diagonal"), QtCore.Qt.FDiagPattern)
        self.brushStyleComboBox.addItem(self.tr("Diagonal Cross"), QtCore.Qt.DiagCrossPattern)
        self.brushStyleComboBox.addItem(self.tr("Dense 1"), QtCore.Qt.Dense1Pattern)
        self.brushStyleComboBox.addItem(self.tr("Dense 2"), QtCore.Qt.Dense2Pattern)
        self.brushStyleComboBox.addItem(self.tr("Dense 3"), QtCore.Qt.Dense3Pattern)
        self.brushStyleComboBox.addItem(self.tr("Dense 4"), QtCore.Qt.Dense4Pattern)
        self.brushStyleComboBox.addItem(self.tr("Dense 5"), QtCore.Qt.Dense5Pattern)
        self.brushStyleComboBox.addItem(self.tr("Dense 6"), QtCore.Qt.Dense6Pattern)
        self.brushStyleComboBox.addItem(self.tr("Dense 7"), QtCore.Qt.Dense7Pattern)
        self.brushStyleComboBox.addItem(self.tr("None"), QtCore.Qt.NoBrush)

        self.brushStyleLabel = QtGui.QLabel(self.tr("&Brush Style:"))
        self.brushStyleLabel.setBuddy(self.brushStyleComboBox)

        self.antialiasingCheckBox = QtGui.QCheckBox(self.tr("&Antialiasing"))
        self.transformationsCheckBox = QtGui.QCheckBox(self.tr("&Transformations"))

        self.connect(self.shapeComboBox, QtCore.SIGNAL("activated(int)"),
                     self.shapeChanged)
        self.connect(self.penWidthSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.penChanged)
        self.connect(self.penStyleComboBox, QtCore.SIGNAL("activated(int)"),
                     self.penChanged)
        self.connect(self.penCapComboBox, QtCore.SIGNAL("activated(int)"),
                     self.penChanged)
        self.connect(self.penJoinComboBox, QtCore.SIGNAL("activated(int)"),
                     self.penChanged)
        self.connect(self.brushStyleComboBox, QtCore.SIGNAL("activated(int)"),
                     self.brushChanged)
        self.connect(self.antialiasingCheckBox, QtCore.SIGNAL("toggled(bool)"),
                     self.renderArea.setAntialiased)
        self.connect(self.transformationsCheckBox, QtCore.SIGNAL("toggled(bool)"),
                     self.renderArea.setTransformed)

        checkBoxLayout = QtGui.QHBoxLayout()
        checkBoxLayout.addWidget(self.antialiasingCheckBox)
        checkBoxLayout.addWidget(self.transformationsCheckBox)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.renderArea, 0, 0, 1, 2)
        mainLayout.addWidget(self.shapeLabel, 1, 0)
        mainLayout.addWidget(self.shapeComboBox, 1, 1)
        mainLayout.addWidget(self.penWidthLabel, 2, 0)
        mainLayout.addWidget(self.penWidthSpinBox, 2, 1)
        mainLayout.addWidget(self.penStyleLabel, 3, 0)
        mainLayout.addWidget(self.penStyleComboBox, 3, 1)
        mainLayout.addWidget(self.penCapLabel, 4, 0)
        mainLayout.addWidget(self.penCapComboBox, 4, 1)
        mainLayout.addWidget(self.penJoinLabel, 5, 0)
        mainLayout.addWidget(self.penJoinComboBox, 5, 1)
        mainLayout.addWidget(self.brushStyleLabel, 6, 0)
        mainLayout.addWidget(self.brushStyleComboBox, 6, 1)
        mainLayout.addLayout(checkBoxLayout, 7, 0, 1, 2)
        self.setLayout(mainLayout)

        self.shapeChanged()
        self.penChanged()
        self.brushChanged()
        self.renderArea.setAntialiased(False)
        self.renderArea.setTransformed(False)

        self.setWindowTitle(self.tr("Basic Drawing"))

    def shapeChanged(self):
        shape = int(self.shapeComboBox.itemData(
            self.shapeComboBox.currentIndex(), IdRole))
        self.renderArea.setShape(shape)

    def penChanged(self):
        width = self.penWidthSpinBox.value()
        style = QtCore.Qt.PenStyle(int(self.penStyleComboBox.itemData(
            self.penStyleComboBox.currentIndex(), IdRole)))
        cap = QtCore.Qt.PenCapStyle(int(self.penCapComboBox.itemData(
            self.penCapComboBox.currentIndex(), IdRole)))
        join = QtCore.Qt.PenJoinStyle(int(self.penJoinComboBox.itemData(
            self.penJoinComboBox.currentIndex(), IdRole)))

        self.renderArea.setPen(QtGui.QPen(QtCore.Qt.blue, width, style, cap, join))

    def brushChanged(self):
        style = QtCore.Qt.BrushStyle(int(self.brushStyleComboBox.itemData(
            self.brushStyleComboBox.currentIndex(), IdRole)))

        if style == QtCore.Qt.LinearGradientPattern:
            linearGradient = QtGui.QLinearGradient(0, 0, 100, 100)
            linearGradient.setColorAt(0.0, QtCore.Qt.white)
            linearGradient.setColorAt(0.2, QtCore.Qt.green)
            linearGradient.setColorAt(1.0, QtCore.Qt.black)
            self.renderArea.setBrush(QtGui.QBrush(linearGradient))
        elif style == QtCore.Qt.RadialGradientPattern:
            radialGradient = QtGui.QRadialGradient(50, 50, 50, 50, 50)
            radialGradient.setColorAt(0.0, QtCore.Qt.white)
            radialGradient.setColorAt(0.2, QtCore.Qt.green)
            radialGradient.setColorAt(1.0, QtCore.Qt.black)
            self.renderArea.setBrush(QtGui.QBrush(radialGradient))
        elif style == QtCore.Qt.ConicalGradientPattern:
            conicalGradient = QtGui.QConicalGradient(50, 50, 150)
            conicalGradient.setColorAt(0.0, QtCore.Qt.white)
            conicalGradient.setColorAt(0.2, QtCore.Qt.green)
            conicalGradient.setColorAt(1.0, QtCore.Qt.black)
            self.renderArea.setBrush(QtGui.QBrush(conicalGradient))
        elif style == QtCore.Qt.TexturePattern:
            self.renderArea.setBrush(QtGui.QBrush(QtGui.QPixmap(":/images/brick.png")))
        else:
            self.renderArea.setBrush(QtGui.QBrush(QtCore.Qt.green, style))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
