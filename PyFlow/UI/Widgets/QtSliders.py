#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import struct
from Qt import QtGui, QtCore, QtWidgets

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
FLOAT_RANGE_MIN = 0.1 + (-maxint - 1.0)
FLOAT_RANGE_MAX = maxint + 0.1
INT_RANGE_MIN = -maxint + 0
INT_RANGE_MAX = maxint + 0

sliderStyleSheetA = """
QWidget{
    border: 1.25 solid black;
}
QSlider::groove:horizontal,
    QSlider::sub-page:horizontal {
    background: orange;
}
QSlider::add-page:horizontal,
    QSlider::sub-page:horizontal:disabled {
    background: rgb(53, 53, 53);
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
sliderStyleSheetC = """

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
dragerstyleSheet = """
QGroupBox{
    border: 1.25 solid lightgrey;
    background : black;
    color: white;
}
QLabel{
    background: transparent;
    color: white;
}
"""
dragerstyleSheetHover = """
QGroupBox{
    border: 1.25 solid lightgrey;
    background : orange;
    color: white;
}
QLabel{
    background: transparent;
    color: white;
}
"""

class inputDrager(QtWidgets.QWidget):
    ## PopUp Draggers Houdini Style
    valueChanged = QtCore.Signal(float)
    def __init__(self, parent, factor, *args, **kargs):
        super(inputDrager, self).__init__(*args, **kargs)
        self.parent = parent
        self.setLayout(QtWidgets.QVBoxLayout())
        self.frame = QtWidgets.QGroupBox()
        self.frame.setLayout(QtWidgets.QVBoxLayout())
        self.label = QtWidgets.QLabel(str(factor))
        self.valueLabel = QtWidgets.QLabel("0")
        self.frame.setContentsMargins(0, 0, 0, 0)
        self.frame.layout().setContentsMargins(0, 0, 0, 0)
        self.frame.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        font = self.label.font()
        font.setPointSize(8)
        self.label.setFont(font)
        self.valueLabel.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.valueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.frame.layout().addWidget(self.label)
        self.frame.layout().addWidget(self.valueLabel)
        self.layout().addWidget(self.frame)
        self.setStyleSheet(dragerstyleSheet)
        self.size = 35
        self.setMinimumHeight(self.size)
        self.setMinimumWidth(self.size)
        self.setMaximumHeight(self.size)
        self.setMaximumWidth(self.size)
        self._value = 0
        self._startValue = 0
        self._factor = factor
        self.startDragpos = QtCore.QPointF(QtGui.QCursor.pos())
        self.setAttribute(QtCore.Qt.WA_Hover)        
        self.installEventFilter(self)
        self.label.installEventFilter(self)
        self.valueLabel.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self._value = 0
            self.valueLabel.setText(str(self._value))
            self.startDragpos = event.pos()
            self._startValue = self.parent._value            
        if event.type() == QtCore.QEvent.HoverEnter:
            self._value = 0
            self.startDragpos = self.mapToGlobal(event.pos())
            self.setStyleSheet(dragerstyleSheetHover)
            self.parent.activeDrag = self
            for drag in self.parent.drags:
                if drag != self:
                    drag.setStyleSheet(dragerstyleSheet)            
        if event.type() == QtCore.QEvent.HoverLeave:
            self._value = 0
            self.startDragpos = self.mapToGlobal(event.pos())
            if event.pos().y() > self.height() or event.pos().y() < 0:
                self.setStyleSheet(dragerstyleSheet)

        return False

class draggers(QtWidgets.QWidget):
    ## PopUp Draggers Houdini Style
    def __init__(self, parent=None,isFloat=True):
        super(draggers, self).__init__(parent)    
        self._value = 0
        self._startValue = 0
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)
        self.setWindowFlags(QtCore.Qt.Popup)
        self.activeDrag = None
        self.drags = []
        self.dragsPos = []
        lista = [100.0,10.0,1.0,0.1,0.01,0.001,0.0001]
        if not isFloat:
            lista = [100,10,1]
        for i in lista:
            drag = inputDrager(self,i)
            drag.valueChanged.connect(self.setValue)
            self.drags.append(drag)
            self.layout().addWidget(drag)
        self.installEventFilter(self)

    def setValue(self,value):
        self._value = value
        self.parent().setValue(self._startValue+self._value)
        self.parent().editingFinished.emit()

    def show(self):
        self._startValue = self.parent().value()
        super(draggers, self).show()
        for drag in self.drags:
            self.dragsPos.append(drag.pos())

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if self.activeDrag:
                self.activeDrag.setStyleSheet(dragerstyleSheetHover)
                deltaX = self.activeDrag.mapToGlobal(event.pos()).x() - self.activeDrag.startDragpos.x()
                if event.pos().x() > self.activeDrag.width() or event.pos().x() < 0:
                    self.activeDrag._value = (deltaX / 8) * self.activeDrag._factor
                    self.activeDrag.valueLabel.setText(str(self.activeDrag._value))
                    self.activeDrag.valueChanged.emit(self.activeDrag._startValue + self.activeDrag._value)
                else:
                    self.activeDrag._value = 0
                    self.activeDrag.valueLabel.setText(str(self.activeDrag._value))
                    self.activeDrag.startDragpos = self.activeDrag.mapToGlobal(event.pos())
                    self.activeDrag._startValue = self.activeDrag.parent._value
                    self.activeDrag.valueChanged.emit(0)

        if event.type() == QtCore.QEvent.MouseButtonRelease:
            self.hide()
            self.parent().setValue(self._startValue+self._value)
            self.parent().editingFinished.emit()
            del(self)
        return False

class slider(QtWidgets.QSlider):
    ## Customized Int Slider
    def __init__(self, decimals=3, *args, **kargs):
        super(slider, self).__init__(*args, **kargs)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.deltaValue = 0
        self.startDragpos = QtCore.QPointF()
        self.realStartDragpos = QtCore.QPointF()

    def mousePressEvent(self, event):
        self.prevValue = self.value()
        self.startDragpos = event.pos()
        if event.button() == QtCore.Qt.LeftButton and event.modifiers() not in [QtCore.Qt.ControlModifier, QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]:
            butts = QtCore.Qt.MouseButtons(QtCore.Qt.MidButton)
            nevent = QtGui.QMouseEvent(event.type(), event.pos(),
                                       QtCore.Qt.MidButton, butts,
                                       event.modifiers())
            super(slider, self).mousePressEvent(nevent)

        elif event.modifiers() in [QtCore.Qt.ControlModifier, QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]:
            st_slider = QtWidgets.QStyleOptionSlider()
            st_slider.initFrom(self)
            st_slider.orientation = self.orientation()
            available = self.style().pixelMetric(
                QtWidgets.QStyle.PM_SliderSpaceAvailable, st_slider, self)
            xloc = QtWidgets.QStyle.sliderPositionFromValue(self._min_value,
                                                            self._max_value, super(slider, self).value(), available)
            butts = QtCore.Qt.MouseButtons(QtCore.Qt.MidButton)
            newPos = QtCore.QPointF()
            newPos.setX(xloc)
            nevent = QtGui.QMouseEvent(event.type(), newPos,
                                       QtCore.Qt.MidButton, butts,
                                       event.modifiers())
            self.startDragpos = newPos
            self.realStartDragpos = event.pos()
            super(slider, self).mousePressEvent(nevent)
            self.deltaValue = self.value() - self.prevValue
            self.setValue(self.prevValue)

        else:
            super(slider, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        deltaX = event.pos().x() - self.realStartDragpos.x()
        deltaY = event.pos().y() - self.realStartDragpos.y()
        newPos = QtCore.QPointF()
        if event.modifiers() in [QtCore.Qt.ControlModifier, QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]:
            if event.modifiers() == QtCore.Qt.ControlModifier:
                newPos.setX(self.startDragpos.x() + deltaX / 2)
                newPos.setY(self.startDragpos.y() + deltaY / 2)
            elif event.modifiers() == QtCore.Qt.ShiftModifier:
                newPos.setX(self.startDragpos.x() + deltaX / 4)
                newPos.setY(self.startDragpos.y() + deltaY / 4)
            elif event.modifiers() == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier:
                newPos.setX(self.startDragpos.x() + deltaX / 8)
                newPos.setY(self.startDragpos.y() + deltaY / 8)
            nevent = QtGui.QMouseEvent(event.type(), newPos,
                                       event.button(), event.buttons(),
                                       event.modifiers())
            super(slider, self).mouseMoveEvent(nevent)
            self.setValue(self.value() - self.deltaValue)
        else:
            super(slider, self).mouseMoveEvent(event)

    def keyPressEvent(self, event):
        p = self.mapFromGlobal(QtGui.QCursor.pos())
        self.startDragpos = p
        self.realStartDragpos = p
        self.deltaValue = 0
        super(slider, self).keyPressEvent(event)

class doubleSlider(slider):
    ## Customized Float Slider
    doubleValueChanged = QtCore.Signal(float)

    def __init__(self, decimals=3, *args, **kargs):
        super(doubleSlider, self).__init__(*args, **kargs)
        self._multi = 10 ** decimals
        self._min_value = 0
        self._max_value = 0
        self.valueChanged.connect(self.emitDoubleValueChanged)

    def setDecimals(self, decimals):
        self._multi = 10 ** decimals

    def emitDoubleValueChanged(self):
        value = float(super(doubleSlider, self).value()) / self._multi
        self.doubleValueChanged.emit(value)

    def value(self):
        return float(super(doubleSlider, self).value()) / self._multi

    def minimun(self):
        return float(super(doubleSlider, self).minimun()) / self._multi

    def maximum(self):
        return float(super(doubleSlider, self).maximum()) / self._multi

    def setMinimum(self, value):
        self._min_value = max(INT_RANGE_MIN, value * self._multi)
        return super(doubleSlider, self).setMinimum(self._min_value)

    def setMaximum(self, value):
        self._max_value = min(INT_RANGE_MAX, value * self._multi)
        return super(doubleSlider, self).setMaximum(self._max_value)

    def setSingleStep(self, value):
        return super(doubleSlider, self).setSingleStep(value * self._multi)

    def singleStep(self):
        return float(super(doubleSlider, self).singleStep()) / self._multi

    def setValue(self, value):
        super(doubleSlider, self).setValue(int(value * self._multi))

class valueBox(QtWidgets.QDoubleSpinBox):
    ## Input Text Values with Draggers
    def __init__(self,type="float",*args, **kargs):
        super(valueBox, self).__init__(*args, **kargs)
        self.isFloat = type=="float"
        if not self.isFloat:
            self.setDecimals(0)
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setStyleSheet(sliderStyleSheetA)
        self.lineEdit().installEventFilter(self)
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.MiddleButton:
                dragger = draggers(self,self.isFloat)
                dragger.show()
                if self.isFloat:
                    dragger.move(self.mapToGlobal(QtCore.QPoint(event.pos().x(
                    ) - dragger.width() / 2, event.pos().y() - dragger.height() / 2)))
                else:
                    dragger.move(self.mapToGlobal(QtCore.QPoint(event.pos().x(
                    ) - dragger.width() / 2, event.pos().y() - (dragger.height() - dragger.height() / 6))))
        return False

class pyf_Slider(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(float)

    def __init__(self, parent, type="float", style=0, name=None, *args):
        super(pyf_Slider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.setLayout(QtWidgets.QHBoxLayout())
        self.input = valueBox(type=type)
        self.input.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        if type == "int":
            self.sld = slider()
            self.input.setDecimals(0)
        else:
            self.sld = doubleSlider()
            self.input.setDecimals(3)

        self.layout().setContentsMargins(10, 0, 0, 0)
        self.input.setContentsMargins(0, 0, 0, 0)
        self.sld.setContentsMargins(0, 0, 0, 0)
        self.label = None  
        if name:
            self.label = QtWidgets.QLabel(name + "  ")
            self.layout().addWidget(self.label)
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
            self.sld.setStyleSheet(sliderStyleSheetA)
        elif style == 1:
            self.sld.setStyleSheet(sliderStyleSheetB)
        self.input.setStyleSheet(sliderStyleSheetA)
        if type == "int":
            self.sld.valueChanged.connect(
                lambda: self.setValue(self.sld.value()))
        else:
            self.sld.doubleValueChanged.connect(
                lambda: self.setValue(self.sld.value()))
        self.input.editingFinished.connect(
            lambda: self.setValue(self.input.value()))
        self._value = 0.0
        self._dispMin = 0.0
        self._dispMax = 1.0
        self.setMinimum(-100.0)
        self.setMaximum(100.0)
        self.setDisplayMinimun(0)
        self.setDisplayMaximum(1)
        self.setValue(0.5)

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
            if value > self._dispMax:
                self.setDisplayMaximum(
                    min(self.maximum, value * 2))
            if value < self._dispMin:
                self.setDisplayMinimun(
                    max(self.minimum, value * 2))
            self.sld.setValue(value)
            self._value = self.sld.value()
            self.input.setValue(self.value())
            self.valueChanged.emit(self._value)

    def setMinimum(self, value):
        self.input.setMinimum(value)
        self.sld.setMinimum(value)

    def setMaximum(self, value):
        self.input.setMaximum(value)
        self.sld.setMaximum(value)

    def setRange(self, min, max):
        self.setMinimum(min)
        self.setMaximum(max)

    def setDisplayMinimun(self, value):
        self._dispMin = value
        self.sld.setMinimum(value)

    def setDisplayMaximum(self, value):
        self._dispMax = value
        self.sld.setMaximum(value)

    def setDecimals(self, decimals):
        self.input.setDecimals(decimals)
        if type != "int":
            self.sld.setDecimals(decimals)

    def setSingleStep(self, step):
        self.input.setSingleStep(step)

    def hideLabel(self):
        if self.label:
            self.label.hide()

    def showLabel(self):
        if self.label:
            self.label.show()

    def hideSlider(self):
        self.sld.hide()

    def showSlider(self):
        self.sld.show()

class pyf_HueSlider(doubleSlider):

    def __init__(self, parent, *args):
        super(pyf_HueSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.color = QtGui.QColor()
        self.color.setHslF(0, 1, 0.5, 1)
        self.defColor = self.color.name()
        self.setStyleSheet(sliderStyleSheetC)
        self.light = 0.5
        self.setMinimum(0.0)
        self.setMaximum(1.0)

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

class pyf_GradientSlider(doubleSlider):

    def __init__(self, parent, *args):
        super(pyf_GradientSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.color1 = QtGui.QColor()
        self.color1.setHslF(0, 0, 0, 1)
        self.color2 = QtGui.QColor()
        self.color2.setHslF(0, 1, 1, 1)
        self.setMinimum(0.0)
        self.setMaximum(1.0)
        self.setStyleSheet(sliderStyleSheetC)

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
        self.layout().addWidget(doubleSlider())
        self.layout().addWidget(pyf_Slider(self, style=0))
        self.layout().addWidget(pyf_Slider(self, type = "int",style=1))
        self.layout().addWidget(pyf_HueSlider(self))
        self.layout().addWidget(pyf_GradientSlider(self))
        self.layout().addWidget(valueBox(type="int"))
        self.setStyleSheet("background:grey")

def main():

    app = QtWidgets.QApplication(sys.argv)

    ex = testWidg(None)
    ex.setStyle(QtWidgets.QStyleFactory.create("motif"))
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
