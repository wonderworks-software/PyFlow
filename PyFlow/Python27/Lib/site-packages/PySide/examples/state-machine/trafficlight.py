#!/usr/bin/env python
#Author velociraptor Genjix <aphidia@hotmail.com>

from PySide.QtGui import *
from PySide.QtCore import *

class LightWidget(QWidget):
    def __init__(self, colour):
        super(LightWidget, self).__init__()
        self.colour = colour
        self.onVal = False
    def isOn(self):
        return self.onVal
    def setOn(self, on):
        if self.onVal == on:
            return
        self.onVal = on
        self.update()
    @Slot()
    def turnOff(self):
        self.setOn(False)
    @Slot()
    def turnOn(self):
        self.setOn(True)
    def paintEvent(self, e):
        if not self.onVal:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.colour)
        painter.drawEllipse(0, 0, self.width(), self.height())

    on = Property(bool, isOn, setOn)

class TrafficLightWidget(QWidget):
    def __init__(self):
        super(TrafficLightWidget, self).__init__()
        vbox = QVBoxLayout(self)
        self.redLight = LightWidget(Qt.red)
        vbox.addWidget(self.redLight)
        self.yellowLight = LightWidget(Qt.yellow)
        vbox.addWidget(self.yellowLight)
        self.greenLight = LightWidget(Qt.green)
        vbox.addWidget(self.greenLight)
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.black)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

def createLightState(light, duration, parent=None):
    lightState = QState(parent)
    timer = QTimer(lightState)
    timer.setInterval(duration)
    timer.setSingleShot(True)
    timing = QState(lightState)
    timing.entered.connect(light.turnOn)
    timing.entered.connect(timer.start)
    timing.exited.connect(light.turnOff)
    done = QFinalState(lightState)
    timing.addTransition(timer, SIGNAL('timeout()'), done)
    lightState.setInitialState(timing)
    return lightState

class TrafficLight(QWidget):
    def __init__(self):
        super(TrafficLight, self).__init__()
        vbox = QVBoxLayout(self)
        widget = TrafficLightWidget()
        vbox.addWidget(widget)
        vbox.setContentsMargins(0, 0, 0, 0)

        machine = QStateMachine(self)
        redGoingYellow = createLightState(widget.redLight, 1000)
        redGoingYellow.setObjectName('redGoingYellow')
        yellowGoingGreen = createLightState(widget.redLight, 1000)
        yellowGoingGreen.setObjectName('redGoingYellow')
        redGoingYellow.addTransition(redGoingYellow, SIGNAL('finished()'), yellowGoingGreen)
        greenGoingYellow = createLightState(widget.yellowLight, 3000)
        greenGoingYellow.setObjectName('redGoingYellow')
        yellowGoingGreen.addTransition(yellowGoingGreen, SIGNAL('finished()'), greenGoingYellow)
        yellowGoingRed = createLightState(widget.greenLight, 1000)
        yellowGoingRed.setObjectName('redGoingYellow')
        greenGoingYellow.addTransition(greenGoingYellow, SIGNAL('finished()'), yellowGoingRed)
        yellowGoingRed.addTransition(yellowGoingRed, SIGNAL('finished()'), redGoingYellow)

        machine.addState(redGoingYellow)
        machine.addState(yellowGoingGreen)
        machine.addState(greenGoingYellow)
        machine.addState(yellowGoingRed)
        machine.setInitialState(redGoingYellow)
        machine.start()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = TrafficLight()
    widget.resize(110, 300)
    widget.show()
    sys.exit(app.exec_())
