#!/usr/bin/env python

from PySide import QtCore, QtGui

import easing_rc
from ui_form import Ui_Form


class Animation(QtCore.QPropertyAnimation):
    LinearPath, CirclePath = range(2)

    def __init__(self, target, prop):
        super(Animation, self).__init__(target, prop)
        self.setPathType(Animation.LinearPath)

    def setPathType(self, pathType):
        self.m_pathType = pathType
        self.m_path = QtGui.QPainterPath()

    def updateCurrentTime(self, currentTime):
        if self.m_pathType == Animation.CirclePath:
            if self.m_path.isEmpty():
                end = self.endValue()
                start = self.startValue()
                self.m_path.moveTo(start)
                self.m_path.addEllipse(QtCore.QRectF(start, end))

            dura = self.duration()
            if dura == 0:
                progress = 1.0
            else:
                progress = (((currentTime - 1) % dura) + 1) / float(dura)

            easedProgress = self.easingCurve().valueForProgress(progress)
            if easedProgress > 1.0:
                easedProgress -= 1.0
            elif easedProgress < 0:
                easedProgress += 1.0

            pt = self.m_path.pointAtPercent(easedProgress)
            self.updateCurrentValue(pt)
            self.valueChanged.emit(pt)
        else:
            super(Animation, self).updateCurrentTime(currentTime)

# PyQt doesn't support deriving from more than one wrapped class so we use
# composition and delegate the property.
class Pixmap(QtCore.QObject):
    def __init__(self, pix):
        super(Pixmap, self).__init__()

        self.pixmap_item = QtGui.QGraphicsPixmapItem(pix)
        self.pixmap_item.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)

    def set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    def get_pos(self):
        return self.pixmap_item.pos()

    pos = QtCore.Property(QtCore.QPointF, get_pos, set_pos)
    

class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.m_iconSize = QtCore.QSize(64, 64)
        self.m_scene = QtGui.QGraphicsScene()
        
        m_ui = Ui_Form()
        m_ui.setupUi(self)
        m_ui.easingCurvePicker.setIconSize(self.m_iconSize)
        m_ui.easingCurvePicker.setMinimumHeight(self.m_iconSize.height() + 50)
        m_ui.buttonGroup.setId(m_ui.lineRadio, 0)
        m_ui.buttonGroup.setId(m_ui.circleRadio, 1)

        dummy = QtCore.QEasingCurve()
        m_ui.periodSpinBox.setValue(dummy.period())
        m_ui.amplitudeSpinBox.setValue(dummy.amplitude())
        m_ui.overshootSpinBox.setValue(dummy.overshoot())

        m_ui.easingCurvePicker.currentRowChanged.connect(self.curveChanged)
        m_ui.buttonGroup.buttonClicked[int].connect(self.pathChanged)
        m_ui.periodSpinBox.valueChanged.connect(self.periodChanged)
        m_ui.amplitudeSpinBox.valueChanged.connect(self.amplitudeChanged)
        m_ui.overshootSpinBox.valueChanged.connect(self.overshootChanged)
        
        self.m_ui = m_ui
        self.createCurveIcons()

        pix = QtGui.QPixmap(':/images/qt-logo.png')
        self.m_item = Pixmap(pix)
        self.m_scene.addItem(self.m_item.pixmap_item)
        self.m_ui.graphicsView.setScene(self.m_scene)

        self.m_anim = Animation(self.m_item, 'pos')
        self.m_anim.setEasingCurve(QtCore.QEasingCurve.OutBounce)
        self.m_ui.easingCurvePicker.setCurrentRow(int(QtCore.QEasingCurve.OutBounce))        
        
        self.startAnimation()

    def createCurveIcons(self):
        pix = QtGui.QPixmap(self.m_iconSize)
        painter = QtGui.QPainter()

        gradient = QtGui.QLinearGradient(0, 0, 0, self.m_iconSize.height())
        gradient.setColorAt(0.0, QtGui.QColor(240, 240, 240))
        gradient.setColorAt(1.0, QtGui.QColor(224, 224, 224))

        brush = QtGui.QBrush(gradient)

        # The original C++ code uses undocumented calls to get the names of the
        # different curve types.  We do the Python equivalant (but without
        # cheating)
        curve_types = [(n, c) for n, c in QtCore.QEasingCurve.__dict__.items()
                        if isinstance(c, QtCore.QEasingCurve.Type) \
                            and c != QtCore.QEasingCurve.Custom    \
                            and c != QtCore.QEasingCurve.NCurveTypes]
        curve_types.sort(key=lambda ct: ct[1])
        
        painter.begin(pix)

        for curve_name, curve_type in curve_types:
            painter.fillRect(QtCore.QRect(QtCore.QPoint(0, 0), self.m_iconSize), brush)
            curve = QtCore.QEasingCurve(curve_type)

            painter.setPen(QtGui.QColor(0, 0, 255, 64))
            xAxis = self.m_iconSize.height() / 1.5
            yAxis = self.m_iconSize.width() / 3.0
            painter.drawLine(0, xAxis, self.m_iconSize.width(),  xAxis)
            painter.drawLine(yAxis, 0, yAxis, self.m_iconSize.height())

            curveScale = self.m_iconSize.height() / 2.0;

            painter.setPen(QtCore.Qt.NoPen)

            # Start point.
            painter.setBrush(QtCore.Qt.red)
            start = QtCore.QPoint(yAxis,
                    xAxis - curveScale * curve.valueForProgress(0))
            painter.drawRect(start.x() - 1, start.y() - 1, 3, 3)

            # End point.
            painter.setBrush(QtCore.Qt.blue)
            end = QtCore.QPoint(yAxis + curveScale,
                    xAxis - curveScale * curve.valueForProgress(1))
            painter.drawRect(end.x() - 1, end.y() - 1, 3, 3)

            curvePath = QtGui.QPainterPath()
            curvePath.moveTo(QtCore.QPointF(start))
            t = 0.0
            while t <= 1.0:
                to = QtCore.QPointF(yAxis + curveScale * t,
                        xAxis - curveScale * curve.valueForProgress(t))
                curvePath.lineTo(to)
                t += 1.0 / curveScale

            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.strokePath(curvePath, QtGui.QColor(32, 32, 32))
            painter.setRenderHint(QtGui.QPainter.Antialiasing, False)

            item = QtGui.QListWidgetItem()
            item.setIcon(QtGui.QIcon(pix))
            item.setText(curve_name)
            self.m_ui.easingCurvePicker.addItem(item)

        painter.end()

    def startAnimation(self):
        self.m_anim.setStartValue(QtCore.QPointF(0, 0))
        self.m_anim.setEndValue(QtCore.QPointF(100, 100))
        self.m_anim.setDuration(2000)
        self.m_anim.setLoopCount(-1)
        self.m_anim.start()

    def curveChanged(self, row):
        curveType = QtCore.QEasingCurve.Type(row)
        self.m_anim.setEasingCurve(curveType)
        self.m_anim.setCurrentTime(0)

        isElastic = (curveType >= QtCore.QEasingCurve.InElastic
                    and curveType <= QtCore.QEasingCurve.OutInElastic)
        isBounce = (curveType >= QtCore.QEasingCurve.InBounce
                    and curveType <= QtCore.QEasingCurve.OutInBounce)

        self.m_ui.periodSpinBox.setEnabled(isElastic)
        self.m_ui.amplitudeSpinBox.setEnabled(isElastic or isBounce)
        self.m_ui.overshootSpinBox.setEnabled(curveType >= QtCore.QEasingCurve.InBack
                                          and curveType <= QtCore.QEasingCurve.OutInBack)

    def pathChanged(self, index):
        self.m_anim.setPathType(index)

    def periodChanged(self, value):
        curve = self.m_anim.easingCurve()
        curve.setPeriod(value)
        self.m_anim.setEasingCurve(curve)

    def amplitudeChanged(self, value):
        curve = self.m_anim.easingCurve()
        curve.setAmplitude(value)
        self.m_anim.setEasingCurve(curve)

    def overshootChanged(self, value):
        curve = self.m_anim.easingCurve()
        curve.setOvershoot(value)
        self.m_anim.setEasingCurve(curve)


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.resize(600, 600)
    w.show()
    sys.exit(app.exec_())
