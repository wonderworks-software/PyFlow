import sys

from PySide import QtGui


class Colors(object):
    # Colors:
    sceneBg1 = QtGui.QColor(91, 91, 91)
    sceneBg1Line = QtGui.QColor(114, 108, 104)
    sceneBg2 = QtGui.QColor(0, 0, 0)
    sceneLine = QtGui.QColor(255, 255, 255)
    paperBg = QtGui.QColor(100, 100, 100)
    menuTextFg = QtGui.QColor(255, 0, 0)
    buttonBgLow = QtGui.QColor(255, 255, 255, 90)
    buttonBgHigh = QtGui.QColor(255, 255, 255, 20)
    buttonText = QtGui.QColor(255, 255, 255)
    tt_green = QtGui.QColor(166, 206, 57)
    fadeOut = QtGui.QColor(206, 246, 117, 0)
    heading = QtGui.QColor(190, 230, 80)
    contentColor = "<font color='#eeeeee'>"
    glVersion = "Not detected!"

    # Guides:
    stageStartY = 8
    stageHeight = 536
    stageStartX = 8
    stageWidth = 785
    contentStartY = 22
    contentHeight = 510

    # Properties:
    openGlRendering = False
    direct3dRendering = False
    softwareRendering = False
    openGlAvailable = True
    openGlAdequate = True
    direct3dAvailable = True
    xRenderPresent = True

    noTicker = False
    noRescale = False
    noAnimations = False
    noBlending = False
    noScreenSync = False
    fullscreen = False
    usePixmaps = False
    useLoop = False
    showBoundingRect = False
    showFps = False
    noAdapt = False
    noWindowMask = True
    useButtonBalls = False
    useEightBitPalette = False
    noTimerUpdate = False
    noTickerMorph = False
    adapted = False
    verbose = False
    pause = True

    fps = 100
    menuCount = 18
    animSpeed = 1.0
    animSpeedButtons = 1.0
    benchmarkFps = -1.0
    tickerLetterCount = 80;
    tickerMoveSpeed = 0.4
    tickerMorphSpeed = 2.5
    tickerText = ".EROM ETAERC .SSEL EDOC"
    rootMenuName = "PyQt Examples and Demos"

    @staticmethod
    def contentFont():
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)

        if sys.platform == 'darwin':
            font.setPixelSize(14)
            font.setFamily('Arial')
        else:
            font.setPixelSize(13)
            font.setFamily('Verdana')

        return font

    @staticmethod
    def headingFont():
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)

        font.setPixelSize(23)
        font.setBold(True)
        font.setFamily('Verdana')

        return font;

    @staticmethod
    def buttonFont():
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)

        font.setPixelSize(11)
        font.setFamily('Verdana')

        return font

    @staticmethod
    def tickerFont():
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)

        if sys.platform == 'darwin':
            font.setPixelSize(11)
            font.setBold(True)
            font.setFamily('Arial')
        else:
            font.setPixelSize(10)
            font.setBold(True)
            font.setFamily('sans serif')

        return font

    @classmethod
    def debug(cls, *args):
        if cls.verbose:
            sys.stderr.write("%s\n" % " ".join([str(arg) for arg in args]))

    @classmethod
    def parseArgs(cls, argv):
        # Some arguments should be processed before others.  Handle them now.
        if "-verbose" in argv:
            cls.verbose = True

        cls.detectSystemResources()

        # Handle the rest of the arguments.  They may override attributes
        # already set.
        for s in argv:
            if s == "-opengl":
                cls.openGlRendering = True
            elif s == "-direct3d":
                cls.direct3dRendering = True
            elif s == "-software":
                cls.softwareRendering = True
            elif s == "-no-opengl":
                cls.softwareRendering = True
            elif s == "-no-ticker":
                cls.noTicker = True
            elif s.startswith("-ticker"):
                cls.noTicker =  not bool(parseFloat(s, "-ticker"))
            elif s == "-no-animations":
                cls.noAnimations = True
            elif s.startswith("-animations"):
                cls.noAnimations = not bool(parseFloat(s, "-animations"))
            elif s == "-no-adapt":
                cls.noAdapt = True
            elif s == "-low":
                cls.setLowSettings()
            elif s == "-no-rescale":
                cls.noRescale = True
            elif s == "-use-pixmaps":
                cls.usePixmaps = True
            elif s == "-fullscreen":
                cls.fullscreen = True
            elif s == "-show-br":
                cls.showBoundingRect = True
            elif s == "-show-fps":
                cls.showFps = True
            elif s == "-no-blending":
                cls.noBlending = True
            elif s == "-no-sync":
                cls.noScreenSync = True
            elif s.startswith("-menu"):
                cls.menuCount = int(parseFloat(s, "-menu"))
            elif s.startswith("-use-timer-update"):
                cls.noTimerUpdate = not bool(parseFloat(s, "-use-timer-update"))
            elif s.startswith("-pause"):
                cls.pause = bool(parseFloat(s, "-pause"))
            elif s == "-no-ticker-morph":
                cls.noTickerMorph = True
            elif s == "-use-window-mask":
                cls.noWindowMask = False
            elif s == "-use-loop":
                cls.useLoop = True
            elif s == "-use-8bit":
                cls.useEightBitPalette = True
            elif s.startswith("-8bit"):
                cls.useEightBitPalette = bool(parseFloat(s, "-8bit"))
            elif s == "-use-balls":
                cls.useButtonBalls = True
            elif s.startswith("-ticker-letters"):
                cls.tickerLetterCount = int(parseFloat(s, "-ticker-letters"))
            elif s.startswith("-ticker-text"):
                cls.tickerText = parseText(s, "-ticker-text")
            elif s.startswith("-ticker-speed"):
                cls.tickerMoveSpeed = parseFloat(s, "-ticker-speed")
            elif s.startswith("-ticker-morph-speed"):
                cls.tickerMorphSpeed = parseFloat(s, "-ticker-morph-speed")
            elif s.startswith("-animation-speed"):
                cls.animSpeed = parseFloat(s, "-animation-speed")
            elif s.startswith("-fps"):
                cls.fps = int(parseFloat(s, "-fps"))
            elif s.startswith("-h") or s.startswith("-help"):
                QtGui.QMessageBox.warning(None, "Arguments",
                        "Usage: qtdemo.py [-verbose] [-no-adapt] [-opengl] "
                        "[-direct3d] [-software] [-fullscreen] [-ticker[0|1]] "
                        "[-animations[0|1]] [-no-blending] [-no-sync] "
                        "[-use-timer-update[0|1]] [-pause[0|1]] "
                        "[-use-window-mask] [-no-rescale] [-use-pixmaps] "
                        "[-show-fps] [-show-br] [-8bit[0|1]] [-menu<int>] "
                        "[-use-loop] [-use-balls] [-animation-speed<float>] "
                        "[-fps<int>] [-low] [-ticker-letters<int>] "
                        "[-ticker-speed<float>] [-no-ticker-morph] "
                        "[-ticker-morph-speed<float>] [-ticker-text<string>]")
                sys.exit(0)

        cls.postConfigure()

    @classmethod
    def setLowSettings(cls):
        cls.openGlRendering = False
        cls.direct3dRendering = False
        cls.softwareRendering = True
        cls.noTicker = True
        cls.noTimerUpdate = True
        cls.fps = 30
        cls.usePixmaps = True
        cls.noAnimations = True
        cls.noBlending = True

    @classmethod
    def detectSystemResources(cls):
        try:
            from PySide import QtOpenGL
            cls.openGlAvailable = True
        except ImportError:
            cls.openGlAvailable = False

        if cls.openGlAvailable:
            version_flags = QtOpenGL.QGLFormat.openGLVersionFlags()

            if version_flags & QtOpenGL.QGLFormat.OpenGL_Version_2_0:
                cls.glVersion = "2.0 or higher"
            elif version_flags & QtOpenGL.QGLFormat.OpenGL_Version_1_5:
                cls.glVersion = "1.5"
            elif version_flags & QtOpenGL.QGLFormat.OpenGL_Version_1_4:
                cls.glVersion = "1.4"
            elif version_flags & QtOpenGL.QGLFormat.OpenGL_Version_1_3:
                cls.glVersion = "1.3 or lower"

            cls.debug("- OpenGL version:", cls.glVersion)

            glw = QtOpenGL.QGLWidget()

            if (not QtOpenGL.QGLFormat.hasOpenGL() or
                    not glw.format().directRendering() or
                    not (version_flags & QtOpenGL.QGLFormat.OpenGL_Version_1_5) or
                    glw.depth() < 24):
                cls.openGlAdequate = False
                cls.debug("- OpenGL not recommended on this system")
        else:
            cls.openGlAdequate = False
            cls.debug("- OpenGL not supported by current build of Qt")

        if sys.platform == 'win32':
            # For now.
            cls.direct3dAvailable = False

        # Check if X Render is present.
        if hasattr(QtGui.QPixmap, 'x11PictureHandle'):
            tmp = QtGui.QPixmap(1, 1)

            if not tmp.x11PictureHandle():
                cls.xRenderPresent = False
                cls.debug("- X render not present")

        w = QtGui.QWidget()
        cls.debug("- Color depth: %d" % w.depth())

    @classmethod
    def postConfigure(cls):
        if not cls.noAdapt:
            w = QtGui.QWidget()

            if w.depth() < 16:
                cls.useEightBitPalette = True
                cls.adapted = True
                cls.debug("- Adapt: Color depth less than 16 bit. Using 8 bit palette")

            if not cls.xRenderPresent:
                cls.setLowSettings()
                cls.adapted = True
                cls.debug("- Adapt: X renderer not present. Using low settings")

        if sys.platform != 'win32':
            if cls.direct3dRendering:
                cls.direct3dRendering = False
                cls.debug("- WARNING: Direct3D specified, but not supported on this platform")

        if (not cls.openGlRendering and not cls.direct3dRendering and
                not cls.softwareRendering):
            # The user has not specified a rendering system so we do it.
            if sys.platform == 'win32':
                if cls.direct3dAvailable:
                    cls.direct3dRendering = True

            if not cls.direct3dRendering:
                if cls.openGlAdequate:
                    cls.openGlRendering = True
                else:
                    cls.softwareRendering = True


def parseFloat(argument, name):
    try:
        value = float(parseText(argument, name))
    except ValueError:
        value = 0.0

    return value


def parseText(argument, name):
    if len(name) == len(argument):
        QtGui.QMessageBox.warning(None, "Arguments",
                "No argument number found for %s. Remember to put name and "
                "value adjacent! (e.g. -fps100)")
        sys.exit(0)

    return argument[len(name):]
