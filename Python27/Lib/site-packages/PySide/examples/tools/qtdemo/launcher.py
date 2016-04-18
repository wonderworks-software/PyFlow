#!/usr/bin/env python
############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

import sys
import re

from PySide import QtCore, QtGui, QtHelp, QtNetwork, QtXml

from displaywidget import DisplayWidget
from displayshape import TitleShape, DisplayShape, PanelShape, ImageShape, DocumentShape

class Launcher(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)

        self.categories = {}
        self.runningProcesses = {}
        self.examples = {}
        self.runningExamples = []
        self.titleFont = QtGui.QFont(self.font())
        self.titleFont.setWeight(QtGui.QFont.Bold)
        self.fontRatio = 0.8
        self.documentFont = self.font()
        self.inFullScreenResize = False
        self.currentCategory = "[starting]"
        self.qtLogo = QtGui.QImage()
        self.rbLogo = QtGui.QImage()
        self.currentExample = ""
        self.assistantProcess = QtCore.QProcess()

        parentPageAction1 = QtGui.QAction(self.tr("Show Parent Page"), self)
        parentPageAction2 = QtGui.QAction(self.tr("Show Parent Page"), self)
        parentPageAction3 = QtGui.QAction(self.tr("Show Parent Page"), self)
        parentPageAction1.setShortcut(QtGui.QKeySequence(self.tr("Escape")))
        parentPageAction2.setShortcut(QtGui.QKeySequence(self.tr("Backspace")))
        parentPageAction3.setShortcut(QtGui.QKeySequence(self.tr("Alt+Left")))

        fullScreenAction = QtGui.QAction(self.tr("Toggle &Full Screen"), self)
        fullScreenAction.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+F")))

        exitAction = QtGui.QAction(self.tr("E&xit"), self)
        exitAction.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+Q")))

        self.connect(parentPageAction1, QtCore.SIGNAL("triggered()"), self, QtCore.SIGNAL("showPage()"))
        self.connect(parentPageAction2, QtCore.SIGNAL("triggered()"), self, QtCore.SIGNAL("showPage()"))
        self.connect(parentPageAction3, QtCore.SIGNAL("triggered()"), self, QtCore.SIGNAL("showPage()"))
        self.connect(fullScreenAction, QtCore.SIGNAL("triggered()"), self.toggleFullScreen)
        self.connect(exitAction, QtCore.SIGNAL("triggered()"), self.close)

        self.display = DisplayWidget()

        self.addAction(parentPageAction1)
        self.addAction(parentPageAction2)
        self.addAction(parentPageAction3)
        self.addAction(fullScreenAction)
        self.addAction(exitAction)

        self.slideshowTimer = QtCore.QTimer(self)
        self.slideshowTimer.setInterval(5000)
        self.resizeTimer = QtCore.QTimer(self)
        self.resizeTimer.setSingleShot(True)
        self.connect(self.resizeTimer, QtCore.SIGNAL("timeout()"), self.redisplayWindow)

        self.connect(self.display, QtCore.SIGNAL("actionRequested"),
                     self.executeAction)
        self.connect(self.display, QtCore.SIGNAL("categoryRequested"),
                     self.showExamples)
        self.connect(self.display, QtCore.SIGNAL("documentationRequested"),
                     self.showExampleDocumentation)
        self.connect(self.display, QtCore.SIGNAL("exampleRequested"),
                     self.showExampleSummary)

        self.connect(self.display, QtCore.SIGNAL("launchRequested"),
                     self.launchExample)

        self.connect(self, QtCore.SIGNAL("showPage()"), self.showParentPage,
                QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("windowResized()"), self.redisplayWindow,
                QtCore.Qt.QueuedConnection)

        self.setCentralWidget(self.display)
        self.setMaximumSize(QtGui.QApplication.desktop().screenGeometry().size())
        self.setWindowTitle(self.tr("PyQt Examples and Demos"))
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/images/qt4-logo.png")))

    def initHelpEngine(self):
        self.helpRootUrl = QtCore.QString("qthelp://com.trolltech.qt.%d%d%d/qdoc/" % (QtCore.QT_VERSION >> 16, ((QtCore.QT_VERSION >> 8) & 0xff), (QtCore.QT_VERSION & 0xff)))

        # Store help collection file in cache dir of assistant.
        cacheDir = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation) + "/Trolltech/Assistant"
        helpDataFile = "qtdemo_%s.qhc" % QtCore.QT_VERSION_STR

        dir = QtCore.QDir()
        if not dir.exists(cacheDir):
            dir.mkpath(cacheDir)

        # Create the help engine (and a new helpDataFile if it does not exist).
        self.helpEngine = QtHelp.QHelpEngineCore(cacheDir + helpDataFile)
        self.helpEngine.setupData()

        qtDocRoot = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.DocumentationPath) + "/qch"
        qtDocRoot = QtCore.QDir(qtDocRoot).absolutePath()

        qchFiles = ["/qt.qch", "/designer.qch", "/linguist.qch"]

        oldDir = self.helpEngine.customValue("docDir", QtCore.QVariant(QtCore.QString())).toString()
        if oldDir != qtDocRoot:
            for qchFile in qchFiles:
                self.helpEngine.unregisterDocumentation(QtHelp.QHelpEngineCore.namespaceName(qtDocRoot + qchFile))

        # If the data that the engine will work on is not yet registered, do it
        # now.
        for qchFile in qchFiles:
            self.helpEngine.registerDocumentation(qtDocRoot + qchFile)

        self.helpEngine.setCustomValue("docDir", QtCore.QVariant(qtDocRoot))

    def setup(self):
        self.initHelpEngine()

        self.documentationDir = QtCore.QDir(
                                        QtCore.QLibraryInfo.location(
                                                QtCore.QLibraryInfo.DocumentationPath))

        self.imagesDir = QtCore.QDir(self.documentationDir)

        if self.documentationDir.cd("html") and self.documentationDir.cd("images"):
            self.imagesDir.setPath(self.documentationDir.path())
            self.documentationDir.cdUp()
        else:
            QtGui.QMessageBox.warning(self, self.tr("No Documentation Found"),
                    self.tr("I could not find the Qt documentation."))

        self.maximumLabels = 0

        self.demosDir = QtCore.QDir("./../../demos")
        demoCategories = self.readInfo(":/demos.xml", self.demosDir)

        self.examplesDir = QtCore.QDir("./../../")
        exampleCategories = self.readInfo(":/examples.xml", self.examplesDir)

        if demoCategories + exampleCategories <= 0:
            QtGui.QMessageBox.warning(self, self.tr("No Examples or Demos found"),
                                        self.tr("I could not find any PyQt examples or demos.\n"\
                                                "Please ensure that PyQt is installed correctly."),
                                        QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton)
            return False

        self.maximumLabels = max(demoCategories + exampleCategories, self.maximumLabels)

        for category in self.categories:
            self.maximumLabels = max(len(self.categories[category]['examples']) + 1, self.maximumLabels)

        mainDescription = self.categories['[main]']['description']
        if len(mainDescription) > 0:
            mainDescription += self.tr("\n")

        self.categories['[main]']['description'] = mainDescription + self.tr(
            "<p>Press <b>Escape</b>, <b>Backspace</b>, or <b>%1</b> to "
            "return to a previous menu.</p>"
            "<p>Press <b>%2</b> to switch between normal and full screen "
            "modes.</p>"
            "<p>Use <b>%3</b> to exit the launcher.</p>") \
                .arg(QtCore.QString(QtGui.QKeySequence(self.tr("Alt+Left")))) \
                .arg(QtCore.QString(QtGui.QKeySequence(self.tr("Ctrl+F")))) \
                .arg(QtCore.QString(QtGui.QKeySequence(self.tr("Ctrl+Q"))))

        self.emit(QtCore.SIGNAL("showPage()"))
        return True

    def enableLaunching(self):
        process = self.sender()
        example = self.runningProcesses[process]
        del self.runningProcesses[process]
        process.deleteLater()
        self.runningExamples.remove(example)

        if example == self.currentExample:
            for i in range(0, self.display.shapesCount()):
                shape = self.display.shape(i)
                if shape.metadata.get("launch", "") == example:
                    shape.metadata["fade"] = 15
                    self.display.enableUpdates()

            self.slideshowTimer.start()

    def executeAction(self, action):
        if action == "parent":
            self.showParentPage()
        elif action == "exit":
            if len(self.runningExamples) == 0:
                self.connect(self.display, QtCore.SIGNAL("displayEmpty()"), self.close)
                self.display.reset()
            else:
                self.close()

    def launchExample(self, uniquename):
        if uniquename in self.runningExamples:
            return

        process = QtCore.QProcess(self)
        self.connect(process, QtCore.SIGNAL("finished(int)"), self.enableLaunching)

        self.runningExamples.append(uniquename)
        self.runningProcesses[process] = uniquename

        if self.examples[uniquename]['changedirectory'] == 'true':
            process.setWorkingDirectory(self.examples[uniquename]['absolute path'])

        process.start(sys.executable, [self.examples[uniquename]['path']])

        if process.state() == QtCore.QProcess.Starting:
            self.slideshowTimer.stop()

    def showCategories(self):
        self.newPage()
        self.fadeShapes()
        self.currentCategory = ""
        self.currentExample = ""

        # Sort the category names excluding any "Qt" prefix.
        def csort(c1, c2):
            if c1.startsWith("Qt "):
                c1 = c1[3:]

            if c2.startsWith("Qt "):
                c2 = c2[3:]

            return cmp(c1, c2)

        categories = [c for c in self.categories.keys() if c != "[main]"]
        categories.sort(csort)

        horizontalMargin = 0.025*self.width()
        verticalMargin = 0.025*self.height()
        title = TitleShape(self.tr("PyQt Examples and Demos"),
                        self.titleFont, QtGui.QPen(QtGui.QColor("#a6ce39")), QtCore.QPointF(),
                        QtCore.QSizeF(0.5*self.width(), 4*verticalMargin))

        title.setPosition(QtCore.QPointF(self.width() / 2 - title.rect().width() / 2,
                                         -title.rect().height()))
        title.setTarget(QtCore.QPointF(title.position().x(), verticalMargin))

        self.display.appendShape(title)

        topMargin = 6*verticalMargin
        bottomMargin = self.height() - 3.2*verticalMargin
        space = bottomMargin - topMargin
        step = min(title.rect().height() / self.fontRatio, space/self.maximumLabels )
        textHeight = self.fontRatio * step

        startPosition = QtCore.QPointF(0.0, topMargin)
        maxSize = QtCore.QSizeF(10.8*horizontalMargin, textHeight)
        maxWidth = 0.0

        newShapes = []

        for category in categories:
            caption = TitleShape(category, self.font(), QtGui.QPen(), QtCore.QPointF(startPosition), QtCore.QSizeF(maxSize))
            caption.setPosition(QtCore.QPointF(-caption.rect().width(),
                                caption.position().y()))
            caption.setTarget(QtCore.QPointF(2*horizontalMargin, caption.position().y()))

            newShapes.append(caption)
            startPosition += QtCore.QPointF(0.0, step)
            maxWidth = max(maxWidth, caption.rect().width() )

        exitButton = TitleShape(self.tr("Exit"), self.font(), QtGui.QPen(QtCore.Qt.white),
                                   QtCore.QPointF(startPosition), QtCore.QSizeF(maxSize))
        exitButton.setTarget(QtCore.QPointF(2*horizontalMargin, exitButton.position().y()))
        newShapes.append(exitButton)

        startPosition = QtCore.QPointF(self.width(), topMargin )

        extra = (step - textHeight)/4

        backgroundPath = QtGui.QPainterPath()
        backgroundPath.addRect(-2*extra, -extra, maxWidth + 4*extra, textHeight + 2*extra)

        for category in categories:
            background = PanelShape(backgroundPath,
                QtGui.QBrush(self.categories[category]['color']), QtGui.QBrush(QtGui.QColor("#e0e0ff")),
                QtGui.QPen(QtCore.Qt.NoPen), QtCore.QPointF(startPosition),
                QtCore.QSizeF(maxWidth + 4*extra, textHeight + 2*extra))

            background.metadata["category"] = category
            background.setInteractive(True)
            background.setTarget(QtCore.QPointF(2*horizontalMargin,
                                          background.position().y()))
            self.display.insertShape(0, background)
            startPosition += QtCore.QPointF(0.0, step)

        exitPath = QtGui.QPainterPath()
        exitPath.moveTo(-2*extra, -extra)
        exitPath.lineTo(-8*extra, textHeight/2)
        exitPath.lineTo(-extra, textHeight + extra)
        exitPath.lineTo(maxWidth + 2*extra, textHeight + extra)
        exitPath.lineTo(maxWidth + 2*extra, -extra)
        exitPath.closeSubpath()

        exitBackground = PanelShape(exitPath,
            QtGui.QBrush(QtGui.QColor("#a6ce39")), QtGui.QBrush(QtGui.QColor("#c7f745")),
            QtGui.QPen(QtCore.Qt.NoPen), QtCore.QPointF(startPosition),
            QtCore.QSizeF(maxWidth + 10*extra, textHeight + 2*extra))

        exitBackground.metadata["action"] = "exit"
        exitBackground.setInteractive(True)
        exitBackground.setTarget(QtCore.QPointF(2*horizontalMargin,
                                          exitBackground.position().y()))
        self.display.insertShape(0, exitBackground)

        for caption in newShapes:
            position = caption.target()
            size = caption.rect().size()
            caption.setPosition(QtCore.QPointF(-maxWidth, position.y()))
            self.display.appendShape(caption)

        leftMargin = 3*horizontalMargin + maxWidth
        rightMargin = self.width() - 3*horizontalMargin

        description = DocumentShape(self.categories['[main]']['description'],
            self.documentFont, QtCore.QPointF(leftMargin, topMargin),
                QtCore.QSizeF(rightMargin - leftMargin, space))

        description.metadata["fade"] = 10
        self.display.appendShape(description)

        imageHeight = title.rect().height() + verticalMargin

        qtLength = min(imageHeight, title.rect().left()-3*horizontalMargin)
        qtMaxSize = QtCore.QSizeF(qtLength, qtLength)

        qtShape = ImageShape(self.qtLogo,
                QtCore.QPointF(2*horizontalMargin-extra, -imageHeight), qtMaxSize, 0,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        qtShape.metadata["fade"] = 15
        qtShape.setTarget(QtCore.QPointF(qtShape.rect().x(), verticalMargin))
        self.display.insertShape(0, qtShape)

        trolltechMaxSize = QtCore.QSizeF(
                self.width()-3*horizontalMargin-title.rect().right(), imageHeight)

        trolltechShape = ImageShape(self.rbLogo,
                QtCore.QPointF(self.width()-2*horizontalMargin-trolltechMaxSize.width()+extra,
                        -imageHeight),
                trolltechMaxSize, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        trolltechShape.metadata["fade"] = 15
        trolltechShape.setTarget(QtCore.QPointF(trolltechShape.rect().x(),
                            verticalMargin))

        self.display.insertShape(0, trolltechShape)

        self.addVersionAndCopyright(QtCore.QRectF(2*horizontalMargin,
                    self.height() - verticalMargin - textHeight,
                    self.width() - 4*horizontalMargin, textHeight))

    def showExampleDocumentation(self, uniqueName):
        self.disconnect(self.display, QtCore.SIGNAL("displayEmpty()"), self.resizeWindow)
        self.disconnect(self.display, QtCore.SIGNAL("displayEmpty()"), self.close)
        self.currentExample = uniqueName

        url = self.helpRootUrl + self.examples[uniqueName]["document path"]

        # Start assistant if it isn't already running.
        if self.assistantProcess.state() != QtCore.QProcess.Running:
            app = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath) + QtCore.QDir.separator()
            if sys.platform == 'darwin':
                app += "Assistant.app/Contents/MacOS/Assistant"
            else:
                app += "assistant"

            self.assistantProcess.start(app, ["-enableRemoteControl"])

            if not self.assistantProcess.waitForStarted():
                QtGui.QMessageBox.critical(None, "Qt Demo", "Could not start Qt Assistant.")
                return

        # Send command through remote control even if the process was started
        # to activate assistant and bring it to front.
        str = QtCore.QTextStream(self.assistantProcess)
        str << "SetSource " << url << '\n'

    def showExamples(self, category):
        self.newPage()
        self.fadeShapes()
        self.currentCategory = category
        self.currentExample = ""

        horizontalMargin = 0.025*self.width()
        verticalMargin = 0.025*self.height()

        title = self.addTitle(category, verticalMargin)
        self.addTitleBackground(title)

        topMargin = 6*verticalMargin
        bottomMargin = self.height() - 3.2*verticalMargin
        space = bottomMargin - topMargin
        step = min(title.rect().height() / self.fontRatio, space/self.maximumLabels )
        textHeight = self.fontRatio * step

        startPosition = QtCore.QPointF(2*horizontalMargin, self.height()+topMargin)
        finishPosition = QtCore.QPointF(2*horizontalMargin, topMargin)
        maxSize = QtCore.QSizeF(32*horizontalMargin, textHeight)
        maxWidth = 0.0

        for example in self.categories[self.currentCategory]['examples']:
            caption = TitleShape(example, self.font(), QtGui.QPen(), QtCore.QPointF(startPosition), QtCore.QSizeF(maxSize))
            caption.setTarget(QtCore.QPointF(finishPosition))

            self.display.appendShape(caption)

            startPosition += QtCore.QPointF(0.0, step)

            finishPosition += QtCore.QPointF(0.0, step)
            maxWidth = max(maxWidth, caption.rect().width() )

        menuButton = TitleShape(self.tr("Main Menu"), self.font(),
                                QtGui.QPen(QtCore.Qt.white),
                                QtCore.QPointF(startPosition),
                                QtCore.QSizeF(maxSize))
        menuButton.setTarget(QtCore.QPointF(finishPosition))
        self.display.appendShape(menuButton)

        startPosition = QtCore.QPointF(self.width(), topMargin )
        extra = (step - textHeight)/4

        for example in self.categories[self.currentCategory]['examples']:
            uniquename = self.currentCategory + "-" + example

            path = QtGui.QPainterPath()

            path.addRect(-2*extra, -extra, maxWidth + 4*extra, textHeight+2*extra)

            background = PanelShape(path,
                QtGui.QBrush(self.examples[uniquename]['color']),
                QtGui.QBrush(QtGui.QColor("#e0e0ff")),
                QtGui.QPen(QtCore.Qt.NoPen), QtCore.QPointF(startPosition),
                QtCore.QSizeF(maxWidth + 4*extra, textHeight + 2*extra))

            background.metadata["example"] =  uniquename
            background.setInteractive(True)
            background.setTarget(QtCore.QPointF(2*horizontalMargin,
                                          background.position().y()))
            self.display.insertShape(0, background)
            startPosition += QtCore.QPointF(0.0, step)

        backPath = QtGui.QPainterPath()
        backPath.moveTo(-2*extra, -extra)
        backPath.lineTo(-8*extra, textHeight/2)
        backPath.lineTo(-extra, textHeight + extra)
        backPath.lineTo(maxWidth + 2*extra, textHeight + extra)
        backPath.lineTo(maxWidth + 2*extra, -extra)
        backPath.closeSubpath()

        buttonBackground = PanelShape(backPath,
            QtGui.QBrush(QtGui.QColor("#a6ce39")), QtGui.QBrush(QtGui.QColor("#c7f745")),
            QtGui.QPen(QtCore.Qt.NoPen), QtCore.QPointF(startPosition),
            QtCore.QSizeF(maxWidth + 10*extra, textHeight + 2*extra))

        buttonBackground.metadata["action"] =  "parent"
        buttonBackground.setInteractive(True)
        buttonBackground.setTarget(QtCore.QPointF(2*horizontalMargin,
                                          buttonBackground.position().y()))
        self.display.insertShape(0, buttonBackground)

        leftMargin = 3*horizontalMargin + maxWidth
        rightMargin = self.width() - 3*horizontalMargin

        description = DocumentShape(self.categories[self.currentCategory]['description'],
            self.documentFont, QtCore.QPointF(leftMargin, topMargin),
                QtCore.QSizeF(rightMargin - leftMargin, space), 0)

        description.metadata["fade"] =  10
        self.display.appendShape(description)

        self.addVersionAndCopyright(QtCore.QRectF(2*horizontalMargin,
                    self.height() - verticalMargin - textHeight,
                    self.width() - 4*horizontalMargin, textHeight))

    def showExampleSummary(self, uniquename):
        self.newPage()
        self.fadeShapes()
        self.currentExample = uniquename

        horizontalMargin = 0.025*self.width()
        verticalMargin = 0.025*self.height()

        title = self.addTitle(self.examples[uniquename]['name'], verticalMargin)
        titleBackground = self.addTitleBackground(title)

        topMargin = 2*verticalMargin + titleBackground.rect().bottom()
        bottomMargin = self.height() - 8*verticalMargin
        space = bottomMargin - topMargin
        step = min(title.rect().height() / self.fontRatio,
                    ( bottomMargin + 4.8*verticalMargin - topMargin )/self.maximumLabels )
        footerTextHeight = self.fontRatio * step

        leftMargin = 3*horizontalMargin
        rightMargin = self.width() - 3*horizontalMargin

        if self.examples[self.currentExample].has_key('description'):
            description = DocumentShape( self.examples[self.currentExample]['description'],
                                self.documentFont, QtCore.QPointF(leftMargin, topMargin),
                                QtCore.QSizeF(rightMargin-leftMargin, space), 0 )
            description.metadata["fade"] = 10

            description.setPosition(QtCore.QPointF(description.position().x(),
                            0.8*self.height()-description.rect().height()))

            self.display.appendShape(description)
            space = description.position().y() - topMargin - 2*verticalMargin

        if self.examples[self.currentExample].has_key('image files'):
            image = QtGui.QImage(self.examples[self.currentExample]['image files'][0])
            imageMaxSize = QtCore.QSizeF(self.width() - 8*horizontalMargin, space)

            self.currentFrame = ImageShape( image,
                            QtCore.QPointF(self.width()-imageMaxSize.width()/2, topMargin),
                            QtCore.QSizeF(imageMaxSize ))

            self.currentFrame.metadata["fade"] = 15
            self.currentFrame.setTarget(QtCore.QPointF(self.width()/2-imageMaxSize.width()/2,
                                    topMargin))
            self.display.appendShape(self.currentFrame)

            if len(self.examples[self.currentExample]['image files']) > 1:
                self.connect(self.slideshowTimer, QtCore.SIGNAL("timeout()"),
                        self.updateExampleSummary)
                self.slideshowFrame = 0
                self.slideshowTimer.start()

        maxSize = QtCore.QSizeF(0.3*self.width(),2*verticalMargin)
        leftMargin = 0.0
        rightMargin = 0.0

        backButton = TitleShape(self.currentCategory, self.font(),
            QtGui.QPen(QtCore.Qt.white), QtCore.QPointF(0.1*self.width(), self.height()), QtCore.QSizeF(maxSize),
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        backButton.setTarget(QtCore.QPointF(backButton.position().x(),
                                      self.height() - 5.2*verticalMargin))

        self.display.appendShape(backButton)

        maxWidth = backButton.rect().width()
        textHeight = backButton.rect().height()
        extra = (3*verticalMargin - textHeight)/4

        path = QtGui.QPainterPath()
        path.moveTo(-extra, -extra)
        path.lineTo(-4*extra, textHeight/2)
        path.lineTo(-extra, textHeight + extra)
        path.lineTo(maxWidth + 2*extra, textHeight + extra)
        path.lineTo(maxWidth + 2*extra, -extra)
        path.closeSubpath()

        buttonBackground = PanelShape(path,
            QtGui.QBrush(QtGui.QColor("#a6ce39")), QtGui.QBrush(QtGui.QColor("#c7f745")), QtGui.QPen(QtCore.Qt.NoPen),
            QtCore.QPointF(backButton.position()),
            QtCore.QSizeF(maxWidth + 6*extra, textHeight + 2*extra))

        buttonBackground.metadata["category"] =  self.currentCategory
        buttonBackground.setInteractive(True)
        buttonBackground.setTarget(QtCore.QPointF(backButton.target()))

        self.display.insertShape(0, buttonBackground)

        leftMargin = buttonBackground.rect().right()

        if self.examples[self.currentExample].has_key('absolute path'):
            launchCaption = TitleShape(self.tr("Launch"),
                self.font(), QtGui.QPen(QtCore.Qt.white), QtCore.QPointF(0.0, 0.0), QtCore.QSizeF(maxSize),
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            launchCaption.setPosition(QtCore.QPointF(
                0.9*self.width() - launchCaption.rect().width(), self.height()))
            launchCaption.setTarget(QtCore.QPointF(launchCaption.position().x(),
                                             self.height() - 5.2*verticalMargin))

            self.display.appendShape(launchCaption)

            maxWidth = launchCaption.rect().width()
            textHeight = launchCaption.rect().height()
            extra = (3*verticalMargin - textHeight)/4

            path = QtGui.QPainterPath()
            path.addRect(-2*extra, -extra, maxWidth + 4*extra, textHeight + 2*extra)

            backgroundColor = QtGui.QColor("#a63e39")
            highlightedColor = QtGui.QColor("#f95e56")

            background = PanelShape(path,
                QtGui.QBrush(backgroundColor), QtGui.QBrush(highlightedColor), QtGui.QPen(QtCore.Qt.NoPen),
                QtCore.QPointF(launchCaption.position()),
                QtCore.QSizeF(maxWidth + 4*extra, textHeight + 2*extra))

            background.metadata["fade minimum"] =  120
            background.metadata["launch"] =  self.currentExample
            background.setInteractive(True)
            background.setTarget(QtCore.QPointF(launchCaption.target()))

            if self.currentExample in self.runningExamples:
                background.metadata["highlight"] =  True
                background.metadata["highlight scale"] =  0.99
                background.animate()
                background.metadata["fade"] =  -135
                self.slideshowTimer.stop()
            self.display.insertShape(0, background)

            rightMargin = background.rect().left()

        if self.examples[self.currentExample]['document path']:

            documentCaption = TitleShape(self.tr("Show Documentation"),
                self.font(), QtGui.QPen(QtCore.Qt.white), QtCore.QPointF(0.0, 0.0), QtCore.QSizeF(maxSize),
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

            if rightMargin == 0.0:
                documentCaption.setPosition(QtCore.QPointF(
                    0.9*self.width() - documentCaption.rect().width(), self.height()))
            else:
                documentCaption.setPosition(QtCore.QPointF(
                    leftMargin/2 + rightMargin/2 - documentCaption.rect().width()/2,
                    self.height()))

            documentCaption.setTarget(QtCore.QPointF(documentCaption.position().x(),
                                               self.height() - 5.2*verticalMargin))

            self.display.appendShape(documentCaption)

            maxWidth = documentCaption.rect().width()
            textHeight = documentCaption.rect().height()
            extra = (3*verticalMargin - textHeight)/4

            path = QtGui.QPainterPath()
            path.addRect(-2*extra, -extra, maxWidth + 4*extra, textHeight + 2*extra)

            background = PanelShape(path,
                QtGui.QBrush(QtGui.QColor("#9c9cff")), QtGui.QBrush(QtGui.QColor("#cfcfff")), QtGui.QPen(QtCore.Qt.NoPen),
                QtCore.QPointF(documentCaption.position()),
                QtCore.QSizeF(maxWidth + 4*extra, textHeight + 2*extra))

            background.metadata["fade minimum"] =  120
            background.metadata["documentation"] =  self.currentExample
            background.setInteractive(True)
            background.setTarget(QtCore.QPointF(documentCaption.target()))

            self.display.insertShape(0, background)

        self.addVersionAndCopyright(QtCore.QRectF(2*horizontalMargin,
                    self.height() - verticalMargin - footerTextHeight,
                    self.width() - 4*horizontalMargin, footerTextHeight))

    def showParentPage(self):
        self.slideshowTimer.stop()
        self.disconnect(self.slideshowTimer, QtCore.SIGNAL("timeout()"), self.updateExampleSummary)

        if len(self.currentExample) > 0:
            self.currentExample = ""
            self.redisplayWindow()
        elif len(self.currentCategory) > 0:
            self.currentCategory = ""
            self.redisplayWindow()

    def updateExampleSummary(self):
        if self.examples[self.currentExample].has_key('image files'):
            self.currentFrame.metadata["fade"] = -15
            self.currentFrame.setTarget(QtCore.QPointF((self.currentFrame.position() -
                        QtCore.QPointF(0.5*self.width(), 0))))
            self.slideshowFrame = (self.slideshowFrame+1) % len(self.examples[self.currentExample]['image files'])
            image = QtGui.QImage(self.examples[self.currentExample]['image files'][self.slideshowFrame])

            imageSize = self.currentFrame.maxSize
            imagePosition = QtCore.QPointF(self.width() - imageSize.width()/2,
                                    self.currentFrame.position().y())

            self.currentFrame = ImageShape(image, QtCore.QPointF(imagePosition), QtCore.QSizeF(imageSize))
            self.currentFrame.metadata["fade"] = 15
            self.currentFrame.setTarget(QtCore.QPointF(self.width()/2-imageSize.width()/2,
                            imagePosition.y()))

            self.display.appendShape(self.currentFrame)

    def closeEvent(self, event):
        if len(self.runningExamples) > 0:
            if QtGui.QMessageBox.warning(self, self.tr("Examples Running"),
                    self.tr("There are examples running. Do you really want to exit?"),
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No ) == QtGui.QMessageBox.No:
                event.ignore()
                return

        for example in self.runningProcesses.keys():
            example.terminate()
            example.waitForFinished(1000)

        self.runningProcesses.clear()
        self.resizeTimer.stop()
        self.slideshowTimer.stop()

    def resizeEvent(self, event):
        self.documentFont = QtGui.QFont(self.font())
        self.documentFont.setPointSizeF(min(self.documentFont.pointSizeF()*self.width()/640.0,
                                            self.documentFont.pointSizeF()*self.height()/480.0))

        if self.inFullScreenResize:
            self.emit(QtCore.SIGNAL("windowResized()"))
            self.inFullScreenResize = False
        elif self.currentCategory != "[starting]":
            self.resizeTimer.start(500)

    def toggleFullScreen(self):
        if self.inFullScreenResize:
            return

        self.inFullScreenResize = True
        self.connect(self.display, QtCore.SIGNAL("displayEmpty()"), self.resizeWindow, QtCore.Qt.QueuedConnection)
        self.display.reset()

    def redisplayWindow(self):
        if len(self.currentExample) > 0:
            self.showExampleSummary(self.currentExample)
        elif len(self.currentCategory) > 0:
            self.showExamples(self.currentCategory)
        else:
            self.showCategories()

    def resizeWindow(self):
        self.disconnect(self.display, QtCore.SIGNAL("displayEmpty()"), self.resizeWindow)

        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def addTitle(self, title, verticalMargin):
        titlePosition = QtCore.QPointF(0.0, 2*verticalMargin)

        newTitle = TitleShape(title, self.titleFont, QtGui.QPen(QtCore.Qt.white),
                            QtCore.QPointF(titlePosition), QtCore.QSizeF(0.5*self.width(), 2*verticalMargin ),
                            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop )
        newTitle.setPosition(QtCore.QPointF(-newTitle.rect().width(), titlePosition.y()))
        newTitle.setTarget(QtCore.QPointF(0.25*self.width(), titlePosition.y()))
        newTitle.metadata["fade"] =  15

        self.display.appendShape(newTitle)

        return newTitle

    def addTitleBackground(self, titleShape):
        backgroundPath = QtGui.QPainterPath()

        backgroundPath.addRect(0, -titleShape.rect().height()*0.3, self.width(),
                                titleShape.rect().height()*1.6)

        titleBackground = PanelShape(backgroundPath, QtGui.QBrush(QtGui.QColor("#a6ce39") ),
                                    QtGui.QBrush(QtGui.QColor("#a6ce39") ), QtGui.QPen(QtCore.Qt.NoPen),
                                    QtCore.QPointF( self.width(), titleShape.position().y() ),
                                    QtCore.QSizeF(backgroundPath.boundingRect().size() ))
        titleBackground.setTarget(QtCore.QPointF(0.0, titleShape.position().y()))

        self.display.insertShape(0, titleBackground)

        return titleBackground

    def readExampleDescription(self, parentNode):
        node = parentNode.firstChild()
        description = ""
        while not node.isNull():
            if node.isText():
                description += node.nodeValue()
            elif node.hasChildNodes():
                if node.nodeName() == "b":
                    beginTag = "<b>"
                    endTag = "</b>"
                elif node.nodeName() == "a":
                    beginTag = "<font color=\"blue\">"
                    endTag = "</font>"
                elif node.nodeName() == "i":
                    beginTag = "<i>"
                    endTag = "</i>"
                elif node.nodeName() == "tt":
                    beginTag = "<tt>"
                    endTag = "</tt>"

                description += beginTag + self.readExampleDescription(node) + endTag

            node = node.nextSibling()

        return description

    def readInfo(self, resource, dir_):
        categoriesFile = QtCore.QFile(resource)
        document = QtXml.QDomDocument()
        document.setContent(categoriesFile)
        documentElement = document.documentElement()
        categoryNodes = documentElement.elementsByTagName("category")

        self.categories['[main]'] = {}
        self.categories['[main]']['examples'] = []
        self.categories['[main]']['color'] = QtGui.QColor("#f0f0f0")

        self.readCategoryDescription(dir_, '[main]')
        self.qtLogo.load(self.imagesDir.absoluteFilePath(":/images/qt4-logo.png"))
        self.rbLogo.load(self.imagesDir.absoluteFilePath(":/images/rb-logo.png"))

        for i in range(categoryNodes.length()):
            elem = categoryNodes.item(i).toElement()
            categoryName = QtCore.QString(elem.attribute("name"))
            categoryDirName = QtCore.QString(elem.attribute("dirname"))
            categoryDocName = QtCore.QString(elem.attribute("docname"))
            categoryColor = QtGui.QColor(elem.attribute("color", "#f0f0f0"))

            categoryDir = QtCore.QDir(dir_)

            if categoryDir.cd(categoryDirName):
                self.categories[categoryName] = {}

                self.readCategoryDescription(categoryDir, categoryName)

                self.categories[categoryName]['examples'] = []

                exampleNodes = elem.elementsByTagName("example")
                self.maximumLabels = max(self.maximumLabels, exampleNodes.length())

                # Only add those examples we can find.
                for j in range(exampleNodes.length()):
                    exampleDir = QtCore.QDir(categoryDir)

                    exampleNode = exampleNodes.item(j)
                    element = exampleNode.toElement()
                    exampleName = element.attribute("name")
                    exampleFileName = element.attribute("filename")

                    uniqueName = categoryName + "-" + exampleName

                    self.examples[uniqueName] = {}

                    if not categoryDocName.isEmpty():
                        docName = categoryDocName + "-" + exampleFileName + ".html"
                    else:
                        docName = categoryDirName + "-" + exampleFileName + ".html"

                    self.examples[uniqueName]['name'] = exampleName
                    self.examples[uniqueName]['document path'] = ""
                    self.findDescriptionAndImages(uniqueName, docName)

                    self.examples[uniqueName]['changedirectory'] = element.attribute("changedirectory", "true")
                    self.examples[uniqueName]['color'] = QtGui.QColor(element.attribute("color", "#f0f0f0"))

                    if element.attribute("executable", "true") != "true":
                        del self.examples[uniqueName]
                        continue

                    examplePath = None

                    if sys.platform == "win32":
                        examplePyName = exampleFileName + ".pyw"
                    else:
                        examplePyName = exampleFileName + ".py"

                    if exampleDir.exists(examplePyName):
                        examplePath = exampleDir.absoluteFilePath(examplePyName)
                    elif exampleDir.cd(exampleFileName):
                        if exampleDir.exists(examplePyName):
                            examplePath = exampleDir.absoluteFilePath(examplePyName)

                    if examplePath and not examplePath.isNull():
                        self.examples[uniqueName]['absolute path'] = exampleDir.absolutePath()
                        self.examples[uniqueName]['path'] = examplePath

                        self.categories[categoryName]['examples'].append(exampleName)
                    else:
                        del self.examples[uniqueName]

                self.categories[categoryName]['color'] = categoryColor

        return len(self.categories)

    def addVersionAndCopyright(self, rect):
        versionCaption = TitleShape(QtCore.QString("Qt %1").arg(QtCore.QT_VERSION_STR),
                                    self.font(), QtGui.QPen(QtGui.QColor(0,0,0,0)),
                                    QtCore.QPointF(rect.center().x(), rect.top()),
                                    QtCore.QSizeF(0.5*rect.width(), rect.height()),
                                    QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        versionCaption.metadata["fade"] = 15
        self.display.appendShape(versionCaption)

        copyrightCaption = TitleShape(QtCore.QString("Copyright \xa9 2005-2006 Trolltech AS"),
                                    self.font(), QtGui.QPen(QtGui.QColor(0,0,0,0)),
                                    QtCore.QPointF(rect.topLeft()),
                                    QtCore.QSizeF(0.5*rect.width(), rect.height()),
                                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        copyrightCaption.metadata["fade"] = 15
        self.display.appendShape(copyrightCaption)

    def fadeShapes(self):
        for i in range(0, self.display.shapesCount()):
            shape = self.display.shape(i)
            shape.metadata["fade"] = -15
            shape.metadata["fade minimum"] = 0

    def findDescriptionAndImages(self, uniqueName, docName):
        if self.documentationDir.exists(docName):
            self.examples[uniqueName]['document path'] = docName

            exampleDoc = QtXml.QDomDocument()

            exampleFile = QtCore.QFile(self.documentationDir.absoluteFilePath(docName))
            exampleDoc.setContent(exampleFile)

            paragraphs = exampleDoc.elementsByTagName("p")

            for p in range(paragraphs.length()):
                descriptionNode = paragraphs.item(p)
                description = self.readExampleDescription(descriptionNode)

                if QtCore.QString(description).indexOf(QtCore.QRegExp(QtCore.QString("((The|This) )?(%1 )?.*(example|demo)").arg(self.examples[uniqueName]['name']), QtCore.Qt.CaseInsensitive)) != -1:
                    self.examples[uniqueName]['description'] = description
                    break

            images = exampleDoc.elementsByTagName("img")
            imageFiles = []

            for i in range(images.length()):
                imageElement = images.item(i).toElement()
                source = QtCore.QString(imageElement.attribute("src"))
                if "-logo" not in source:
                    imageFiles.append(self.documentationDir.absoluteFilePath(source))

            if len(imageFiles) > 0:
                self.examples[uniqueName]['image files'] = imageFiles

    def newPage(self):
        self.slideshowTimer.stop()
        self.disconnect(self.slideshowTimer, QtCore.SIGNAL("timeout()"), self.updateExampleSummary)
        self.disconnect(self.display, QtCore.SIGNAL("displayEmpty()"), self.resizeWindow)

    def readCategoryDescription(self, categoryDir, categoryName):
##        categoryDirName = categoryDir.absolutePath()
##        if categoryDirName.find("examples") != -1:
##            categoryDirName = re.sub(".*/examples(.*)", r"%s\1" % QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.ExamplesPath), categoryDirName)
##        else:
##            categoryDirName = re.sub(".*/demos(.*)", r"%s\1" % QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.DemosPath), categoryDirName)
##        categoryDir = QtCore.QDir(categoryDirName)
        if categoryDir.exists("README"):
            file = QtCore.QFile(categoryDir.absoluteFilePath("README"))

            if not file.open(QtCore.QFile.ReadOnly):
                return

            inputStream = QtCore.QTextStream(file)

            paragraphs = []
            currentPara = []
            openQuote = True

            while not inputStream.atEnd():
                line = inputStream.readLine()

                at = line.indexOf("\"", 0)

                while at != -1:
                    if openQuote:
                        line.replace(at, 1, QtCore.QChar(QtCore.QChar.Punctuation_InitialQuote))
                    else:
                        line.replace(at, 1, QtCore.QChar(QtCore.QChar.Punctuation_FinalQuote))
                    openQuote = not openQuote
                    at = line.indexOf("\"", at)

                if not line.trimmed().isEmpty():
                    currentPara.append(str(line.trimmed()))
                elif len(currentPara) > 0:
                    paragraphs.append(" ".join(currentPara))
                    currentPara = []
                else:
                    break


            if len(currentPara) > 0:
                paragraphs.append(" ".join(currentPara))

            self.categories[categoryName]['description'] = "<p>"+"\n</p><p>".join(paragraphs)+"</p>"

    def slotShowPage(self):
        self.emit(QtCore.SIGNAL("showPage()"))
