#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from Qt import QtGui, QtCore, QtWidgets


class _DoubleSlider(QtWidgets.QSlider):

    def __init__(self, *args, **kwargs):
        super(_DoubleSlider, self).__init__(*args, **kwargs)
        self.decimals = 5
        self._max_int = 10 ** self.decimals
        super(_DoubleSlider, self).setMinimum(0)
        super(_DoubleSlider, self).setMaximum(self._max_int)
        self._min_value = 0.0
        self._max_value = 1.0
        self.startDragpos = QtCore.QPointF()
        self.setOrientation(QtCore.Qt.Horizontal)

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super(_DoubleSlider, self).value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        super(_DoubleSlider, self).setValue(
            int((value - self._min_value) / self._value_range * self._max_int))

    def setDecimals(self, decimals):
        self.decimals = decimals
        self._max_int = 10 ** self.decimals

    def setRange(self, min, max):
        self.setMinimum(min)
        self.setMaximum(max)

    def setMinimum(self, value):
        if value > self._max_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._min_value = value
        self.setValue(self.value())

    def setMaximum(self, value):
        if value < self._min_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._max_value = value
        self.setValue(self.value())

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value

    def mousePressEvent(self, event):
        self.prevValue = self.value()
        self.startDragpos = event.pos()
        if event.button() == QtCore.Qt.LeftButton:
            butts = QtCore.Qt.MouseButtons(QtCore.Qt.MidButton)
            nevent = QtGui.QMouseEvent(event.type(), event.pos(),
                                       QtCore.Qt.MidButton, butts,
                                       event.modifiers())
            super(_DoubleSlider, self).mousePressEvent(nevent)
        # else:

        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.setValue(self.prevValue)
            st_slider = QtWidgets.QStyleOptionSlider()
            st_slider.initFrom(self)
            st_slider.orientation = self.orientation()
            available = self.style().pixelMetric(
                QtWidgets.QStyle.PM_SliderSpaceAvailable, st_slider, self)
            xloc = QtWidgets.QStyle.sliderPositionFromValue(0,
                                                            self._max_int, super(_DoubleSlider, self).value(), available)
            butts = QtCore.Qt.MouseButtons(QtCore.Qt.MidButton)
            newPos = QtCore.QPointF()
            newPos.setX(xloc)
            nevent = QtGui.QMouseEvent(event.type(), newPos,
                                       QtCore.Qt.MidButton, butts,
                                       event.modifiers())
            self.startDragpos = newPos
            super(_DoubleSlider, self).mousePressEvent(nevent)
            print xloc, event.pos().x()

        else:
            super(_DoubleSlider, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        deltaX = event.pos().x() - self.startDragpos.x()
        deltaY = event.pos().y() - self.startDragpos.y()
        newPos = QtCore.QPointF()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            newPos.setX(self.startDragpos.x() + deltaX / 2)
            newPos.setY(self.startDragpos.y() + deltaY / 2)
            nevent = QtGui.QMouseEvent(event.type(), newPos,
                                       event.button(), event.buttons(),
                                       event.modifiers())
            super(_DoubleSlider, self).mouseMoveEvent(nevent)
            self.setValue(self.value())  # - self.prevValue)
        elif event.modifiers() == QtCore.Qt.ShiftModifier:
            newPos.setX(self.startDragpos.x() + deltaX * 2)
            newPos.setY(self.startDragpos.y() + deltaY * 2)
            nevent = QtGui.QMouseEvent(event.type(), newPos,
                                       event.button(), event.buttons(),
                                       event.modifiers())
            super(_DoubleSlider, self).mouseMoveEvent(nevent)
        else:
            super(_DoubleSlider, self).mouseMoveEvent(event)

    def keyPressEvent(self, event):
        p = self.mapFromGlobal(QtGui.QCursor.pos())
        self.startDragpos = p


class DoubleSlider(QtWidgets.QSlider):

    # create our our signal that we can connect to if necessary
    doubleValueChanged = QtCore.Signal(float)

    def __init__(self, decimals=3, *args, **kargs):
        super(DoubleSlider, self).__init__(*args, **kargs)
        self._multi = 10 ** decimals
        self.setOrientation(QtCore.Qt.Horizontal)
        self.valueChanged.connect(self.emitDoubleValueChanged)

    def emitDoubleValueChanged(self):
        value = float(super(DoubleSlider, self).value()) / self._multi
        self.doubleValueChanged.emit(value)

    def value(self):
        return float(super(DoubleSlider, self).value()) / self._multi

    def minimun(self):
        return float(super(DoubleSlider, self).minimun()) / self._multi

    def maximum(self):
        return float(super(DoubleSlider, self).maximum()) / self._multi

    def setMinimum(self, value):
        return super(DoubleSlider, self).setMinimum(value * self._multi)

    def setMaximum(self, value):
        return super(DoubleSlider, self).setMaximum(value * self._multi)

    def setSingleStep(self, value):
        return super(DoubleSlider, self).setSingleStep(value * self._multi)

    def singleStep(self):
        return float(super(DoubleSlider, self).singleStep()) / self._multi

    def setValue(self, value):
        super(DoubleSlider, self).setValue(int(value * self._multi))


class pyf_FloatSlider(QtWidgets.QWidget):
    sliderStyleSheetA = """
    QWidget{
        background: white;
        border: 1.25 solid black;
        color : black
    }
    QSlider::groove:horizontal,
        QSlider::sub-page:horizontal {
        background: orange;
    }
    QSlider::add-page:horizontal,
        QSlider::sub-page:horizontal:disabled {
        background: lightgrey;
    }
    QSlider::add-page:horizontal:disabled {
        background: grey;
    }
    QSlider::handle:horizontal {
        width: 1px;
     }
    """
    sliderStyleSheetB = """
    QSlider::groove:horizontal {
        border: 1px solid #bbb;
        background: white;
        height: 2px;
        border-radius: 4px;
    }

    QSlider::sub-page:horizontal {
        background: orange;
        border: 1px solid #777;
        height: 2px;
        border-radius: 4px;
    }

    QSlider::add-page:horizontal {
        background: #fff;
        border: 1px solid #777;
        height: 2px;
        border-radius: 4px;
    }

    QSlider::handle:horizontal {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eee, stop:1 #ccc);
        border: 1px solid #777;
        width: 4px;
        margin-top: -8px;
        margin-bottom: -8px;
        border-radius: 2px;
        height : 10px;
    }

    QSlider::handle:horizontal:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #fff, stop:1 #ddd);
        border: 1px solid #444;
        border-radius: 2px;
    }

    QSlider::sub-page:horizontal:disabled {
        background: #bbb;
        border-color: #999;
    }

    QSlider::add-page:horizontal:disabled {
        background: #eee;
        border-color: #999;
    }

    QSlider::handle:horizontal:disabled {
        background: #eee;
        border: 1px solid #aaa;
        border-radius: 4px;
        height : 10;
    }
    """
    valueChanged = QtCore.Signal(float)

    def __init__(self, parent, style=1, *args):
        super(pyf_FloatSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.setLayout(QtWidgets.QHBoxLayout())
        self.sld = DoubleSlider()
        self.input = QtWidgets.QDoubleSpinBox()
        self.input.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.input.setDecimals(3)
        self.input.setSingleStep(0.1)
        self.layout().setContentsMargins(10, 0, 0, 0)
        self.input.setContentsMargins(0, 0, 0, 0)
        self.sld.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.input)
        self.layout().addWidget(self.sld)
        h = 20
        self.input.setMinimumWidth(50)
        self.input.setMaximumWidth(50)
        self.setMaximumHeight(h)
        self.setMinimumHeight(h)
        self.sld.setMaximumHeight(h)
        self.sld.setMinimumHeight(h)
        self.input.setMaximumHeight(h)
        self.input.setMinimumHeight(h)
        if style == 0:
            self.layout().setSpacing(0)
            self.sld.setStyleSheet(self.sliderStyleSheetA)
        elif style == 1:
            self.sld.setStyleSheet(self.sliderStyleSheetB)
        self.input.setStyleSheet(self.sliderStyleSheetA)
        self.sld.doubleValueChanged.connect(
            lambda: self.setValue(self.sld.value()))
        self.input.editingFinished.connect(
            lambda: self.setValue(self.input.value()))
        self._value = 0.0
        self.setMinimum(-100)
        self.setMaximum(100.0)
        self.setValue(0.5)
        # self.setDisabled(True)

    @property
    def _value_range(self):
        return self.maximum - self.minimum

    @property
    def minimum(self):
        return self.input.minimum()

    @property
    def maximum(self):
        return self.input.maximum()

    def value(self):
        self._value = self.sld.value()
        return self._value

    def setValue(self, value):
        if value >= self.minimum and value <= self.maximum:
            if value > self.sld.maximum():
                self.sld.setMaximum(
                    min(self.maximum, value * 2))
            print value, self.sld.maximum()
            print value, self.sld.minimum()
            if value < self.sld.minimum():
                print max(self.minimum, value * 2)
                self.sld.setMinimum(
                    max(self.minimum, value * 2))
            self.sld.setValue(value)
            self._value = self.sld.value()
            self.input.setValue(self.value())
            self.valueChanged.emit(self._value)

    def setMinimum(self, value):
        self.input.setMinimum(value)
        print min(self.maximum, -(self._value_range % 10))
        self.setDisplayMinimun(min(self.maximum, -(self._value_range % 10)))

    def setMaximum(self, value):
        self.input.setMaximum(value)
        print "value range", self._value_range
        print self._value_range % 10
        self.setDisplayMaximum(max(self.minimum, self._value_range % 10))

    def setDisplayMinimun(self, value):
        print "dispMin", value
        self.sld.setMinimum(value)

    def setDisplayMaximum(self, value):
        print "dispMax", value
        self.sld.setMaximum(value)

    def setRange(self, min, max):
        self.setMinimum(min)
        self.setMaximum(max)

    def setDecimals(self, decimals):
        self.input.setDecimals(decimals)
        self.sld.setDecimals(decimals)

    def setSingleStep(self, step):
        self.input.setSingleStep(step)


class pyf_HueSlider(_DoubleSlider):
    styleSheet = """

    QSlider,QSlider:disabled,QSlider:focus     {
                              background: qcolor(0,0,0,0);   }

     QSlider::groove:horizontal {

        border: 1px solid #999999;
        background: qcolor(0,0,0,0);
     }
    QSlider::handle:horizontal {
        background:  rgba(100,100,100,255);
        width: 6px;
     }
    """

    def __init__(self, parent, *args):
        super(pyf_HueSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.color = QtGui.QColor()
        self.color.setHslF(0, 1, 0.5, 1)
        self.defColor = self.color.name()
        self.setStyleSheet(self.styleSheet)
        self.setMouseTracking(True)
        self.light = 0.5

    def setColor(self, color):
        if isinstance(color, QtGui.QColor):
            self.color = color
            self.defColor = self.color.name()
            self.update()

    def setLightness(self, light):
        self.light = light

    def getColor(self):
        return self.getHue(self.value())

    def getHue(self, hue):
        c = QtGui.QColor(self.defColor)
        h, s, l, a = c.getHslF()
        c.setHslF((h + hue) % 1, s, self.light, a)
        return c

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
        super(pyf_HueSlider, self).paintEvent(event)

    def drawWidget(self, qp):
        w = self.width()
        h = self.height()

        gradient = QtGui.QLinearGradient(0, 0, w, h)
        for i in range(11):
            gradient.setColorAt(i * 0.1, self.getHue(i * 0.1))

        qp.setBrush(QtGui.QBrush(gradient))

        qp.drawRect(0, 0, w, h)


class pyf_GradientSlider(_DoubleSlider):
    styleSheet = """

    QSlider,QSlider:disabled,QSlider:focus     {
                              background: qcolor(0,0,0,0);   }

     QSlider::groove:horizontal {

        border: 1px solid #999999;
        background: qcolor(0,0,0,0);
     }
    QSlider::handle:horizontal {
        background:  rgba(100,100,100,255);
        width: 6px;
     }
    """

    def __init__(self, parent, *args):
        super(pyf_GradientSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.color1 = QtGui.QColor()
        self.color1.setHslF(0, 0, 0, 1)
        self.color2 = QtGui.QColor()
        self.color2.setHslF(0, 1, 1, 1)

        self.setStyleSheet(self.styleSheet)
        self.setMouseTracking(True)

    def getColor(self):
        r, g, b = self.color1.getRGB()
        r1, g1, b1 = self.color2.getRGB()

        r2 = (r1 - r) * self.value() + r
        g2 = (g1 - g) * self.value() + g
        b2 = (b1 - b) * self.value() + b
        c = QtGui.QColor(r2, g2, b2)
        return c

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
        super(pyf_GradientSlider, self).paintEvent(event)

    def drawWidget(self, qp):
        w = self.width()
        h = self.height()

        gradient = QtGui.QLinearGradient(0, 0, w, h)
        gradient.setColorAt(0, self.color1)
        gradient.setColorAt(1, self.color2)
        qp.setBrush(QtGui.QBrush(gradient))

        qp.drawRect(0, 0, w, h)


class testWidg(QtWidgets.QWidget):

    def __init__(self, parent):
        super(testWidg, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(_DoubleSlider(self))
        self.layout().addWidget(pyf_FloatSlider(self, style=0))
        #self.layout().addWidget(pyf_FloatSlider(self, style=1))
        self.layout().addWidget(pyf_HueSlider(self))
        self.layout().addWidget(pyf_GradientSlider(self))
        # self.setStyleSheet("background:grey")


def main():

    app = QtWidgets.QApplication(sys.argv)

    ex = testWidg(None)
    ex.setStyle(QtWidgets.QStyleFactory.create("motif"))
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
