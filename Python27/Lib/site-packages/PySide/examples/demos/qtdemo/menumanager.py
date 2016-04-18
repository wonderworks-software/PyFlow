import os
import sys

from PySide import QtCore, QtGui, QtHelp, QtXml

from colors import Colors
from demoitemanimation import DemoItemAnimation
from examplecontent import ExampleContent
from itemcircleanimation import ItemCircleAnimation
from menucontent import MenuContentItem
from score import Score
from textbutton import TextButton

class MenuManager(QtCore.QObject):
    ROOT, MENU1, MENU2, LAUNCH, DOCUMENTATION, QUIT, FULLSCREEN, UP, DOWN, \
            BACK = range(10)

    pInstance = None

    def __init__(self):
        super(MenuManager, self).__init__()

        self.contentsDoc = None
        self.assistantProcess = QtCore.QProcess()
        self.helpRootUrl = ''
        self.docDir = QtCore.QDir()
        self.imgDir = QtCore.QDir()

        self.info = {}
        self.window = None

        self.ticker = None
        self.tickerInAnim = None
        self.upButton = None
        self.downButton = None
        self.helpEngine = None
        self.score = Score()
        self.currentMenu = "[no menu visible]"
        self.currentCategory = "[no category visible]"
        self.currentMenuButtons = "[no menu buttons visible]"
        self.currentInfo = "[no info visible]"
        self.currentMenuCode = -1
        self.readXmlDocument()
        self.initHelpEngine()

    @classmethod
    def instance(cls):
        if cls.pInstance is None:
            cls.pInstance = cls()

        return cls.pInstance

    def getResource(self, name):
        ba = self.helpEngine.fileData(QtCore.QUrl(name))

        if ba.isEmpty():
            Colors.debug(" - WARNING: Could not get", name)

        return ba

    def readXmlDocument(self):
        self.contentsDoc = QtXml.QDomDocument()

        xml_file = QtCore.QFile(':/xml/examples.xml')
        statusOK, errorStr, errorLine, errorColumn = \
                self.contentsDoc.setContent(xml_file, True)

        if not statusOK:
            QtGui.QMessageBox.critical(None, "DOM Parser",
                    "Could not read or find the contents document. Error at "
                    "line %d, column %d:\n%s" % (errorLine, errorColumn, errorStr))
            sys.exit(-1)

    def initHelpEngine(self):
        self.helpRootUrl = 'qthelp://com.trolltech.qt.%d%d%d/qdoc/' % QtCore.__version_info__

        # Store help collection file in cache dir of assistant.
        cacheDir = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation) + '/Trolltech/Assistant/'
        helpDataFile = 'qtdemo_%s.qhc' % QtCore.__version__

        dir = QtCore.QDir()
        if not dir.exists(cacheDir):
            dir.mkpath(cacheDir)

        # Create help engine (and new helpDataFile if it does not exist).
        self.helpEngine = QtHelp.QHelpEngineCore(cacheDir + helpDataFile)
        self.helpEngine.setupData()

        qtDocRoot = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.DocumentationPath) + '/qch'
        qtDocRoot = QtCore.QDir(qtDocRoot).absolutePath()

        qchFiles = ['/qt.qch', '/designer.qch', '/linguist.qch']

        oldDir = self.helpEngine.customValue('docDir', '')
        if oldDir != qtDocRoot:
            for qchFile in qchFiles:
                self.helpEngine.unregisterDocumentation(QtHelp.QHelpEngineCore.namespaceName(qtDocRoot + qchFile))

        # If the data that the engine will work on is not yet registered, do it
        # now.
        for qchFile in qchFiles:
            self.helpEngine.registerDocumentation(qtDocRoot + qchFile)

        self.helpEngine.setCustomValue('docDir', qtDocRoot)

    def itemSelected(self, userCode, menuName):
        if userCode == MenuManager.LAUNCH:
            self.launchExample(self.currentInfo)
        elif userCode == MenuManager.DOCUMENTATION:
            self.showDocInAssistant(self.currentInfo)
        elif userCode == MenuManager.QUIT:
            self.window.loop = False
            QtCore.QCoreApplication.quit()
        elif userCode == MenuManager.FULLSCREEN:
            self.window.toggleFullscreen()
        elif userCode == MenuManager.ROOT:
            # Out.
            self.score.queueMovie(self.currentMenu + ' -out', Score.FROM_START,
                    Score.LOCK_ITEMS)
            self.score.queueMovie(self.currentMenuButtons + ' -out',
                    Score.FROM_START, Score.LOCK_ITEMS)
            self.score.queueMovie(self.currentInfo + ' -out')
            self.score.queueMovie(self.currentInfo + ' -buttons -out',
                    Score.NEW_ANIMATION_ONLY)
            self.score.queueMovie('back -out', Score.ONLY_IF_VISIBLE)

            # Book-keeping.
            self.currentMenuCode = MenuManager.ROOT
            self.currentMenu = menuName + ' -menu1'
            self.currentMenuButtons = menuName + ' -buttons'
            self.currentInfo = menuName + ' -info'

            # In.
            self.score.queueMovie('upndown -shake')
            self.score.queueMovie(self.currentMenu, Score.FROM_START,
                    Score.UNLOCK_ITEMS)
            self.score.queueMovie(self.currentMenuButtons, Score.FROM_START,
                    Score.UNLOCK_ITEMS)
            self.score.queueMovie(self.currentInfo)

            if not Colors.noTicker:
                self.ticker.doIntroTransitions = True
                self.tickerInAnim.startDelay = 2000
                self.ticker.useGuideQt()
                self.score.queueMovie('ticker', Score.NEW_ANIMATION_ONLY)
        elif userCode == MenuManager.MENU1:
            # Out.
            self.score.queueMovie(self.currentMenu + ' -out', Score.FROM_START,
                    Score.LOCK_ITEMS)
            self.score.queueMovie(self.currentMenuButtons + ' -out',
                    Score.FROM_START, Score.LOCK_ITEMS)
            self.score.queueMovie(self.currentInfo + ' -out')

            # Book-keeping.
            self.currentMenuCode = MenuManager.MENU1
            self.currentCategory = menuName
            self.currentMenu = menuName + ' -menu1'
            self.currentInfo = menuName + ' -info'

            # In.
            self.score.queueMovie('upndown -shake')
            self.score.queueMovie('back -in')
            self.score.queueMovie(self.currentMenu, Score.FROM_START,
                    Score.UNLOCK_ITEMS)
            self.score.queueMovie(self.currentInfo)

            if not Colors.noTicker:
                self.ticker.useGuideTt()
        elif userCode == MenuManager.MENU2:
            # Out.
            self.score.queueMovie(self.currentInfo + ' -out',
                    Score.NEW_ANIMATION_ONLY)
            self.score.queueMovie(self.currentInfo + ' -buttons -out',
                    Score.NEW_ANIMATION_ONLY)

            # Book-keeping.
            self.currentMenuCode = MenuManager.MENU2
            self.currentInfo = menuName

            # In/shake.
            self.score.queueMovie('upndown -shake')
            self.score.queueMovie('back -shake')
            self.score.queueMovie(self.currentMenu + ' -shake')
            self.score.queueMovie(self.currentInfo, Score.NEW_ANIMATION_ONLY)
            self.score.queueMovie(self.currentInfo + ' -buttons',
                    Score.NEW_ANIMATION_ONLY)

            if not Colors.noTicker:
                self.score.queueMovie('ticker -out', Score.NEW_ANIMATION_ONLY)
        elif userCode == MenuManager.UP:
            backMenu = self.info[self.currentMenu]['back']
            if backMenu:
                self.score.queueMovie(self.currentMenu + ' -top_out',
                        Score.FROM_START, Score.LOCK_ITEMS)
                self.score.queueMovie(backMenu + ' -bottom_in',
                        Score.FROM_START, Score.UNLOCK_ITEMS)
                self.currentMenu = backMenu
        elif userCode == MenuManager.DOWN:
            moreMenu = self.info[self.currentMenu]['more']
            if moreMenu:
                self.score.queueMovie(self.currentMenu + ' -bottom_out',
                        Score.FROM_START, Score.LOCK_ITEMS)
                self.score.queueMovie(moreMenu + ' -top_in', Score.FROM_START,
                        Score.UNLOCK_ITEMS)
                self.currentMenu = moreMenu
        elif userCode == MenuManager.BACK:
            if self.currentMenuCode == MenuManager.MENU2:
                # Out.
                self.score.queueMovie(self.currentInfo + ' -out',
                        Score.NEW_ANIMATION_ONLY)
                self.score.queueMovie(self.currentInfo + ' -buttons -out',
                        Score.NEW_ANIMATION_ONLY)

                # Book-keeping.
                self.currentMenuCode = MenuManager.MENU1
                self.currentMenuButtons = self.currentCategory + ' -buttons'
                self.currentInfo = self.currentCategory + ' -info'

                # In/shake.
                self.score.queueMovie('upndown -shake')
                self.score.queueMovie(self.currentMenu + ' -shake')
                self.score.queueMovie(self.currentInfo,
                        Score.NEW_ANIMATION_ONLY)
                self.score.queueMovie(self.currentInfo + ' -buttons',
                        Score.NEW_ANIMATION_ONLY)

                if not Colors.noTicker:
                    self.ticker.doIntroTransitions = False
                    self.tickerInAnim.startDelay = 500
                    self.score.queueMovie('ticker', Score.NEW_ANIMATION_ONLY)
            elif self.currentMenuCode != MenuManager.ROOT:
                self.itemSelected(MenuManager.ROOT, Colors.rootMenuName)

        # Update back and more buttons.
        if self.info.setdefault(self.currentMenu, {}).get('back'):
            back_state = TextButton.OFF
        else:
            back_state = TextButton.DISABLED

        if self.info[self.currentMenu].get('more'):
            more_state = TextButton.OFF
        else:
            more_state = TextButton.DISABLED

        self.upButton.setState(back_state)
        self.downButton.setState(more_state)

        if self.score.hasQueuedMovies():
            self.score.playQue()
            # Playing new movies might include loading etc., so ignore the FPS
            # at this point.
            self.window.fpsHistory = []

    def showDocInAssistant(self, name):
        url = self.resolveDocUrl(name)
        Colors.debug("Sending URL to Assistant:", url)

        # Start assistant if it's not already running.
        if self.assistantProcess.state() != QtCore.QProcess.Running:
            app = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath) + QtCore.QDir.separator()

            if sys.platform == 'darwin':
                app += 'Assistant.app/Contents/MacOS/Assistant'
            else:
                app += 'assistant'

            args = ['-enableRemoteControl']
            self.assistantProcess.start(app, args)
            if not self.assistantProcess.waitForStarted():
                QtGui.QMessageBox.critical(None, "PyQt Demo",
                        "Could not start %s." % app)
                return

        # Send command through remote control even if the process was just
        # started to activate assistant and bring it to the front.
        cmd_str = QtCore.QTextStream(self.assistantProcess)
        cmd_str << 'SetSource ' << url << '\n'

    def launchExample(self, name):
        executable = self.resolveExeFile(name)

        process = QtCore.QProcess(self)
        process.finished.connect(self.exampleFinished)
        process.error.connect(self.exampleError)

        if sys.platform == 'win32':
            # Make sure it finds the DLLs on Windows.
            curpath = os.getenv('PATH')
            newpath = 'PATH=%s;%s' % (QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath), curpath)
            process.setEnvironment([newpath])

        if self.info[name]['changedirectory'] != 'false':
            workingDirectory = self.resolveDataDir(name)
            process.setWorkingDirectory(workingDirectory)
            Colors.debug("Setting working directory:", workingDirectory)

        Colors.debug("Launching:", executable)
        process.start(sys.executable, [executable])

    def exampleFinished(self):
        pass

    def exampleError(self, error):
        if error != QtCore.QProcess.Crashed:
            QtGui.QMessageBox.critical(None, "Failed to launch the example",
                    "Could not launch the example. Ensure that it has been "
                    "built.",
                    QtGui.QMessageBox.Cancel)

    def init(self, window):
        self.window = window

        # Create div.
        self.createTicker()
        self.createUpnDownButtons()
        self.createBackButton()

        # Create first level menu.
        rootElement = self.contentsDoc.documentElement()
        self.createRootMenu(rootElement)

        # Create second level menus.
        level2MenuNode = rootElement.firstChild()
        while not level2MenuNode.isNull():
            level2MenuElement = level2MenuNode.toElement()
            self.createSubMenu(level2MenuElement)

            # Create leaf menu and example info.
            exampleNode = level2MenuElement.firstChild()
            while not exampleNode.isNull():
                exampleElement = exampleNode.toElement()
                self.readInfoAboutExample(exampleElement)
                self.createLeafMenu(exampleElement)
                exampleNode = exampleNode.nextSibling()

            level2MenuNode = level2MenuNode.nextSibling()

    def readInfoAboutExample(self, example):
        name = str(example.attribute('name'))
        if name in self.info:
            Colors.debug("__WARNING: MenuManager.readInfoAboutExample: "
                         "Demo/example with name", name, "appears twice in "
                         "the xml-file!__")

        self.info.setdefault(name, {})['filename'] = str(example.attribute('filename'))
        self.info[name]['category'] = str(example.parentNode().toElement().tagName())
        self.info[name]['dirname'] = str(example.parentNode().toElement().attribute('dirname'))
        self.info[name]['changedirectory'] = str(example.attribute('changedirectory'))
        self.info[name]['image'] = str(example.attribute('image'))

    def resolveDir(self, name):
        dirName = self.info[name]['dirname']
        category = self.info[name]['category']
        fileName = self.info[name]['filename']

        dir = QtCore.QFileInfo(__file__).dir()
        dir.cdUp()

        if category != 'demos':
            dir.cdUp()

        dir.cd(dirName)

        # This may legitimately fail if the example is just a simple .py file.
        dir.cd(fileName)

        return dir

    def resolveDataDir(self, name):
        return self.resolveDir(name).absolutePath()

    def resolveExeFile(self, name):
        dir = self.resolveDir(name)

        fileName = self.info[name]['filename']

        pyFile = QtCore.QFile(dir.path() + '/' + fileName + '.py')
        if pyFile.exists():
            return pyFile.fileName()

        pywFile = QtCore.QFile(dir.path() + '/' + fileName + '.pyw')
        if pywFile.exists():
            return pywFile.fileName()

        Colors.debug("- WARNING: Could not resolve executable:", dir.path(),
                fileName)
        return '__executable not found__'

    def resolveDocUrl(self, name):
        dirName = self.info[name]['dirname']
        category = self.info[name]['category']
        fileName = self.info[name]['filename']

        if category == 'demos':
            return self.helpRootUrl + 'demos-' + fileName + '.html'
        else:
            return self.helpRootUrl + dirName.replace('/', '-') + '-' + fileName + '.html'

    def resolveImageUrl(self, name):
        return self.helpRootUrl + 'images/' + name

    def getHtml(self, name):
        return self.getResource(self.resolveDocUrl(name))

    def getImage(self, name):
        imageName = self.info[name]['image']
        category = self.info[name]['category']
        fileName = self.info[name]['filename']

        if not imageName:
            if category == 'demos':
                imageName = fileName + '-demo.png'
            else:
                imageName = fileName + '-example.png'

            if self.getResource(self.resolveImageUrl(imageName)).isEmpty():
                imageName = fileName + '.png'

            if self.getResource(self.resolveImageUrl(imageName)).isEmpty():
                imageName = fileName + 'example.png'

        return self.getResource(self.resolveImageUrl(imageName))

    def createRootMenu(self, el):
        name = str(el.attribute('name'))
        self.createMenu(el, MenuManager.MENU1)
        self.createInfo(MenuContentItem(el, self.window.scene), name + ' -info')

        menuButtonsIn = self.score.insertMovie(name + ' -buttons')
        menuButtonsOut = self.score.insertMovie(name + ' -buttons -out')
        self.createLowLeftButton("Quit", MenuManager.QUIT, menuButtonsIn,
                menuButtonsOut, None)
        self.createLowRightButton("Toggle fullscreen", MenuManager.FULLSCREEN,
                menuButtonsIn, menuButtonsOut, None)

    def createSubMenu(self, el):
        name = str(el.attribute('name'))
        self.createMenu(el, MenuManager.MENU2)
        self.createInfo(MenuContentItem(el, self.window.scene), name + ' -info')

    def createLeafMenu(self, el):
        name = str(el.attribute('name'))
        self.createInfo(ExampleContent(name, self.window.scene), name)

        infoButtonsIn = self.score.insertMovie(name + ' -buttons')
        infoButtonsOut = self.score.insertMovie(name + ' -buttons -out')
        self.createLowRightLeafButton("Documentation", 600,
                MenuManager.DOCUMENTATION, infoButtonsIn, infoButtonsOut, None)
        if str(el.attribute('executable')) != 'false':
            self.createLowRightLeafButton("Launch", 405, MenuManager.LAUNCH,
                    infoButtonsIn, infoButtonsOut, None)

    def createMenu(self, category, type):
        sw = self.window.scene.sceneRect().width()
        xOffset = 15
        yOffset = 10
        maxExamples = Colors.menuCount
        menuIndex = 1
        name = str(category.attribute('name'))
        currentNode = category.firstChild()
        currentMenu = '%s -menu%d' % (name, menuIndex)

        while not currentNode.isNull():
            movieIn = self.score.insertMovie(currentMenu)
            movieOut = self.score.insertMovie(currentMenu + ' -out')
            movieNextTopOut = self.score.insertMovie(currentMenu + ' -top_out')
            movieNextBottomOut = self.score.insertMovie(currentMenu + ' -bottom_out')
            movieNextTopIn = self.score.insertMovie(currentMenu + ' -top_in')
            movieNextBottomIn = self.score.insertMovie(currentMenu + ' -bottom_in')
            movieShake = self.score.insertMovie(currentMenu + ' -shake')

            i = 0
            while not currentNode.isNull() and i < maxExamples:
                # Create a normal menu button.
                label = str(currentNode.toElement().attribute('name'))
                item = TextButton(label, TextButton.LEFT, type,
                        self.window.scene)
                currentNode = currentNode.nextSibling()

                # Skip the OpenGL examples if they can't run.
                if str(currentNode.toElement().attribute('dirname')) == 'opengl':
                    if not Colors.openGlAvailable:
                        currentNode = currentNode.nextSibling()

                item.setRecursiveVisible(False)
                item.setZValue(10)
                ih = item.sceneBoundingRect().height()
                iw = item.sceneBoundingRect().width()
                ihp = ih + 3

                # Create in-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
                anim.setDuration(float(1000 + (i * 20)) * Colors.animSpeedButtons)
                anim.setStartPos(QtCore.QPointF(xOffset, -ih))
                anim.setPosAt(0.20, QtCore.QPointF(xOffset, -ih))
                anim.setPosAt(0.50, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY + (10 * float(i / 4.0))))
                anim.setPosAt(0.60, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(0.70, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY + (5 * float(i / 4.0))))
                anim.setPosAt(0.80, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(0.90, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY + (2 * float(i / 4.0))))
                anim.setPosAt(1.00, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                movieIn.append(anim)

                # Create out-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
                anim.hideOnFinished = True
                anim.setDuration((700 + (30 * i)) * Colors.animSpeedButtons)
                anim.setStartPos(QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(0.60, QtCore.QPointF(xOffset, 600 - ih - ih))
                anim.setPosAt(0.65, QtCore.QPointF(xOffset + 20, 600 - ih))
                anim.setPosAt(1.00, QtCore.QPointF(sw + iw, 600 - ih))
                movieOut.append(anim)

                # Create shake-animation.
                anim = DemoItemAnimation(item)
                anim.setDuration(700 * Colors.animSpeedButtons)
                anim.setStartPos(QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(0.55, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY - i*2.0))
                anim.setPosAt(0.70, QtCore.QPointF(xOffset - 10, (i * ihp) + yOffset + Colors.contentStartY - i*1.5))
                anim.setPosAt(0.80, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY - i*1.0))
                anim.setPosAt(0.90, QtCore.QPointF(xOffset - 2, (i * ihp) + yOffset + Colors.contentStartY - i*0.5))
                anim.setPosAt(1.00, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                movieShake.append(anim)

                # Create next-menu top-out-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
                anim.hideOnFinished = True
                anim.setDuration((200 + (30 * i)) * Colors.animSpeedButtons)
                anim.setStartPos(QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(0.70, QtCore.QPointF(xOffset, yOffset + Colors.contentStartY))
                anim.setPosAt(1.00, QtCore.QPointF(-iw, yOffset + Colors.contentStartY))
                movieNextTopOut.append(anim)

                # Create next-menu bottom-out-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
                anim.hideOnFinished = True
                anim.setDuration((200 + (30 * i)) * Colors.animSpeedButtons)
                anim.setStartPos(QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(0.70, QtCore.QPointF(xOffset, (maxExamples * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(1.00, QtCore.QPointF(-iw, (maxExamples * ihp) + yOffset + Colors.contentStartY))
                movieNextBottomOut.append(anim)

                # Create next-menu top-in-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
                anim.setDuration((700 - (30 * i)) * Colors.animSpeedButtons)
                anim.setStartPos(QtCore.QPointF(-iw, yOffset + Colors.contentStartY))
                anim.setPosAt(0.30, QtCore.QPointF(xOffset, yOffset + Colors.contentStartY))
                anim.setPosAt(1.00, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                movieNextTopIn.append(anim)

                # Create next-menu bottom-in-animation.
                reverse = maxExamples - i
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
                anim.setDuration((1000 - (30 * reverse)) * Colors.animSpeedButtons)
                anim.setStartPos(QtCore.QPointF(-iw, (maxExamples * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(0.30, QtCore.QPointF(xOffset, (maxExamples * ihp) + yOffset + Colors.contentStartY))
                anim.setPosAt(1.00, QtCore.QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                movieNextBottomIn.append(anim)

                i += 1

            if not currentNode.isNull() and i == maxExamples:
                # We need another menu, so register for 'more' and 'back'
                # buttons.
                menuIndex += 1
                self.info.setdefault(currentMenu, {})['more'] = '%s -menu%d' % (name, menuIndex)
                currentMenu = '%s -menu%d' % (name, menuIndex)
                self.info.setdefault(currentMenu, {})['back'] = '%s -menu%d' % (name, menuIndex - 1)

    def createLowLeftButton(self, label, type, movieIn, movieOut, movieShake, menuString=""):
        button = TextButton(label, TextButton.RIGHT, type, self.window.scene,
                None, TextButton.PANEL)
        if menuString:
            button.setMenuString(menuString)
        button.setRecursiveVisible(False)
        button.setZValue(10)

        iw = button.sceneBoundingRect().width()
        xOffset = 15

        # Create in-animation.
        buttonIn = DemoItemAnimation(button, DemoItemAnimation.ANIM_IN)
        buttonIn.setDuration(1800 * Colors.animSpeedButtons)
        buttonIn.setStartPos(QtCore.QPointF(-iw, Colors.contentStartY + Colors.contentHeight - 35))
        buttonIn.setPosAt(0.5, QtCore.QPointF(-iw, Colors.contentStartY + Colors.contentHeight - 35))
        buttonIn.setPosAt(0.7, QtCore.QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 35))
        buttonIn.setPosAt(1.0, QtCore.QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 26))
        movieIn.append(buttonIn)

        # Create out-animation.
        buttonOut = DemoItemAnimation(button, DemoItemAnimation.ANIM_OUT)
        buttonOut.hideOnFinished = True
        buttonOut.setDuration(400 * Colors.animSpeedButtons)
        buttonOut.setStartPos(QtCore.QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 26))
        buttonOut.setPosAt(1.0, QtCore.QPointF(-iw, Colors.contentStartY + Colors.contentHeight - 26))
        movieOut.append(buttonOut)

        if movieShake is not None:
            shakeAnim = DemoItemAnimation(button, DemoItemAnimation.ANIM_UNSPECIFIED)
            shakeAnim.timeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
            shakeAnim.setDuration(650)
            shakeAnim.setStartPos(buttonIn.posAt(1.0))
            shakeAnim.setPosAt(0.60, buttonIn.posAt(1.0))
            shakeAnim.setPosAt(0.70, buttonIn.posAt(1.0) + QtCore.QPointF(-3, 0))
            shakeAnim.setPosAt(0.80, buttonIn.posAt(1.0) + QtCore.QPointF(2, 0))
            shakeAnim.setPosAt(0.90, buttonIn.posAt(1.0) + QtCore.QPointF(-1, 0))
            shakeAnim.setPosAt(1.00, buttonIn.posAt(1.0))
            movieShake.append(shakeAnim)

    def createLowRightButton(self, label, type, movieIn, movieOut, movieShake):
        item = TextButton(label, TextButton.RIGHT, type, self.window.scene,
                None, TextButton.PANEL)
        item.setRecursiveVisible(False)
        item.setZValue(10)

        sw = self.window.scene.sceneRect().width()
        xOffset = 70

        # Create in-animation.
        anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
        anim.setDuration(1800 * Colors.animSpeedButtons)
        anim.setStartPos(QtCore.QPointF(sw, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(0.5, QtCore.QPointF(sw, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(0.7, QtCore.QPointF(xOffset + 535, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(1.0, QtCore.QPointF(xOffset + 535, Colors.contentStartY + Colors.contentHeight - 26))
        movieIn.append(anim)

        # Create out-animation.
        anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
        anim.hideOnFinished = True
        anim.setDuration(400 * Colors.animSpeedButtons)
        anim.setStartPos(QtCore.QPointF(xOffset + 535, Colors.contentStartY + Colors.contentHeight - 26))
        anim.setPosAt(1.0, QtCore.QPointF(sw, Colors.contentStartY + Colors.contentHeight - 26))
        movieOut.append(anim)

    def createLowRightLeafButton(self, label, xOffset, type, movieIn, movieOut, movieShake):
        item = TextButton(label, TextButton.RIGHT, type, self.window.scene,
                None, TextButton.PANEL)
        item.setRecursiveVisible(False)
        item.setZValue(10)

        sw = self.window.scene.sceneRect().width()
        sh = self.window.scene.sceneRect().height()

        # Create in-animation.
        anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
        anim.setDuration(1050 * Colors.animSpeedButtons)
        anim.setStartPos(QtCore.QPointF(sw, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(0.10, QtCore.QPointF(sw, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(0.30, QtCore.QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(0.35, QtCore.QPointF(xOffset + 30, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(0.40, QtCore.QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(0.45, QtCore.QPointF(xOffset + 5, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(0.50, QtCore.QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setPosAt(1.00, QtCore.QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 26))
        movieIn.append(anim)

        # Create out-animation.
        anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
        anim.hideOnFinished = True
        anim.setDuration(300 * Colors.animSpeedButtons)
        anim.setStartPos(QtCore.QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 26))
        anim.setPosAt(1.0, QtCore.QPointF(xOffset, sh))
        movieOut.append(anim)

    def createInfo(self, item, name):
        movie_in = self.score.insertMovie(name)
        movie_out = self.score.insertMovie(name + ' -out')
        item.setZValue(8)
        item.setRecursiveVisible(False)

        xOffset = 230.0
        infoIn = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
        infoIn.timeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        infoIn.setDuration(650)
        infoIn.setStartPos(QtCore.QPointF(self.window.scene.sceneRect().width(), Colors.contentStartY))
        infoIn.setPosAt(0.60, QtCore.QPointF(xOffset, Colors.contentStartY))
        infoIn.setPosAt(0.70, QtCore.QPointF(xOffset + 20, Colors.contentStartY))
        infoIn.setPosAt(0.80, QtCore.QPointF(xOffset, Colors.contentStartY))
        infoIn.setPosAt(0.90, QtCore.QPointF(xOffset + 7, Colors.contentStartY))
        infoIn.setPosAt(1.00, QtCore.QPointF(xOffset, Colors.contentStartY))
        movie_in.append(infoIn)

        infoOut = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
        infoOut.timeline.setCurveShape(QtCore.QTimeLine.EaseInCurve)
        infoOut.setDuration(300)
        infoOut.hideOnFinished = True
        infoOut.setStartPos(QtCore.QPointF(xOffset, Colors.contentStartY))
        infoOut.setPosAt(1.0, QtCore.QPointF(-600, Colors.contentStartY))
        movie_out.append(infoOut)

    def createTicker(self):
        if Colors.noTicker:
            return

        movie_in = self.score.insertMovie('ticker')
        movie_out = self.score.insertMovie('ticker -out')
        movie_activate = self.score.insertMovie('ticker -activate')
        movie_deactivate = self.score.insertMovie('ticker -deactivate')

        self.ticker = ItemCircleAnimation(self.window.scene)
        self.ticker.setZValue(50)
        self.ticker.hide()

        # Move ticker in.
        qtendpos = 485
        qtPosY = 120
        self.tickerInAnim = DemoItemAnimation(self.ticker,
                DemoItemAnimation.ANIM_IN)
        self.tickerInAnim.setDuration(500)
        self.tickerInAnim.setStartPos(QtCore.QPointF(self.window.scene.sceneRect().width(), Colors.contentStartY + qtPosY))
        self.tickerInAnim.setPosAt(0.60, QtCore.QPointF(qtendpos, Colors.contentStartY + qtPosY))
        self.tickerInAnim.setPosAt(0.70, QtCore.QPointF(qtendpos + 30, Colors.contentStartY + qtPosY))
        self.tickerInAnim.setPosAt(0.80, QtCore.QPointF(qtendpos, Colors.contentStartY + qtPosY))
        self.tickerInAnim.setPosAt(0.90, QtCore.QPointF(qtendpos + 5, Colors.contentStartY + qtPosY))
        self.tickerInAnim.setPosAt(1.00, QtCore.QPointF(qtendpos, Colors.contentStartY + qtPosY))
        movie_in.append(self.tickerInAnim)

        # Move ticker out.
        qtOut = DemoItemAnimation(self.ticker, DemoItemAnimation.ANIM_OUT)
        qtOut.hideOnFinished = True
        qtOut.setDuration(500)
        qtOut.setStartPos(QtCore.QPointF(qtendpos, Colors.contentStartY + qtPosY))
        qtOut.setPosAt(1.00, QtCore.QPointF(self.window.scene.sceneRect().width() + 700, Colors.contentStartY + qtPosY))
        movie_out.append(qtOut)

        # Move ticker in on activate.
        qtActivate = DemoItemAnimation(self.ticker)
        qtActivate.setDuration(400)
        qtActivate.setStartPos(QtCore.QPointF(self.window.scene.sceneRect().width(), Colors.contentStartY + qtPosY))
        qtActivate.setPosAt(0.60, QtCore.QPointF(qtendpos, Colors.contentStartY + qtPosY))
        qtActivate.setPosAt(0.70, QtCore.QPointF(qtendpos + 30, Colors.contentStartY + qtPosY))
        qtActivate.setPosAt(0.80, QtCore.QPointF(qtendpos, Colors.contentStartY + qtPosY))
        qtActivate.setPosAt(0.90, QtCore.QPointF(qtendpos + 5, Colors.contentStartY + qtPosY))
        qtActivate.setPosAt(1.00, QtCore.QPointF(qtendpos, Colors.contentStartY + qtPosY))
        movie_activate.append(qtActivate)

        # Move ticker out on deactivate.
        qtDeactivate = DemoItemAnimation(self.ticker)
        qtDeactivate.hideOnFinished = True
        qtDeactivate.setDuration(400)
        qtDeactivate.setStartPos(QtCore.QPointF(qtendpos, Colors.contentStartY + qtPosY))
        qtDeactivate.setPosAt(1.00, QtCore.QPointF(qtendpos, 800))
        movie_deactivate.append(qtDeactivate)

    def createUpnDownButtons(self):
        xOffset = 15.0
        yOffset = 450.0

        self.upButton = TextButton("", TextButton.LEFT, MenuManager.UP,
                self.window.scene, None, TextButton.UP)
        self.upButton.prepare()
        self.upButton.setPos(xOffset, yOffset)
        self.upButton.setState(TextButton.DISABLED)

        self.downButton = TextButton("", TextButton.LEFT, MenuManager.DOWN,
                self.window.scene, None, TextButton.DOWN)
        self.downButton.prepare()
        self.downButton.setPos(xOffset + 10 + self.downButton.sceneBoundingRect().width(), yOffset)

        movieShake = self.score.insertMovie('upndown -shake')

        shakeAnim = DemoItemAnimation(self.upButton,
                DemoItemAnimation.ANIM_UNSPECIFIED)
        shakeAnim.timeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        shakeAnim.setDuration(650)
        shakeAnim.setStartPos(self.upButton.pos())
        shakeAnim.setPosAt(0.60, self.upButton.pos())
        shakeAnim.setPosAt(0.70, self.upButton.pos() + QtCore.QPointF(-2, 0))
        shakeAnim.setPosAt(0.80, self.upButton.pos() + QtCore.QPointF(1, 0))
        shakeAnim.setPosAt(0.90, self.upButton.pos() + QtCore.QPointF(-1, 0))
        shakeAnim.setPosAt(1.00, self.upButton.pos())
        movieShake.append(shakeAnim)

        shakeAnim = DemoItemAnimation(self.downButton,
                DemoItemAnimation.ANIM_UNSPECIFIED)
        shakeAnim.timeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        shakeAnim.setDuration(650)
        shakeAnim.setStartPos(self.downButton.pos())
        shakeAnim.setPosAt(0.60, self.downButton.pos())
        shakeAnim.setPosAt(0.70, self.downButton.pos() + QtCore.QPointF(-5, 0))
        shakeAnim.setPosAt(0.80, self.downButton.pos() + QtCore.QPointF(-3, 0))
        shakeAnim.setPosAt(0.90, self.downButton.pos() + QtCore.QPointF(-1, 0))
        shakeAnim.setPosAt(1.00, self.downButton.pos())
        movieShake.append(shakeAnim)

    def createBackButton(self):
        backIn = self.score.insertMovie('back -in')
        backOut = self.score.insertMovie('back -out')
        backShake = self.score.insertMovie('back -shake')
        self.createLowLeftButton("Back", MenuManager.ROOT, backIn, backOut,
                backShake, Colors.rootMenuName)
