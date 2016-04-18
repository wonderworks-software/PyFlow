#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2007-2008 Trolltech ASA. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## Licensees holding a valid Qt License Agreement may use this file in
## accordance with the rights, responsibilities and obligations
## contained therein.  Please consult your licensing agreement or
## contact sales@trolltech.com if any conditions of this licensing
## agreement are not clear to you.
##
## Further information about Qt licensing is available at:
## http://www.trolltech.com/products/qt/licensing.html or by
## contacting info@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

import sys
from PySide import QtCore, QtGui

try:
    from PySide.phonon import Phonon
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "Music Player",
            "Your Qt installation does not have Phonon support.",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.metaInformationResolver = Phonon.MediaObject(self)

        self.mediaObject.setTickInterval(1000)

        self.connect(self.mediaObject, QtCore.SIGNAL('tick(qint64)'),
                self.tick)
        self.connect(self.mediaObject,
                QtCore.SIGNAL('stateChanged(Phonon::State, Phonon::State)'),
                self.stateChanged)
        self.connect(self.metaInformationResolver,
                QtCore.SIGNAL('stateChanged(Phonon::State, Phonon::State)'),
                self.metaStateChanged)
        self.connect(self.mediaObject,
                QtCore.SIGNAL('currentSourceChanged(Phonon::MediaSource)'),
                self.sourceChanged)
        self.connect(self.mediaObject, QtCore.SIGNAL('aboutToFinish()'),
                self.aboutToFinish)

        Phonon.createPath(self.mediaObject, self.audioOutput)

        self.setupActions()
        self.setupMenus()
        self.setupUi()
        self.timeLcd.display("00:00") 

        self.sources = []

    def sizeHint(self):
        return QtCore.QSize(500, 300)

    def addFiles(self):
        files,_ = QtGui.QFileDialog.getOpenFileNames(self,
                  self.tr("Select Music Files"),
                  QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation))

        if files=="":
            return

        index = len(self.sources)

        for string in files:
            self.sources.append(Phonon.MediaSource(string))

        if self.sources:
            self.metaInformationResolver.setCurrentSource(self.sources[index])

    def about(self):
        QtGui.QMessageBox.information(self, self.tr("About Music Player"),
                self.tr("The Music Player example shows how to use Phonon - "
                        "the multimedia framework that comes with Qt - to "
                        "create a simple music player."))

    def stateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            if self.mediaObject.errorType() == Phonon.FatalError:
                QtGui.QMessageBox.warning(self, self.tr("Fatal Error"),
                        self.mediaObject.errorString())
            else:
                QtGui.QMessageBox.warning(self, self.tr("Error"),
                        self.mediaObject.errorString())

        elif newState == Phonon.PlayingState:
            self.playAction.setEnabled(False)
            self.pauseAction.setEnabled(True)
            self.stopAction.setEnabled(True)

        elif newState == Phonon.StoppedState:
            self.stopAction.setEnabled(False)
            self.playAction.setEnabled(True)
            self.pauseAction.setEnabled(False)
            self.timeLcd.display("00:00")

        elif newState == Phonon.PausedState:
            self.pauseAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.playAction.setEnabled(True)

    def tick(self, time):
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.timeLcd.display(displayTime.toString('mm:ss'))

    def tableClicked(self, row, column):
        oldState = self.mediaObject.state()

        self.mediaObject.stop()
        self.mediaObject.clearQueue()

        self.mediaObject.setCurrentSource(self.sources[row])

        if oldState == Phonon.PlayingState:
            self.mediaObject.play()

    def sourceChanged(self, source):
        self.musicTable.selectRow(self.sources.index(source))
        self.timeLcd.display("00:00")

    def metaStateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            QtGui.QMessageBox.warning(self, self.tr("Error opening files"),
                    self.metaInformationResolver.errorString())

            while self.sources and self.sources.pop() != self.metaInformationResolver.currentSource():
                pass

            return

        if newState != Phonon.StoppedState and newState != Phonon.PausedState:
            return

        if self.metaInformationResolver.currentSource().type() == Phonon.MediaSource.Invalid:
            return

        metaData = self.metaInformationResolver.metaData()

        title = metaData.get('TITLE', [""])[0]
        if title=="":
            title = self.metaInformationResolver.currentSource().fileName()

        titleItem = QtGui.QTableWidgetItem(title)
        titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)

        artist = metaData.get('ARTIST', [""])[0]
        artistItem = QtGui.QTableWidgetItem(artist)
        artistItem.setFlags(artistItem.flags() ^ QtCore.Qt.ItemIsEditable)

        album = metaData.get('ALBUM', [""])[0]
        albumItem = QtGui.QTableWidgetItem(album)
        albumItem.setFlags(albumItem.flags() ^ QtCore.Qt.ItemIsEditable)

        year = metaData.get('DATE', [""])[0]
        yearItem = QtGui.QTableWidgetItem(year)
        yearItem.setFlags(yearItem.flags() ^ QtCore.Qt.ItemIsEditable)

        currentRow = self.musicTable.rowCount()
        self.musicTable.insertRow(currentRow)
        self.musicTable.setItem(currentRow, 0, titleItem)
        self.musicTable.setItem(currentRow, 1, artistItem)
        self.musicTable.setItem(currentRow, 2, albumItem)
        self.musicTable.setItem(currentRow, 3, yearItem)

        if not self.musicTable.selectedItems():
            self.musicTable.selectRow(0)
            self.mediaObject.setCurrentSource(self.metaInformationResolver.currentSource())

        source = self.metaInformationResolver.currentSource()
        index = self.sources.index(self.metaInformationResolver.currentSource()) + 1

        if len(self.sources) > index:
            self.metaInformationResolver.setCurrentSource(self.sources[index])
        else:
            self.musicTable.resizeColumnsToContents()
            if self.musicTable.columnWidth(0) > 300:
                self.musicTable.setColumnWidth(0, 300)

    def aboutToFinish(self):
        index = self.sources.index(self.mediaObject.currentSource()) + 1
        if len(self.sources) > index:
            self.mediaObject.enqueue(self.sources[index])

    def setupActions(self):
        self.playAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), self.tr("Play"), self)
        self.playAction.setShortcut(self.tr("Crl+P"))
        self.playAction.setDisabled(True)

        self.pauseAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPause), self.tr("Pause"), self)
        self.pauseAction.setShortcut(self.tr("Ctrl+A"))
        self.pauseAction.setDisabled(True)

        self.stopAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaStop), self.tr("Stop"), self)
        self.stopAction.setShortcut(self.tr("Ctrl+S"))
        self.stopAction.setDisabled(True)

        self.nextAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaSkipForward), self.tr("Next"), self)
        self.nextAction.setShortcut(self.tr("Ctrl+N"))

        self.previousAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaSkipBackward), self.tr("Previous"), self)
        self.previousAction.setShortcut(self.tr("Ctrl+R"))

        self.addFilesAction = QtGui.QAction(self.tr("Add &Files"), self)
        self.addFilesAction.setShortcut(self.tr("Ctrl+F"))

        self.exitAction = QtGui.QAction(self.tr("E&xit"), self)
        self.exitAction.setShortcut(self.tr("Ctrl+X"))

        self.aboutAction = QtGui.QAction(self.tr("A&bout"), self)
        self.aboutAction.setShortcut(self.tr("Ctrl+B"))

        self.aboutQtAction = QtGui.QAction(self.tr("About &Qt"), self)
        self.aboutQtAction.setShortcut(self.tr("Ctrl+Q"))

        self.connect(self.playAction, QtCore.SIGNAL('triggered()'),
                self.mediaObject, QtCore.SLOT('play()'))
        self.connect(self.pauseAction, QtCore.SIGNAL('triggered()'),
                self.mediaObject, QtCore.SLOT('pause()'))
        self.connect(self.stopAction, QtCore.SIGNAL('triggered()'),
                self.mediaObject, QtCore.SLOT('stop()'))
        self.connect(self.addFilesAction, QtCore.SIGNAL('triggered()'),
                self.addFiles)
        self.connect(self.exitAction, QtCore.SIGNAL('triggered()'),
                self, QtCore.SLOT('close()'))
        self.connect(self.aboutAction, QtCore.SIGNAL('triggered()'),
                self.about)
        self.connect(self.aboutQtAction, QtCore.SIGNAL('triggered()'),
                QtGui.qApp, QtCore.SLOT('aboutQt()'))

    def setupMenus(self):
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        fileMenu.addAction(self.addFilesAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        aboutMenu = self.menuBar().addMenu(self.tr("&Help"))
        aboutMenu.addAction(self.aboutAction)
        aboutMenu.addAction(self.aboutQtAction)

    def setupUi(self):
        bar = QtGui.QToolBar()

        bar.addAction(self.playAction)
        bar.addAction(self.pauseAction)
        bar.addAction(self.stopAction)

        self.seekSlider = Phonon.SeekSlider(self)
        self.seekSlider.setMediaObject(self.mediaObject)

        self.volumeSlider = Phonon.VolumeSlider(self)
        self.volumeSlider.setAudioOutput(self.audioOutput)
        self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Maximum,
                QtGui.QSizePolicy.Maximum)

        volumeLabel = QtGui.QLabel()
        volumeLabel.setPixmap(QtGui.QPixmap('images/volume.png'))

        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkGray)

        self.timeLcd = QtGui.QLCDNumber()
        self.timeLcd.setPalette(palette)

        headers = [self.tr("Title"), self.tr("Artist"), self.tr("Album"), self.tr("Year")]

        self.musicTable = QtGui.QTableWidget(0, 4)
        self.musicTable.setHorizontalHeaderLabels(headers)
        self.musicTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.musicTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.connect(self.musicTable, QtCore.SIGNAL('cellPressed(int, int)'),
                self.tableClicked)

        seekerLayout = QtGui.QHBoxLayout()
        seekerLayout.addWidget(self.seekSlider)
        seekerLayout.addWidget(self.timeLcd)

        playbackLayout = QtGui.QHBoxLayout()
        playbackLayout.addWidget(bar)
        playbackLayout.addStretch()
        playbackLayout.addWidget(volumeLabel)
        playbackLayout.addWidget(self.volumeSlider)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.musicTable)
        mainLayout.addLayout(seekerLayout)
        mainLayout.addLayout(playbackLayout)

        widget = QtGui.QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)
        self.setWindowTitle("Phonon Music Player")


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Music Player")
    app.setQuitOnLastWindowClosed(True)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
