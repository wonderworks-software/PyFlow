## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from copy import copy
from Qt import QtGui, QtCore, QtWidgets

from PyFlow.UI.Canvas.UICommon import SessionDescriptor
from PyFlow.UI.Utils.stylesheet import editableStyleSheet, Colors
from PyFlow.Core.Common import *
from PyFlow.Core import structs


FLOAT_SLIDER_DRAG_STEPS = [100.0, 10.0, 1.0, 0.1, 0.01, 0.001]
INT_SLIDER_DRAG_STEPS = [100.0, 10.0, 1.0]


class inputDragger(QtWidgets.QWidget):
    """Custom Widget to drag values when midClick over field type input widget, Right Drag increments value, Left Drag decreases Value

    Signals:
        :valueChanged: Signal Emitted when value has change (float)
    """

    def __init__(self, parent, factor, *args, **kwargs):
        """
        :param parent: parent Widget
        :type parent: QtWidget
        :param factor: amount to increment the value
        :type factor: float/int
        """
        super(inputDragger, self).__init__(*args, **kwargs)
        self.parent = parent
        self.setLayout(QtWidgets.QVBoxLayout())
        self.frame = QtWidgets.QGroupBox()
        self.frame.setLayout(QtWidgets.QVBoxLayout())
        self.label = QtWidgets.QLabel("+" + str(factor))
        self.frame.setContentsMargins(0, 0, 0, 0)
        self.frame.layout().setContentsMargins(0, 0, 0, 0)
        self.frame.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        font = self.label.font()
        font.setPointSize(7)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.frame.layout().addWidget(self.label)
        self.layout().addWidget(self.frame)
        self.setStyleSheet(
            editableStyleSheet().getSliderStyleSheet("draggerstyleSheet")
        )
        self.size = 35
        self.setMinimumHeight(self.size)
        self.setMinimumWidth(self.size)
        self.setMaximumHeight(self.size)
        self.setMaximumWidth(self.size)
        self._factor = factor
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)
        self.label.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            self.setStyleSheet(
                editableStyleSheet().getSliderStyleSheet("draggerstyleSheetHover")
            )
            self.parent.activeDrag = self
            for drag in self.parent.drags:
                if drag != self:
                    drag.setStyleSheet(
                        editableStyleSheet().getSliderStyleSheet("draggerstyleSheet")
                    )
        if event.type() == QtCore.QEvent.HoverLeave:
            if event.pos().y() > self.height() or event.pos().y() < 0:
                self.setStyleSheet(
                    editableStyleSheet().getSliderStyleSheet("draggerstyleSheet")
                )

        if event.type() == QtCore.QEvent.MouseMove:
            self.parent.eventFilter(self, event)

        return False


class draggers(QtWidgets.QWidget):
    """PopUp Draggers Houdini Style

    Custom Widget that holds a bunch of :obj:`inputDragger` to drag values when midClick over field type input widget, Right Drag increments value, Left Drag decreases Value
    """

    increment = QtCore.Signal(object)

    def __init__(self, parent=None, isFloat=True, draggerSteps=FLOAT_SLIDER_DRAG_STEPS):
        super(draggers, self).__init__(parent)
        self.initialPos = None
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(QtCore.Qt.Popup)
        self.activeDrag = None
        self.lastDeltaX = 0
        self.drags = []
        steps = copy(draggerSteps)
        if not isFloat:
            # if int, cut steps less than 1.0
            steps = list(filter(lambda x: abs(x) >= 1.0, steps))
        for i in steps:
            drag = inputDragger(self, i)
            self.drags.append(drag)
            self.layout().addWidget(drag)
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if self.activeDrag:
                modifiers = event.modifiers()
                self.activeDrag.setStyleSheet(
                    editableStyleSheet().getSliderStyleSheet("draggerstyleSheetHover")
                )
                if self.initialPos is None:
                    self.initialPos = event.globalPos()
                deltaX = event.globalPos().x() - self.initialPos.x()
                self._changeDirection = clamp(deltaX - self.lastDeltaX, -1.0, 1.0)

                if self._changeDirection != 0:
                    v = self._changeDirection * self.activeDrag._factor

                    if modifiers == QtCore.Qt.NoModifier and deltaX % 4 == 0:
                        self.increment.emit(v)
                    if (
                        modifiers
                        in [QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier]
                        and deltaX % 8 == 0
                    ):
                        self.increment.emit(v)
                    if (
                        modifiers == QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier
                        and deltaX % 32 == 0
                    ):
                        self.increment.emit(v)

                self.lastDeltaX = deltaX

        if event.type() == QtCore.QEvent.MouseButtonRelease:
            self.hide()
            self.lastDeltaX = 0
            del self
        return False


class slider(QtWidgets.QSlider):
    """Customized Int QSlider

    Re implements QSlider adding a few enhancements

    Modifiers:
        :Left/Mid:  Click to move handle
        :Ctrl:  and drag to move handle half velocity
        :Shift:  and drag to move handle quarter velocity
        :Ctrl+Shift:  and drag to move handle eighth velocity

    Extends:
        QtWidgets.QSlider
    """

    editingFinished = QtCore.Signal()
    valueIncremented = QtCore.Signal(object)
    floatValueChanged = QtCore.Signal(object)

    def __init__(
        self,
        parent=None,
        draggerSteps=INT_SLIDER_DRAG_STEPS,
        sliderRange=[-100, 100],
        *args,
        **kwargs,
    ):
        super(slider, self).__init__(parent, **kwargs)
        self.sliderRange = sliderRange
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.draggerSteps = draggerSteps
        self.isFloat = False
        self.deltaValue = 0
        self.startDragpos = QtCore.QPointF()
        self.realStartDragpos = QtCore.QPointF()
        self.LeftButton = QtCore.Qt.LeftButton
        self.MidButton = QtCore.Qt.MidButton
        self.draggers = None
        if SessionDescriptor().software == "maya":
            self.LeftButton = QtCore.Qt.MidButton
            self.MidButton = QtCore.Qt.LeftButton
        self.setRange(self.sliderRange[0], self.sliderRange[1])

    def mousePressEvent(self, event):
        self.prevValue = self.value()
        self.startDragpos = event.pos()
        if event.button() == QtCore.Qt.MidButton:
            if self.draggers is None:
                self.draggers = draggers(
                    self, self.isFloat, draggerSteps=self.draggerSteps
                )
                self.draggers.increment.connect(self.valueIncremented.emit)
            self.draggers.show()
            if self.isFloat:
                self.draggers.move(
                    self.mapToGlobal(
                        QtCore.QPoint(
                            event.pos().x() - 1,
                            event.pos().y() - self.draggers.height() / 2,
                        )
                    )
                )
            else:
                self.draggers.move(
                    self.mapToGlobal(
                        QtCore.QPoint(
                            event.pos().x() - 1,
                            event.pos().y()
                            - (self.draggers.height() - self.draggers.height() / 6),
                        )
                    )
                )

        elif event.button() == self.LeftButton and event.modifiers() not in [
            QtCore.Qt.ControlModifier,
            QtCore.Qt.ShiftModifier,
            QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier,
        ]:
            butts = QtCore.Qt.MouseButtons(self.MidButton)
            nevent = QtGui.QMouseEvent(
                event.type(), event.pos(), self.MidButton, butts, event.modifiers()
            )
            super(slider, self).mousePressEvent(nevent)

        elif event.modifiers() in [
            QtCore.Qt.ControlModifier,
            QtCore.Qt.ShiftModifier,
            QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier,
        ]:
            st_slider = QtWidgets.QStyleOptionSlider()
            st_slider.initFrom(self)
            st_slider.orientation = self.orientation()
            available = self.style().pixelMetric(
                QtWidgets.QStyle.PM_SliderSpaceAvailable, st_slider, self
            )
            xloc = QtWidgets.QStyle.sliderPositionFromValue(
                self.minimum(), self.maximum(), super(slider, self).value(), available
            )
            butts = QtCore.Qt.MouseButtons(self.MidButton)
            newPos = QtCore.QPointF()
            newPos.setX(xloc)
            nevent = QtGui.QMouseEvent(
                event.type(), newPos, self.MidButton, butts, event.modifiers()
            )
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
        if event.modifiers() in [
            QtCore.Qt.ControlModifier,
            QtCore.Qt.ShiftModifier,
            QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier,
        ]:
            if event.modifiers() == QtCore.Qt.ControlModifier:
                newPos.setX(self.startDragpos.x() + deltaX / 2)
                newPos.setY(self.startDragpos.y() + deltaY / 2)
            elif event.modifiers() == QtCore.Qt.ShiftModifier:
                newPos.setX(self.startDragpos.x() + deltaX / 4)
                newPos.setY(self.startDragpos.y() + deltaY / 4)
            elif (
                event.modifiers() == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier
            ):
                newPos.setX(self.startDragpos.x() + deltaX / 8)
                newPos.setY(self.startDragpos.y() + deltaY / 8)
            nevent = QtGui.QMouseEvent(
                event.type(), newPos, event.button(), event.buttons(), event.modifiers()
            )
            super(slider, self).mouseMoveEvent(nevent)
            self.setValue(self.value() - self.deltaValue)
        else:
            super(slider, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
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


class DoubleSlider(slider):
    doubleValueChanged = QtCore.Signal(float)

    def __init__(
        self,
        parent=None,
        sliderRange=(-100.0, 100.0),
        defaultValue=0.0,
        dencity=1000000,
        draggerSteps=FLOAT_SLIDER_DRAG_STEPS,
    ):
        super(DoubleSlider, self).__init__(
            parent, draggerSteps=draggerSteps, sliderRange=sliderRange
        )
        self.isFloat = True
        self._dencity = abs(dencity)
        self.setOrientation(QtCore.Qt.Horizontal)

        # set internal int slider range (dencity)
        self.setMinimum(0)
        self.setMaximum(self._dencity)

        # set out range
        self.valueChanged.connect(self.onInternalValueChanged)
        self.valueIncremented.connect(self.onValueIncremented)
        self.setMappedValue(defaultValue, True)

    def onValueIncremented(self, step):
        # convert step value to slider internal space
        sliderInternalRange = (self.minimum(), self.maximum())
        sliderDistance = max(sliderInternalRange) - min(sliderInternalRange)
        valueDistance = max(self.sliderRange) - min(self.sliderRange)
        factor = sliderDistance / valueDistance
        unMappedStep = step * factor

        currentInternalValue = self.value()
        newUnmappedValue = currentInternalValue + unMappedStep
        self.setValue(newUnmappedValue)

    def mappedValue(self):
        return self.mapValue(self.value())

    def setMappedValue(self, value, blockSignals=False):
        # convert mapped value to slider internal integer
        internalValue = self.unMapValue(value)

        if blockSignals:
            self.blockSignals(True)

        self.setValue(internalValue)

        if self.signalsBlocked() and blockSignals:
            self.blockSignals(False)

    def mapValue(self, inValue):
        # convert slider int value to slider float range value
        return mapRangeUnclamped(
            inValue,
            self.minimum(),
            self.maximum(),
            self.sliderRange[0],
            self.sliderRange[1],
        )

    def unMapValue(self, outValue):
        # convert mapped float value to slider integer
        return int(
            mapRangeUnclamped(
                outValue,
                self.sliderRange[0],
                self.sliderRange[1],
                self.minimum(),
                self.maximum(),
            )
        )

    def onInternalValueChanged(self, x):
        mappedValue = self.mapValue(x)
        self.doubleValueChanged.emit(mappedValue)


class valueBox(QtWidgets.QDoubleSpinBox):
    """Custom QDoubleSpinBox

    Custom SpinBox with Houdini Style draggers, :obj:`draggers`. Middle Click to display a bunch of draggers to change value by adding different delta values

    Extends:
        QtWidgets.QDoubleSpinBox
    """

    valueIncremented = QtCore.Signal(object)

    def __init__(
        self,
        labelText="",
        type="float",
        buttons=False,
        decimals=3,
        draggerSteps=FLOAT_SLIDER_DRAG_STEPS,
        *args,
        **kwargs,
    ):
        """
        :param type: Choose if create a float or int spinBox, defaults to "float"
        :type type: str, optional
        :param buttons: Show or hidden right up/Down Buttons, defaults to False
        :type buttons: bool, optional
        :param decimals: Number of decimals if type is "float", defaults to 3
        :type decimals: int, optional
        :param *args: [description]
        :type *args: [type]
        :param **kwargs: [description]
        :type **kwargs: [type]
        """
        super(valueBox, self).__init__(*args, **kwargs)
        self.labelFont = QtGui.QFont("Serif", 10, QtGui.QFont.Bold)
        self.labelText = labelText
        self.draggerSteps = copy(draggerSteps)
        self.isFloat = type == "float"
        if not self.isFloat:
            self.setDecimals(0)
        else:
            self.setDecimals(decimals)
        if not buttons:
            self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setStyleSheet(
            editableStyleSheet().getSliderStyleSheet("sliderStyleSheetA")
        )
        self.lineEdit().installEventFilter(self)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.draggers = None
        self.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)

    def paintEvent(self, event):
        super(valueBox, self).paintEvent(event)
        p = QtGui.QPainter()
        p.begin(self)
        p.setPen(Colors.DarkGray)
        p.setFont(self.labelFont)
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, self.labelText)
        p.end()

    def wheelEvent(self, event):
        if not self.hasFocus():
            event.ignore()
        else:
            super(valueBox, self).wheelEvent(event)

    def onValueIncremented(self, step):
        self.valueIncremented.emit(step)
        val = self.value() + step
        self.setValue(val)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.MiddleButton:
                if self.draggers is None:
                    self.draggers = draggers(
                        self, self.isFloat, draggerSteps=self.draggerSteps
                    )
                    self.draggers.increment.connect(self.onValueIncremented)
                self.draggers.show()
                if self.isFloat:
                    self.draggers.move(
                        self.mapToGlobal(
                            QtCore.QPoint(
                                event.pos().x() - 1,
                                event.pos().y() - self.draggers.height() / 2,
                            )
                        )
                    )
                else:
                    self.draggers.move(
                        self.mapToGlobal(
                            QtCore.QPoint(
                                event.pos().x() - 1,
                                event.pos().y() - self.draggers.height() + 15,
                            )
                        )
                    )
        return False

    def update(self):
        self.setStyleSheet(
            editableStyleSheet().getSliderStyleSheet("sliderStyleSheetA")
        )
        super(valueBox, self).update()


class pyf_Slider(QtWidgets.QWidget):
    """Custom Slider that encapsulates a :obj:`slider` or a :obj:`DoubleSlider` and a :obj:`valueBox` linked together

    Signals:
        :valueChanged: Signal emitted when slider or valueBox value changes, int/float
    """

    valueChanged = QtCore.Signal(object)

    def __init__(
        self,
        parent,
        type="float",
        style=0,
        name=None,
        sliderRange=(-100.0, 100.0),
        defaultValue=0.0,
        draggerSteps=FLOAT_SLIDER_DRAG_STEPS,
        *args,
    ):
        """
        :param parent: Parent Widget
        :type parent: QtWidgets.QWidget
        :param type: Choose if create a float or int Slider, defaults to "float"
        :type type: str, optional
        :param style: Choose looking style, 0 is a full colored xsi style slider, and 1 is a normal colored slider, defaults to 0
        :type style: number, optional
        :param name: Name to display in a label, if None no label created, defaults to None
        :type name: [type], optional
        :param *args: [description]
        :type *args: [type]
        """
        super(pyf_Slider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.setLayout(QtWidgets.QHBoxLayout())
        self.input = valueBox(type=type)
        self.input.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.input.valueIncremented.connect(self.incrementValue)
        self.type = type

        if self.type == "float":
            self.sld = DoubleSlider(
                self,
                defaultValue=defaultValue,
                sliderRange=sliderRange,
                draggerSteps=draggerSteps,
            )
        if self.type == "int":
            self.sld = slider(self, sliderRange=sliderRange)
            self.sld.valueIncremented.connect(self.incrementValue)

        self.input.setRange(sliderRange[0], sliderRange[1])

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
        self.styleSheetType = style
        if self.styleSheetType == 0:
            self.layout().setSpacing(0)
            self.sld.setStyleSheet(
                editableStyleSheet().getSliderStyleSheet("sliderStyleSheetA")
            )
        elif self.styleSheetType == 1:
            self.sld.setStyleSheet(
                editableStyleSheet().getSliderStyleSheet("sliderStyleSheetB")
            )

        self.sld.valueChanged.connect(self.sliderValueChanged)
        self.input.valueChanged.connect(self.valBoxValueChanged)

        self._value = 0.0

    def sliderValueChanged(self, x):
        outValue = mapRangeUnclamped(
            x,
            self.sld.minimum(),
            self.sld.maximum(),
            self.input.minimum(),
            self.input.maximum(),
        )
        self.input.blockSignals(True)
        self.input.setValue(outValue)
        self.input.blockSignals(False)
        self.valueChanged.emit(outValue)

    def valBoxValueChanged(self, x):
        val = self.input.value()
        sv = mapRangeUnclamped(
            val,
            self.input.minimum(),
            self.input.maximum(),
            self.sld.minimum(),
            self.sld.maximum(),
        )
        self.sld.blockSignals(True)
        self.sld.setValue(int(sv))
        self.sld.blockSignals(False)
        self.valueChanged.emit(x)

    def update(self):
        if self.styleSheetType == 0:
            self.layout().setSpacing(0)
            self.sld.setStyleSheet(
                editableStyleSheet().getSliderStyleSheet("sliderStyleSheetA")
            )
        elif self.styleSheetType == 1:
            self.sld.setStyleSheet(
                editableStyleSheet().getSliderStyleSheet("sliderStyleSheetB")
            )
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
        self._value = self.input.value()
        if self.type == "int":
            self._value = int(self._value)
        return self._value

    def incrementValue(self, delta):
        if delta == 0.0:
            return
        old = self.input.value()
        new = old + delta
        self.input.setValue(new)
        self.valueChanged.emit(new)

    def setValue(self, value):
        self.input.setValue(value)
        self._value = self.input.value()
        self.valueChanged.emit(self.value())
        self.valBoxValueChanged(0)

    def setMinimum(self, value):
        # self.input.setMinimum(value)
        # self.sld.setMinimum(value)
        pass

    def setMaximum(self, value):
        # self.input.setMaximum(value)
        # self.sld.setMaximum(value)
        pass

    def setRange(self, min, max):
        """Sets the range for the input value, real max and min range

        :param min: Minimum Value
        :type min: float/int
        :param max: Maximum Value
        :type max: float/int
        """
        self.setMinimum(min)
        self.setMaximum(max)

    def setDisplayMinimun(self, value):
        """Sets the Minimum value for display options, real min value don't touched, if current value is less than this display value,Widget automatically recalculates minDisplay

        :param value: New Display MinValue
        :type value: float/int
        """
        # self._dispMin = value
        # self.sld.setMinimum(value)
        pass

    def setDisplayMaximum(self, value):
        """Sets the Maximum value for display options, real max value don't touched, if current value is bigger than this display value,Widget automatically recalculates maxDisplay

        :param value: New Display MaxValue
        :type value: float/int
        """
        # self._dispMax = value
        # self.sld.setMaximum(value)
        pass

    def setDecimals(self, decimals):
        self.input.setDecimals(decimals)
        # if type != "int":
        #     self.sld.setDecimals(decimals)

    def setSingleStep(self, step):
        self.input.setSingleStep(step)

    def hideLabel(self):
        """Hides Name label
        """
        if self.label:
            self.label.hide()

    def showLabel(self):
        """Shows Name label
        """
        if self.label:
            self.label.show()

    def hideSlider(self):
        """Hides Slider
        """
        self.sld.hide()

    def showSlider(self):
        """Show Slider
        """
        self.sld.show()


class pyf_HueSlider(DoubleSlider):
    """Custom Slider to select a color by a hue selector

    Extends:
        :obj: `DoubleSlider`
    """

    def __init__(self, parent, *args):
        """
        :param parent: Parent QtWidget
        :type parent: QtWidgets.QWidget
        """
        super(pyf_HueSlider, self).__init__(
            parent=parent,
            sliderRange=(0.0, 1.0),
            draggerSteps=[0.1, 0.01, 0.001],
            *args,
        )
        self.parent = parent
        self.color = QtGui.QColor()
        self.color.setHslF(0, 1, 0.5, 1)
        self.defColor = self.color.name()
        self.setStyleSheet(
            editableStyleSheet().getSliderStyleSheet("sliderStyleSheetC")
        )
        self.light = 0.5

    def setColor(self, color):
        """Sets the current start color where hue will be calculated from

        :param color: Float list in range 0-1 representing rgb colors
        :type color: [float,float,float]
        """
        if isinstance(color, list) and len(color) == 3:
            self.color = QtGui.QColor(
                color[0] * 255.0, color[1] * 255.0, color[2] * 255.0
            )
            self.defColor = self.color.name()
            self.update()

    def setLightness(self, light):
        """Sets the lightness of the current slider that will be user for Hue calculations

        :param light: lightness value
        :type light: float
        """
        self.light = light

    def getColor(self):
        """Gets the current Color

        :returns:  Float list in range 0-1 representing rgb colors
        :rtype: [float,float,float]
        """
        return self.getHue(self.mappedValue())

    def getHue(self, hue):
        """Compute hue based on input value in range 0-1

        :param hue: U value where to calculate hue
        :type hue: float
        :returns:  Float list in range 0-1 representing rgb colors
        :rtype: [float,float,float]
        """
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
            gradient.setColorAt(
                i * 0.1, QtGui.QColor(hue[0] * 255, hue[1] * 255, hue[2] * 255)
            )

        qp.setBrush(QtGui.QBrush(gradient))

        qp.drawRect(0, 0, w, h)


class pyf_GradientSlider(DoubleSlider):
    """Custom Slider to select a color by Non Editable gradient

    # Extends:
    #     :obj: `DoubleSlider`
    """

    def __init__(
        self,
        parent,
        color1=[0, 0, 0],
        color2=[255, 255, 255],
        sliderRange=(0.0, 255.0),
        draggerSteps=[5.0, 1.0, 0.25],
        *args,
    ):
        """
        :param parent: Parent QtWidget
        :type parent: QtWidgets.QWidget
        :param color1:  Start Color in range 0-255 , defaults to [0, 0, 0]
        :type color1: [int,int,int], optional
        :param color2: End Color in range 0-255, defaults to [255, 255, 255]
        :type color2: [int,int,int], optional
        """
        super(pyf_GradientSlider, self).__init__(
            parent=parent, sliderRange=sliderRange, draggerSteps=draggerSteps, *args
        )
        self.parent = parent
        self.color1 = QtGui.QColor(color1[0], color1[1], color1[2])
        self.color2 = QtGui.QColor(color2[0], color2[1], color2[2])
        self.setStyleSheet(
            editableStyleSheet().getSliderStyleSheet("sliderStyleSheetC")
        )

    def getColor(self):
        """Computes the current Color

        :returns:  Int list in range 0-255 representing rgb colors
        :rtype: [int, int, int]
        """
        r, g, b = self.color1.getRGB()
        r1, g1, b1 = self.color2.getRGB()

        r2 = (r1 - r) * self.mappedValue() + r
        g2 = (g1 - g) * self.mappedValue() + g
        b2 = (b1 - b) * self.mappedValue() + b
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
    """Custom Slider to choose a color by components. It encapsulates a bunch of :obj:`valueBox` and :obj:`pyf_GradientSlider`

    Signals:
        :valueChanged: Signal emitted when any of the sliders/valueBoxes changes
    """

    valueChanged = QtCore.Signal(list)

    def __init__(
        self, parent=None, startColor=[0, 0, 0], type="float", alpha=False, h=50, *args
    ):
        """
        :param parent: Parent Widget
        :type parent: QtWidgets.QWidget
        :param startColor: Initialization color, defaults to [0, 0, 0]
        :type startColor: list(float/int), optional
        :param type: Choose if create a float or int Slider, defaults to "float"
        :type type: str, optional
        :param alpha: Choose if create a 4 input for the alpha channel, defaults to False
        :type alpha: bool, optional
        :param h: Maximum Widget Height, defaults to 50
        :type h: int, optional
        """
        super(pyf_ColorSlider, self).__init__(parent=parent, *args)
        self.parent = parent
        self.setLayout(QtWidgets.QHBoxLayout())
        self.type = type
        self.alpha = alpha
        self.RBox = valueBox(type=self.type)
        self.GBox = valueBox(type=self.type)
        self.BBox = valueBox(type=self.type)
        self.ABox = valueBox(type=self.type)

        for i in [self.RBox, self.GBox, self.BBox, self.ABox]:
            i.setMinimum(0)
            if type == "int":
                i.setMaximum(255)
            else:
                i.setMaximum(1.0)

        self.RSlider = pyf_GradientSlider(self, color2=[255, 0, 0])
        self.GSlider = pyf_GradientSlider(self, color2=[0, 255, 0])
        self.BSlider = pyf_GradientSlider(self, color2=[0, 0, 255])
        self.ASlider = pyf_GradientSlider(self, color2=[255, 255, 255])

        self.RBox.valueChanged.connect(lambda x: self.RSlider.setMappedValue(float(x)))
        self.RSlider.doubleValueChanged.connect(lambda x: self.RBox.setValue(x))
        self.GBox.valueChanged.connect(lambda x: self.GSlider.setMappedValue(float(x)))
        self.GSlider.doubleValueChanged.connect(lambda x: self.GBox.setValue(x))
        self.BBox.valueChanged.connect(lambda x: self.BSlider.setMappedValue(float(x)))
        self.BSlider.doubleValueChanged.connect(lambda x: self.BBox.setValue(x))
        self.ABox.valueChanged.connect(lambda x: self.ASlider.setMappedValue(float(x)))
        self.ASlider.doubleValueChanged.connect(lambda x: self.ABox.setValue(x))

        rLay = QtWidgets.QHBoxLayout()
        rLay.addWidget(self.RBox)
        rLay.addWidget(self.RSlider)
        gLay = QtWidgets.QHBoxLayout()
        gLay.addWidget(self.GBox)
        gLay.addWidget(self.GSlider)
        bLay = QtWidgets.QHBoxLayout()
        bLay.addWidget(self.BBox)
        bLay.addWidget(self.BSlider)
        aLay = QtWidgets.QHBoxLayout()
        aLay.addWidget(self.ABox)
        aLay.addWidget(self.ASlider)

        self.ASlider.setMappedValue(255)
        self.Color = QtWidgets.QPushButton()
        self.Color.clicked.connect(self.showColorDialog)

        self.Color.setMaximumWidth(h)
        self.Color.setMinimumWidth(h)
        self.Color.setMaximumHeight(h - 12)
        self.Color.setMinimumHeight(h - 12)
        self.slidersLay = QtWidgets.QVBoxLayout()
        inpList = [rLay, gLay, bLay]

        if self.alpha:
            inpList.append(aLay)
        else:
            self.ASlider.hide()

        for i in [
            self.RSlider,
            self.GSlider,
            self.BSlider,
            self.ASlider,
            self.RBox,
            self.GBox,
            self.BBox,
            self.ABox,
        ]:
            i.setMaximumHeight(h / (len(inpList) + 1))
            i.setMinimumHeight(h / (len(inpList) + 1))

        for i in [self.RSlider, self.GSlider, self.BSlider, self.ASlider]:
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
        if isinstance(startColor, list) and len(startColor) >= 3:
            self.setColor(startColor)
        self.Color.setStyleSheet(
            self.styleSheetString
            % (
                self.RSlider.mappedValue(),
                self.GSlider.mappedValue(),
                self.BSlider.mappedValue(),
                self.ASlider.mappedValue(),
            )
        )
        self._menu = QtWidgets.QMenu()
        self.actionReset = self._menu.addAction("ResetValue")
        self.actionReset.triggered.connect(self.onResetValue)

    def onResetValue(self):
        if self.defaultColor:
            self.setColor(self.defaultColor)

    def setColor(self, color):
        """Sets the current color

        :param color: Input color to use
        :type color: list(int/float)
        """
        self.RSlider.setMappedValue(color[0])
        self.GSlider.setMappedValue(color[1])
        self.BSlider.setMappedValue(color[2])
        if len(color) > 3:
            self.ASlider.setMappedValue(color[3])

    def colorChanged(self, value):
        self.Color.setStyleSheet(
            self.styleSheetString
            % (
                self.RSlider.mappedValue(),
                self.GSlider.mappedValue(),
                self.BSlider.mappedValue(),
                self.ASlider.mappedValue(),
            )
        )
        valueList = [
            self.RSlider.mappedValue(),
            self.GSlider.mappedValue(),
            self.BSlider.mappedValue(),
        ]
        if self.alpha:
            valueList.append(self.ASlider.mappedValue())
        if self.type == "int":
            valueList = [clamp(int(i), 0, 255) for i in valueList]
        self.valueChanged.emit(valueList)

    def showColorDialog(self):
        if self.alpha:
            color = QtWidgets.QColorDialog.getColor(
                options=QtWidgets.QColorDialog.ShowAlphaChannel
            )
        else:
            color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.RSlider.setMappedValue(
                mapRangeUnclamped(
                    color.redF(),
                    0.0,
                    1.0,
                    self.RSlider.sliderRange[0],
                    self.RSlider.sliderRange[1],
                )
            )
            self.GSlider.setMappedValue(
                mapRangeUnclamped(
                    color.greenF(),
                    0.0,
                    1.0,
                    self.GSlider.sliderRange[0],
                    self.GSlider.sliderRange[1],
                )
            )
            self.BSlider.setMappedValue(
                mapRangeUnclamped(
                    color.blueF(),
                    0.0,
                    1.0,
                    self.BSlider.sliderRange[0],
                    self.BSlider.sliderRange[1],
                )
            )
            self.ASlider.setMappedValue(
                mapRangeUnclamped(
                    color.alphaF(),
                    0.0,
                    1.0,
                    self.ASlider.sliderRange[0],
                    self.ASlider.sliderRange[1],
                )
            )

    def contextMenuEvent(self, event):
        self._menu.exec_(event.globalPos())


class pyf_timeline(QtWidgets.QSlider):
    def __init__(self, parent, *args):
        super(pyf_timeline, self).__init__(parent=parent, *args)
        self.parent = parent
        self.cachedFrmaes = []
        self.missingFrames = []
        self.hover = False
        self.hoverPos = None
        self.PressPos = None
        self.MovePos = None
        self.setRange(0, 30)
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
        super(pyf_timeline, self).update()

    def setRange(self, min, max, setOrig=True):
        if setOrig:
            self.origMax = max
            self.oriMin = min
        return super(pyf_timeline, self).setRange(min, max)

    def setCached(self, cached):
        self.cachedFrmaes = cached

    def setMissing(self, missing):
        self.missingFrames = missing

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
        super(pyf_timeline, self).paintEvent(event)

    def drawWidget(self, qp):
        font = QtGui.QFont("Serif", 7, QtGui.QFont.Light)
        qp.setFont(font)

        w = self.width()
        h = self.height()
        nb = self.maximum() - self.minimum()
        if nb == 0:
            return
        fStep = float(w) / nb
        step = max(1, int(round(fStep)))

        pen = QtGui.QPen(QtGui.QColor(200, 200, 200), 1, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)

        pxNb = int(round((nb + 1) * step))
        r = range(self.minimum(), self.maximum() + 1, 1)
        metrics = qp.fontMetrics()
        fh = metrics.height()
        for e, i in enumerate(range(0, pxNb, step)):
            pos = self.style().sliderPositionFromValue(
                self.minimum(), self.maximum(), r[e], self.width()
            )
            half = h / 2
            if r[e] in self.cachedFrmaes:
                qp.setPen(QtGui.QColor(0, 255, 0))
                qp.setBrush(QtGui.QColor(0, 255, 0))
                qp.drawRect(pos - (fStep / 2), half + 5, fStep, 1.5)
                qp.setPen(pen)
                qp.setBrush(QtCore.Qt.NoBrush)
            elif r[e] in self.missingFrames:
                qp.setPen(QtGui.QColor(255, 0, 0))
                qp.setBrush(QtGui.QColor(255, 0, 0))
                qp.drawRect(pos - (fStep / 2), half + 5, fStep, 1.5)
                qp.setPen(pen)
                qp.setBrush(QtCore.Qt.NoBrush)
            if (r[e] % 5) == 0:
                s = 4
                text = r[e]
                fw = metrics.horizontalAdvance(str(text))
                qp.drawText((pos) - fw / 2, h - fh / 3, str(text))
            else:
                s = 1.5
            qp.drawLine(pos, half + s, pos, half - s)
        pos = self.style().sliderPositionFromValue(
            self.minimum(), self.maximum(), self.value(), self.width()
        )
        fw = metrics.horizontalAdvance("0")
        qp.setPen(editableStyleSheet().MainColor)
        if self.value() > self.maximum() - (self.maximum() / 2):
            fw += metrics.horizontalAdvance(str(self.value()))
            fw *= -1
        qp.drawText((pos) + fw, 0 + fh, str(self.value()))
        if self.hover:
            val = self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(), self.hoverPos.x(), self.width()
            )
            if val != self.value():
                pos = self.style().sliderPositionFromValue(
                    self.minimum(), self.maximum(), val, self.width()
                )
                fw = metrics.horizontalAdvance("0")
                if val > self.maximum() - (self.maximum() / 2):
                    fw += metrics.horizontalAdvance(str(val))
                    fw *= -1
                color2 = QtGui.QColor(editableStyleSheet().MainColor)
                color2.setAlpha(100)
                pen2 = QtGui.QPen(color2, 2, QtCore.Qt.SolidLine)
                qp.setPen(pen2)
                qp.drawLine(pos, 0, pos, h)
                qp.drawText((pos) + fw, 0 + fh, str(val))
        qp.setPen(pen)

    def mousePressEvent(self, event):
        if event.modifiers() == QtCore.Qt.AltModifier:
            self.PressPos = event.globalPos()
            self.MovePos = event.globalPos()
        if (
            event.button() == QtCore.Qt.LeftButton
            and event.modifiers() != QtCore.Qt.AltModifier
        ):
            butts = QtCore.Qt.MouseButtons(QtCore.Qt.MidButton)
            nevent = QtGui.QMouseEvent(
                event.type(),
                QtCore.QPointF(event.pos()),
                QtCore.QPointF(event.globalPos()),
                QtCore.Qt.MidButton,
                butts,
                event.modifiers(),
            )
            super(pyf_timeline, self).mousePressEvent(nevent)
        elif event.modifiers() != QtCore.Qt.AltModifier:
            super(pyf_timeline, self).mousePressEvent(event)

    def wheelEvent(self, event):
        newMin = self.minimum() + (round(120 / event.delta()))
        newMax = self.maximum() - (round(120 / event.delta()))
        distance = newMax - newMin
        if distance > 0:
            self.setRange(newMin, newMax)
            self.repaint()

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.MouseMove:
            self.hover = True
            self.hoverPos = event.pos()
            self.repaint()
        elif event.type() == QtCore.QEvent.Leave:
            self.hover = False
            self.repaint()
        return super(pyf_timeline, self).eventFilter(widget, event)

    def mouseMoveEvent(self, event):
        if event.modifiers() == QtCore.Qt.AltModifier:
            if event.buttons() in [QtCore.Qt.MidButton, QtCore.Qt.LeftButton]:
                globalPos = event.globalPos()
                diff = globalPos - self.MovePos
                a = self.width() / (self.maximum() - self.minimum())
                if abs(diff.x()) > a:
                    self.MovePos = globalPos
                    newMin = self.minimum() - (1 * (diff.x() / abs(diff.x())))
                    newMax = self.maximum() - (1 * (diff.x() / abs(diff.x())))
                    self.setRange(newMin, newMax)
                    self.repaint()
        else:
            return super(pyf_timeline, self).mouseMoveEvent(event)


class uiTick(QtWidgets.QGraphicsWidget):
    """ UiElement For Ramp Widgets.

    Holds a :obj:`PyFlow.Core.structs.Tick` inside with U,V attributes and expand it to use colors in V instead of floats for use in gradient sliders """

    def __init__(self, raw_tick, parent=None):
        """
        :param raw_tick: Input Core Tick
        :type raw_tick: :obj:`PyFlow.Core.structs.Tick`
        :param parent: Parent QWidget
        :type parent: QtWidgets.QWidget, optional
        """
        super(uiTick, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self._width = 6
        self._height = 6
        self.hovered = False
        self.setFlag(QtWidgets.QGraphicsWidget.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsWidget.ItemIsFocusable)
        self.setFlag(QtWidgets.QGraphicsWidget.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsWidget.ItemSendsGeometryChanges)
        self._rawTick = raw_tick
        self._color = QtGui.QColor(0)

    def getU(self):
        """Get Current U value
        """
        return self._rawTick._u

    def getV(self):
        """Get Current V value
        """
        return self._rawTick._v

    def getColor(self):
        """Get Current Color value
        """
        r, g, b = self._rawTick._v
        return QtGui.QColor().fromRgb(r, g, b)

    def setU(self, u):
        """Sets U value

        :param u: new position
        :type u: float
        """
        self._rawTick._u = u

    def setV(self, v):
        """Sets V value

        :param v: new Y position
        :type v: object
        """
        self._rawTick._v = v

    def setColor(self, color):
        """Sets Color value

        :param color: New Color Value in 0-255 range
        :type color: [int,int,int]
        """
        try:
            r, g, b = color
        except:
            r, g, b = 0, 0, 0
        self.setV([r, g, b])
        self._color = QtGui.QColor().fromRgb(r, g, b)
        self.update()
        self.scene().update()

    def setSelected(self, selected):
        super(uiTick, self).setSelected(selected)
        self._rawTick.setSelected(selected)

    def hoverEnterEvent(self, event):
        super(uiTick, self).hoverEnterEvent(event)
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        super(uiTick, self).hoverLeaveEvent(event)
        self.hovered = False
        self.update()

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self._width, self._height)

    def paint(self, painter, option, widget):
        bgRect = self.boundingRect()
        painter.setBrush(QtGui.QColor(255, 255, 255, 150))
        pen = QtGui.QPen(QtCore.Qt.black, 1.5)
        if self.isSelected():
            pen.setColor(editableStyleSheet().MainColor)
        elif self.hovered:
            MainColor_Lighter = QtGui.QColor(editableStyleSheet().MainColor)
            MainColor_Lighter.setAlpha(128)
            pen.setColor(MainColor_Lighter)
            pen.setWidth(2.25)
        painter.setPen(pen)
        painter.drawRoundedRect(bgRect, 2, 2)


class pyf_RampSpline(QtWidgets.QGraphicsView):
    """Ui Ramp/Curve Editor that encapsulates a :obj:`PyFlow.Core.structs.splineRamp` to edit it

    Signals:
        :tickClicked: Signal emitted when a UiTick element clicked, emits UiTick
        :valueClicked: Signal emitted when a UiTick element clicked, emits (u,v)
        :tickAdded: Signal emitted when a UiTick element added
        :tickChanged: Signal emitted when a UiTick element changes values
        :tickMoved: Signal emitted when a UiTick element moved
        :tickRemoved: Signal emitted when a UiTick element deleted
    """

    tickClicked = QtCore.Signal(object)
    tickAdded = QtCore.Signal(object)
    tickChanged = QtCore.Signal(object)
    tickMoved = QtCore.Signal(object)
    tickRemoved = QtCore.Signal()
    valueClicked = QtCore.Signal(object, object)

    def __init__(self, raw_ramp, parent=None, bezier=False):
        """
        :param raw_ramp: Core ramp that will perform the interpolation
        :type raw_ramp: :obj:`PyFlow.Core.structs.splineRamp`
        :param parent: Parent QWidget
        :type parent: QtWidgets.QWidget, optional
        :param bezier: Initialize as linear or bezier, defaults to False
        :type bezier: bool, optional
        """
        super(pyf_RampSpline, self).__init__(parent)
        self._rawRamp = raw_ramp
        self.bezier = bezier
        self._scene = QtWidgets.QGraphicsScene(self)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setMaximumHeight(60)
        self.setMinimumHeight(60)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.mousePressPose = QtCore.QPointF(0, 0)
        self.mousePos = QtCore.QPointF(0, 0)
        self._lastMousePos = QtCore.QPointF(0, 0)
        self.pressed_item = None
        self.itemSize = 6
        self.displayPoints = []

        for x in self._rawRamp.sortedItems():
            self.addItem(raw_item=x)
        self.update()

    def updateFromRaw(self):
        """Updates Ui representation of the internal :obj:`PyFlow.Core.structs.splineRamp`
        """
        try:
            for item in self.items():
                self._scene.removeItem(item)
                del item
            for x in self._rawRamp.sortedItems():
                self.addItem(raw_item=x)
            self.update()
        except:
            pass

    def __getitem__(self, index):
        """
        :param index: What UiTick to get, orderer by U
        :type index: int
        :returns: Ui Tick
        :rtype: :obj:`UiTick`
        """
        if index in range(0, len(self.items())):
            return self.sortedItems()[index]
        else:
            return None

    @property
    def uValues(self):
        """Get all x positions in the curve
        :returns: List of U values
        :rtype: list(float)
        """
        return self._rawRamp.uValues

    @property
    def yValues(self):
        """Get all y positions in the curve
        :returns: List of V values
        :rtype: list(float)
        """
        return self._rawRamp.yValues

    def setBezier(self, isBezier):
        """Sets interpolation to bezier/linear

        :param isBezier: If true bezier interpolation used
        :type isBezier: bool
        """
        self.bezier = isBezier
        self.computeDisplayPoints()
        self.update()

    def sortedItems(self):
        """Returns all the :obj:`UiTick` in the ramp sorted by x position

        :returns: all :obj:`UiTick` in the ramp
        :rtype: list(:obj:`UiTick`)
        """
        itms = list(self.items())
        itms.sort(key=lambda x: x.getU())
        return itms

    def addItem(self, u=0, v=0, raw_item=None):
        """Adds a new Item to the ramp

        :param u: X position for the item, defaults to 0
        :type u: float, optional
        :param v: Y position for the item, defaults to 0
        :type v: float, optional
        :param raw_item: Existing :obj:`PyFlow.Core.structs.Tick` to link with, if none, one new created , defaults to None
        :type raw_item: :obj:`PyFlow.Core.structs.Tick`, optional
        """
        if raw_item is None:
            raw_item = self._rawRamp.addItem(u, v)
        item = uiTick(raw_item)
        item.setSelected(raw_item.isSelected())
        item._width = item._height = 6
        self._scene.addItem(item)
        self.updateItemPos(item)
        self.computeDisplayPoints()

    def setU(self, u, index=-1):
        """Sets the X position for the selected item if no index provided

        :param u: New x position
        :type u: float
        :param index: Index of the tick to set the value in, orderer by current X position, if -1 will try to set value in all selected Ticks, defaults to -1
        :type index: int, optional
        """
        if index in range(0, len(self.items()) - 1):
            item = self.sortedItems()[index]
            item.setU(u)
            self.updateItemPos(item)
            self.tickChanged.emit(item)
        elif len(self.items()) > 0:
            for item in self.items():
                if item.isSelected():
                    item.setU(u)
                    self.updateItemPos(item)
                    self.tickChanged.emit(item)
        self.computeDisplayPoints()

    def setV(self, v, index=-1):
        """Sets the Y position for the selected item if no index provided

        :param v: New y position
        :type v: float
        :param index: Index of the tick to set the value in, orderer by current X position, if -1 will try to set value in all selected Ticks, defaults to -1
        :type index: int, optional
        """
        if index in range(0, len(self.items()) - 1):
            item = self.sortedItems()[index]
            item.setV(v)
            self.updateItemPos(item)
            self.tickChanged.emit(item)
        elif len(self.items()) > 0:
            for item in self.items():
                if item.isSelected():
                    item.setV(v)
                    self.updateItemPos(item)
                    self.tickChanged.emit(item)
        self.computeDisplayPoints()

    def evaluateAt(self, value):
        """Computes the result of the interpolation for the guiven U value

        :param value: x position to evaluate at
        :type value: float
        :returns: modified value by the curve
        :rtype: float
        """
        return self._rawRamp.evaluateAt(value, self.bezier)

    def computeItemU(self, item):
        return max(
            min(item.scenePos().x() / (self.frameSize().width() - self.itemSize), 1), 0
        )

    def computeItemV(self, item):
        return max(
            min(
                1 - (item.scenePos().y() / (self.frameSize().height() - self.itemSize)),
                1,
            ),
            0,
        )

    def updateItemPos(self, item):
        item.setPos(
            item.getU() * (self.sceneRect().width() - self.itemSize),
            (1 - item.getV()) * (self.sceneRect().height() - self.itemSize),
        )

    def resizeEvent(self, event):
        super(pyf_RampSpline, self).resizeEvent(event)
        self.scene().setSceneRect(
            0, 0, self.frameSize().width(), self.frameSize().height()
        )
        self.fitInView(
            0, 0, self.scene().sceneRect().width(), 60, QtCore.Qt.IgnoreAspectRatio
        )
        for item in self.items():
            self.updateItemPos(item)
            item.update()
        self.computeDisplayPoints()

    def clearSelection(self):
        """Deselect all items
        """
        for item in self.items():
            item.setSelected(False)

    def mousePressEvent(self, event):
        self.pressed_item = self.itemAt(event.pos())
        self.mousePressPose = event.pos()
        self._lastMousePos = event.pos()
        if event.button() == QtCore.Qt.RightButton:
            if self.pressed_item:
                self._scene.removeItem(self.pressed_item)
                self._rawRamp.removeItem(self.pressed_item._rawTick)
                del self.pressed_item._rawTick
                del self.pressed_item
                self.pressed_item = None
                self.computeDisplayPoints()
                self.tickRemoved.emit()
        elif event.button() == QtCore.Qt.LeftButton and not self.pressed_item:
            raw_item = self._rawRamp.addItem(0, 0)
            item = uiTick(raw_item)
            item._width = item._height = 6
            self._scene.addItem(item)
            item.setPos(self.mapToScene(event.pos()))
            item.setU(self.computeItemU(item))
            item.setV(self.computeItemV(item))
            self.updateItemPos(item)
            self.pressed_item = item
            self.computeDisplayPoints()
            self.tickAdded.emit(item)
        self.clearSelection()
        if self.pressed_item:
            self.pressed_item.setSelected(True)
            self.tickClicked.emit(self.pressed_item)
            self.valueClicked.emit(self.pressed_item.getU(), self.pressed_item.getV())
        self.scene().update()

    def mouseMoveEvent(self, event):
        super(pyf_RampSpline, self).mouseMoveEvent(event)
        self.mousePos = event.pos()
        mouseDelta = QtCore.QPointF(self.mousePos) - self._lastMousePos
        if self.pressed_item:
            self.pressed_item.moveBy(mouseDelta.x(), mouseDelta.y())
            self.pressed_item.setU(self.computeItemU(self.pressed_item))
            self.pressed_item.setV(self.computeItemV(self.pressed_item))
            self.updateItemPos(self.pressed_item)
            self.computeDisplayPoints()
        self._lastMousePos = event.pos()
        self.tickMoved.emit(self.pressed_item)
        self.scene().update()

    def mouseReleaseEvent(self, event):
        super(pyf_RampSpline, self).mouseReleaseEvent(event)
        self.pressed_item = None
        self.scene().update()

    def getCornerPoints(self, corner=0):
        if corner == 0:
            return [
                QtCore.QPointF(
                    self.itemSize / 2, self.frameSize().height() - self.itemSize / 2
                ),
                QtCore.QPointF(
                    self.itemSize / 2,
                    self.sortedItems()[0].scenePos().y()
                    - self.mapToScene(QtCore.QPoint(-1.5, -1.5)).y(),
                ),
            ]
        else:
            return [
                QtCore.QPointF(
                    self.frameSize().width() - self.itemSize / 2,
                    self.sortedItems()[-1].scenePos().y()
                    - self.mapToScene(QtCore.QPoint(-1.5, -1.5)).y(),
                ),
                QtCore.QPointF(
                    self.frameSize().width() - self.itemSize / 2,
                    self.frameSize().height() - self.itemSize / 2,
                ),
            ]

    def computeDisplayPoints(self, nonLinearRes=50):
        items = self.sortedItems()
        points = []
        if len(items):
            for item in items:
                points.append(
                    item.scenePos() - self.mapToScene(QtCore.QPoint(-1.5, -1.5))
                )

            if self.bezier:
                bezierPoints = []
                numSteps = nonLinearRes
                for k in range(numSteps):
                    t = float(k) / (numSteps - 1)
                    x = int(
                        self._rawRamp.interpolateBezier(
                            [p.x() for p in points], 0, len(items) - 1, t
                        )
                    )
                    y = int(
                        self._rawRamp.interpolateBezier(
                            [p.y() for p in points], 0, len(items) - 1, t
                        )
                    )
                    bezierPoints.append(QtCore.QPointF(x, y))
                points = bezierPoints
            points = self.getCornerPoints(0) + points + self.getCornerPoints(1)
        self.displayPoints = points

    def drawBackground(self, painter, rect):
        painter.fillRect(
            rect.adjusted(
                self.itemSize / 2,
                self.itemSize / 2,
                -self.itemSize / 2,
                -self.itemSize / 2,
            ),
            editableStyleSheet().InputFieldColor,
        )
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.setPen(QtGui.QColor(0, 0, 0, 255))
        painter.drawRect(
            rect.adjusted(
                self.itemSize / 2,
                self.itemSize / 2,
                -self.itemSize / 2,
                -self.itemSize / 2,
            )
        )
        items = self.sortedItems()
        if len(items):
            painter.setBrush(QtGui.QColor(100, 100, 100))
            painter.drawPolygon(self.displayPoints, QtCore.Qt.WindingFill)
        # else:
        #     b = editableStyleSheet().InputFieldColor


class pyf_RampColor(pyf_RampSpline):
    """Similar to the :obj:`pyf_RampSpline` to create editable gradients with interpolation support

    Signals:
        :tickClicked: Signal emitted when a UiTick element clicked, emits UiTick
        :valueClicked: Signal emitted when a UiTick element clicked, emits (u,v)
        :colorClicked: Signal emitted when a UiTick element clicked. emits [float,float,float] in range 0-1
        :tickAdded: Signal emitted when a UiTick element added
        :tickChanged: Signal emitted when a UiTick element changes values
        :tickMoved: Signal emitted when a UiTick element moved
        :tickRemoved: Signal emitted when a UiTick element deleted

    Extends:
        :obj: `pyf_RampSpline`
    """

    colorClicked = QtCore.Signal(list)

    def __init__(self, raw_ramp, parent=None, bezier=True):
        super(pyf_RampColor, self).__init__(raw_ramp, parent, bezier)
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        self.itemSize = 10

    @property
    def values(self):
        """Get all colors in the curve
        :returns: List of color values in range 0-1
        :rtype: list([float,float,float])
        """
        return [x.getColor().getRgbF() for x in self.sortedItems()]

    def addItem(self, u=0, v=[0, 0, 0], raw_item=None):
        """Adds a new Item to the ramp

        :param u: X position for the item, defaults to 0
        :type u: float, optional
        :param v: color value for the item, defaults to [0,0,0]
        :type v: [float,float,float], optional
        :param raw_item: Existing :obj:`PyFlow.Core.structs.Tick` to link with, if none, one new created , defaults to None
        :type raw_item: :obj:`PyFlow.Core.structs.Tick`, optional
        """
        if raw_item is None:
            raw_item = self._rawRamp.addItem(u, v)
        item = uiTick(raw_item)
        item.setSelected(raw_item.isSelected())
        item._width = 10
        item._height = 17
        r, g, b = v
        item._color = QtGui.QColor.fromRgb(r, g, b)
        self._scene.addItem(item)
        self.updateItemPos(item)

    def setColor(self, color, index=-1):
        """Sets the color value for the selected item if no index provided

        :param color: New color
        :type color: [float,float,float]
        :param index: Index of the tick to set the value in, orderer by current X position, if -1 will try to set value in all selected Ticks, defaults to -1
        :type index: int, optional
        """
        if index in range(0, len(self.items()) - 1):
            self.sortedItems()[index].setColor(color)
        elif len(self.items()) > 0:
            for item in self.items():
                if item.isSelected():
                    item.setColor(color)
                    self.tickChanged.emit(item)

    def computeItemU(self, item):
        return max(min(item.scenePos().x() / (self.frameSize().width() - 10), 1), 0)

    def updateItemPos(self, item):
        item.setPos(item.getU() * (self.sceneRect().width() - 10), 1)

    def resizeEvent(self, event):
        super(pyf_RampColor, self).resizeEvent(event)
        self.scene().setSceneRect(
            0, 0, self.frameSize().width(), self.frameSize().height()
        )
        self.fitInView(
            0, 0, self.scene().sceneRect().width(), 15, QtCore.Qt.IgnoreAspectRatio
        )
        for item in self.items():
            self.updateItemPos(item)
            item.update()

    def mousePressEvent(self, event):
        self.pressed_item = self.itemAt(event.pos())
        self.mousePressPose = event.pos()
        self._lastMousePos = event.pos()
        if event.button() == QtCore.Qt.RightButton:
            if self.pressed_item:
                self._scene.removeItem(self.pressed_item)
                self._rawRamp.removeItem(self.pressed_item._rawTick)
                del self.pressed_item._rawTick
                del self.pressed_item
                self.pressed_item = None
                self.tickRemoved.emit()
        else:
            if not self.pressed_item:
                color = self.evaluateAt(
                    self.mapToScene(event.pos()).x() / self.frameSize().width()
                )
                raw_item = self._rawRamp.addItem(0, color)
                item = uiTick(raw_item)
                item._width = 10
                item._height = 17
                self._scene.addItem(item)
                item.setColor(color)
                item.setPos(self.mapToScene(event.pos()).x(), 1)
                item.setU(self.computeItemU(item))
                self.updateItemPos(item)
                self.pressed_item = item
                self.tickAdded.emit(item)
        self.clearSelection()
        if self.pressed_item:
            self.pressed_item.setSelected(True)
            self.tickClicked.emit(self.pressed_item)
            self.colorClicked.emit(
                [(x + 0.5) for x in self.pressed_item.getColor().getRgb()]
            )
            self.valueClicked.emit(self.pressed_item.getU(), self.pressed_item.getV())
        self.scene().update()

    def mouseMoveEvent(self, event):
        QtWidgets.QGraphicsView.mouseMoveEvent(self, event)
        self.mousePos = event.pos()
        mouseDelta = QtCore.QPointF(self.mousePos) - self._lastMousePos
        if self.pressed_item:
            self.pressed_item.moveBy(mouseDelta.x(), 0)
            self.pressed_item.setU(self.computeItemU(self.pressed_item))
            self.updateItemPos(self.pressed_item)
        self._lastMousePos = event.pos()
        self.scene().update()
        self.tickMoved.emit(self.pressed_item)

    def drawBackground(self, painter, rect):
        super(pyf_RampColor, self).drawBackground(painter, rect)
        if len(self.items()):
            b = QtGui.QLinearGradient(0, 0, rect.width(), 0)
            if not self.bezier:
                for item in self.items():
                    b.setColorAt(item.getU(), item.getColor())
            else:
                items = self.sortedItems()
                numSteps = 50
                for k in range(numSteps):
                    t = float(k) / (numSteps - 1)
                    color = []
                    for i in range(len(items[0].getV())):
                        color.append(
                            self._rawRamp.interpolateBezier(
                                [p.getV()[i] for p in items], 0, len(items) - 1, t
                            )
                        )
                    x = self._rawRamp.interpolateBezier(
                        [p.getU() for p in items], 0, len(items) - 1, t
                    )
                    b.setColorAt(
                        x, QtGui.QColor().fromRgb(color[0], color[1], color[2])
                    )
        else:
            b = editableStyleSheet().InputFieldColor
        painter.fillRect(rect, b)


class testWidg(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(testWidg, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(pyf_Slider(self, style=0))
        self.layout().addWidget(pyf_Slider(self, type="int", style=1))
        self.layout().addWidget(pyf_HueSlider(self))
        self.layout().addWidget(pyf_GradientSlider(self))
        self.layout().addWidget(valueBox(type="int"))
        self.layout().addWidget(valueBox(type="float", buttons=True))
        tim = pyf_timeline(self)
        tim.setCached([0, 1, 2, 3, 4, 15, 20])
        self.layout().addWidget(tim)
        color = pyf_ColorSlider(self, type="int")
        raw_ramp = structs.splineRamp()
        raw_ramp.addItem(0.1, [10, 50, 90])
        raw_ramp.addItem(0.9, [30, 120, 90])
        ramp = pyf_RampColor(raw_ramp, self)
        color.valueChanged.connect(ramp.setColor)
        ramp.colorClicked.connect(color.setColor)
        self.layout().addWidget(ramp)
        self.layout().addWidget(color)
        raw_ramp = structs.splineRamp()
        raw_ramp.addItem(0.0, 0.0)
        raw_ramp.addItem(1.0, 1.0)
        ramp2 = pyf_RampSpline(raw_ramp, self)

        self.layout().addWidget(ramp2)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("plastique"))
    app.setStyleSheet(editableStyleSheet().getStyleSheet())
    ex = testWidg()
    ex.show()
    sys.exit(app.exec_())
