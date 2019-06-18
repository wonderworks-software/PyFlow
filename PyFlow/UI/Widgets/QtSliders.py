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

sys.path.append(r"C:\Users\pedro\OneDrive\pcTools_v5\PyFlow")
from PyFlow.UI.Utils.stylesheet import editableStyleSheet


def clamp(n, vmin, vmax):
    return max(min(n, vmax), vmin)

class inputDrager(QtWidgets.QWidget):
    ## PopUp Draggers Houdini Style
    valueChanged = QtCore.Signal(float)
    def __init__(self, parent, factor, *args, **kargs):
        super(inputDrager, self).__init__(*args, **kargs)
        self.parent = parent
        self.setLayout(QtWidgets.QVBoxLayout())
        self.frame = QtWidgets.QGroupBox()
        self.frame.setLayout(QtWidgets.QVBoxLayout())
        self.label = QtWidgets.QLabel("+"+str(factor))
        self.valueLabel = QtWidgets.QLabel("0")
        self.frame.setContentsMargins(0, 0, 0, 0)
        self.frame.layout().setContentsMargins(0, 0, 0, 0)
        self.frame.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        font = self.label.font()
        font.setPointSize(7)
        self.label.setFont(font)
        self.valueLabel.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.valueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.frame.layout().addWidget(self.label)
        self.frame.layout().addWidget(self.valueLabel)
        self.layout().addWidget(self.frame)
        self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("dragerstyleSheet"))
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
            self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("dragerstyleSheetHover"))
            self.parent.activeDrag = self
            for drag in self.parent.drags:
                if drag != self:
                    drag.setStyleSheet(editableStyleSheet().getSliderStyleSheet("dragerstyleSheet"))            
        if event.type() == QtCore.QEvent.HoverLeave:
            self._value = 0
            self.startDragpos = self.mapToGlobal(event.pos())
            if event.pos().y() > self.height() or event.pos().y() < 0:
                self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("dragerstyleSheet"))

        return False

class draggers(QtWidgets.QWidget):
    ## PopUp Draggers Houdini Style
    def __init__(self, parent=None,isFloat=True,startValue=0.0):
        super(draggers, self).__init__(parent)    
        if not isFloat:
            startValue = int(startValue)
        self.initValue = startValue
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
                self.activeDrag.setStyleSheet(editableStyleSheet().getSliderStyleSheet("dragerstyleSheetHover"))
                deltaX = self.activeDrag.mapToGlobal(event.pos()).x() - self.activeDrag.startDragpos.x()
                if event.pos().x() > self.activeDrag.width() or event.pos().x() < 0:
                    self.activeDrag._value = (deltaX / 8) * self.activeDrag._factor
                    self.activeDrag.valueLabel.setText(str(self.initValue+self.activeDrag._value))
                    self.activeDrag.valueChanged.emit(self.activeDrag._startValue + self.activeDrag._value)
                else:
                    self.activeDrag._value = 0
                    self.activeDrag.valueLabel.setText(str(self.initValue+self.activeDrag._value))
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
    def __init__(self, *args, **kargs):
        super(slider, self).__init__(*args, **kargs)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.deltaValue = 0
        self.startDragpos = QtCore.QPointF()
        self.realStartDragpos = QtCore.QPointF()
        self.setFocusPolicy(QtCore.Qt.StrongFocus )

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
            
    def wheelEvent(self,event):
        if not self.hasFocus():
            event.ignore()
        else:
            super(slider, self).wheelEvent(event)
    def keyPressEvent(self, event):
        p = self.mapFromGlobal(QtGui.QCursor.pos())
        self.startDragpos = p
        self.realStartDragpos = p
        self.deltaValue = 0
        super(slider, self).keyPressEvent(event)

class doubleSlider(slider):
    ## Customized Float Slider
    doubleValueChanged = QtCore.Signal(float)

    def __init__(self, decimals=4, *args, **kargs):
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
    def __init__(self,type="float",buttons=False,*args, **kargs):
        super(valueBox, self).__init__(*args, **kargs)
        self.isFloat = type=="float"
        if not self.isFloat:
            self.setDecimals(0)
        else:
            self.setDecimals(4)
        if not buttons:
            self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("sliderStyleSheetA"))
        self.lineEdit().installEventFilter(self)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus )

    def wheelEvent(self,event):
        if not self.hasFocus():
            event.ignore()
        else:
            super(valueBox, self).wheelEvent(event)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.MiddleButton:
                dragger = draggers(self,self.isFloat,startValue=self.value())
                dragger.show()
                if self.isFloat:
                    dragger.move(self.mapToGlobal(QtCore.QPoint(event.pos().x(
                    ) - dragger.width() / 2, event.pos().y() - dragger.height() / 2)))
                else:
                    dragger.move(self.mapToGlobal(QtCore.QPoint(event.pos().x(
                    ) - dragger.width() / 2, event.pos().y() - (dragger.height() - dragger.height() / 6))))
        return False
    def update(self):
        self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("sliderStyleSheetA"))
        super(valueBox, self).update()

class pyf_Slider(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(object)

    def __init__(self, parent, type="float", style=0, name=None, *args):
        super(pyf_Slider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.setLayout(QtWidgets.QHBoxLayout())
        self.input = valueBox(type=type)
        self.input.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.type = type
        if self.type == "int":
            self.sld = slider()
        else:
            self.sld = doubleSlider()

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
        self.stypeSheetType = style
        if self.stypeSheetType == 0:
            self.layout().setSpacing(0)
            self.sld.setStyleSheet(editableStyleSheet().getSliderStyleSheet("sliderStyleSheetA"))
        elif self.stypeSheetType == 1:
            self.sld.setStyleSheet(editableStyleSheet().getSliderStyleSheet("sliderStyleSheetB"))
        if self.type == "int":
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
    def update(self):
        if self.stypeSheetType == 0:
            self.layout().setSpacing(0)
            self.sld.setStyleSheet(editableStyleSheet().getSliderStyleSheet("sliderStyleSheetA"))
        elif self.stypeSheetType == 1:
            self.sld.setStyleSheet(editableStyleSheet().getSliderStyleSheet("sliderStyleSheetB"))
        super(pyf_Slider, self).update()

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
        if self.type == "int":
            self._value = int(self._value)    
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
            self.valueChanged.emit(self.value())

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
        self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("sliderStyleSheetC"))
        self.light = 0.5
        self.setMinimum(0.0)
        self.setMaximum(1.0)

    def setColor(self, color):
        if isinstance(color, list) and len(color)==3:
            self.color = QtGui.QColor(color[0]*255.0,color[1]*255.0,color[2]*255.0)
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
        rgb = c.getRgbF() 
        return list(rgb)

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
            hue = self.getHue(i * 0.1)
            gradient.setColorAt(i * 0.1, QtGui.QColor(hue[0]*255,hue[1]*255,hue[2]*255))

        qp.setBrush(QtGui.QBrush(gradient))

        qp.drawRect(0, 0, w, h)

class pyf_GradientSlider(doubleSlider):

    def __init__(self, parent,color1=[0,0,0],color2=[255,255,255], *args):
        super(pyf_GradientSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.color1 = QtGui.QColor(color1[0],color1[1],color1[2])
        self.color2 = QtGui.QColor(color2[0],color2[1],color2[2])
        self.setMinimum(0.0)
        self.setMaximum(1.0)
        self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("sliderStyleSheetC"))

    def getColor(self):
        r, g, b = self.color1.getRGB()
        r1, g1, b1 = self.color2.getRGB()

        r2 = (r1 - r) * self.value() + r
        g2 = (g1 - g) * self.value() + g
        b2 = (b1 - b) * self.value() + b
        return [r2, g2, b2]

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

class pyf_ColorSlider(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(list)

    def __init__(self, parent=None,startColor=[0,0,0], type="float",alpha=False,h = 50, *args):
        super(pyf_ColorSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.setLayout(QtWidgets.QHBoxLayout())
        self.type = type
        self.alpha = alpha
        self.RBox = valueBox(type=self.type)
        self.GBox = valueBox(type=self.type)
        self.BBox = valueBox(type=self.type)
        self.ABox = valueBox(type=self.type)

        for i in [self.RBox,self.GBox,self.BBox,self.ABox]:
            i.setMinimum(0)
            if type == "int":
                i.setMaximum(255)
            else:
                i.setMaximum(1.0)
        
        self.R = pyf_GradientSlider(self,color2=[255,0,0])
        self.G = pyf_GradientSlider(self,color2=[0,255,0])
        self.B = pyf_GradientSlider(self,color2=[0,0,255])
        self.A = pyf_GradientSlider(self,color2=[255,255,255])

        div = 1.0
        if self.type == "int":
            div = 255.0

        self.RBox.editingFinished.connect( lambda: self.R.setValue(float(self.RBox.value())/div))
        self.R.doubleValueChanged.connect( lambda: self.RBox.setValue(self.R.value()*div))
        self.GBox.editingFinished.connect( lambda: self.G.setValue(float(self.GBox.value())/div))
        self.G.doubleValueChanged.connect( lambda: self.GBox.setValue(self.G.value()*div))
        self.BBox.editingFinished.connect( lambda: self.B.setValue(float(self.BBox.value())/div))
        self.B.doubleValueChanged.connect( lambda: self.BBox.setValue(self.B.value()*div))
        self.ABox.editingFinished.connect( lambda: self.A.setValue(float(self.ABox.value())/div))
        self.A.doubleValueChanged.connect( lambda: self.ABox.setValue(self.A.value()*div))
                        
        rLay = QtWidgets.QHBoxLayout()
        rLay.addWidget(self.RBox)
        rLay.addWidget(self.R)
        gLay = QtWidgets.QHBoxLayout()
        gLay.addWidget(self.GBox)
        gLay.addWidget(self.G)
        bLay = QtWidgets.QHBoxLayout()
        bLay.addWidget(self.BBox)
        bLay.addWidget(self.B)        
        aLay = QtWidgets.QHBoxLayout()
        aLay.addWidget(self.ABox)
        aLay.addWidget(self.A)

        self.A.setValue(1.0)
        self.Color  = QtWidgets.QPushButton()
        self.Color.clicked.connect(self.showColorDialog)

        self.Color.setMaximumWidth(h)
        self.Color.setMinimumWidth(h)
        self.Color.setMaximumHeight(h-12)
        self.Color.setMinimumHeight(h-12)        
        self.slidersLay = QtWidgets.QVBoxLayout()
        inpList =  [rLay,gLay,bLay]

        if self.alpha:
            inpList.append(aLay)
        else:
            self.A.hide()

        for i in [self.R,self.G,self.B,self.A,self.RBox,self.GBox,self.BBox,self.ABox]:
            
            i.setMaximumHeight(h/(len(inpList)+1))
            i.setMinimumHeight(h/(len(inpList)+1))
        for i in [self.R,self.G,self.B,self.A]:
            i.doubleValueChanged.connect(self.colorChanged)

        for i in inpList:
            self.slidersLay.addLayout(i)

        self.setMaximumHeight(h)
        self.layout().addWidget(self.Color)
        self.layout().addLayout(self.slidersLay)
        self.layout().setSpacing(5)
        self.slidersLay.setSpacing(0)
        self.styleSheetString = "QPushButton{ background-color: rgba(%f,%f,%f,%f);border-color: black;border-radius: 2px;border-style: outset;border-width: 1px;}\nQPushButton:pressed{ border-style: inset;border-color: beige}"
        self.defaultColor = startColor
        if isinstance(startColor,list) and len(startColor)>=3:
            self.setColor(startColor)
        self.Color.setStyleSheet(self.styleSheetString % (self.R.value()*255,self.G.value()*255,self.B.value()*255,self.A.value()*255))
        self._menu = QtWidgets.QMenu()
        self.actionReset = self._menu.addAction("ResetValue")
        self.actionReset.triggered.connect(self.onResetValue)

    def onResetValue(self):
        if self.defaultColor:
            self.setColor(self.defaultColor)

    def setColor(self,color):
        self.R.setValue(color[0])
        self.G.setValue(color[1])
        self.B.setValue(color[2])
        if len(color)>3:
            self.A.setValue(color[3])

    def colorChanged(self,value):
        self.Color.setStyleSheet(self.styleSheetString % (self.R.value()*255,self.G.value()*255,self.B.value()*255,self.A.value()*255))
        valueList = [self.R.value(),self.G.value(),self.B.value()]
        if self.alpha:
            valueList.append(self.A.value())
        if self.type == "int":
            valueList = [clamp(int(i*255),0,255) for i in valueList]
        self.valueChanged.emit(valueList)   

    def showColorDialog(self):
        if self.alpha:
            color = QtWidgets.QColorDialog.getColor(options=QtWidgets.QColorDialog.ShowAlphaChannel)
        else:
            color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.R.setValue(color.redF())
            self.G.setValue(color.greenF())
            self.B.setValue(color.blueF())
            self.A.setValue(color.alphaF())

    def contextMenuEvent(self, event):
        self._menu.exec_(event.globalPos())
        
class pyf_timeline(QtWidgets.QSlider):
    def __init__(self, parent,*args):
        super(pyf_timeline, self).__init__(parent=parent,*args)
        self.parent = parent
        self.cachedFrmaes = []
        self.missingFrames=[]
        self.hover = False
        self.hoverPos = None
        self.PressPos = None
        self.MovePos = None
        self.setRange(0,30)
        self.origMax = self.maximum()
        self.oriMin = self.minimum()
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("timeStyleSheet"))
        self.setMouseTracking(True)
        self.setPageStep(1)
        self.setMinimumSize(1, 40)
        self.installEventFilter(self)
    def update(self):
        self.setStyleSheet(editableStyleSheet().getSliderStyleSheet("timeStyleSheet"))
        super(pyf_timeline,self).update()
    def setRange(self,min,max,setOrig=True):
        if setOrig:
            self.origMax = max
            self.oriMin = min
        return super(pyf_timeline, self).setRange( min, max)
    def setCached(self,cached):
        self.cachedFrmaes = cached
    def setMissing(self,missing):
        self.missingFrames = missing        
    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()        
        super(pyf_timeline, self).paintEvent(event)
    def drawWidget(self, qp):
        font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        qp.setFont(font)

        w = self.width()
        h = self.height()
        nb =  (self.maximum()-self.minimum())
        fStep = float(w) / nb
        step = max(1,int(round(fStep)))
        
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200), 1, 
            QtCore.Qt.SolidLine)
            
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        #qp.drawRect(0, 0, w-50, h-50)
        
        pxNb = int(round((nb+1)*step))
        r = range(self.minimum(),self.maximum()+1,1)
        metrics = qp.fontMetrics()
        fh = metrics.height()      
        for e,i in enumerate(range(0,pxNb, step)):
            pos = self.style().sliderPositionFromValue(self.minimum(),self.maximum(),r[e],self.width())
            half = h/2
            if r[e] in self.cachedFrmaes:
                qp.setPen(QtGui.QColor(0, 255, 0))
                qp.setBrush(QtGui.QColor(0, 255, 0))
                qp.drawRect(pos-(fStep/2),half+5, fStep, 1.5)  
                qp.setPen(pen)
                qp.setBrush(QtCore.Qt.NoBrush)
            elif r[e] in self.missingFrames:
                qp.setPen(QtGui.QColor(255, 0, 0))
                qp.setBrush(QtGui.QColor(255, 0, 0))
                qp.drawRect(pos-(fStep/2),half+5, fStep, 1.5)  
                qp.setPen(pen)
                qp.setBrush(QtCore.Qt.NoBrush)                
            if (r[e]%5) == 0:
                s = 4
                text = r[e]
                fw = metrics.width(str(text))
                qp.drawText((pos)-fw/2, h-fh/3, str(text))
            else:
                s = 1.5
            qp.drawLine(pos,half+s, pos,half-s)
        pos = self.style().sliderPositionFromValue(self.minimum(),self.maximum(),self.value(),self.width())
        fw = metrics.width("0")
        qp.setPen(editableStyleSheet().MainColor)
        if self.value() > self.maximum()-(self.maximum()/2):
            fw += metrics.width(str(self.value()))
            fw *= -1
        qp.drawText((pos)+fw, 0+fh, str(self.value())) 
        if self.hover:
            val = self.style().sliderValueFromPosition(self.minimum(),self.maximum(),self.hoverPos.x(),self.width())
            if val != self.value():
                    pos = self.style().sliderPositionFromValue(self.minimum(),self.maximum(),val,self.width())
                    fw = metrics.width("0")
                    if val > self.maximum()-(self.maximum()/2):
                        fw += metrics.width(str(val))
                        fw *= -1
                    color2 = QtGui.QColor(editableStyleSheet().MainColor)
                    color2.setAlpha(100)
                    pen2 = QtGui.QPen(color2, 2, QtCore.Qt.SolidLine)
                    qp.setPen(pen2)
                    qp.drawLine(pos,0, pos,h)
                    qp.drawText((pos)+fw, 0+fh, str(val)) 
        qp.setPen(pen)       
    def mousePressEvent(self,event):
        if event.modifiers() == QtCore.Qt.AltModifier:
            self.PressPos = event.globalPos()
            self.MovePos = event.globalPos()
        if event.button() == QtCore.Qt.LeftButton and event.modifiers() != QtCore.Qt.AltModifier:
            butts = QtCore.Qt.MouseButtons(QtCore.Qt.MidButton)
            nevent = QtGui.QMouseEvent(event.type(),QtCore.QPointF(event.pos()),QtCore.QPointF(event.globalPos()),QtCore.Qt.MidButton,butts,event.modifiers())
            super(pyf_timeline, self).mousePressEvent(nevent)
        elif event.modifiers() != QtCore.Qt.AltModifier:
            super(pyf_timeline, self).mousePressEvent(event)
    def wheelEvent(self,event):
        newMin = self.minimum()+(round(120/event.delta()))
        newMax = self.maximum()-(round(120/event.delta()))
        self.setRange(newMin,newMax)
        self.repaint()
    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.MouseMove:
            self.hover = True
            self.hoverPos = event.pos()
            self.repaint()
        elif event.type() == QtCore.QEvent.Leave:
            self.hover = False
            self.repaint()
        return super(pyf_timeline, self).eventFilter( widget, event)

    def mouseMoveEvent(self, event):
        if event.modifiers() == QtCore.Qt.AltModifier:
            if event.buttons() in [QtCore.Qt.MidButton,QtCore.Qt.LeftButton] :
                globalPos = event.globalPos()
                diff = globalPos - self.MovePos
                a = (self.width()/(self.maximum()-self.minimum()))
                if abs(diff.x()) > a : 
                    self.MovePos = globalPos
                    newMin = self.minimum()-(1*(diff.x()/abs(diff.x())))
                    newMax = self.maximum()-(1*(diff.x()/abs(diff.x())))
                    self.setRange(newMin,newMax)
                    self.repaint()
        else:
            return super(pyf_timeline, self).mouseMoveEvent( event)

class testWidg(QtWidgets.QWidget):

    def __init__(self, parent):
        super(testWidg, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(pyf_Slider(self, style=0))
        self.layout().addWidget(pyf_Slider(self, type = "int",style=1))
        self.layout().addWidget(pyf_HueSlider(self))
        self.layout().addWidget(pyf_GradientSlider(self))
        self.layout().addWidget(valueBox(type="int"))
        self.layout().addWidget(valueBox(type="float",buttons=True))
        self.layout().addWidget(pyf_ColorSlider(self))
        tim = pyf_timeline(self)
        tim.setCached([0,1,2,3,4,15,20])
        self.layout().addWidget(tim)


def main():
    import os
    import sys

    app = QtWidgets.QApplication(sys.argv)

    app.setStyle(QtWidgets.QStyleFactory.create("plastique"))
    ex = testWidg(None)
    app.setStyleSheet(editableStyleSheet().getStyleSheet())  
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
