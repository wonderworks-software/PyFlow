#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from Qt import QtGui, QtCore, QtWidgets

class pyf_DoubleSlider(QtWidgets.QSlider):

    def __init__(self, *args, **kwargs):
        super(pyf_DoubleSlider, self).__init__(*args, **kwargs)
        self.decimals = 5
        self._max_int = 10 ** self.decimals

        super(pyf_DoubleSlider, self).setMinimum(0)
        super(pyf_DoubleSlider, self).setMaximum(self._max_int)
        self._min_value = 0.0
        self._max_value = 1.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super(pyf_DoubleSlider, self).value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        super(pyf_DoubleSlider, self).setValue(
            int((value - self._min_value) / self._value_range * self._max_int))

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
        if event.button() == QtCore.Qt.LeftButton:
            butts = QtCore.Qt.MouseButtons(QtCore.Qt.MidButton)
            try:  # maya PySide?
                nevent = QtGui.QMouseEvent(event.type(), QtCore.QPointF(event.pos()), QtCore.QPointF(
                    event.globalPos()), QtCore.Qt.MidButton, butts, event.modifiers())
            except:
                nevent = QtGui.QMouseEvent(event.type(), event.pos(), event.globalPos(
                ), QtCore.Qt.MidButton, butts, event.modifiers())
            super(pyf_DoubleSlider, self).mousePressEvent(nevent)
        # else:
        super(pyf_DoubleSlider, self).mousePressEvent(event)


class pyf_FloatSlider(QtWidgets.QWidget):
    sliderStyleSheet = """
    QSlider::groove:horizontal,
    QSlider::sub-page:horizontal {
        background: white;
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
    inputStyleSheet = """
    QWidget{
        background: white;
        border: 0px;
    }
    """    
    def __init__(self, parent, *args):
        super(pyf_FloatSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.setLayout(QtWidgets.QHBoxLayout())
        self.sld = pyf_DoubleSlider(self)
        self.sld.setOrientation(QtCore.Qt.Horizontal)
        self.sld.setStyleSheet(self.sliderStyleSheet)
        self.input = QtWidgets.QLineEdit()
        self.input.setStyleSheet(self.inputStyleSheet)
        self.input.setMaximumWidth(50)
        self.layout().setSpacing(0)
        self.input.setContentsMargins(2,0,0,0)
        self.sld.setContentsMargins(0,0,0,0)
        self.layout().addWidget(self.input)
        self.layout().addWidget(self.sld)
        self.sld.valueChanged.connect(
            lambda: self.input.setText(str(self.sld.value())))
        self.sld.setMinimum(0)
        self.sld.setMaximum(10)
        self.sld.setValue(5.0)
        self.radius = 10
        a = 50
        self.sld.setMaximumHeight(a)
        self.input.setMaximumHeight(a)
        self.setMaximumHeight(a)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
        super(pyf_FloatSlider, self).paintEvent(event)

    def drawWidget(self, qp):
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.childrenRect()),self.radius,self.radius)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())

        self.setMask(mask)


class pyf_HueSlider(pyf_DoubleSlider):
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
        self.setOrientation(QtCore.Qt.Horizontal)
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


class pyf_GradientSlider(pyf_DoubleSlider):
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

        self.setOrientation(QtCore.Qt.Horizontal)
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
        self.sld = pyf_FloatSlider(self)
        self.layout().addWidget(self.sld)
        #self.setStyleSheet("background:black")


def main():

    app = QtWidgets.QApplication(sys.argv)

    ex = testWidg(None)
    ex.setStyle(QtWidgets.QStyleFactory.create("motif"))
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
