from PySide import QtCore, QtGui

from colors import Colors
from demoitem import DemoItem
from demoitemanimation import DemoItemAnimation
from demotextitem import DemoTextItem
from scanitem import ScanItem


class ButtonBackground(DemoItem):
    def __init__(self, type, highlighted, pressed, logicalSize, scene, parent):
        super(ButtonBackground, self).__init__(scene, parent)

        self.type = type
        self.highlighted = highlighted
        self.pressed = pressed
        self.logicalSize = logicalSize
        self.useSharedImage('%s%d%d%d' % (__file__, type, highlighted, pressed))

    def createImage(self, matrix):
        if self.type in (TextButton.SIDEBAR, TextButton.PANEL):
            return self.createRoundButtonBackground(matrix)
        else:
            return self.createArrowBackground(matrix)

    def createRoundButtonBackground(self, matrix):
        scaledRect = matrix.mapRect(QtCore.QRect(0, 0,
                self.logicalSize.width(), self.logicalSize.height()))

        image = QtGui.QImage(scaledRect.width(), scaledRect.height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.QColor(0, 0, 0, 0).rgba())
        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        if Colors.useEightBitPalette:
            painter.setPen(QtGui.QColor(120, 120, 120))
            if self.pressed:
                painter.setBrush(QtGui.QColor(60, 60, 60))
            elif self.highlighted:
                painter.setBrush(QtGui.QColor(100, 100, 100))
            else:
                painter.setBrush(QtGui.QColor(80, 80, 80))
        else:
            outlinebrush = QtGui.QLinearGradient(0, 0, 0, scaledRect.height())
            brush = QtGui.QLinearGradient(0, 0, 0, scaledRect.height())

            brush.setSpread(QtGui.QLinearGradient.PadSpread)
            highlight = QtGui.QColor(255, 255, 255, 70)
            shadow = QtGui.QColor(0, 0, 0, 70)
            sunken = QtGui.QColor(220, 220, 220, 30)

            if self.type == TextButton.PANEL:
                normal1 = QtGui.QColor(200, 170, 160, 50)
                normal2 = QtGui.QColor(50, 10, 0, 50)
            else:
                normal1 = QtGui.QColor(255, 255, 245, 60)
                normal2 = QtGui.QColor(255, 255, 235, 10)

            if self.pressed:
                outlinebrush.setColorAt(0, shadow)
                outlinebrush.setColorAt(1, highlight)
                brush.setColorAt(0, sunken)
                painter.setPen(QtCore.Qt.NoPen)
            else:
                outlinebrush.setColorAt(1, shadow)
                outlinebrush.setColorAt(0, highlight)
                brush.setColorAt(0, normal1)
                if not self.highlighted:
                    brush.setColorAt(1, normal2)
                painter.setPen(QtGui.QPen(outlinebrush, 1))

            painter.setBrush(brush)

        if self.type == TextButton.PANEL:
            painter.drawRect(0, 0, scaledRect.width(), scaledRect.height())
        else:
            painter.drawRoundedRect(0, 0, scaledRect.width(),
                    scaledRect.height(), 10, 90, QtCore.Qt.RelativeSize)

        return image

    def createArrowBackground(self, matrix):
        scaledRect = matrix.mapRect(QtCore.QRect(0, 0,
                self.logicalSize.width(), self.logicalSize.height()))

        image = QtGui.QImage(scaledRect.width(), scaledRect.height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.QColor(0, 0, 0, 0).rgba())
        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        if Colors.useEightBitPalette:
            painter.setPen(QtGui.QColor(120, 120, 120))
            if self.pressed:
                painter.setBrush(QtGui.QColor(60, 60, 60))
            elif self.highlighted:
                painter.setBrush(QtGui.QColor(100, 100, 100))
            else:
                painter.setBrush(QtGui.QColor(80, 80, 80))
        else:
            outlinebrush = QtGui.QLinearGradient(0, 0, 0, scaledRect.height())
            brush = QtGui.QLinearGradient(0, 0, 0, scaledRect.height())

            brush.setSpread(QtGui.QLinearGradient.PadSpread)
            highlight = QtGui.QColor(255, 255, 255, 70)
            shadow = QtGui.QColor(0, 0, 0, 70)
            sunken = QtGui.QColor(220, 220, 220, 30)
            normal1 = QtGui.QColor(200, 170, 160, 50)
            normal2 = QtGui.QColor(50, 10, 0, 50)

            if self.pressed:
                outlinebrush.setColorAt(0, shadow)
                outlinebrush.setColorAt(1, highlight)
                brush.setColorAt(0, sunken)
                painter.setPen(QtCore.Qt.NoPen)
            else:
                outlinebrush.setColorAt(1, shadow)
                outlinebrush.setColorAt(0, highlight)
                brush.setColorAt(0, normal1)
                if not self.highlighted:
                    brush.setColorAt(1, normal2)
                painter.setPen(QtGui.QPen(outlinebrush, 1))

            painter.setBrush(brush);

        painter.drawRect(0, 0, scaledRect.width(), scaledRect.height())

        xOff = scaledRect.width() / 2
        yOff = scaledRect.height() / 2
        sizex = 3.0 * matrix.m11()
        sizey = 1.5 * matrix.m22()
        if self.type == TextButton.UP:
            sizey *= -1
        path = QtGui.QPainterPath()
        path.moveTo(xOff, yOff + (5 * sizey))
        path.lineTo(xOff - (4 * sizex), yOff - (3 * sizey))
        path.lineTo(xOff + (4 * sizex), yOff - (3 * sizey))
        path.lineTo(xOff, yOff + (5 * sizey))
        painter.drawPath(path)

        return image


class TextButton(DemoItem):
    BUTTON_WIDTH = 180
    BUTTON_HEIGHT = 19

    LEFT, RIGHT = range(2)

    SIDEBAR, PANEL, UP, DOWN = range(4)

    ON, OFF, HIGHLIGHT, DISABLED = range(4)

    def __init__(self, text, align=LEFT, userCode=0, scene=None, parent=None, type=SIDEBAR):
        super(TextButton, self).__init__(scene, parent)

        # Prevent a circular import.
        from menumanager import MenuManager
        self._menu_manager = MenuManager.instance()

        self.menuString = text
        self.buttonLabel = text
        self.alignment = align
        self.buttonType = type
        self.userCode = userCode
        self.scanAnim = None
        self.bgOn = None
        self.bgOff = None
        self.bgHighlight = None
        self.bgDisabled = None
        self.state = TextButton.OFF

        self.setAcceptsHoverEvents(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        # Calculate the button size.
        if type in (TextButton.SIDEBAR, TextButton.PANEL):
            self.logicalSize = QtCore.QSize(TextButton.BUTTON_WIDTH, TextButton.BUTTON_HEIGHT)
        else:
            self.logicalSize = QtCore.QSize(int((TextButton.BUTTON_WIDTH / 2.0) - 5), int(TextButton.BUTTON_HEIGHT * 1.5))

    def setMenuString(self, menu):
        self.menuString = menu

    def prepare(self):
        if not self.prepared:
            self.prepared = True
            self.setupHoverText()
            self.setupScanItem()
            self.setupButtonBg()

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.logicalSize.width(),
                self.logicalSize.height())

    def setupHoverText(self):
        if not self.buttonLabel:
            return

        textItem = DemoTextItem(self.buttonLabel, Colors.buttonFont(),
                Colors.buttonText, -1, self.scene(), self)
        textItem.setZValue(self.zValue() + 2)
        textItem.setPos(16, 0)

    def setupScanItem(self):
        if Colors.useButtonBalls:
            scanItem = ScanItem(None, self)
            scanItem.setZValue(self.zValue() + 1)

            self.scanAnim = DemoItemAnimation(scanItem)
            self.scanAnim.timeline.setLoopCount(1)

            x = 1.0
            y = 1.5
            stop = TextButton.BUTTON_WIDTH - scanItem.boundingRect().width() - x
            if self.alignment == TextButton.LEFT:
                self.scanAnim.setDuration(2500)
                self.scanAnim.setPosAt(0.0, QtCore.QPointF(x, y))
                self.scanAnim.setPosAt(0.5, QtCore.QPointF(x, y))
                self.scanAnim.setPosAt(0.7, QtCore.QPointF(stop, y))
                self.scanAnim.setPosAt(1.0, QtCore.QPointF(x, y))
                scanItem.setPos(QtCore.QPointF(x, y))
            else:
                self.scanAnim.setPosAt(0.0, QtCore.QPointF(stop, y))
                self.scanAnim.setPosAt(0.5, QtCore.QPointF(x, y))
                self.scanAnim.setPosAt(1.0, QtCore.QPointF(stop, y))
                scanItem.setPos(QtCore.QPointF(stop, y))

    def setState(self, state):
        self.state = state
        self.bgOn.setRecursiveVisible(state == TextButton.ON)
        self.bgOff.setRecursiveVisible(state == TextButton.OFF)
        self.bgHighlight.setRecursiveVisible(state == TextButton.HIGHLIGHT)
        self.bgDisabled.setRecursiveVisible(state == TextButton.DISABLED)
        if state == TextButton.DISABLED:
            self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            self.setCursor(QtCore.Qt.PointingHandCursor)

    def setupButtonBg(self):
        self.bgOn = ButtonBackground(self.buttonType, True, True,
                self.logicalSize, self.scene(), self)
        self.bgOff = ButtonBackground(self.buttonType, False, False,
                self.logicalSize, self.scene(), self)
        self.bgHighlight = ButtonBackground(self.buttonType, True, False,
                self.logicalSize, self.scene(), self)
        self.bgDisabled = ButtonBackground(self.buttonType, True, True,
                self.logicalSize, self.scene(), self)
        self.setState(TextButton.OFF)

    def hoverEnterEvent(self, event):
        if self.locked or self.state == TextButton.DISABLED:
            return

        if self.state == TextButton.OFF:
            self.setState(TextButton.HIGHLIGHT)

            if Colors.noAnimations and Colors.useButtonBalls:
                # Wait a bit in the beginning to enhance the effect.  We have
                # to do this here so that the adaption can be dynamic.
                self.scanAnim.setDuration(1000)
                self.scanAnim.setPosAt(0.2, self.scanAnim.posAt(0))

            if (self._menu_manager.window.fpsMedian > 10 or Colors.noAdapt or
                    Colors.noTimerUpdate):
                if Colors.useButtonBalls:
                    self.scanAnim.play(True, True)

    def hoverLeaveEvent(self, event):
        if self.state == TextButton.DISABLED:
            return

        self.setState(TextButton.OFF)

        if Colors.noAnimations and Colors.useButtonBalls:
            self.scanAnim.stop()

    def mousePressEvent(self, event):
        if self.state == TextButton.DISABLED:
            return

        if self.state == TextButton.HIGHLIGHT or self.state == TextButton.OFF:
            self.setState(TextButton.ON)

    def mouseReleaseEvent(self, event):
        if self.state == TextButton.ON:
            self.setState(TextButton.OFF)
            if not self.locked and self.boundingRect().contains(event.pos()):
                self._menu_manager.itemSelected(self.userCode, self.menuString)

    def animationStarted(self, _):
        if self.state == TextButton.DISABLED:
            return

        self.setState(TextButton.OFF)
