#!/usr/bin/python

#       pysideqplayer.py
#       
#       Copyright 2009 ahmed youssef <xmonader@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.



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

import qrc_resources

class QPlayer(QtGui.QWidget):

    def __init__(self):
        #QtGui.QWidget.__init__(self)
        super(QPlayer, self).__init__()
        self.audioOuptut=Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.player=Phonon.MediaObject(self)
        Phonon.createPath(self.player, self.audioOuptut)

        self.videoWidget=Phonon.VideoWidget(self)
        Phonon.createPath(self.player, self.videoWidget)

        self.player.setTickInterval(1000)
        self.connect(self.player, QtCore.SIGNAL("tick(qint64)"), self.tick)

        self.seekSlider=Phonon.SeekSlider(self.player, self)
        self.volumeSlider=Phonon.VolumeSlider(self.audioOuptut, self)

        self.buildGUI()
        self.setupConnections()

    def buildGUI(self):

        self.fileLabel = QtGui.QLabel("File")
        self.fileEdit = QtGui.QLineEdit()
        self.fileLabel.setBuddy(self.fileEdit)

        self.lcdTimer=QtGui.QLCDNumber()
        self.lcdTimer.display("00:00")

        self.browseButton=QtGui.QPushButton("Browse")
        self.browseButton.setIcon(QtGui.QIcon(":/images/folder-music.png"))

        self.playButton=QtGui.QPushButton("Play")
        self.playButton.setIcon(QtGui.QIcon(":/images/play.png"))
        self.playButton.setEnabled(False)

        self.pauseButton=QtGui.QPushButton("Pause")
        self.pauseButton.setIcon(QtGui.QIcon(":/images/pause.png"))

        self.stopButton=QtGui.QPushButton("Stop")
        self.stopButton.setIcon(QtGui.QIcon(":/images/stop.png"))

        upperLayout=QtGui.QHBoxLayout()
        upperLayout.addWidget(self.fileLabel)
        upperLayout.addWidget(self.fileEdit)
        upperLayout.addWidget(self.browseButton)

        midLayout=QtGui.QHBoxLayout()
        midLayout.addWidget(self.seekSlider)
        midLayout.addWidget(self.lcdTimer)

        lowerLayout=QtGui.QHBoxLayout()
        lowerLayout.addWidget(self.playButton)
        lowerLayout.addWidget(self.pauseButton)
        lowerLayout.addWidget(self.stopButton)
        lowerLayout.addWidget(self.volumeSlider)

        layout=QtGui.QVBoxLayout()
        layout.addLayout(upperLayout)
        layout.addWidget(self.videoWidget)
        layout.addLayout(midLayout)
        layout.addLayout(lowerLayout)

        self.setLayout(layout)
        self.lcdTimer.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.seekSlider.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)


    def setupConnections(self):
        self.connect(self.browseButton, QtCore.SIGNAL("clicked()"), self.browseClicked)
        self.connect(self.playButton, QtCore.SIGNAL("clicked()"), self.playClicked)#self.playClicked)
        self.connect(self.pauseButton, QtCore.SIGNAL("clicked()"), self.pauseClicked)
        self.connect(self.stopButton, QtCore.SIGNAL("clicked()"), self.stopClicked)
        self.connect(self.fileEdit, QtCore.SIGNAL("textChanged(const QString&)"), self.checkFileName)

    def tick(self, time):
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.lcdTimer.display(displayTime.toString('mm:ss'))

    def playClicked(self):
        self.player.setCurrentSource(Phonon.MediaSource(self.fileEdit.text()))
        self.player.play()

    def pauseClicked(self):
        self.player.pause()

    def stopClicked(self):
        self.player.stop()
        self.lcdTimer.display("00:00")

    def browseClicked(self):
        f, _ = QtGui.QFileDialog.getOpenFileName(self)
        if f!="":
            self.fileEdit.setText(f)

    def checkFileName(self, s):
        if s!="":
            self.playButton.setEnabled(True)
        else:
            self.playButton.setEnabled(False)

if __name__=="__main__":
    qapp=QtGui.QApplication(sys.argv)
    w=QPlayer()
    w.show()
    sys.exit(qapp.exec_())
