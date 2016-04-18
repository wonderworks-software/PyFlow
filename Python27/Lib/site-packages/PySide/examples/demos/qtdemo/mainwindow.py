from PySide import QtCore, QtGui

from colors import Colors
from demoitem import DemoItem
from demoscene import DemoScene
from demotextitem import DemoTextItem
from imageitem import ImageItem
from menumanager import MenuManager


class MainWindow(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.updateTimer = QtCore.QTimer(self)
        self.demoStartTime = QtCore.QTime()
        self.fpsTime = QtCore.QTime()
        self.background = QtGui.QPixmap()

        self.scene = None
        self.frameTimeList = []
        self.fpsHistory = []

        self.currentFps = Colors.fps
        self.loop = False
        self.fpsMedian = -1
        self.fpsLabel = None
        self.pausedLabel = None
        self.doneAdapt = False
        self.useTimer = False
        self.updateTimer.setSingleShot(True)
        self.trolltechLogo = None
        self.qtLogo = None

        self.setupWidget()
        self.setupScene()
        self.setupSceneItems()
        self.drawBackgroundToPixmap()

    def setupWidget(self):
        desktop = QtGui.QApplication.desktop()
        screenRect = desktop.screenGeometry(desktop.primaryScreen())
        windowRect = QtCore.QRect(0, 0, 800, 600)

        if screenRect.width() < 800:
            windowRect.setWidth(screenRect.width())

        if screenRect.height() < 600:
            windowRect.setHeight(screenRect.height())

        windowRect.moveCenter(screenRect.center())
        self.setGeometry(windowRect)
        self.setMinimumSize(80, 60)

        self.setWindowTitle("PyQt Examples and Demos")
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setRenderingSystem()
        self.updateTimer.timeout.connect(self.tick)

    def setRenderingSystem(self):
        if Colors.direct3dRendering:
            viewport.setAttribute(QtCore.Qt.WA_MSWindowsUseDirect3D)
            self.setCacheMode(QtGui.QGraphicsView.CacheNone)
            Colors.debug("- using Direct3D")
        elif Colors.openGlRendering:
            from PySide import QtOpenGL

            viewport = QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))

            if Colors.noScreenSync:
                viewport.format().setSwapInterval(0)

            viewport.setAutoFillBackground(False)
            self.setCacheMode(QtGui.QGraphicsView.CacheNone)
            Colors.debug("- using OpenGL")
        else:
            viewport = QtGui.QWidget()
            self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
            Colors.debug("- using software rendering")

        self.setViewport(viewport)

    def start(self):
        self.switchTimerOnOff(True)
        self.demoStartTime.restart()
        MenuManager.instance().itemSelected(MenuManager.ROOT,
                Colors.rootMenuName)
        Colors.debug("- starting demo")

    def enableMask(self, enable):
        if not enable or Colors.noWindowMask:
            self.clearMask()
        else:
            region = QtGui.QPolygon([
                    # North side.
                    0, 0,
                    800, 0,
                    # East side.
                    # 800, 70,
                    # 790, 90,
                    # 790, 480,
                    # 800, 500,
                    800, 600,
                    # South side.
                    700, 600,
                    670, 590,
                    130, 590,
                    100, 600,
                    0, 600,
                    # West side.
                    # 0, 550,
                    # 10, 530,
                    # 10, 520,
                    # 0, 520,
                    0, 0])

            self.setMask(QtCore.QRegion(region))

    def setupScene(self):
        self.scene = DemoScene(self)
        self.scene.setSceneRect(0, 0, 800, 600)
        self.setScene(self.scene)
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

    def switchTimerOnOff(self, on):
        ticker = MenuManager.instance().ticker
        if ticker and ticker.scene():
            ticker.tickOnPaint = not on or Colors.noTimerUpdate

        if on and not Colors.noTimerUpdate:
            self.useTimer = True
            self.fpsTime = QtCore.QTime.currentTime()
            self.updateTimer.start(int(1000 / Colors.fps))
            update_mode = QtGui.QGraphicsView.NoViewportUpdate
        else:
            self.useTimer = False
            self.updateTimer.stop()

            if Colors.softwareRendering:
                if Colors.noTicker:
                    update_mode = QtGui.QGraphicsView.MinimalViewportUpdate
                else:
                    update_mode = QtGui.QGraphicsView.SmartViewportUpdate
            else:
                update_mode = QtGui.QGraphicsView.FullViewportUpdate

        self.setViewportUpdateMode(update_mode)

    def measureFps(self):
        # Calculate time difference.
        t = self.fpsTime.msecsTo(QtCore.QTime.currentTime())
        if t == 0:
            t = 0.01

        self.currentFps = (1000.0 / t)
        self.fpsHistory.append(self.currentFps)
        self.fpsTime = QtCore.QTime.currentTime()

        # Calculate median.
        size = len(self.fpsHistory)

        if size == 10:
            self.fpsHistory.sort()
            self.fpsMedian = self.fpsHistory[int(size / 2)]
            if self.fpsMedian == 0:
                self.fpsMedian = 0.01

            self.fpsHistory = []

            return True

        return False

    def forceFpsMedianCalculation(self):
        # Used for adaption in case things are so slow that no median has yet
        # been calculated.
        if self.fpsMedian != -1:
            return

        size = len(self.fpsHistory)

        if size == 0:
            self.fpsMedian = 0.01
            return

        self.fpsHistory.sort()
        self.fpsMedian = self.fpsHistory[size // 2]
        if self.fpsMedian == 0:
            self.fpsMedian = 0.01

    def tick(self):
        medianChanged = self.measureFps()
        self.checkAdapt()

        if medianChanged and self.fpsLabel and Colors.showFps:
            self.fpsLabel.setText("FPS: %d" % int(self.currentFps))

        if MenuManager.instance().ticker:
            MenuManager.instance().ticker.tick()

        self.viewport().update()
        if Colors.softwareRendering:
            QtGui.QApplication.syncX()

        if self.useTimer:
            self.updateTimer.start(int(1000 / Colors.fps))

    def setupSceneItems(self):
        if Colors.showFps:
            self.fpsLabel = DemoTextItem("FPS: --", Colors.buttonFont(),
                    QtCore.Qt.white, -1, self.scene, None,
                    DemoTextItem.DYNAMIC_TEXT)
            self.fpsLabel.setZValue(100)
            self.fpsLabel.setPos(Colors.stageStartX,
                    600 - QtGui.QFontMetricsF(Colors.buttonFont()).height() - 5)

        self.trolltechLogo = ImageItem(QtGui.QImage(':/images/trolltech-logo.png'),
                1000, 1000, self.scene, None, True, 0.5)
        self.qtLogo = ImageItem(QtGui.QImage(':/images/qtlogo_small.png'), 1000,
                1000, self.scene, None, True, 0.5)
        self.trolltechLogo.setZValue(100)
        self.qtLogo.setZValue(100)
        self.pausedLabel = DemoTextItem("PAUSED", Colors.buttonFont(),
                QtCore.Qt.white, -1, self.scene, None)
        self.pausedLabel.setZValue(100)
        fm = QtGui.QFontMetricsF(Colors.buttonFont())
        self.pausedLabel.setPos(Colors.stageWidth - fm.width("PAUSED"),
                590 - fm.height())
        self.pausedLabel.setRecursiveVisible(False)

    def checkAdapt(self):
        if self.doneAdapt or Colors.noTimerUpdate or self.demoStartTime.elapsed() < 2000:
            return

        self.doneAdapt = True
        self.forceFpsMedianCalculation()
        Colors.benchmarkFps = self.fpsMedian
        Colors.debug("- benchmark: %d FPS" % int(Colors.benchmarkFps))

        if Colors.noAdapt:
            return

        if self.fpsMedian < 30:
            ticker = MenuManager.instance().ticker
            if ticker and ticker.scene():
                self.scene.removeItem(ticker)
                Colors.noTimerUpdate = True
                self.switchTimerOnOff(False)

                if self.fpsLabel:
                    self.fpsLabel.setText("FPS: (%d)" % int(self.fpsMedian))

                Colors.debug("- benchmark adaption: removed ticker (fps < 30)")

            if self.fpsMedian < 20:
                Colors.noAnimations = True
                Colors.debug("- benchmark adaption: animations switched off (fps < 20)")

            Colors.adapted = True

    def drawBackgroundToPixmap(self):
        r = self.scene.sceneRect()
        self.background = QtGui.QPixmap(QtCore.qRound(r.width()),
                QtCore.qRound(r.height()))
        self.background.fill(QtCore.Qt.black)
        painter = QtGui.QPainter(self.background)

        bg = QtGui.QImage(':/images/demobg.png')
        painter.drawImage(0, 0, bg)

    def drawBackground(self, painter, rect):
        painter.drawPixmap(QtCore.QPoint(0, 0), self.background)

    def toggleFullscreen(self):
        if self.isFullScreen():
            self.enableMask(True)
            self.showNormal()
            if MenuManager.instance().ticker:
                MenuManager.instance().ticker.pause(False)
        else:
            self.enableMask(False)
            self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.loop = False
            QtGui.QApplication.quit()
        elif event.key() == QtCore.Qt.Key_1:
            s = ""
            s += "Rendering system: "
            if Colors.openGlRendering:
                s += "OpenGL"
            elif Colors.direct3dRendering:
                s += "Direct3D"
            else:
                s += "software"

            s += "\nAdapt: "
            s += ["on", "off"][Colors.noAdapt]
            s += "\nAdaption occured: "
            s += ["no", "yes"][Colors.adapted]
            s += "\nOpenGL version: "
            s += Colors.glVersion
            w = QtGui.QWidget()
            s += "\nColor bit depth: %d" % w.depth()
            s += "\nWanted FPS: %d" % Colors.fps
            s += "\nBenchmarked FPS: ";
            if Colors.benchmarkFps != -1:
                s += "%d" % Colors.benchmarkFps
            else:
                s += "not calculated"
            s += "\nAnimations: ";
            s += ["on", "off"][Colors.noAnimations]
            s += "\nBlending: ";
            s += ["on", "off"][Colors.useEightBitPalette]
            s += "\nTicker: ";
            s += ["on", "off"][Colors.noTicker]
            s += "\nPixmaps: ";
            s += ["off", "on"][Colors.usePixmaps]
            s += "\nRescale images on resize: ";
            s += ["on", "off"][Colors.noRescale]
            s += "\nTimer based updates: ";
            s += ["on", "off"][Colors.noTimerUpdate]
            s += "\nSeparate loop: ";
            s += ["no", "yes"][Colors.useLoop]
            s += "\nScreen sync: ";
            s += ["yes", "no"][Colors.noScreenSync]
            QtGui.QMessageBox.information(None, "Current configuration", s)

    def focusInEvent(self, event):
        if not Colors.pause:
            return

        if MenuManager.instance().ticker:
            MenuManager.instance().ticker.pause(False)

        code = MenuManager.instance().currentMenuCode
        if code in (MenuManager.ROOT, MenuManager.MENU1):
            self.switchTimerOnOff(True)

        self.pausedLabel.setRecursiveVisible(False)

    def focusOutEvent(self, event):
        if not Colors.pause:
            return

        if MenuManager.instance().ticker:
            MenuManager.instance().ticker.pause(True)

        code = MenuManager.instance().currentMenuCode
        if code in (MenuManager.ROOT, MenuManager.MENU1):
            self.switchTimerOnOff(False)

        self.pausedLabel.setRecursiveVisible(True)

    def resizeEvent(self, event):
        self.resetMatrix()
        self.scale(event.size().width() / 800.0, event.size().height() / 600.0)

        super(MainWindow, self).resizeEvent(event)

        DemoItem.setMatrix(self.matrix())

        if self.trolltechLogo:
            r = self.scene.sceneRect()
            ttb = self.trolltechLogo.boundingRect()
            self.trolltechLogo.setPos(int((r.width() - ttb.width()) / 2),
                    595 - ttb.height())
            qtb = self.qtLogo.boundingRect()
            self.qtLogo.setPos(802 - qtb.width(), 0)

        # Changing size will almost always hurt FPS during the change so ignore
        # it.
        self.fpsHistory = []
